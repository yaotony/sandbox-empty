using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;

using FubonE01API;
using System.Xml;
using System.IO;

namespace FubonAPIDemoPro
{
    public partial class Form1 : Form
    {
        public Fubon_Mananger_API my_api;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            my_api = new Fubon_Mananger_API();
        }

        // 紀錄各項 Log 
        public void LogMessage(string str)
        {
            lock (textBox_msgxml)
            {
                textBox_msgxml.Text = DateTime.Now.ToString("HH:mm:ss.fff") + ": " + str + "\r\n" + "\r\n" + textBox_msgxml.Text;
            }
        }

        // 登入
        private void button_login_Click(object sender, EventArgs e)
        {
            string UserInfo = "";

             //textBox_status_code.Text = my_api.eLogin(textBox_id.Text, textBox_passwd.Text, ref UserInfo).ToString(); // 不收回報
             textBox_status_code.Text = my_api.eLogin_MsgServ(textBox_id.Text, textBox_passwd.Text, axFbs_MsgServ1, ref UserInfo).ToString();

            LogMessage(string.Format("{0}", UserInfo));

            insert_acno();

            textBox_status_code.Text = my_api.Set_Trans_Position(true).ToString();
        }

        // 登出
        private void button_logout_Click(object sender, EventArgs e)
        {
            textBox_status_code.Text = my_api.eLogout().ToString();
            clear_acno();
            textBox_msgxml.Clear();
        }

        // 清除期貨可用帳號
        private void clear_acno()
        {
            comboBox_acno.Items.Clear();
            comboBox_acno.Text = "";
        }

        // 將接收到的帳號新增進帳號的 ComboBox 中
        private void insert_acno()
        {
            string my_MsgKey = null;

            if (textBox_status_code.Text == "0")
            {
                my_MsgKey = my_api.Find_MsgKey_by_ID(textBox_id.Text.ToUpper(), 1);

                if (my_MsgKey != null)
                    comboBox_acno.Items.Add(my_MsgKey);
            }

            if (comboBox_acno.Items.Count > 0)
                comboBox_acno.SelectedIndex = 0;
        }

        // 執行
        private void button_exec_Click(object sender, EventArgs e)
        {
            string UserInfo = "";


            switch (comboBox_type.Text.Trim())
            {
                // 委託
                case "委託":
                    switch (tabControl1.SelectedIndex)
                    {
                        case 0: // 期權
                            if (comboBox_ptype.Text.Substring(0, 1) == "0")
                            {
                                LogMessage("efOrder(" + string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}", comboBox_acno.Text, ""
                                , comboBox_ptype.Text.Substring(0, 1), comboBox_pid.Text.ToUpper(), "", textBox_ym.Text, "",
                                comboBox_bs.Text.Substring(0, 1), comboBox_limit.Text.Substring(0, 1),
                                textBox_price.Text, textBox_lot.Text, comboBox_offset.Text.Substring(0, 1),
                                comboBox_rif.Text.Substring(0, 1)) + ")");



                                textBox_status_code.Text = my_api.efOrder(comboBox_acno.Text, ""
                                    , comboBox_ptype.Text.Substring(0, 1), comboBox_pid.Text.ToUpper(), "", textBox_ym.Text, "",
                                    comboBox_bs.Text.Substring(0, 1), comboBox_limit.Text.Substring(0, 1),
                                    textBox_price.Text, textBox_lot.Text, comboBox_offset.Text.Substring(0, 1),
                                    comboBox_rif.Text.Substring(0, 1), ref UserInfo).ToString();
                            }
                            else
                            {
                                LogMessage("efOrder(" + string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12}", comboBox_acno.Text,
                                "", comboBox_ptype.Text.Substring(0, 1), comboBox_pid.Text.ToUpper(), textBox_optep.Text, textBox_ym.Text,
                                comboBox_cp.Text.Substring(0, 1), "", comboBox_bs.Text.Substring(0, 1), comboBox_limit.Text.Substring(0, 1),
                                textBox_price.Text, textBox_lot.Text, comboBox_offset.Text.Substring(0, 1), comboBox_rif.Text.Substring(0, 1)) + ")");

