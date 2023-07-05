using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResearchQuery
{

    /// <summary>
    /// A wrapper for all parameters that the application might need to filter calculation tables.
    /// </summary>
    internal class FilterSet
    {
        private CheckBox selectDailyVariablesRef;
        private CheckBox selectWeeklyVariablesRef;

        private List<KeyValuePair<string, int>> selectedCohorts;
        private Dictionary<(int, int), bool> selectedDateRanges;

        private bool combineTables;


        /// <summary>
        /// Initializes a new instance of the <see cref="FilterSet"/> class.
        /// </summary>
        /// <param name="daily_variable_checkbox">Used to supply a reference to the checkbox value for using daily variables.</param>
        /// <param name="weekly_variable_checkbox">Used to supply a reference to the checkbox value for using weekly variables.</param>
        public FilterSet(ref CheckBox daily_variable_checkbox, ref CheckBox weekly_variable_checkbox)
        {
            this.selectDailyVariablesRef = daily_variable_checkbox;
            this.selectWeeklyVariablesRef = weekly_variable_checkbox;

            this.selectedCohorts = new List<KeyValuePair<string, int>>();
            this.selectedDateRanges = new Dictionary<(int, int), bool>();
        }

        /// <summary>
        /// Gets a value indicating whether or not a calculation table should contain daily variables.
        /// </summary>
        public bool SelectDailyVariables
        {
            get
            {
                return this.selectDailyVariablesRef.Checked;
            }
        }

        /// <summary>
        /// Gets a value indicating whether or not a calculation table should contain weekly variables.
        /// </summary>
        public bool SelectWeeklyVariables
        {
            get
            {
                return this.selectWeeklyVariablesRef.Checked;
            }
        }

        /// <summary>
        /// Gets a list of string,int pairs for all the study,cohorts the user has selected to view.
        /// </summary>
        public KeyValuePair<string, int>[] SelectedCohorts
        {
            get
            {
                return this.selectedCohorts.ToArray();
            }
        }

        /// <summary>
        /// Gets a list of week,year tuples the user has selected to filter the calculation table by.
        /// </summary>
        public (int, int)[] SelectedDateRanges
        {
            get
            {
                List<(int, int)> selected_ranges = new List<(int, int)>();

                foreach (var item in this.selectedDateRanges)
                {
                    if (item.Value)
                    {
                        selected_ranges.Add(item.Key);
                    }
                }

                return selected_ranges.ToArray();
            }
        }

        /// <summary>
        /// Gets or sets a value indicating whether to combine the tables when downloading the query.
        /// </summary>
        public bool CombineTables
        {
            get
            {
                return this.combineTables;
            }

            set
            {
                this.combineTables = value;
            }
        }


        /// <summary>
        /// Updates the filtering option for selected study and cohorts.
        /// </summary>
        /// <param name="nSelectedCohorts">A new list of selected study,cohort pairs.</param>
        public void UpdateSelectedCohorts(List<KeyValuePair<string, int>> nSelectedCohorts)
        {
            this.selectedCohorts = nSelectedCohorts;
        }

        /// <summary>
        /// Creates a new selected date range list, storing all the available data ranges with their boolean check values.
        /// </summary>
        /// <param name="dateRangeRows">An already initialized collection of date ranges.</param>
        public void ResetSelectedDateRanges(DataGridViewRowCollection dateRangeRows)
        {
            this.selectedDateRanges = new Dictionary<(int, int), bool>();


            foreach (DataGridViewRow row in dateRangeRows) 
            {
                int week = (int)row.Cells["WeekDateRangeColumn"].Value;
                int year = (int)row.Cells["YearDateRangeColumn"].Value;
                var check = row.Cells["CheckDateRangeColumn"].Value;

                if (check is null)
                {
                    check = false;
                }

                this.selectedDateRanges[(week, year)] = (bool)check;
            }
        }

        /// <summary>
        /// Update a week,year date range to be checked or not checked (to use in calculations).
        /// </summary>
        /// <param name="week">Week of the calculation table.</param>
        /// <param name="year">Year of the calculation table.</param>
        /// <param name="check">True, when the user wants to include in query.</param>
        public void UpdateSelectedDateRange(int week, int year, bool check)
        {
            this.selectedDateRanges[(week, year)] = check;
        }

        /// <summary>
        /// Gets the value indicating whether the date range for the given week and year has been selected.
        /// </summary>
        /// <param name="week">Week of the calculation table.</param>
        /// <param name="year">Year of the calculation table.</param>
        /// <returns>True if the user has selected this week,year.</returns>
        public bool GetSelectedValueDateRange(int week, int year)
        {
            return this.selectedDateRanges[(week, year)];
        }

    }
}
