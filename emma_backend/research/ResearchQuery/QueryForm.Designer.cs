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
            this.StudyCheckListLabel = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // StudyCheckListBox
            // 
            this.StudyCheckListBox.FormattingEnabled = true;
            this.StudyCheckListBox.Location = new System.Drawing.Point(31, 48);
            this.StudyCheckListBox.Name = "StudyCheckListBox";
            this.StudyCheckListBox.Size = new System.Drawing.Size(177, 158);
            this.StudyCheckListBox.TabIndex = 0;
            // 
            // StudyCheckListLabel
            // 
            this.StudyCheckListLabel.AutoSize = true;
            this.StudyCheckListLabel.Location = new System.Drawing.Point(35, 20);
            this.StudyCheckListLabel.Name = "StudyCheckListLabel";
            this.StudyCheckListLabel.Size = new System.Drawing.Size(46, 20);
            this.StudyCheckListLabel.TabIndex = 1;
            this.StudyCheckListLabel.Text = "Study";
            // 
            // QueryForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(550, 500);
            this.Controls.Add(this.StudyCheckListLabel);
            this.Controls.Add(this.StudyCheckListBox);
            this.Name = "QueryForm";
            this.Text = "Research Query";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private CheckedListBox StudyCheckListBox;
        private Label StudyCheckListLabel;
    }
}