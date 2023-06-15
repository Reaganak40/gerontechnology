using MySql.Data.MySqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ResearchQuery
{
    internal class EMMABackendSqlConnection
    {
        private MySqlConnection connection;
        private string myConnectionString;
        
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
        }
    }
}
