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
            this.CohortCheckListBox = new System.Windows.Forms.CheckedListBox();
            this.CohortLabel = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // StudyCheckListBox
            // 
            this.StudyCheckListBox.CheckOnClick = true;
            this.StudyCheckListBox.FormattingEnabled = true;
            this.StudyCheckListBox.Location = new System.Drawing.Point(31, 48);
            this.StudyCheckListBox.Name = "StudyCheckListBox";
            this.StudyCheckListBox.Size = new System.Drawing.Size(177, 158);
            this.StudyCheckListBox.TabIndex = 0;
            this.StudyCheckListBox.MouseUp += new System.Windows.Forms.MouseEventHandler(this.StudyCheckListBox_MouseUp);
            // 
            // StudyLabel
            // 
            this.StudyLabel.AutoSize = true;
            this.StudyLabel.Location = new System.Drawing.Point(31, 25);
            this.StudyLabel.Name = "StudyLabel";
            this.StudyLabel.Size = new System.Drawing.Size(46, 20);
            this.StudyLabel.TabIndex = 1;
            this.StudyLabel.Text = "Study";
            // 
            // CohortCheckListBox
            // 
            this.CohortCheckListBox.CheckOnClick = true;
            this.CohortCheckListBox.FormattingEnabled = true;
            this.CohortCheckListBox.Location = new System.Drawing.Point(234, 48);
            this.CohortCheckListBox.Name = "CohortCheckListBox";
            this.CohortCheckListBox.Size = new System.Drawing.Size(283, 158);
            this.CohortCheckListBox.TabIndex = 2;
            // 
            // CohortLabel
            // 
            this.CohortLabel.AutoSize = true;
            this.CohortLabel.Location = new System.Drawing.Point(234, 25);
            this.CohortLabel.Name = "CohortLabel";
            this.CohortLabel.Size = new System.Drawing.Size(54, 20);
            this.CohortLabel.TabIndex = 3;
            this.CohortLabel.Text = "Cohort";
            // 
            // QueryForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(550, 500);
            this.Controls.Add(this.CohortLabel);
            this.Controls.Add(this.CohortCheckListBox);
            this.Controls.Add(this.StudyLabel);
            this.Controls.Add(this.StudyCheckListBox);
            this.Name = "QueryForm";
            this.Text = "Research Query";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private CheckedListBox StudyCheckListBox;
        private Label StudyLabel;
        private CheckedListBox CohortCheckListBox;
        private Label CohortLabel;
    }
}