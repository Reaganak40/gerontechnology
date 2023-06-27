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
            this.StudyCheckListBox = new System.Windows.Forms.CheckedListBox();
            this.StudyLabel = new System.Windows.Forms.Label();
            this.CohortLabel = new System.Windows.Forms.Label();
            this.CurrentCalculationTableView = new System.Windows.Forms.DataGridView();
            this.CohortSelectionView = new System.Windows.Forms.DataGridView();
            this.CheckCohortColumn = new System.Windows.Forms.DataGridViewCheckBoxColumn();
            this.StudyOptionColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.CohortSelectionColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.ViewCalculationTableButton = new System.Windows.Forms.Button();
            this.DailyVariableCheckbox = new System.Windows.Forms.CheckBox();
            this.WeeklyVariablesCheckbox = new System.Windows.Forms.CheckBox();
            this.FormSplitContainer = new System.Windows.Forms.SplitContainer();
            this.DateRangeLabel = new System.Windows.Forms.Label();
            this.DateRangeSelectionView = new System.Windows.Forms.DataGridView();
            this.CheckDateRangeColumn = new System.Windows.Forms.DataGridViewCheckBoxColumn();
            this.CohortSelectionDateRangeColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.StudySelectionDateRangeColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.WeekDateRangeColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.YearDateRangeColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.StartDateRangeColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            this.EndDateRangeColumn = new System.Windows.Forms.DataGridViewTextBoxColumn();
            ((System.ComponentModel.ISupportInitialize)(this.CurrentCalculationTableView)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.CohortSelectionView)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.FormSplitContainer)).BeginInit();
            this.FormSplitContainer.Panel1.SuspendLayout();
            this.FormSplitContainer.Panel2.SuspendLayout();
            this.FormSplitContainer.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.DateRangeSelectionView)).BeginInit();
            this.SuspendLayout();
            // 
            // StudyCheckListBox
            // 
            this.StudyCheckListBox.BackColor = System.Drawing.SystemColors.Control;
            this.StudyCheckListBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.StudyCheckListBox.CheckOnClick = true;
            this.StudyCheckListBox.FormattingEnabled = true;
            this.StudyCheckListBox.Location = new System.Drawing.Point(26, 45);
            this.StudyCheckListBox.Name = "StudyCheckListBox";
            this.StudyCheckListBox.Size = new System.Drawing.Size(177, 156);
            this.StudyCheckListBox.TabIndex = 0;
            this.StudyCheckListBox.MouseUp += new System.Windows.Forms.MouseEventHandler(this.StudyCheckListBox_MouseUp);
            // 
            // StudyLabel
            // 
            this.StudyLabel.AutoSize = true;
            this.StudyLabel.Location = new System.Drawing.Point(26, 22);
            this.StudyLabel.Name = "StudyLabel";
            this.StudyLabel.Size = new System.Drawing.Size(46, 20);
            this.StudyLabel.TabIndex = 1;
            this.StudyLabel.Text = "Study";
            // 
            // CohortLabel
            // 
            this.CohortLabel.AutoSize = true;
            this.CohortLabel.Location = new System.Drawing.Point(229, 22);
            this.CohortLabel.Name = "CohortLabel";
            this.CohortLabel.Size = new System.Drawing.Size(54, 20);
            this.CohortLabel.TabIndex = 3;
            this.CohortLabel.Text = "Cohort";
            // 
            // CurrentCalculationTableView
            // 
            this.CurrentCalculationTableView.AllowUserToAddRows = false;
            this.CurrentCalculationTableView.AllowUserToDeleteRows = false;
            this.CurrentCalculationTableView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            this.CurrentCalculationTableView.Dock = System.Windows.Forms.DockStyle.Fill;
            this.CurrentCalculationTableView.Location = new System.Drawing.Point(15, 15);
            this.CurrentCalculationTableView.Name = "CurrentCalculationTableView";
            this.CurrentCalculationTableView.ReadOnly = true;
            this.CurrentCalculationTableView.RowHeadersWidth = 51;
            this.CurrentCalculationTableView.RowTemplate.Height = 29;
            this.CurrentCalculationTableView.Size = new System.Drawing.Size(751, 823);
            this.CurrentCalculationTableView.TabIndex = 4;
            // 
            // CohortSelectionView
            // 
            this.CohortSelectionView.AllowUserToAddRows = false;
            this.CohortSelectionView.AllowUserToDeleteRows = false;
            this.CohortSelectionView.AllowUserToResizeColumns = false;
            this.CohortSelectionView.AllowUserToResizeRows = false;
            this.CohortSelectionView.BackgroundColor = System.Drawing.SystemColors.Control;
            this.CohortSelectionView.ColumnHeadersHeight = 29;
            this.CohortSelectionView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.DisableResizing;
            this.CohortSelectionView.ColumnHeadersVisible = false;
            this.CohortSelectionView.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.CheckCohortColumn,
            this.StudyOptionColumn,
            this.CohortSelectionColumn});
            this.CohortSelectionView.GridColor = System.Drawing.SystemColors.Control;
            this.CohortSelectionView.Location = new System.Drawing.Point(229, 45);
            this.CohortSelectionView.MultiSelect = false;
            this.CohortSelectionView.Name = "CohortSelectionView";
            this.CohortSelectionView.RowHeadersVisible = false;
            this.CohortSelectionView.RowHeadersWidth = 51;
            this.CohortSelectionView.RowTemplate.Height = 29;
            this.CohortSelectionView.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.CohortSelectionView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.CohortSelectionView.Size = new System.Drawing.Size(300, 158);
            this.CohortSelectionView.TabIndex = 5;
            this.CohortSelectionView.CellClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.CohortSelectionView_CellClick);
            // 
            // CheckCohortColumn
            // 
            this.CheckCohortColumn.HeaderText = "";
            this.CheckCohortColumn.MinimumWidth = 6;
            this.CheckCohortColumn.Name = "CheckCohortColumn";
            this.CheckCohortColumn.ReadOnly = true;
            this.CheckCohortColumn.Width = 50;
            // 
            // StudyOptionColumn
            // 
            this.StudyOptionColumn.HeaderText = "Study";
            this.StudyOptionColumn.MinimumWidth = 6;
            this.StudyOptionColumn.Name = "StudyOptionColumn";
            this.StudyOptionColumn.Width = 125;
            // 
            // CohortSelectionColumn
            // 
            this.CohortSelectionColumn.HeaderText = "Cohort #";
            this.CohortSelectionColumn.MinimumWidth = 6;
            this.CohortSelectionColumn.Name = "CohortSelectionColumn";
            this.CohortSelectionColumn.Width = 125;
            // 
            // ViewCalculationTableButton
            // 
            this.ViewCalculationTableButton.Enabled = false;
            this.ViewCalculationTableButton.Location = new System.Drawing.Point(26, 528);
            this.ViewCalculationTableButton.Name = "ViewCalculationTableButton";
            this.ViewCalculationTableButton.Size = new System.Drawing.Size(503, 29);
            this.ViewCalculationTableButton.TabIndex = 6;
            this.ViewCalculationTableButton.Text = "View Calculation Table";
            this.ViewCalculationTableButton.UseVisualStyleBackColor = true;
            this.ViewCalculationTableButton.MouseClick += new System.Windows.Forms.MouseEventHandler(this.ViewCalculationTableButton_MouseClick);
            // 
            // DailyVariableCheckbox
            // 
            this.DailyVariableCheckbox.AutoSize = true;
            this.DailyVariableCheckbox.Checked = true;
            this.DailyVariableCheckbox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.DailyVariableCheckbox.Location = new System.Drawing.Point(26, 468);
            this.DailyVariableCheckbox.Name = "DailyVariableCheckbox";
            this.DailyVariableCheckbox.Size = new System.Drawing.Size(129, 24);
            this.DailyVariableCheckbox.TabIndex = 7;
            this.DailyVariableCheckbox.Text = "Daily Variables";
            this.DailyVariableCheckbox.UseVisualStyleBackColor = true;
            // 
            // WeeklyVariablesCheckbox
            // 
            this.WeeklyVariablesCheckbox.AutoSize = true;
            this.WeeklyVariablesCheckbox.Checked = true;
            this.WeeklyVariablesCheckbox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.WeeklyVariablesCheckbox.Location = new System.Drawing.Point(26, 498);
            this.WeeklyVariablesCheckbox.Name = "WeeklyVariablesCheckbox";
            this.WeeklyVariablesCheckbox.Size = new System.Drawing.Size(142, 24);
            this.WeeklyVariablesCheckbox.TabIndex = 8;
            this.WeeklyVariablesCheckbox.Text = "Weekly Variables";
            this.WeeklyVariablesCheckbox.UseVisualStyleBackColor = true;
            // 
            // FormSplitContainer
            // 
            this.FormSplitContainer.Dock = System.Windows.Forms.DockStyle.Fill;
            this.FormSplitContainer.FixedPanel = System.Windows.Forms.FixedPanel.Panel1;
            this.FormSplitContainer.Location = new System.Drawing.Point(0, 0);
            this.FormSplitContainer.Name = "FormSplitContainer";
            // 
            // FormSplitContainer.Panel1
            // 
            this.FormSplitContainer.Panel1.Controls.Add(this.DateRangeLabel);
            this.FormSplitContainer.Panel1.Controls.Add(this.DateRangeSelectionView);
            this.FormSplitContainer.Panel1.Controls.Add(this.CohortSelectionView);
            this.FormSplitContainer.Panel1.Controls.Add(this.StudyCheckListBox);
            this.FormSplitContainer.Panel1.Controls.Add(this.WeeklyVariablesCheckbox);
            this.FormSplitContainer.Panel1.Controls.Add(this.StudyLabel);
            this.FormSplitContainer.Panel1.Controls.Add(this.DailyVariableCheckbox);
            this.FormSplitContainer.Panel1.Controls.Add(this.CohortLabel);
            this.FormSplitContainer.Panel1.Controls.Add(this.ViewCalculationTableButton);
            // 
            // FormSplitContainer.Panel2
            // 
            this.FormSplitContainer.Panel2.Controls.Add(this.CurrentCalculationTableView);
            this.FormSplitContainer.Panel2.Padding = new System.Windows.Forms.Padding(15);
            this.FormSplitContainer.Size = new System.Drawing.Size(1332, 853);
            this.FormSplitContainer.SplitterDistance = 547;
            this.FormSplitContainer.TabIndex = 9;
            // 
            // DateRangeLabel
            // 
            this.DateRangeLabel.AutoSize = true;
            this.DateRangeLabel.Location = new System.Drawing.Point(26, 225);
            this.DateRangeLabel.Name = "DateRangeLabel";
            this.DateRangeLabel.Size = new System.Drawing.Size(87, 20);
            this.DateRangeLabel.TabIndex = 10;
            this.DateRangeLabel.Text = "Date Range";
            // 
            // DateRangeSelectionView
            // 
            this.DateRangeSelectionView.AllowUserToAddRows = false;
            this.DateRangeSelectionView.AllowUserToDeleteRows = false;
            this.DateRangeSelectionView.AllowUserToResizeColumns = false;
            this.DateRangeSelectionView.AllowUserToResizeRows = false;
            this.DateRangeSelectionView.BackgroundColor = System.Drawing.SystemColors.Control;
            this.DateRangeSelectionView.ColumnHeadersHeight = 29;
            this.DateRangeSelectionView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.DisableResizing;
            this.DateRangeSelectionView.ColumnHeadersVisible = false;
            this.DateRangeSelectionView.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.CheckDateRangeColumn,
            this.CohortSelectionDateRangeColumn,
            this.StudySelectionDateRangeColumn,
            this.WeekDateRangeColumn,
            this.YearDateRangeColumn,
            this.StartDateRangeColumn,
            this.EndDateRangeColumn});
            this.DateRangeSelectionView.EditMode = System.Windows.Forms.DataGridViewEditMode.EditProgrammatically;
            this.DateRangeSelectionView.GridColor = System.Drawing.SystemColors.Control;
            this.DateRangeSelectionView.Location = new System.Drawing.Point(26, 248);
            this.DateRangeSelectionView.Name = "DateRangeSelectionView";
            this.DateRangeSelectionView.RowHeadersVisible = false;
            this.DateRangeSelectionView.RowHeadersWidth = 51;
            this.DateRangeSelectionView.RowTemplate.Height = 29;
            this.DateRangeSelectionView.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.DateRangeSelectionView.Size = new System.Drawing.Size(503, 198);
            this.DateRangeSelectionView.TabIndex = 9;
            // 
            // CheckDateRangeColumn
            // 
            this.CheckDateRangeColumn.HeaderText = "";
            this.CheckDateRangeColumn.MinimumWidth = 6;
            this.CheckDateRangeColumn.Name = "CheckDateRangeColumn";
            this.CheckDateRangeColumn.Width = 125;
            // 
            // CohortSelectionDateRangeColumn
            // 
            this.CohortSelectionDateRangeColumn.HeaderText = "Cohort #";
            this.CohortSelectionDateRangeColumn.MinimumWidth = 6;
            this.CohortSelectionDateRangeColumn.Name = "CohortSelectionDateRangeColumn";
            this.CohortSelectionDateRangeColumn.Width = 125;
            // 
            // StudySelectionDateRangeColumn
            // 
            this.StudySelectionDateRangeColumn.HeaderText = "Study";
            this.StudySelectionDateRangeColumn.MinimumWidth = 6;
            this.StudySelectionDateRangeColumn.Name = "StudySelectionDateRangeColumn";
            this.StudySelectionDateRangeColumn.Width = 125;
            // 
            // WeekDateRangeColumn
            // 
            this.WeekDateRangeColumn.HeaderText = "Week";
            this.WeekDateRangeColumn.MinimumWidth = 6;
            this.WeekDateRangeColumn.Name = "WeekDateRangeColumn";
            this.WeekDateRangeColumn.Width = 125;
            // 
            // YearDateRangeColumn
            // 
            this.YearDateRangeColumn.HeaderText = "Year";
            this.YearDateRangeColumn.MinimumWidth = 6;
            this.YearDateRangeColumn.Name = "YearDateRangeColumn";
            this.YearDateRangeColumn.Width = 125;
            // 
            // StartDateRangeColumn
            // 
            this.StartDateRangeColumn.HeaderText = "Start Date";
            this.StartDateRangeColumn.MinimumWidth = 6;
            this.StartDateRangeColumn.Name = "StartDateRangeColumn";
            this.StartDateRangeColumn.Width = 125;
            // 
            // EndDateRangeColumn
            // 
            this.EndDateRangeColumn.HeaderText = "End Date";
            this.EndDateRangeColumn.MinimumWidth = 6;
            this.EndDateRangeColumn.Name = "EndDateRangeColumn";
            this.EndDateRangeColumn.Width = 125;
            // 
            // QueryForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1332, 853);
            this.Controls.Add(this.FormSplitContainer);
            this.Name = "QueryForm";
            this.Text = "Research Query";
            ((System.ComponentModel.ISupportInitialize)(this.CurrentCalculationTableView)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.CohortSelectionView)).EndInit();
            this.FormSplitContainer.Panel1.ResumeLayout(false);
            this.FormSplitContainer.Panel1.PerformLayout();
            this.FormSplitContainer.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.FormSplitContainer)).EndInit();
            this.FormSplitContainer.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.DateRangeSelectionView)).EndInit();
            this.ResumeLayout(false);

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
        private DataGridViewCheckBoxColumn CheckDateRangeColumn;
        private DataGridViewTextBoxColumn CohortSelectionDateRangeColumn;
        private DataGridViewTextBoxColumn StudySelectionDateRangeColumn;
        private DataGridViewTextBoxColumn WeekDateRangeColumn;
        private DataGridViewTextBoxColumn YearDateRangeColumn;
        private DataGridViewTextBoxColumn StartDateRangeColumn;
        private DataGridViewTextBoxColumn EndDateRangeColumn;
        private DataGridViewCheckBoxColumn CheckCohortColumn;
        private DataGridViewTextBoxColumn StudyOptionColumn;
        private DataGridViewTextBoxColumn CohortSelectionColumn;
    }
}