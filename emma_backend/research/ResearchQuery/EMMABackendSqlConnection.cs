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
        private MySqlDataReader reader;

        private string myConnectionString;

        private List<string> studies; // studies available from the database
        private List<KeyValuePair<string, int>> cohorts; // cohorts from selected studies

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
            }
            catch (MySqlException ex)
            {
                MessageBox.Show(ex.Message);
            }

            this.connection.Close();

            this.studies = new List<string>();
            this.cohorts = new List<KeyValuePair<string, int>>();

            this.GetStudies();
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

        public DataTable GetCalculationTable(KeyValuePair<string, int>[] cohorts)
        {
            StringBuilder sql_str = new StringBuilder("SELECT * FROM CALCULATIONS");

            return this.ExecuteQuery(sql_str.ToString());
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
