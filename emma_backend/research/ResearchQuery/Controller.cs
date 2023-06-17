using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResearchQuery
{
    internal class Controller
    {
        private EMMABackendSqlConnection? database;

        /// <summary>
        /// Initializes a new instance of the <see cref="Controller"/> class.
        /// </summary>
        public Controller()
        {
            this.database = null;
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

        public string[] GetCohorts(string[] selected_studies)
        {
            if (this.database == null)
            {
                return new string[0];
            }

            return this.database.GetCohortsFrom(selected_studies);
        }
    }
}
