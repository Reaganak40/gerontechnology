using MySqlX.XDevAPI.Common;
using MySqlX.XDevAPI.Relational;
using System;
using System.Collections.Generic;
using System.Data;
using System.IO;
using System.Reflection;
using System.Text;
using System.Windows.Forms;

namespace ResearchQuery
{
    /// <summary>
    /// The form for all querying of the EMMA Database.
    /// </summary>
    public partial class QueryForm : Form
    {
        private Controller controller;
        private FilterSet filters;
        private string downloadPath;
        private int downloadTableCount;

        /// <summary>
        /// Initializes a new instance of the <see cref="QueryForm"/> class.
        /// </summary>
        public QueryForm()
        {
            this.InitializeComponent();

            // connect to the EMMA Backend server.
            this.controller = new Controller();
            if (!this.controller.ConnectToDatabase())
            {
                this.Shown += new EventHandler(this.ResearchQuery_CloseOnStart);
            }

            this.controller.LoadFilteringData();


            // initialize filters
            this.filters = new FilterSet(ref this.DailyVariableCheckbox, ref this.WeeklyVariablesCheckbox);

            // get all studies in the EMMA Backend database.
            this.InitializeStudyListBox();

            // programmatically adjust settings for DateRangeSelectionView
            this.InitializeDateRangeView();

            // programmatically adjust settings for CurrentCalculationTableView
            this.InitializeCalculationTableView();

            // Determine the automatic path to download calculation tables.
            this.downloadPath = string.Empty;
            this.InitializeDownloadPath();
            this.DownloadTableCount = 0;
        }

        private int DownloadTableCount
        {
            get
            {
                return this.downloadTableCount;
            }

            set
            {
                this.downloadTableCount = value;

                if (!this.CombineTablesCheckBox.Checked)
                {
                    StringBuilder sb = new StringBuilder($"Download Results ({this.downloadTableCount} table");
                    if (this.downloadTableCount != 1)
                    {
                        sb.Append('s');
                    }

                    sb.Append(')');

                    this.DownloadResultsButton.Text = sb.ToString();
                }
                else
                {
                    if (this.downloadTableCount == 0)
                    {
                        this.DownloadResultsButton.Text = "Download Results (0 tables)";
                    }
                    else
                    {
                        this.DownloadResultsButton.Text = "Download Results (1 table)";

                    }
                }
            }
        }

        private void InitializeStudyListBox()
        {
            // Get all the available studies in the database.
            string[] studies = this.controller.GetStudies();

            foreach (string study in studies)
            {
                this.StudyCheckListBox.Items.Add(study);
            }
        }

        private void InitializeDateRangeView()
        {
            foreach (DataGridViewColumn column in this.DateRangeSelectionView.Columns)
            {
                column.SortMode = DataGridViewColumnSortMode.NotSortable;
            }
        }

        private void InitializeCalculationTableView()
        {
            // enable double-buffering for calculation table display
            this.CurrentCalculationTableView.GetType()?.
                GetProperty("DoubleBuffered", BindingFlags.Instance | BindingFlags.NonPublic)?.
                SetValue(this.CurrentCalculationTableView, true, null);

            // apply these optiosn from improved performance
            this.CurrentCalculationTableView.RowHeadersVisible = false;
            this.CurrentCalculationTableView.RowHeadersWidthSizeMode = DataGridViewRowHeadersWidthSizeMode.EnableResizing;
        }

        private void InitializeDownloadPath()
        {
            string? dPath = Controller.GetDownloadFolderPath();

            if (dPath is null)
            {
                dPath = Directory.GetCurrentDirectory();
            }

            this.downloadPath = dPath;
            this.DownloadPathLabel.Text = "Download Path: " + dPath;
        }

