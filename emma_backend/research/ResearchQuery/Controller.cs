using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResearchQuery
{
    internal class Controller
    {
        private EMMABackendSqlConnection? database;
        private string[] dailyVariables;
        private string[] weeklyVariables;

        /// <summary>
        /// Initializes a new instance of the <see cref="Controller"/> class.
        /// </summary>
        public Controller()
        {
            this.database = null;

            this.dailyVariables = new string[0];
            this.weeklyVariables = new string[0];
        }

        /// <summary>
        /// Initilize EMMA backend database connection.
        /// </summary>
        /// <param name="server">the name of the server-host where the EMMA Backend database is located.</param>
        /// <param name="user">username for credentials.</param>
        /// <param name="password">password for credentials.</param>
        public void ConnectToDatabase(string server, string user, string password)
        {
            this.database = new EMMABackendSqlConnection(server, user, password);
            if (!this.database.Connected)
            {
                this.database = null;
            }
        }

        /// <summary>
        /// Uses the database to get the filtering parameters beforehand.
        /// </summary>
        public void LoadFilteringData()
        {
            if (this.database == null)
            {
                return;
            }

            // get daily and weekly variables
            List<string> dv_list = new List<string>();
            List<string> wv_list = new List<string>();

            foreach (string variable in this.database.CalculationTableColumns)
            {
                if (variable.Equals("participant_id") || variable.Equals("week_number") || variable.Equals("year_number"))
                {
                    continue;
                }

                if (variable.Contains("Monday") || variable.Contains("Tuesday") || variable.Contains("Wednesday") ||
                    variable.Contains("Thursday") || variable.Contains("Friday") || variable.Contains("Saturday") || variable.Contains("Sunday"))
                {
                    dv_list.Add(variable);
                }
                else
                {
                    wv_list.Add(variable);
                }
            }

            this.dailyVariables = dv_list.ToArray();
            this.weeklyVariables = wv_list.ToArray();
        }

        /// <summary>
        /// Gets the studies in the database for the forms.
        /// </summary>
        /// <returns>The sql query result to find all the studies in the database.</returns>
        public string[] GetStudies()
        {
            if (this.database == null)
            {
                return new string[0];
            }

            return this.database.Studies;
        }

        /// <summary>
        /// Gets all cohorts from the selected studies.
        /// </summary>
        /// <param name="selected_studies">A list of valid studies to query the database with.</param>
        /// <returns>A formatted list of strings containing the study-cohort results.</returns>
        public KeyValuePair<string, int>[] GetCohorts(string[] selected_studies)
        {
            if (this.database == null)
            {
                return new KeyValuePair<string, int>[0];
            }

            return this.database.UpdateSelectedCohorts(selected_studies);
        }

        /// <summary>
        /// Given querying parameters, gets updated table results to provide a view of calculations to the screen.
        /// </summary>
        /// <param name="cohorts">What study-cohort pairs to look for.</param>
        /// <returns>A filtered datatable according to the requested parameters.</returns>
        public DataTable? GetCalculationTable(KeyValuePair<string, int>[] cohorts)
        {
            if (this.database == null)
            {
                return null;
            }

            DataTable calculation_table = this.database.GetCalculationTable(cohorts);

            // remove v_ from all variable column names.
            foreach (DataColumn variable_col in calculation_table.Columns)
            {
                if (!variable_col.ColumnName.Contains("v_"))
                {
                    continue;
                }

                variable_col.ColumnName = variable_col.ColumnName[2..];
            }

            return calculation_table;
        }

        /// <summary>
        /// Goes to the database to find the proper column names for the DataGridView.
        /// </summary>
        /// <returns>A list of column names.</returns>
        public string[] GetCalculationTableColumns()
        {
            if (this.database == null)
            {
                return new string[0];
            }

            return this.database.CalculationTableColumns;
        }
    }
}
