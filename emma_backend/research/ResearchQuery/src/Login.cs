using Deedle;
using Microsoft.VisualBasic.ApplicationServices;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace ResearchQuery
{
    public partial class LoginForm : Form
    {
        internal EMMABackendSqlConnection? database;
        public LoginForm()
        {
            this.InitializeComponent();
        }

        /// <summary>
        /// Gets the database connection from the form.
        /// </summary>
        internal EMMABackendSqlConnection? Database
        {
            get
            {
                return this.database;
            }
        }

        private void LoginButton_Click(object sender, EventArgs e)
        {
            this.UseCredentials();
        }

        private void PasswordInput_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                this.UseCredentials();
            }
        }

        private void UseCredentials()
        {
            this.database = new EMMABackendSqlConnection(this.ServerInput.Text, this.UserInput.Text, this.PasswordInput.Text);

            if (this.database.Connected)
            {
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
            else
            {
                this.InvalidLabel.Visible = true;
                this.database = null;
            }
        }
    }
}
