// UartCommunication.cs
using System;
using System.IO.Ports;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.ComponentModel;

namespace UartCommunication
{
    public partial class MainForm : Form
    {
        private SerialPort serialPort;
        private StringBuilder receivedData = new StringBuilder();

        public MainForm()
        {
            InitializeComponent();
            InitializeSerialPortSettings();
        }

        private void InitializeSerialPortSettings()
        {
            // Load available COM ports
            string[] ports = SerialPort.GetPortNames();
            comboBoxPorts.Items.AddRange(ports);
            if (ports.Length > 0)
                comboBoxPorts.SelectedIndex = 0;

            // Add baudrate options
            int[] baudRates = { 1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200 };
            foreach (int rate in baudRates)
                comboBoxBaudRate.Items.Add(rate);
            comboBoxBaudRate.SelectedIndex = 7; // Default to 115200

            // Initialize serialPort
            serialPort = new SerialPort();
            serialPort.DataReceived += SerialPort_DataReceived;
        }

        private void InitializeComponent()
        {
            this.comboBoxPorts = new System.Windows.Forms.ComboBox();
            this.comboBoxBaudRate = new System.Windows.Forms.ComboBox();
            this.buttonConnect = new System.Windows.Forms.Button();
            this.buttonSend = new System.Windows.Forms.Button();
            this.textBoxSend = new System.Windows.Forms.TextBox();
            this.textBoxReceive = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.buttonClear = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // comboBoxPorts
            // 
            this.comboBoxPorts.FormattingEnabled = true;
            this.comboBoxPorts.Location = new System.Drawing.Point(115, 11);
            this.comboBoxPorts.Name = "comboBoxPorts";
            this.comboBoxPorts.Size = new System.Drawing.Size(121, 20);
            this.comboBoxPorts.TabIndex = 0;
            // 
            // comboBoxBaudRate
            // 
            this.comboBoxBaudRate.FormattingEnabled = true;
            this.comboBoxBaudRate.Location = new System.Drawing.Point(115, 36);
            this.comboBoxBaudRate.Name = "comboBoxBaudRate";
            this.comboBoxBaudRate.Size = new System.Drawing.Size(121, 20);
            this.comboBoxBaudRate.TabIndex = 1;
            // 
            // buttonConnect
            // 
            this.buttonConnect.Location = new System.Drawing.Point(251, 14);
            this.buttonConnect.Name = "buttonConnect";
            this.buttonConnect.Size = new System.Drawing.Size(77, 45);
            this.buttonConnect.TabIndex = 2;
            this.buttonConnect.Text = "Connect";
            this.buttonConnect.UseVisualStyleBackColor = true;
            this.buttonConnect.Click += new System.EventHandler(this.buttonConnect_Click);
            // 
            // buttonSend
            // 
            this.buttonSend.Enabled = false;
            this.buttonSend.Location = new System.Drawing.Point(12, 273);
            this.buttonSend.Name = "buttonSend";
            this.buttonSend.Size = new System.Drawing.Size(75, 21);
            this.buttonSend.TabIndex = 3;
            this.buttonSend.Text = "Send Hex";
            this.buttonSend.UseVisualStyleBackColor = true;
            this.buttonSend.Click += new System.EventHandler(this.buttonSend_Click);
            // 
            // textBoxSend
            // 
            this.textBoxSend.Location = new System.Drawing.Point(12, 228);
            this.textBoxSend.Multiline = true;
            this.textBoxSend.Name = "textBoxSend";
            this.textBoxSend.Size = new System.Drawing.Size(394, 40);
            this.textBoxSend.TabIndex = 4;
            this.textBoxSend.Text = "Enter hex values (e.g. 01 02 03 0A FF)";
            // 
            // textBoxReceive
            // 
            this.textBoxReceive.Location = new System.Drawing.Point(12, 90);
            this.textBoxReceive.Multiline = true;
            this.textBoxReceive.Name = "textBoxReceive";
            this.textBoxReceive.ReadOnly = true;
            this.textBoxReceive.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.textBoxReceive.Size = new System.Drawing.Size(394, 117);
            this.textBoxReceive.TabIndex = 5;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 14);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(56, 12);
            this.label1.TabIndex = 6;
            this.label1.Text = "COM Port:";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 39);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(53, 12);
            this.label2.TabIndex = 7;
            this.label2.Text = "Baud rate:";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 76);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(75, 12);
            this.label3.TabIndex = 8;
            this.label3.Text = "Received Data:";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(12, 213);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(55, 12);
            this.label4.TabIndex = 9;
            this.label4.Text = "Send Data:";
            // 
            // buttonClear
            // 
            this.buttonClear.Location = new System.Drawing.Point(331, 273);
            this.buttonClear.Name = "buttonClear";
            this.buttonClear.Size = new System.Drawing.Size(75, 21);
            this.buttonClear.TabIndex = 10;
            this.buttonClear.Text = "Clear";
            this.buttonClear.UseVisualStyleBackColor = true;
            this.buttonClear.Click += new System.EventHandler(this.buttonClear_Click);
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(417, 309);
            this.Controls.Add(this.buttonClear);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.textBoxReceive);
            this.Controls.Add(this.textBoxSend);
            this.Controls.Add(this.buttonSend);
            this.Controls.Add(this.buttonConnect);
            this.Controls.Add(this.comboBoxBaudRate);
            this.Controls.Add(this.comboBoxPorts);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "UART Communication";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        private System.Windows.Forms.ComboBox comboBoxPorts;
        private System.Windows.Forms.ComboBox comboBoxBaudRate;
        private System.Windows.Forms.Button buttonConnect;
        private System.Windows.Forms.Button buttonSend;
        private System.Windows.Forms.TextBox textBoxSend;
        private System.Windows.Forms.TextBox textBoxReceive;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Button buttonClear;

        private void buttonConnect_Click(object sender, EventArgs e)
        {
            try
            {
                if (serialPort.IsOpen)
                {
                    // Disconnect if already connected
                    serialPort.Close();
                    buttonConnect.Text = "Connect";
                    buttonSend.Enabled = false;
                    comboBoxPorts.Enabled = true;
                    comboBoxBaudRate.Enabled = true;
                    UpdateStatus("Disconnected");
                }
                else
                {
                    // Connect to the selected port
                    if (comboBoxPorts.SelectedItem == null)
                    {
                        MessageBox.Show("Please select a COM port.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return;
                    }

                    serialPort.PortName = comboBoxPorts.SelectedItem.ToString();
                    serialPort.BaudRate = Convert.ToInt32(comboBoxBaudRate.SelectedItem);
                    serialPort.DataBits = 8;
                    serialPort.Parity = Parity.None;
                    serialPort.StopBits = StopBits.One;
                    serialPort.Handshake = Handshake.None;

                    serialPort.Open();
                    buttonConnect.Text = "Disconnect";
                    buttonSend.Enabled = true;
                    comboBoxPorts.Enabled = false;
                    comboBoxBaudRate.Enabled = false;
                    UpdateStatus("Connected to " + serialPort.PortName + " at " + serialPort.BaudRate + " baud");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error: " + ex.Message, "Connection Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void SerialPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            try
            {
                // Read data from the serial port
                int bytesToRead = serialPort.BytesToRead;
                byte[] buffer = new byte[bytesToRead];
                serialPort.Read(buffer, 0, bytesToRead);

                // Convert bytes to hex string
                string hexData = BitConverter.ToString(buffer).Replace("-", " ");

                // Update UI on the main thread
                BeginInvoke(new Action(() => {
                    AppendReceivedData(hexData);
                }));
            }
            catch (Exception ex)
            {
                BeginInvoke(new Action(() => {
                    UpdateStatus("Error receiving data: " + ex.Message);
                }));
            }
        }

        private void buttonSend_Click(object sender, EventArgs e)
        {
            if (!serialPort.IsOpen)
            {
                MessageBox.Show("Please connect to a port first.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            try
            {
                string hexText = textBoxSend.Text.Trim();

                // Convert hex string to bytes
                byte[] bytesToSend = HexStringToByteArray(hexText);

                if (bytesToSend.Length > 0)
                {
                    // Send bytes
                    serialPort.Write(bytesToSend, 0, bytesToSend.Length);
                    UpdateStatus("Sent: " + BitConverter.ToString(bytesToSend).Replace("-", " "));
                }
                else
                {
                    MessageBox.Show("Please enter valid hexadecimal values.", "Invalid Data", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error sending data: " + ex.Message, "Send Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private byte[] HexStringToByteArray(string hex)
        {
            // Remove any non-hex characters (spaces, etc.)
            hex = new string(hex.Where(c => char.IsDigit(c) || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')).ToArray());

            // If odd number of characters, pad with a leading zero
            if (hex.Length % 2 != 0)
                hex = "0" + hex;

            byte[] bytes = new byte[hex.Length / 2];

            for (int i = 0; i < hex.Length; i += 2)
            {
                string byteString = hex.Substring(i, 2);
                bytes[i / 2] = Convert.ToByte(byteString, 16);
            }

            return bytes;
        }

        private void AppendReceivedData(string data)
        {
            // Add timestamp
            string timestamp = DateTime.Now.ToString("HH:mm:ss.fff");
            textBoxReceive.AppendText("[" + timestamp + "] RX: " + data + Environment.NewLine);

            // Auto-scroll to the end
            textBoxReceive.SelectionStart = textBoxReceive.Text.Length;
            textBoxReceive.ScrollToCaret();
        }

        private void UpdateStatus(string message)
        {
            string timestamp = DateTime.Now.ToString("HH:mm:ss.fff");
            textBoxReceive.AppendText("[" + timestamp + "] " + message + Environment.NewLine);

            // Auto-scroll to the end
            textBoxReceive.SelectionStart = textBoxReceive.Text.Length;
            textBoxReceive.ScrollToCaret();
        }

        private void buttonClear_Click(object sender, EventArgs e)
        {
            textBoxReceive.Clear();
        }

        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            // Close the serial port if it's open
            if (serialPort != null && serialPort.IsOpen)
            {
                try
                {
                    serialPort.Close();
                }
                catch
                {
                    // Ignore any exceptions during closing
                }
            }
        }

        private void MainForm_Load(object sender, EventArgs e)
        {

        }
    }
}