        private void StudyCheckListBox_MouseUp(object sender, MouseEventArgs e)
        {
            // Updates the cohort options given the selected studies.
            if (sender.GetType() == typeof(CheckedListBox))
            {
                string[] selected_studies = new string[((CheckedListBox)sender).CheckedItems.Count];
                int index = 0;

                // clear cohort options and if nothing is selected leave it cleared
                this.CohortSelectionView.Rows.Clear();
                this.DateRangeSelectionView.Rows.Clear();
                this.DateRangeComboBox.SelectedIndex = -1;
                this.DateRangeComboBox.Enabled = false;
                this.ViewCalculationTableButton.Enabled = false;

                if (selected_studies.Length == 0)
                {
                    return;
                }

                // get the studies selected for further querying
                foreach (string study_name in ((CheckedListBox)sender).CheckedItems)
                {
                    selected_studies[index++] = study_name;
                }

                // update the cohort checklist
                this.ResetCohortSelections(this.controller.GetCohorts(selected_studies));
            }
        }

        private void ResetCohortSelections(KeyValuePair<string, int>[] study_cohort_pairs)
        {
            // Condition: The user has (de)selected a study, and the cohort options need to reset.
            int index = 0;
            foreach (KeyValuePair<string, int> study_cohort_pair in study_cohort_pairs)
            {
                index = this.CohortSelectionView.Rows.Add();
                this.CohortSelectionView.Rows[index].Cells["StudyOptionColumn"].Value = study_cohort_pair.Key;
                this.CohortSelectionView.Rows[index].Cells["StudyOptionColumn"].ReadOnly = true;

                this.CohortSelectionView.Rows[index].Cells["CohortSelectionColumn"].Value = study_cohort_pair.Value;
                this.CohortSelectionView.Rows[index].Cells["CohortSelectionColumn"].ReadOnly = true;
            }

            this.CohortSelectionView.ClearSelection();
        }

        private void CohortSelectionView_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            // updates checkbox if click a row, or the checkbox directly.
            var check = this.CohortSelectionView.Rows[e.RowIndex].Cells["CheckCohortColumn"].Value;
            if (check is null)
            {
                this.CohortSelectionView.Rows[e.RowIndex].Cells["CheckCohortColumn"].Value = true;
            }
            else
            {
                if ((bool)check)
                {
                    this.CohortSelectionView.Rows[e.RowIndex].Cells["CheckCohortColumn"].Value = false;
                }
                else
                {
                    this.CohortSelectionView.Rows[e.RowIndex].Cells["CheckCohortColumn"].Value = true;
                }
            }

            this.UpdateSelectedCohorts();
        }

        private void UpdateSelectedCohorts()
        {
            // Updates the filter for selected study and cohorts.
            List<KeyValuePair<string, int>> selected_cohorts = new List<KeyValuePair<string, int>>();
            foreach (DataGridViewRow cohort_row in this.CohortSelectionView.Rows)
            {
                if (Convert.ToBoolean(cohort_row.Cells["CheckCohortColumn"].Value))
                {
                    string study = (string)cohort_row.Cells["StudyOptionColumn"].Value;
                    int cohort = (int)cohort_row.Cells["CohortSelectionColumn"].Value;

                    selected_cohorts.Add(new KeyValuePair<string, int>(study, cohort));
                }
            }

            this.filters.UpdateSelectedCohorts(selected_cohorts);

            // if the user has selected at least one cohort, allow the user to select data ranges.
            this.ResetDateRangeSelections();
        }

        private void ResetDateRangeSelections()
        {
            DataTable results = this.controller.GetDateRanges(this.filters.SelectedCohorts);
            this.ViewCalculationTableButton.Enabled = false;
            this.DateRangeSelectionView.Rows.Clear();
            this.DateRangeComboBox.SelectedIndex = -1;
            this.DateRangeComboBox.Enabled = false;
            this.downloadTableCount = 0;


            int index = 0;
            foreach (DataRow row in results.Rows)
            {
                object week = row["week_number"];
                if (week.GetType() != typeof(int))
                {
                    throw new NotSupportedException("Row value for week_number should not be of type: " + week.GetType().ToString());
                }
                object year = row["year_number"];
                if (year.GetType() != typeof(int))
                {
                    throw new NotSupportedException("Row value for year_number should not be of type: " + week.GetType().ToString());
                }

                index = this.DateRangeSelectionView.Rows.Add();

                this.DateRangeSelectionView.Rows[index].Cells["WeekDateRangeColumn"].Value = week;
                this.DateRangeSelectionView.Rows[index].Cells["WeekDateRangeColumn"].ReadOnly = true;

                this.DateRangeSelectionView.Rows[index].Cells["YearDateRangeColumn"].Value = year;
                this.DateRangeSelectionView.Rows[index].Cells["YearDateRangeColumn"].ReadOnly = true;

                (string, string) startEndDate = Controller.GetCalenderDateRange((int)week, (int)year);
                this.DateRangeSelectionView.Rows[index].Cells["StartDateRangeColumn"].Value = startEndDate.Item1;
                this.DateRangeSelectionView.Rows[index].Cells["StartDateRangeColumn"].ReadOnly = true;

                this.DateRangeSelectionView.Rows[index].Cells["EndDateRangeColumn"].Value = startEndDate.Item2;
                this.DateRangeSelectionView.Rows[index].Cells["EndDateRangeColumn"].ReadOnly = true;
            }

            if (index != 0)
            {
                this.DateRangeComboBox.Enabled = true;
            }

            this.filters.ResetSelectedDateRanges(this.DateRangeSelectionView.Rows);
        }

