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

        public Controller()
        {
            this.database = null;
        }

        public void ConnectToDatabase(string server, string user, string password)
        {
            this.database = new EMMABackendSqlConnection(server, user, password);
        }
    }
}
