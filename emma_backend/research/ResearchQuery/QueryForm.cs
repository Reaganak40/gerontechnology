using MySqlX.XDevAPI.Common;
using System;
using System.Collections.Generic;
using System.Data;
using System.Reflection;
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

        /// <summary>
        /// Initializes a new instance of the <see cref="QueryForm"/> class.
        /// </summary>
        public QueryForm()
        {
            this.InitializeComponent();

            // connect to the EMMA Backend server.
            this.controller = new Controller();
            this.controller.ConnectToDatabase("localhost", "root", "root");
            this.controller.LoadFilteringData();

            // initialize filters
            this.filters = new FilterSet(ref this.DailyVariableCheckbox, ref this.WeeklyVariablesCheckbox);

            // get all studies in the EMMA Backend database.
            this.InitializeStudyListBox();

            // programmatically adjust settings for DateRangeSelectionView
            this.InitializeDateRangeView();

            // programmatically adjust settings for CurrentCalculationTableView
            this.InitializeCalculationTableView();
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

                this.DateRangeSelectionView.Rows[index].Cells["StartDateRangeColumn"].Value = "Not implemented.";
                this.DateRangeSelectionView.Rows[index].Cells["StartDateRangeColumn"].ReadOnly = true;

                this.DateRangeSelectionView.Rows[index].Cells["EndDateRangeColumn"].Value = "NI";
                this.DateRangeSelectionView.Rows[index].Cells["EndDateRangeColumn"].ReadOnly = true;
            }
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

            this.UpdateSelectedDateRanges();
        }

        private void UpdateSelectedDateRanges()
        {
            // Updates the filter for selected study and cohorts.
            this.ViewCalculationTableButton.Enabled = false;
            List<KeyValuePair<int, int>> selected_dates = new List<KeyValuePair<int, int>>();
            foreach (DataGridViewRow date_range_row in this.DateRangeSelectionView.Rows)
            {
                if (Convert.ToBoolean(date_range_row.Cells["CheckDateRangeColumn"].Value))
                {
                    this.ViewCalculationTableButton.Enabled = true;

                    int week = (int)date_range_row.Cells["WeekDateRangeColumn"].Value;
                    int year = (int)date_range_row.Cells["YearDateRangeColumn"].Value;

                    selected_dates.Add(new KeyValuePair<int, int>(week, year));
                }
            }
        }
    }
}