        private void ViewCalculationTableButton_MouseClick(object sender, MouseEventArgs e)
        {
            // the user has clicked the view calculation table button, and we need to
            // now update the calculation table view.
            if (this.ViewCalculationTableButton.Enabled)
            {
                // Uses controller to logically create the data table for the users selected query.
                this.ShowNewCalculationTable(this.controller.GetCalculationTable(this.filters));
            }
        }

        private void ShowNewCalculationTable(DataTable? calculation_table)
        {
            this.CurrentCalculationTableView.DataSource = calculation_table;
        }

        private void DateRangeSelectionView_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex >= 0)
            {
                this.DateRangeComboBox.SelectedIndex = -1;

                // updates checkbox if click a row, or the checkbox directly.
                var check = this.DateRangeSelectionView.Rows[e.RowIndex].Cells["CheckDateRangeColumn"].Value;
                if (check is null)
                {
                    this.DateRangeSelectionView.Rows[e.RowIndex].Cells["CheckDateRangeColumn"].Value = true;
                }
                else
                {
                    if ((bool)check)
                    {
                        this.DateRangeSelectionView.Rows[e.RowIndex].Cells["CheckDateRangeColumn"].Value = false;
                    }
                    else
                    {
                        this.DateRangeSelectionView.Rows[e.RowIndex].Cells["CheckDateRangeColumn"].Value = true;
                    }
                }
            }

            this.CheckSelectedDateRanges();
        }

        private void CheckSelectedDateRanges()
        {
            foreach (DataGridViewRow date_range_row in this.DateRangeSelectionView.Rows)
            {
                if (Convert.ToBoolean(date_range_row.Cells["CheckDateRangeColumn"].Value))
                {
                    this.ViewCalculationTableButton.Enabled = true;
                    return;
                }
            }
            this.ViewCalculationTableButton.Enabled = false;
        }

        private void DateRangeComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (this.DateRangeComboBox.SelectedIndex >= 0)
            {

#pragma warning disable SA1312 // VariableNamesMustBeginWithLowerCaseLetter
                const int SELECT_ALL = 0;
                const int UNSELECT_ALL = 1;
                const int SELECT_NEWEST = 2;
#pragma warning restore SA1312 // VariableNamesMustBeginWithLowerCaseLetter

                switch (this.DateRangeComboBox.SelectedIndex)
                {
                    case SELECT_ALL:
                        foreach (DataGridViewRow row in this.DateRangeSelectionView.Rows)
                        {
                            row.Cells["CheckDateRangeColumn"].Value = true;
                        }

                        this.ViewCalculationTableButton.Enabled = true;
                        break;
                    case UNSELECT_ALL:
                        foreach (DataGridViewRow row in this.DateRangeSelectionView.Rows)
                        {
                            row.Cells["CheckDateRangeColumn"].Value = false;
                        }

                        this.ViewCalculationTableButton.Enabled = false;
                        break;
                    case SELECT_NEWEST:
                        // assumes bottom row is the newest
                        int newest_week = (int)this.DateRangeSelectionView.Rows[this.DateRangeSelectionView.Rows.Count - 1].Cells["WeekDateRangeColumn"].Value;
                        int newest_year = (int)this.DateRangeSelectionView.Rows[this.DateRangeSelectionView.Rows.Count - 1].Cells["YearDateRangeColumn"].Value;
                        foreach (DataGridViewRow row in this.DateRangeSelectionView.Rows)
                        {
                            int row_week = (int)row.Cells["WeekDateRangeColumn"].Value;
                            int row_year = (int)row.Cells["YearDateRangeColumn"].Value;

                            // get only rows that are within last 4 weeks of the newest row.
                            if ((((newest_week - row_week) < 4) && (newest_year == row_year)) ||
                                ((newest_week < 4) && (52 - row_week < 4 - newest_week) && ((row_year + 1) == newest_year)))
                            {
                                row.Cells["CheckDateRangeColumn"].Value = true;
                            }
                            else
                            {
                                row.Cells["CheckDateRangeColumn"].Value = false;
                            }
                        }

                        this.ViewCalculationTableButton.Enabled = true;
                        break;
                    default:
                        throw new Exception($"DateRangeComboBox Selected Index [{this.DateRangeComboBox.SelectedIndex}] is not defined.");
                }
            }
        }

        private void DateRangeSelectionView_CellValueChanged(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex != -1 && e.ColumnIndex == this.DateRangeSelectionView.Rows[e.RowIndex].Cells["CheckDateRangeColumn"].ColumnIndex)
            {
                int week = (int)this.DateRangeSelectionView.Rows[e.RowIndex].Cells["WeekDateRangeColumn"].Value;
                int year = (int)this.DateRangeSelectionView.Rows[e.RowIndex].Cells["YearDateRangeColumn"].Value;
                bool check = (bool)this.DateRangeSelectionView.Rows[e.RowIndex].Cells["CheckDateRangeColumn"].Value;

                if (check != this.filters.GetSelectedValueDateRange(week, year))
                {
                    this.DownloadTableCount += (check ? 1 : -1) * this.filters.SelectedCohorts.Length;
                    this.filters.UpdateSelectedDateRange(week, year, check);
                }

                this.SuccessLabel.Visible = false;
            }
        }

        private void DownloadPathLabel_SizeChanged(object sender, EventArgs e)
        {
            const int padding = 3;
            int y_absolute_val = this.DownloadResultsButton.Location.Y;

            this.DownloadPathLabel.Location = new Point(
                this.DownloadPathLabel.Location.X,
                y_absolute_val - padding - this.DownloadPathLabel.Size.Height);

            this.CombineTablesCheckBox.Location = new Point(
                this.CombineTablesCheckBox.Location.X,
                this.DownloadPathLabel.Location.Y - padding - this.CombineTablesCheckBox.Size.Height);
        }

        private void BrowseSaveDirButton_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog fb = new FolderBrowserDialog();

            if (fb.ShowDialog() == DialogResult.OK)
            {
                // Now here's our save folder
                this.downloadPath = fb.SelectedPath;
                this.DownloadPathLabel.Text = "Download Path: " + this.downloadPath;
                this.SuccessLabel.Visible = false;
            }
        }

        private void ViewCalculationTableButton_EnabledChanged(object sender, EventArgs e)
        {
            this.DownloadResultsButton.Enabled = this.ViewCalculationTableButton.Enabled;

            if (!this.DownloadResultsButton.Enabled)
            {
                this.DownloadTableCount = 0;
            }
        }

        private void DownloadResultsButton_MouseClick(object sender, MouseEventArgs e)
        {
            this.controller.SaveCalculationTables(this.downloadPath, this.filters);
            this.SuccessLabel.Visible = true;
        }

        private void CombineTablesCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            this.DownloadTableCount = this.DownloadTableCount;
            this.filters.CombineTables = this.CombineTablesCheckBox.Checked;
        }

        private void DownloadResultsButton_EnabledChanged(object sender, EventArgs e)
        {
            if (!this.DownloadResultsButton.Enabled)
            {
                this.SuccessLabel.Visible = false;
            }
        }
        private void ResearchQuery_CloseOnStart(object sender, EventArgs e)
        {
            this.Close();
        }
    }
}