namespace ResearchQuery
{
    public partial class QueryForm : Form
    {
        private Controller controller;
        public QueryForm()
        {
            this.InitializeComponent();

            this.controller = new Controller();
            this.controller.ConnectToDatabase("localhost", "g", "root");

        }
    }
}