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
        /// Updates the filtering option for selected study and cohorts.
        /// </summary>
        /// <param name="nSelectedCohorts">A new list of selected study,cohort pairs.</param>
        public void UpdateSelectedCohorts(List<KeyValuePair<string, int>> nSelectedCohorts)
        {
            this.selectedCohorts = nSelectedCohorts;
        }
    }
}
