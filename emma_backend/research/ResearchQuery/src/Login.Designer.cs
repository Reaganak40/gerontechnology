namespace ResearchQuery
{
    partial class LoginForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            ServerLabel = new Label();
            ServerInput = new TextBox();
            UserLabel = new Label();
            UserInput = new TextBox();
            PasswordLabel = new Label();
            PasswordInput = new TextBox();
            LoginButton = new Button();
            captionLabel = new Label();
            InvalidLabel = new Label();
            SuspendLayout();
            // 
            // ServerLabel
            // 
            ServerLabel.AutoSize = true;
            ServerLabel.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            ServerLabel.Location = new Point(33, 62);
            ServerLabel.Name = "ServerLabel";
            ServerLabel.Size = new Size(71, 28);
            ServerLabel.TabIndex = 0;
            ServerLabel.Text = "Server:";
            // 
            // ServerInput
            // 
            ServerInput.Location = new Point(134, 66);
            ServerInput.Name = "ServerInput";
            ServerInput.Size = new Size(219, 27);
            ServerInput.TabIndex = 1;
            ServerInput.Text = "localhost";
            // 
            // UserLabel
            // 
            UserLabel.AutoSize = true;
            UserLabel.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            UserLabel.Location = new Point(33, 116);
            UserLabel.Name = "UserLabel";
            UserLabel.Size = new Size(55, 28);
            UserLabel.TabIndex = 2;
            UserLabel.Text = "User:";
            // 
            // UserInput
            // 
            UserInput.Location = new Point(134, 120);
            UserInput.Name = "UserInput";
            UserInput.Size = new Size(219, 27);
            UserInput.TabIndex = 3;
            // 
            // PasswordLabel
            // 
            PasswordLabel.AutoSize = true;
            PasswordLabel.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            PasswordLabel.Location = new Point(31, 166);
            PasswordLabel.Name = "PasswordLabel";
            PasswordLabel.Size = new Size(97, 28);
            PasswordLabel.TabIndex = 4;
            PasswordLabel.Text = "Password:";
            // 
            // PasswordInput
            // 
            PasswordInput.Location = new Point(134, 170);
            PasswordInput.Name = "PasswordInput";
            PasswordInput.PasswordChar = '*';
            PasswordInput.Size = new Size(219, 27);
            PasswordInput.TabIndex = 5;
            PasswordInput.KeyDown += PasswordInput_KeyDown;
            // 
            // LoginButton
            // 
            LoginButton.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point);
            LoginButton.Location = new Point(134, 250);
            LoginButton.Name = "LoginButton";
            LoginButton.Size = new Size(119, 44);
            LoginButton.TabIndex = 6;
            LoginButton.Text = "Login";
            LoginButton.UseVisualStyleBackColor = true;
            LoginButton.Click += LoginButton_Click;
            // 
            // captionLabel
            // 
            captionLabel.AutoSize = true;
            captionLabel.Location = new Point(31, 9);
            captionLabel.MaximumSize = new Size(350, 0);
            captionLabel.Name = "captionLabel";
            captionLabel.Size = new Size(298, 40);
            captionLabel.TabIndex = 7;
            captionLabel.Text = "Please provide credentials to access EMMA Backend Database";
            // 
            // InvalidLabel
            // 
            InvalidLabel.AutoSize = true;
            InvalidLabel.ForeColor = Color.Red;
            InvalidLabel.Location = new Point(33, 213);
            InvalidLabel.Name = "InvalidLabel";
            InvalidLabel.Size = new Size(182, 20);
            InvalidLabel.TabIndex = 8;
            InvalidLabel.Text = "* Invalid Login Credentials";
            InvalidLabel.Visible = false;
            // 
            // LoginForm
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(382, 322);
            Controls.Add(InvalidLabel);
            Controls.Add(captionLabel);
            Controls.Add(LoginButton);
            Controls.Add(PasswordInput);
            Controls.Add(PasswordLabel);
            Controls.Add(UserInput);
            Controls.Add(UserLabel);
            Controls.Add(ServerInput);
            Controls.Add(ServerLabel);
            FormBorderStyle = FormBorderStyle.FixedDialog;
            MaximizeBox = false;
            Name = "LoginForm";
            ShowIcon = false;
            Text = "Login to Database";
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private Label ServerLabel;
        private TextBox ServerInput;
        private Label UserLabel;
        private TextBox UserInput;
        private Label PasswordLabel;
        private TextBox PasswordInput;
        private Button LoginButton;
        private Label captionLabel;
        private Label InvalidLabel;
    }
}