                                textBox_status_code.Text = my_api.efOrder(comboBox_acno.Text, ""
                                    , comboBox_ptype.Text.Substring(0, 1), comboBox_pid.Text.ToUpper(), textBox_optep.Text, textBox_ym.Text, comboBox_cp.Text.Substring(0, 1),
                                    comboBox_bs.Text.Substring(0, 1), comboBox_limit.Text.Substring(0, 1),
                                    textBox_price.Text, textBox_lot.Text, comboBox_offset.Text.Substring(0, 1),
                                    comboBox_rif.Text.Substring(0, 1), ref UserInfo).ToString();
                            }

                            break;

                        case 1: // 期貨複式
                            LogMessage("efOrder_2(" + string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17}", comboBox_acno.Text, ""
                                , "3", comboBox_p2pid.Text.ToUpper(), "", textBox_p2ym.Text, "",
                                comboBox_p2bs.Text.Substring(0, 1), comboBox_p2limit.Text.Substring(0, 1),
                                textBox_p2price.Text, textBox_p2lot.Text, comboBox_p2offset.Text.Substring(0, 1),
                                comboBox_p2rif.Text.Substring(0, 1), comboBox_p2pid.Text.ToUpper(), "",
                                textBox_p2ym2.Text, "", comboBox_p2bs2.Text.Substring(0, 1)) + ")");

                            textBox_status_code.Text = my_api.efOrder_2(comboBox_acno.Text, ""
                                , "3", comboBox_p2pid.Text.ToUpper(), "", textBox_p2ym.Text, "",
                                comboBox_p2bs.Text.Substring(0, 1), comboBox_p2limit.Text.Substring(0, 1),
                                textBox_p2price.Text, textBox_p2lot.Text, comboBox_p2offset.Text.Substring(0, 1),
                                comboBox_p2rif.Text.Substring(0, 1), comboBox_p2pid.Text.ToUpper(), "",
                                textBox_p2ym2.Text, "", comboBox_p2bs2.Text.Substring(0, 1), ref UserInfo).ToString();

                            break;

                        case 2: // 選擇權複式
                            LogMessage("efOrder_2(" + string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17}", comboBox_acno.Text, ""
                                , "2", comboBox_p3pid.Text.ToUpper(), textBox_p3optep.Text, textBox_p3ym.Text, comboBox_p3cp.Text.Substring(0, 1),
                                comboBox_p3bs.Text.Substring(0, 1), comboBox_p3limit.Text.Substring(0, 1),
                                textBox_p3price.Text, textBox_p3lot.Text, comboBox_p3offset.Text.Substring(0, 1),
                                comboBox_p3rif.Text.Substring(0, 1), comboBox_p3pid.Text.ToUpper(), textBox_p3optep2.Text,
                                textBox_p3ym2.Text, comboBox_p3cp2.Text.Substring(0, 1), comboBox_p3bs2.Text.Substring(0, 1)) + ")");

                            textBox_status_code.Text = my_api.efOrder_2(comboBox_acno.Text, ""
                                , "2", comboBox_p3pid.Text.ToUpper(), textBox_p3optep.Text, textBox_p3ym.Text, comboBox_p3cp.Text.Substring(0, 1),
                                comboBox_p3bs.Text.Substring(0, 1), comboBox_p3limit.Text.Substring(0, 1),
                                textBox_p3price.Text, textBox_p3lot.Text, comboBox_p3offset.Text.Substring(0, 1),
                                comboBox_p3rif.Text.Substring(0, 1), comboBox_p3pid.Text.ToUpper(), textBox_p3optep2.Text,
                                textBox_p3ym2.Text, comboBox_p3cp2.Text.Substring(0, 1), comboBox_p3bs2.Text.Substring(0, 1), ref UserInfo).ToString();

                            break;

                    }
                    LogMessage(UserInfo);

                    break;

                // 改單
                case "改單":

                    LogMessage("efModifyOrder(" + string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8}", comboBox_acno.Text, "0", textBox_OID.Text,
                        textBox_ordno.Text, textBox_lot.Text, comboBox_ptype.Text.Substring(0, 1), textBox_Qcurrent.Text,
                        textBox_Qmatched.Text, textBox_IsPreOrder.Text) + ")"); 

                    textBox_status_code.Text = my_api.efModifyOrder(comboBox_acno.Text,
                        "0", textBox_OID.Text, textBox_ordno.Text, textBox_lot.Text,
                        comboBox_ptype.Text.Substring(0, 1), textBox_Qcurrent.Text, textBox_Qmatched.Text,
                        textBox_IsPreOrder.Text, ref UserInfo).ToString();

                    LogMessage(UserInfo);

                    break;

                // 刪單
                case "刪單":

                    LogMessage("efModifyOrder(" + string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8}", comboBox_acno.Text,"1", textBox_OID.Text,
                        textBox_ordno.Text, textBox_lot.Text, comboBox_ptype.Text.Substring(0, 1), textBox_Qcurrent.Text,
                        textBox_Qmatched.Text, textBox_IsPreOrder.Text) + ")"); 
                        

                    textBox_status_code.Text = my_api.efModifyOrder(comboBox_acno.Text,
                        "1", textBox_OID.Text, textBox_ordno.Text, textBox_lot.Text,
                        comboBox_ptype.Text.Substring(0, 1), textBox_Qcurrent.Text, textBox_Qmatched.Text,
                        textBox_IsPreOrder.Text, ref UserInfo).ToString();

                    LogMessage(UserInfo);

                    break;

                // 查詢-委託
                case "查詢-委託":

                    LogMessage("efQueryAll(" + string.Format("{0}", comboBox_acno.Text) + ")");

                    textBox_status_code.Text = my_api.efQueryAll(comboBox_acno.Text,
                        ref UserInfo).ToString();

                    LogMessage(UserInfo);

                    break;

                // 查詢-成交
                case "查詢-成交":

                    LogMessage("efMatch(" + string.Format("{0}", comboBox_acno.Text) + ")");

                    textBox_status_code.Text = my_api.efMatch(comboBox_acno.Text,
                        ref UserInfo).ToString();

                    LogMessage(UserInfo);

                    break;

                // 查詢-權益
                case "查詢-權益":

                    LogMessage("efEquity(" + string.Format("{0},{1}", comboBox_acno.Text, comboBox_currency.Text) + ")");
                    
                    textBox_status_code.Text = my_api.efEquity(comboBox_acno.Text,comboBox_currency.Text,
                        ref UserInfo).ToString();

                    LogMessage(UserInfo);

                    break;

                // 查詢-未平倉
                case "查詢-未平倉":

                    LogMessage("efPosition(" + string.Format("{0}", comboBox_acno.Text) + ")");

                    textBox_status_code.Text = my_api.efPosition(comboBox_acno.Text,
                        ref UserInfo).ToString();

                    LogMessage(UserInfo);

                    break;

                // 查詢-帳務
                case "查詢-帳務":

                    LogMessage("efTrans(" + string.Format("{0}", comboBox_acno.Text) + ")");

                    textBox_status_code.Text = my_api.efTrans(comboBox_acno.Text,
                        ref UserInfo).ToString();

                    LogMessage(UserInfo);

                    break;

                // 查詢-版本
                case "查詢-版本":

                    LogMessage("eShowVersion(" + ")");

                    LogMessage(my_api.eShowVersion());

                    break;

                // 查詢-主機
                case "查詢-主機":

                    LogMessage("eShowReg_Server_IP(\"Server_IP\")");

                    LogMessage(my_api.eShowReg_Server_IP("Server_IP"));

                    break;

                // 查詢-交易日
                case "查詢-交易日":

                    string Tdate = "";

                    LogMessage("eTDate(\"F\")");

                    textBox_status_code.Text = my_api.eTDate("F", ref Tdate, ref UserInfo).ToString();

                    LogMessage(Tdate);

                    break;

                default:
                    break;
            }
        }

        // 主動回報
        private void axFubon_Mananger_MsgServer1_OnInstantData(object sender, AxFubonE01API.__Fubon_Mananger_MsgServer_OnInstantDataEvent e)
        {
            LogMessage("OnMsgInstantData(" + e.bsMsgID.ToString() + " : " + e.bsMsgKey.ToString() + " : " + e.bsData.ToString() + ")");
        }

        // 憑證路徑
        private void button_ca_browser_Click(object sender, EventArgs e)
        {
            OpenFileDialog my_ca_file = new OpenFileDialog();
            //FolderBrowserDialog my_ca_file = new FolderBrowserDialog();
            my_ca_file.Filter = "All CA Formats (*.p12;*.pfx)|"+
                "*.p12;*.pfx|EKEY (*.p12)|*.p12|"+
                "EC+ (*.pfx)|*.pfx|All Files (*.*)|*.*";
            my_ca_file.ShowDialog();
            textBox_ca_file.Text = my_ca_file.FileName;
            //textBox_ca_file.Text = my_ca_file.SelectedPath;
        }

        // 憑證設定
        private void button_ca_setting_Click(object sender, EventArgs e)
        {
            if (textBox_ca_file.Text == null || textBox_ca_file.Text == "" || textBox_ca_file.Text.IndexOf(@"\") <= 0)
            {
                LogMessage("請輸入正確路徑");
                return;
            }

            if (my_api.Ekey_AddPreSignData(textBox_ca_id.Text.ToUpper(), textBox_ca_passwd.Text, textBox_ca_file.Text))
            {
                LogMessage("憑證設定成功");
            }
            else
            {
                LogMessage("憑證設定失敗");
            }

        }

        // 期貨 / 選擇權 畫面調整
        private void productchange(object sender, EventArgs e)
        {
            if (comboBox_ptype.Text == "0-期貨")
            {
                label39.Visible = false;
                label40.Visible = false;
                textBox_optep.Visible = false;
                comboBox_cp.Visible = false;
                textBox_price.Text = "7500";
                comboBox_pid.Text = "MXF";
                comboBox_pid.Items.Clear();
                comboBox_pid.Items.Add("MXF");
                comboBox_pid.Items.Add("TXF");
                comboBox_pid.Items.Add("EXF");
                comboBox_pid.Items.Add("FXF");
                comboBox_pid.Items.Add("GDF");
                comboBox_pid.Items.Add("XIF");
            }
            else
            {
                label39.Visible = true;
                label40.Visible = true;
                textBox_optep.Visible = true;
                comboBox_cp.Visible = true;
                textBox_price.Text = "1";
                comboBox_pid.Text = "TXO";
                comboBox_pid.Items.Clear();
                comboBox_pid.Items.Add("TXO");
                comboBox_pid.Items.Add("TEO");
                comboBox_pid.Items.Add("TFO");
                comboBox_pid.Items.Add("TGO");
                comboBox_pid.Items.Add("GTO");
                comboBox_pid.Items.Add("XIO");
            }
        }

        // 委託 / 改單 / 刪單 / 查詢 畫面調整
        private void typechanged(object sender, EventArgs e)
        {
            switch (comboBox_type.Text)
            {
                case "委託":
                    tabControl1.Enabled = true;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                case "改單":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = true;
                    label25.Enabled = true;
                    label26.Enabled = true;
                    label27.Enabled = true;
                    label28.Enabled = true;
                    textBox_ordno.Enabled = true;
                    textBox_OID.Enabled = true;
                    textBox_Qmatched.Enabled = true;
                    textBox_Qcurrent.Enabled = true;
                    textBox_IsPreOrder.Enabled = true;
                    break;
                case "刪單":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = true;
                    label25.Enabled = true;
                    label26.Enabled = true;
                    label27.Enabled = true;
                    label28.Enabled = true;
                    textBox_ordno.Enabled = true;
                    textBox_OID.Enabled = true;
                    textBox_Qmatched.Enabled = true;
                    textBox_Qcurrent.Enabled = true;
                    textBox_IsPreOrder.Enabled = true;
                    break;
                case "查詢-委託":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                case "查詢-成交":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                case "查詢-權益":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = true;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                case "查詢-未平倉":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                case "查詢-帳務":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                case "查詢-版本":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                case "查詢-主機":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                case "查詢-交易日":
                    tabControl1.Enabled = false;
                    comboBox_currency.Enabled = false;
                    label11.Enabled = false;
                    label25.Enabled = false;
                    label26.Enabled = false;
                    label27.Enabled = false;
                    label28.Enabled = false;
                    textBox_ordno.Enabled = false;
                    textBox_OID.Enabled = false;
                    textBox_Qmatched.Enabled = false;
                    textBox_Qcurrent.Enabled = false;
                    textBox_IsPreOrder.Enabled = false;
                    break;
                default:
                    break;

            }
        }

        private void axFbs_MsgServ1_OnInstantData(object sender, AxFubonE01API.__Fbs_MsgServ_OnInstantDataEvent e)
        {
            LogMessage("OnMsgInstantData(" + e.bsMsgID.ToString() + " : " + e.bsMsgKey.ToString() + " : " + e.bsData.ToString() + ")");
        }

        private void axFbs_MsgServ1_OnStatus(object sender, AxFubonE01API.__Fbs_MsgServ_OnStatusEvent e)
        {
            LogMessage("AP OnMsgStatus(" + e.bsMsgID.ToString() + " : " + e.bsMsgKey.ToString() + " : " + e.nStatus.ToString() + ")");
        }

        private void comboBox_acno_TextChanged(object sender, EventArgs e)
        {
            textBox_ca_id.Text = textBox_id.Text;
            textBox_ca_passwd.Text = textBox_passwd.Text;
        }
    }
}