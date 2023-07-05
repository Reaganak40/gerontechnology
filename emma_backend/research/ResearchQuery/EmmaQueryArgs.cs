using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResearchQuery
{
    internal struct EmmaQueryArgs
    {
        /// <summary>
        /// The studies and cohorts to look for.
        /// </summary>
        public KeyValuePair<string, int>[] StudyCohorts;

        /// <summary>
        /// The list filtered variables in the calculation table to include.
        /// </summary>
        public string[]? Variables;


        /// <summary>
        /// A list of selected date ranges to limit where to look for calculation tables.
        /// </summary>
        public (int, int)[] DateRanges;


        /// <summary>
        /// Gets or sets a value indicating whether or not to include the study and cohort in the search query.
        /// </summary>
        public bool AddStudyCohortColumns;


        public EmmaQueryArgs()
        {
            this.StudyCohorts = new KeyValuePair<string, int>[0];
            this.Variables = null;
            this.DateRanges = new (int, int)[0];
            this.AddStudyCohortColumns = false;
        }

    }
}
