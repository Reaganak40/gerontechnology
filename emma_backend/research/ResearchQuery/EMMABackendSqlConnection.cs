using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResearchQuery
{
    /// <summary>
    /// The SqlConnection wrapper to connect and access the EMMA Backend Database.
    /// </summary>
    internal class EMMABackendSqlConnection
    {
        private MySqlConnection connection;
        private MySqlDataReader? reader;

        private string myConnectionString;

        // studies available from the database
        private List<string> studies;

        // cohorts from selected studies
        private List<KeyValuePair<string, int>> cohorts;

        // Columns in the SQL calculation table, converted from SQL naming conventions
        private List<string> calculateTableColumns;

        private bool connected;

        /// <summary>
        /// Initializes a new instance of the <see cref="EMMABackendSqlConnection`1"/> class.
        /// </summary>
        /// <param name="server">the name of the server-host where the EMMA Backend database is located.</param>
        /// <param name="userid">username for credentials.</param>
        /// <param name="password">password for credentials.</param>
        public EMMABackendSqlConnection(string server, string userid, string password)
        {
            this.connection = new MySqlConnection();
            this.myConnectionString = $"server={server};user id={userid};password={password};database=emma_backend";

            try
            {
                this.connection.ConnectionString = this.myConnectionString;
                this.connection.Open();
                this.connected = true;
            }
            catch (MySqlException ex)
            {
                MessageBox.Show(ex.Message);
                this.connected = false;
            }

            this.connection.Close();
            this.reader = null;

            this.studies = new List<string>();
            this.cohorts = new List<KeyValuePair<string, int>>();
            this.calculateTableColumns = new List<string>();
            if (this.Connected)
            {
                this.GetStudies();
                this.GetCalculationTableColumns();
            }
        }

        /// <summary>
        /// Gets a value indicating whether or not a valid connection to the database was created.
        /// </summary>
        public bool Connected
        {
            get
            {
                return this.connected;
            }
        }

        /// <summary>
        /// Gets the list of the studies in the database.
        /// </summary>
        public string[] Studies
        {
            get
            {
                return this.studies.ToArray();
            }
        }

        /// <summary>
        /// Gets the colloquial names for the calculation table columns.
        /// </summary>
        public string[] CalculationTableColumns
        {
            get
            {
                return this.calculateTableColumns.ToArray();
            }
        }

        /// <summary>
        /// Returns the sql query result for a filtered calculation table.
        /// </summary>
        /// <param name="args">A collection of arguments the dynamically defined specified queries.</param>
        /// <returns>The sql table result.</returns>
        public DataTable QueryCalculationTable(EmmaQueryArgs args)
        {
            // Use study-cohort restrictions to only get weekly calculations where the participant_id is in
            // one of the selected studies and cohorts.
            StringBuilder participant_sql_str = new StringBuilder("SELECT participant_id FROM Participants");
            if (args.StudyCohorts.Length > 0)
            {
                participant_sql_str.Append(" WHERE ");
            }

            int index = 0;
            foreach (KeyValuePair<string, int> sc_pair in args.StudyCohorts)
            {
                participant_sql_str.Append($"(study = '{sc_pair.Key}' AND cohort = {sc_pair.Value})");

                index++;
                if (index < args.StudyCohorts.Length)
                {
                    participant_sql_str.Append(" OR ");
                }
            }

            // Determine what columns this query should select.
            StringBuilder calculations_sql_str;
            if (args.Variables is null)
            {
                calculations_sql_str = new StringBuilder("SELECT C.* FROM Calculations C");
            }
            else
            {
                calculations_sql_str = new StringBuilder("SELECT C.participant_id, C.week_number, C.year_number");

                if (args.Variables.Length > 0)
                {
                    calculations_sql_str.Append(", ");
                    index = 0;
                    foreach (string var in args.Variables)
                    {
                        calculations_sql_str.Append("C." + var);

                        index++;
                        if (index < args.Variables.Length)
                        {
                            calculations_sql_str.Append(", ");
                        }
                    }
                }

                calculations_sql_str.Append(" FROM Calculations C");
            }

            // join the query results for participants table with the calculation table.
            calculations_sql_str.Append($" WHERE C.participant_id IN ({participant_sql_str.ToString()})");

            // add date range conditions
            if (args.DateRanges.Length > 0)
            {
                calculations_sql_str.Append(" AND (");
            }

            index = 0;
            foreach (var date in args.DateRanges)
            {
                int week = date.Item1;
                int year = date.Item2;

                calculations_sql_str.Append($"(week_number = {week} AND year_number = {year}");

                if ((index + 1) < args.DateRanges.Length)
                {
                    calculations_sql_str.Append(") OR");
                }
                else
                {
                    calculations_sql_str.Append("))");
                }

                index++;
            }

            return this.ExecuteQuery(calculations_sql_str.ToString());
        }

        /// <summary>
        /// Updates the cohorts based on the selected studies.
        /// </summary>
        /// <param name="selected_studies">The studies the user has selected to find cohorts.</param>
        /// <returns>A list of formatting strings according to study-cohort pairs.</returns>
        /// <exception cref="NoNullAllowedException">Thrown if data gathered in null.</exception>
        public KeyValuePair<string, int>[] UpdateSelectedCohorts(string[] selected_studies)
        {
            // Create and execute sql string
            StringBuilder selection_str;
            if (selected_studies.Length > 0)
            {
                selection_str = new StringBuilder("WHERE ");
                for (int i = 0; i < selected_studies.Length; i++)
                {
                    selection_str.Append("study = '" + selected_studies[i] + "'");

                    if ((i + 1) < selected_studies.Length)
                    {
                        selection_str.Append(" OR ");
                    }
                }
            }
            else
            {
                selection_str = new StringBuilder(string.Empty);
            }

            DataTable query_results = this.ExecuteQuery($"SELECT DISTINCT study, cohort FROM Participants {selection_str.ToString()} ORDER BY study");

            // Create cohort string rows for returned results
            this.cohorts = new List<KeyValuePair<string, int>>();

            foreach (DataRow row in query_results.Rows)
            {
                object study = row["study"];
                if (study.GetType() != typeof(string))
                {
                    throw new NotSupportedException("Row value for study should not be of type: " + study.GetType().ToString());
                }

                object cohort = row["cohort"];
                if (cohort.GetType() != typeof(int))
                {
                    throw new NotSupportedException("Row value for cohort should not be of type: " + study.GetType().ToString());
                }

                this.cohorts.Add(new KeyValuePair<string, int>((string)study, (int)cohort));
            }

            return this.cohorts.ToArray();
        }

        /// <summary>
        /// Gets the queried table showing the available week,year pairs for the provided study_cohorts.
        /// </summary>
        /// <param name="study_cohorts">A list of study-cohort pairs to filter the calculation table with.</param>
        /// <returns>The sql table result.</returns>
        public DataTable QueryDateRanges(KeyValuePair<string, int>[] study_cohorts)
        {
            // Use study-cohort restrictions to only get weekly calculations where the participant_id is in
            // one of the selected studies and cohorts.
            StringBuilder calculations_sql_str = new StringBuilder(
                "SELECT DISTINCT C.week_number, C.year_number FROM Calculations C");

            // Build the right table for left join, that is, the Participant table filtered to the
            // proper study-cohorts.
            StringBuilder participant_sql_str = new StringBuilder("SELECT participant_id FROM Participants");
            if (study_cohorts.Length > 0)
            {
                participant_sql_str.Append(" WHERE ");
            }

            int index = 0;
            foreach (KeyValuePair<string, int> sc_pair in study_cohorts)
            {
                participant_sql_str.Append($"(study = '{sc_pair.Key}' AND cohort = {sc_pair.Value})");

                index++;
                if (index < study_cohorts.Length)
                {
                    participant_sql_str.Append(" OR ");
                }
            }

            // join the query results for participants table with the calculation table.
            calculations_sql_str.Append($" INNER JOIN ({participant_sql_str.ToString()}) P ON C.participant_id = P.participant_id ORDER BY C.year_number ASC, C.week_number ASC");
            return this.ExecuteQuery(calculations_sql_str.ToString());
        }

        private void GetStudies()
        {
            DataTable query_results = this.ExecuteQuery("SELECT DISTINCT(study) FROM Participants ORDER BY study");

            int index = 0;
            foreach (DataRow row in query_results.Rows)
            {
                object study = row["study"];
                if (study.GetType() != typeof(DBNull))
                {
                    this.studies.Add((string)study);
                }

                index += 1;
            }
        }

        private void GetCalculationTableColumns()
        {
            DataTable query_results = this.ExecuteQuery("SHOW COLUMNS FROM Calculations");

            foreach (DataRow row in query_results.Rows)
            {
                object column_name = row["field"];
                if (column_name.GetType() == typeof(string))
                {
                    this.calculateTableColumns.Add((string)column_name);
                }
                else
                {
                    throw new NotImplementedException("GetCalculationTableColumns() cannot process results of type: " + column_name.GetType().ToString());
                }
            }
        }

        private DataTable ExecuteQuery(string sql_str)
        {
            DataTable sqlTable = new DataTable();

            try
            {
                // connect to database
                this.connection.Open();

                // configure sql query string and use reader to get data
                MySqlCommand command = new MySqlCommand();
                command.Connection = this.connection;
                command.CommandText = sql_str;
                this.reader = command.ExecuteReader();

                // store sql query in data table
                sqlTable.Load(this.reader);

                // close sql connection
                this.reader.Close();
                this.connection.Close();

            }
            catch (MySqlException ex)
            {
                MessageBox.Show(ex.Message);
            }

            this.connection.Close();

            return sqlTable;
        }
    }
}
