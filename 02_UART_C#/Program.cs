using System;
using System.Windows.Forms;
using UartCommunication;

namespace UCI_GUI
{
    internal static class Program
    {
        /// <summary>
        /// 應用程式的主要進入點。
        /// </summary>
        [STAThread] // Ensure the main thread is single-threaaded apartment (STA)
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new MainForm());
        }
    }
}