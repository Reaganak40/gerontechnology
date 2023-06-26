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
            this.splitContainer1 = new System.Windows.Forms.SplitContainer();
            ((System.ComponentModel.ISupportInitialize)(this.CurrentCalculationTableView)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.CohortSelectionView)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).BeginInit();
            this.splitContainer1.Panel1.SuspendLayout();
            this.splitContainer1.Panel2.SuspendLayout();
            this.splitContainer1.SuspendLayout();
            this.SuspendLayout();
            // 
            // StudyCheckListBox
            // 
            this.StudyCheckListBox.CheckOnClick = true;
            this.StudyCheckListBox.FormattingEnabled = true;
            this.StudyCheckListBox.Location = new System.Drawing.Point(26, 43);
            this.StudyCheckListBox.Name = "StudyCheckListBox";
            this.StudyCheckListBox.Size = new System.Drawing.Size(177, 158);
            this.StudyCheckListBox.TabIndex = 0;
            this.StudyCheckListBox.MouseUp += new System.Windows.Forms.MouseEventHandler(this.StudyCheckListBox_MouseUp);
            // 
            // StudyLabel
            // 
            this.StudyLabel.AutoSize = true;
            this.StudyLabel.Location = new System.Drawing.Point(26, 20);
            this.StudyLabel.Name = "StudyLabel";
            this.StudyLabel.Size = new System.Drawing.Size(46, 20);
            this.StudyLabel.TabIndex = 1;
            this.StudyLabel.Text = "Study";
            // 
            // CohortLabel
            // 
            this.CohortLabel.AutoSize = true;
            this.CohortLabel.Location = new System.Drawing.Point(229, 20);
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
            this.CurrentCalculationTableView.Location = new System.Drawing.Point(0, 0);
            this.CurrentCalculationTableView.Name = "CurrentCalculationTableView";
            this.CurrentCalculationTableView.ReadOnly = true;
            this.CurrentCalculationTableView.RowHeadersWidth = 51;
            this.CurrentCalculationTableView.RowTemplate.Height = 29;
            this.CurrentCalculationTableView.Size = new System.Drawing.Size(771, 853);
            this.CurrentCalculationTableView.TabIndex = 4;
            // 
            // CohortSelectionView
            // 
            this.CohortSelectionView.AllowUserToAddRows = false;
            this.CohortSelectionView.AllowUserToDeleteRows = false;
            this.CohortSelectionView.AllowUserToResizeColumns = false;
            this.CohortSelectionView.AllowUserToResizeRows = false;
            this.CohortSelectionView.ColumnHeadersHeight = 29;
            this.CohortSelectionView.ColumnHeadersHeightSizeMode = System.Windows.Forms.DataGridViewColumnHeadersHeightSizeMode.DisableResizing;
            this.CohortSelectionView.ColumnHeadersVisible = false;
            this.CohortSelectionView.Columns.AddRange(new System.Windows.Forms.DataGridViewColumn[] {
            this.CheckCohortColumn,
            this.StudyOptionColumn,
            this.CohortSelectionColumn});
            this.CohortSelectionView.EditMode = System.Windows.Forms.DataGridViewEditMode.EditOnF2;
            this.CohortSelectionView.Location = new System.Drawing.Point(229, 43);
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
            this.CohortSelectionView.CellMouseUp += new System.Windows.Forms.DataGridViewCellMouseEventHandler(this.CohortSelectionView_CellMouseUp);
            // 
            // CheckCohortColumn
            // 
            this.CheckCohortColumn.HeaderText = "";
            this.CheckCohortColumn.MinimumWidth = 6;
            this.CheckCohortColumn.Name = "CheckCohortColumn";
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
            this.ViewCalculationTableButton.Location = new System.Drawing.Point(26, 267);
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
            this.DailyVariableCheckbox.Location = new System.Drawing.Point(26, 207);
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
            this.WeeklyVariablesCheckbox.Location = new System.Drawing.Point(26, 237);
            this.WeeklyVariablesCheckbox.Name = "WeeklyVariablesCheckbox";
            this.WeeklyVariablesCheckbox.Size = new System.Drawing.Size(142, 24);
            this.WeeklyVariablesCheckbox.TabIndex = 8;
            this.WeeklyVariablesCheckbox.Text = "Weekly Variables";
            this.WeeklyVariablesCheckbox.UseVisualStyleBackColor = true;
            // 
            // splitContainer1
            // 
            this.splitContainer1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitContainer1.FixedPanel = System.Windows.Forms.FixedPanel.Panel1;
            this.splitContainer1.Location = new System.Drawing.Point(0, 0);
            this.splitContainer1.Name = "splitContainer1";
            // 
            // splitContainer1.Panel1
            // 
            this.splitContainer1.Panel1.Controls.Add(this.CohortSelectionView);
            this.splitContainer1.Panel1.Controls.Add(this.StudyCheckListBox);
            this.splitContainer1.Panel1.Controls.Add(this.WeeklyVariablesCheckbox);
            this.splitContainer1.Panel1.Controls.Add(this.StudyLabel);
            this.splitContainer1.Panel1.Controls.Add(this.DailyVariableCheckbox);
            this.splitContainer1.Panel1.Controls.Add(this.CohortLabel);
            this.splitContainer1.Panel1.Controls.Add(this.ViewCalculationTableButton);
            // 
            // splitContainer1.Panel2
            // 
            this.splitContainer1.Panel2.Controls.Add(this.CurrentCalculationTableView);
            this.splitContainer1.Size = new System.Drawing.Size(1332, 853);
            this.splitContainer1.SplitterDistance = 557;
            this.splitContainer1.TabIndex = 9;
            // 
            // QueryForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1332, 853);
            this.Controls.Add(this.splitContainer1);
            this.Name = "QueryForm";
            this.Text = "Research Query";
            this.Load += new System.EventHandler(this.QueryForm_Load);
            ((System.ComponentModel.ISupportInitialize)(this.CurrentCalculationTableView)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.CohortSelectionView)).EndInit();
            this.splitContainer1.Panel1.ResumeLayout(false);
            this.splitContainer1.Panel1.PerformLayout();
            this.splitContainer1.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitContainer1)).EndInit();
            this.splitContainer1.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private CheckedListBox StudyCheckListBox;
        private Label StudyLabel;
        private Label CohortLabel;
        private DataGridView CurrentCalculationTableView;
        private DataGridView CohortSelectionView;
        private DataGridViewCheckBoxColumn CheckCohortColumn;
        private DataGridViewTextBoxColumn StudyOptionColumn;
        private DataGridViewTextBoxColumn CohortSelectionColumn;
        private Button ViewCalculationTableButton;
        private CheckBox DailyVariableCheckbox;
        private CheckBox WeeklyVariablesCheckbox;
        private SplitContainer splitContainer1;
    }
}