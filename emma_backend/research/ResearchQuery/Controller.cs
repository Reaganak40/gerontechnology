using System;
using System.Collections.Generic;
using System.Data;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResearchQuery
{
    using System.Globalization;
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
        /// Gets the download path for a unix system.
        /// </summary>
        /// <returns>Returns the absolute path to the home directory.</returns>
        public static string? GetHomePath()
        {
            // Not in .NET 2.0
            // System.Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
            if (System.Environment.OSVersion.Platform == System.PlatformID.Unix)
            {
                return System.Environment.GetEnvironmentVariable("HOME");
            }

            return System.Environment.ExpandEnvironmentVariables("%HOMEDRIVE%%HOMEPATH%");
        }

        /// <summary>
        /// Finds the download path for the current system.
        /// </summary>
        /// <returns>An absolute path to the downloads directory.</returns>
        public static string? GetDownloadFolderPath()
        {
            if (System.Environment.OSVersion.Platform == System.PlatformID.Unix)
            {
                string? homepath = GetHomePath();
                if (homepath is null)
                {
                    return homepath;
                }

                string pathDownload = System.IO.Path.Combine(homepath, "Downloads");
                return pathDownload;
            }

            return System.Convert.ToString(
                Microsoft.Win32.Registry.GetValue(
                     @"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
                     "{374DE290-123F-4565-9164-39C4925E467B}",
                     string.Empty));
        }

        public static (string, string) GetCalenderDateRange(int week, int year)
        {
            DateTime end_date = ISOWeek.ToDateTime(year, week, DayOfWeek.Saturday);
            
            if (week == 1)
            {
                week = 53;
                year -= 1;
            }

            DateTime start_date = ISOWeek.ToDateTime(year, week-1, DayOfWeek.Sunday);

            return (start_date.ToString("yyyy-MM-dd"), end_date.ToString("yyyy-MM-dd"));
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
        /// Queries the database for the date ranges belonging to the selected study-cohorts.
        /// </summary>
        /// <param name="study_cohorts">A list of pairs with each study and cohort.</param>
        /// <returns>A sql queried datatable.</returns>
        public DataTable GetDateRanges(KeyValuePair<string, int>[] study_cohorts)
        {
            if (this.database == null || study_cohorts.Length == 0)
            {
                return new DataTable();
            }

            // use the selected study and cohorts to find what week,year items dates they belong to.
            return this.database.QueryDateRanges(study_cohorts);
        }

        /// <summary>
        /// Given querying parameters, gets updated table results to provide a view of calculations to the screen.
        /// </summary>
        /// <param name="filters">A wrapper containing all filtering parameters for the calculation table.</param>
        /// <returns>A filtered datatable according to the requested parameters.</returns>
        public DataTable? GetCalculationTable(FilterSet filters)
        {
            if (this.database == null)
            {
                return null;
            }

            DataTable calculation_table;
            EmmaQueryArgs queryArgs = new ();

            queryArgs.StudyCohorts = filters.SelectedCohorts;
            queryArgs.DateRanges = filters.SelectedDateRanges;

            // else: selected variables is set to null which will lead to: SELECT * FROM Calculations
            if (filters.SelectDailyVariables && !filters.SelectWeeklyVariables)
            {
                queryArgs.Variables = this.dailyVariables;
            }
            else if (!filters.SelectDailyVariables && filters.SelectWeeklyVariables)
            {
                queryArgs.Variables = this.weeklyVariables;
            }
            else if (!(filters.SelectDailyVariables && filters.SelectWeeklyVariables))
            {
                queryArgs.Variables = new string[0];
            }

            calculation_table = this.database.QueryCalculationTable(queryArgs);

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

        
    }
}
