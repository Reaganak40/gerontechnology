namespace ResearchQuery
{
    partial class QueryForm
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            StudyCheckListBox = new CheckedListBox();
            StudyLabel = new Label();
            CohortLabel = new Label();
            CurrentCalculationTableView = new DataGridView();
            CohortSelectionView = new DataGridView();
            CheckCohortColumn = new DataGridViewCheckBoxColumn();
            StudyOptionColumn = new DataGridViewTextBoxColumn();
            CohortSelectionColumn = new DataGridViewTextBoxColumn();
            ViewCalculationTableButton = new Button();
            DailyVariableCheckbox = new CheckBox();
            WeeklyVariablesCheckbox = new CheckBox();
            FormSplitContainer = new SplitContainer();
            panel1 = new Panel();
            SuccessLabel = new Label();
            CombineTablesCheckBox = new CheckBox();
            BrowseSaveDirButton = new Button();
            DownloadPathLabel = new Label();
            DownloadResultsButton = new Button();
            DateRangeComboBox = new ComboBox();
            DateRangeLabel = new Label();
            DateRangeSelectionView = new DataGridView();
            CheckDateRangeColumn = new DataGridViewCheckBoxColumn();
            WeekDateRangeColumn = new DataGridViewTextBoxColumn();
            YearDateRangeColumn = new DataGridViewTextBoxColumn();
            StartDateRangeColumn = new DataGridViewTextBoxColumn();
            EndDateRangeColumn = new DataGridViewTextBoxColumn();
            ((System.ComponentModel.ISupportInitialize)CurrentCalculationTableView).BeginInit();
            ((System.ComponentModel.ISupportInitialize)CohortSelectionView).BeginInit();
            ((System.ComponentModel.ISupportInitialize)FormSplitContainer).BeginInit();
            FormSplitContainer.Panel1.SuspendLayout();
            FormSplitContainer.Panel2.SuspendLayout();
            FormSplitContainer.SuspendLayout();
            panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)DateRangeSelectionView).BeginInit();
            SuspendLayout();
            // 
            // StudyCheckListBox
            // 
            StudyCheckListBox.BackColor = SystemColors.Control;
            StudyCheckListBox.BorderStyle = BorderStyle.FixedSingle;
            StudyCheckListBox.CheckOnClick = true;
            StudyCheckListBox.FormattingEnabled = true;
            StudyCheckListBox.Location = new Point(26, 45);
            StudyCheckListBox.Name = "StudyCheckListBox";
            StudyCheckListBox.Size = new Size(177, 156);
            StudyCheckListBox.TabIndex = 0;
            StudyCheckListBox.MouseUp += StudyCheckListBox_MouseUp;
            // 
            // StudyLabel
            // 
            StudyLabel.AutoSize = true;
            StudyLabel.Location = new Point(26, 22);
            StudyLabel.Name = "StudyLabel";
            StudyLabel.Size = new Size(46, 20);
            StudyLabel.TabIndex = 1;
            StudyLabel.Text = "Study";
            // 
            // CohortLabel
            // 
            CohortLabel.AutoSize = true;
            CohortLabel.Location = new Point(229, 22);
            CohortLabel.Name = "CohortLabel";
            CohortLabel.Size = new Size(54, 20);
            CohortLabel.TabIndex = 3;
            CohortLabel.Text = "Cohort";
            // 
            // CurrentCalculationTableView
            // 
            CurrentCalculationTableView.AllowUserToAddRows = false;
            CurrentCalculationTableView.AllowUserToDeleteRows = false;
            CurrentCalculationTableView.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            CurrentCalculationTableView.Dock = DockStyle.Fill;
            CurrentCalculationTableView.Location = new Point(15, 15);
            CurrentCalculationTableView.Name = "CurrentCalculationTableView";
            CurrentCalculationTableView.ReadOnly = true;
            CurrentCalculationTableView.RowHeadersWidth = 51;
            CurrentCalculationTableView.RowTemplate.Height = 29;
            CurrentCalculationTableView.Size = new Size(733, 695);
            CurrentCalculationTableView.TabIndex = 4;
            // 
            // CohortSelectionView
            // 
            CohortSelectionView.AllowUserToAddRows = false;
            CohortSelectionView.AllowUserToDeleteRows = false;
            CohortSelectionView.AllowUserToResizeColumns = false;
            CohortSelectionView.AllowUserToResizeRows = false;
            CohortSelectionView.BackgroundColor = SystemColors.Control;
            CohortSelectionView.ColumnHeadersHeight = 29;
            CohortSelectionView.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.DisableResizing;
            CohortSelectionView.ColumnHeadersVisible = false;
            CohortSelectionView.Columns.AddRange(new DataGridViewColumn[] { CheckCohortColumn, StudyOptionColumn, CohortSelectionColumn });
            CohortSelectionView.GridColor = SystemColors.Control;
            CohortSelectionView.Location = new Point(229, 45);
            CohortSelectionView.MultiSelect = false;
            CohortSelectionView.Name = "CohortSelectionView";
            CohortSelectionView.RowHeadersVisible = false;
            CohortSelectionView.RowHeadersWidth = 51;
            CohortSelectionView.RowTemplate.Height = 29;
            CohortSelectionView.ScrollBars = ScrollBars.Vertical;
            CohortSelectionView.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            CohortSelectionView.Size = new Size(300, 158);
            CohortSelectionView.TabIndex = 5;
            CohortSelectionView.CellClick += CohortSelectionView_CellClick;
            // 
            // CheckCohortColumn
            // 
            CheckCohortColumn.HeaderText = "";
            CheckCohortColumn.MinimumWidth = 6;
            CheckCohortColumn.Name = "CheckCohortColumn";
            CheckCohortColumn.ReadOnly = true;
            CheckCohortColumn.Width = 50;
            // 
            // StudyOptionColumn
            // 
            StudyOptionColumn.HeaderText = "Study";
            StudyOptionColumn.MinimumWidth = 6;
            StudyOptionColumn.Name = "StudyOptionColumn";
            StudyOptionColumn.Width = 125;
            // 
            // CohortSelectionColumn
            // 
            CohortSelectionColumn.HeaderText = "Cohort #";
            CohortSelectionColumn.MinimumWidth = 6;
            CohortSelectionColumn.Name = "CohortSelectionColumn";
            CohortSelectionColumn.Width = 125;
            // 
            // ViewCalculationTableButton
            // 
            ViewCalculationTableButton.Enabled = false;
            ViewCalculationTableButton.Location = new Point(26, 525);
            ViewCalculationTableButton.Name = "ViewCalculationTableButton";
            ViewCalculationTableButton.Size = new Size(503, 29);
            ViewCalculationTableButton.TabIndex = 6;
            ViewCalculationTableButton.Text = "View Calculation Table";
            ViewCalculationTableButton.UseVisualStyleBackColor = true;
            ViewCalculationTableButton.EnabledChanged += ViewCalculationTableButton_EnabledChanged;
            ViewCalculationTableButton.MouseClick += ViewCalculationTableButton_MouseClick;
            // 
            // DailyVariableCheckbox
            // 
            DailyVariableCheckbox.AutoSize = true;
            DailyVariableCheckbox.Checked = true;
            DailyVariableCheckbox.CheckState = CheckState.Checked;
            DailyVariableCheckbox.Location = new Point(26, 465);
            DailyVariableCheckbox.Name = "DailyVariableCheckbox";
            DailyVariableCheckbox.Size = new Size(129, 24);
            DailyVariableCheckbox.TabIndex = 7;
            DailyVariableCheckbox.Text = "Daily Variables";
            DailyVariableCheckbox.UseVisualStyleBackColor = true;
            // 
            // WeeklyVariablesCheckbox
            // 
            WeeklyVariablesCheckbox.AutoSize = true;
            WeeklyVariablesCheckbox.Checked = true;
            WeeklyVariablesCheckbox.CheckState = CheckState.Checked;
            WeeklyVariablesCheckbox.Location = new Point(26, 495);
            WeeklyVariablesCheckbox.Name = "WeeklyVariablesCheckbox";
            WeeklyVariablesCheckbox.Size = new Size(142, 24);
            WeeklyVariablesCheckbox.TabIndex = 8;
            WeeklyVariablesCheckbox.Text = "Weekly Variables";
            WeeklyVariablesCheckbox.UseVisualStyleBackColor = true;
            // 
            // FormSplitContainer
            // 
            FormSplitContainer.Dock = DockStyle.Fill;
            FormSplitContainer.FixedPanel = FixedPanel.Panel1;
            FormSplitContainer.Location = new Point(0, 0);
            FormSplitContainer.Name = "FormSplitContainer";
            // 
            // FormSplitContainer.Panel1
            // 
            FormSplitContainer.Panel1.Controls.Add(panel1);
            FormSplitContainer.Panel1.Controls.Add(DateRangeComboBox);
            FormSplitContainer.Panel1.Controls.Add(DateRangeLabel);
            FormSplitContainer.Panel1.Controls.Add(DateRangeSelectionView);
            FormSplitContainer.Panel1.Controls.Add(CohortSelectionView);
            FormSplitContainer.Panel1.Controls.Add(StudyCheckListBox);
            FormSplitContainer.Panel1.Controls.Add(WeeklyVariablesCheckbox);
            FormSplitContainer.Panel1.Controls.Add(StudyLabel);
            FormSplitContainer.Panel1.Controls.Add(DailyVariableCheckbox);
            FormSplitContainer.Panel1.Controls.Add(CohortLabel);
            FormSplitContainer.Panel1.Controls.Add(ViewCalculationTableButton);
            // 
            // FormSplitContainer.Panel2
            // 
            FormSplitContainer.Panel2.Controls.Add(CurrentCalculationTableView);
            FormSplitContainer.Panel2.Padding = new Padding(15);
            FormSplitContainer.Size = new Size(1314, 725);
            FormSplitContainer.SplitterDistance = 547;
            FormSplitContainer.TabIndex = 9;
            // 
            // panel1
            // 
            panel1.Controls.Add(SuccessLabel);
            panel1.Controls.Add(CombineTablesCheckBox);
            panel1.Controls.Add(BrowseSaveDirButton);
            panel1.Controls.Add(DownloadPathLabel);
            panel1.Controls.Add(DownloadResultsButton);
            panel1.Dock = DockStyle.Bottom;
            panel1.Location = new Point(0, 560);
            panel1.Name = "panel1";
            panel1.Size = new Size(547, 165);
            panel1.TabIndex = 16;
            // 
            // SuccessLabel
            // 
            SuccessLabel.AutoSize = true;
            SuccessLabel.ForeColor = Color.ForestGreen;
            SuccessLabel.Location = new Point(26, 122);
            SuccessLabel.Name = "SuccessLabel";
            SuccessLabel.Size = new Size(63, 20);
            SuccessLabel.TabIndex = 16;
            SuccessLabel.Text = "Success!";
            SuccessLabel.Visible = false;
            // 
            // CombineTablesCheckBox
            // 
            CombineTablesCheckBox.AutoSize = true;
            CombineTablesCheckBox.Location = new Point(26, 39);
            CombineTablesCheckBox.Name = "CombineTablesCheckBox";
            CombineTablesCheckBox.Size = new Size(136, 24);
            CombineTablesCheckBox.TabIndex = 14;
            CombineTablesCheckBox.Text = "Combine Tables";
            CombineTablesCheckBox.UseVisualStyleBackColor = true;
            CombineTablesCheckBox.CheckedChanged += CombineTablesCheckBox_CheckedChanged;
            // 
            // BrowseSaveDirButton
            // 
            BrowseSaveDirButton.Location = new Point(385, 89);
            BrowseSaveDirButton.Name = "BrowseSaveDirButton";
            BrowseSaveDirButton.Size = new Size(144, 29);
            BrowseSaveDirButton.TabIndex = 13;
            BrowseSaveDirButton.Text = "Browse";
            BrowseSaveDirButton.UseVisualStyleBackColor = true;
            BrowseSaveDirButton.Click += BrowseSaveDirButton_Click;
            // 
            // DownloadPathLabel
            // 
            DownloadPathLabel.AutoSize = true;
            DownloadPathLabel.Location = new Point(26, 66);
            DownloadPathLabel.MaximumSize = new Size(500, 0);
            DownloadPathLabel.Name = "DownloadPathLabel";
            DownloadPathLabel.Size = new Size(113, 20);
            DownloadPathLabel.TabIndex = 15;
            DownloadPathLabel.Text = "Download Path:";
            DownloadPathLabel.SizeChanged += DownloadPathLabel_SizeChanged;
            // 
            // DownloadResultsButton
            // 
            DownloadResultsButton.Enabled = false;
            DownloadResultsButton.Location = new Point(26, 89);
            DownloadResultsButton.Name = "DownloadResultsButton";
            DownloadResultsButton.Size = new Size(353, 29);
            DownloadResultsButton.TabIndex = 12;
            DownloadResultsButton.Text = "Download Results";
            DownloadResultsButton.UseVisualStyleBackColor = true;
            DownloadResultsButton.EnabledChanged += DownloadResultsButton_EnabledChanged;
            DownloadResultsButton.MouseClick += DownloadResultsButton_MouseClick;
            // 
            // DateRangeComboBox
            // 
            DateRangeComboBox.DropDownStyle = ComboBoxStyle.DropDownList;
            DateRangeComboBox.Enabled = false;
            DateRangeComboBox.FormattingEnabled = true;
            DateRangeComboBox.Items.AddRange(new object[] { "Select All", "Unselect All", "Select Newest" });
            DateRangeComboBox.Location = new Point(378, 225);
            DateRangeComboBox.Name = "DateRangeComboBox";
            DateRangeComboBox.Size = new Size(151, 28);
            DateRangeComboBox.TabIndex = 11;
            DateRangeComboBox.SelectedIndexChanged += DateRangeComboBox_SelectedIndexChanged;
            // 
            // DateRangeLabel
            // 
            DateRangeLabel.AutoSize = true;
            DateRangeLabel.Location = new Point(26, 238);
            DateRangeLabel.Name = "DateRangeLabel";
            DateRangeLabel.Size = new Size(87, 20);
            DateRangeLabel.TabIndex = 10;
            DateRangeLabel.Text = "Date Range";
            // 
            // DateRangeSelectionView
            // 
            DateRangeSelectionView.AllowUserToAddRows = false;
            DateRangeSelectionView.AllowUserToDeleteRows = false;
            DateRangeSelectionView.AllowUserToResizeColumns = false;
            DateRangeSelectionView.AllowUserToResizeRows = false;
            DateRangeSelectionView.BackgroundColor = SystemColors.Control;
            DateRangeSelectionView.ColumnHeadersHeight = 29;
            DateRangeSelectionView.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.DisableResizing;
            DateRangeSelectionView.Columns.AddRange(new DataGridViewColumn[] { CheckDateRangeColumn, WeekDateRangeColumn, YearDateRangeColumn, StartDateRangeColumn, EndDateRangeColumn });
            DateRangeSelectionView.EditMode = DataGridViewEditMode.EditProgrammatically;
            DateRangeSelectionView.GridColor = SystemColors.Control;
            DateRangeSelectionView.Location = new Point(26, 261);
            DateRangeSelectionView.MultiSelect = false;
            DateRangeSelectionView.Name = "DateRangeSelectionView";
            DateRangeSelectionView.RowHeadersVisible = false;
            DateRangeSelectionView.RowHeadersWidth = 51;
            DateRangeSelectionView.RowTemplate.Height = 29;
            DateRangeSelectionView.ScrollBars = ScrollBars.Vertical;
            DateRangeSelectionView.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            DateRangeSelectionView.Size = new Size(503, 198);
            DateRangeSelectionView.TabIndex = 9;
            DateRangeSelectionView.CellClick += DateRangeSelectionView_CellClick;
            DateRangeSelectionView.CellValueChanged += DateRangeSelectionView_CellValueChanged;
            // 
            // CheckDateRangeColumn
            // 
            CheckDateRangeColumn.HeaderText = "";
            CheckDateRangeColumn.MinimumWidth = 6;
            CheckDateRangeColumn.Name = "CheckDateRangeColumn";
            CheckDateRangeColumn.Width = 50;
            // 
            // WeekDateRangeColumn
            // 
            WeekDateRangeColumn.HeaderText = "Week";
            WeekDateRangeColumn.MinimumWidth = 6;
            WeekDateRangeColumn.Name = "WeekDateRangeColumn";
            WeekDateRangeColumn.Width = 75;
            // 
            // YearDateRangeColumn
            // 
            YearDateRangeColumn.HeaderText = "Year";
            YearDateRangeColumn.MinimumWidth = 6;
            YearDateRangeColumn.Name = "YearDateRangeColumn";
            YearDateRangeColumn.Width = 75;
            // 
            // StartDateRangeColumn
            // 
            StartDateRangeColumn.HeaderText = "Start Date";
            StartDateRangeColumn.MinimumWidth = 6;
            StartDateRangeColumn.Name = "StartDateRangeColumn";
            StartDateRangeColumn.Width = 150;
            // 
            // EndDateRangeColumn
            // 
            EndDateRangeColumn.HeaderText = "End Date";
            EndDateRangeColumn.MinimumWidth = 6;
            EndDateRangeColumn.Name = "EndDateRangeColumn";
            EndDateRangeColumn.Width = 150;
            // 
            // QueryForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(1314, 725);
            Controls.Add(FormSplitContainer);
            Name = "QueryForm";
            Text = "Research Query v1.2";
            ((System.ComponentModel.ISupportInitialize)CurrentCalculationTableView).EndInit();
            ((System.ComponentModel.ISupportInitialize)CohortSelectionView).EndInit();
            FormSplitContainer.Panel1.ResumeLayout(false);
            FormSplitContainer.Panel1.PerformLayout();
            FormSplitContainer.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)FormSplitContainer).EndInit();
            FormSplitContainer.ResumeLayout(false);
            panel1.ResumeLayout(false);
            panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)DateRangeSelectionView).EndInit();
            ResumeLayout(false);
        }

        #endregion

        private CheckedListBox StudyCheckListBox;
        private Label StudyLabel;
        private Label CohortLabel;
        private DataGridView CurrentCalculationTableView;
        private DataGridView CohortSelectionView;
        private Button ViewCalculationTableButton;
        private CheckBox DailyVariableCheckbox;
        private CheckBox WeeklyVariablesCheckbox;
        private SplitContainer FormSplitContainer;
        private Label DateRangeLabel;
        private DataGridView DateRangeSelectionView;
        private DataGridViewCheckBoxColumn CheckCohortColumn;
        private DataGridViewTextBoxColumn StudyOptionColumn;
        private DataGridViewTextBoxColumn CohortSelectionColumn;
        private DataGridViewCheckBoxColumn CheckDateRangeColumn;
        private DataGridViewTextBoxColumn WeekDateRangeColumn;
        private DataGridViewTextBoxColumn YearDateRangeColumn;
        private DataGridViewTextBoxColumn StartDateRangeColumn;
        private DataGridViewTextBoxColumn EndDateRangeColumn;
        private ComboBox DateRangeComboBox;
        private CheckBox CombineTablesCheckBox;
        private Button BrowseSaveDirButton;
        private Button DownloadResultsButton;
        private Label DownloadPathLabel;
        private Panel panel1;
        private Label SuccessLabel;
    }
}