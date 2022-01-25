using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Xml;
using FubonE01API;

namespace FubonAPIDemoPro
{
    class order
    {

        void log(string msg)
        {
            StreamWriter str = new StreamWriter(@"C:\temp\" + DateTime.Now.ToString("yyyyMMdd") + ".TXT",true);
            
            str.WriteLine(msg);
            str.Close();
        }

        private FubonE01API.Fubon_Mananger_API_2 my_api;
        private string MsgKey = "";

        string readMSGXmlAttributesValue(string xml, string nodeName,string key ) {
            string result = "";
            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.LoadXml(xml);
           

            //擷取節點
            XmlNodeList xmlNodeList = xmlDoc.SelectNodes("/Result/Data");
            //擷取將該節點下的 子節點的值
            foreach (XmlNode node in xmlNodeList)
            {
                for (int i = 0; i < node.ChildNodes.Count; i++)
                {
                    if (node.ChildNodes[i].Name == nodeName)
                    {
                        //找到節點
                        result = node.ChildNodes[i].Attributes[key].Value;
                    }
                }
            }

                return result;
        }
        string readMSGXmlAttributesValue(string xml, string nodeName, string key, string filterKey, string filterValue)
        {
            string result = "";
            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.LoadXml(xml);


            //擷取節點
            XmlNodeList xmlNodeList = xmlDoc.SelectNodes("/Result/Data");
            //擷取將該節點下的 子節點的值
            foreach (XmlNode node in xmlNodeList)
            {
                for (int i = 0; i < node.ChildNodes.Count; i++)
                {
                    if (node.ChildNodes[i].Name == nodeName)
                    {
                        //找到節點
                        if (node.ChildNodes[i].Attributes[filterKey].Value == filterValue)
                            result = node.ChildNodes[i].Attributes[key].Value;
                    }
                }
            }

            return result;
        }


        int readMSGXmlNodeCount(string xml, string nodeName)
        {
            int result = 0;
            XmlDocument xmlDoc = new XmlDocument();
            xmlDoc.LoadXml(xml);

            //擷取節點
            XmlNodeList xmlNodeList = xmlDoc.SelectNodes("/Result/Data");
            //擷取將該節點下的 子節點的值
             foreach (XmlNode node in xmlNodeList)
            {
                for (int i = 0; i < node.ChildNodes.Count; i++)
                {
                    if (node.ChildNodes[i].Name == nodeName)
                    {
                        result = node.ChildNodes[i].ChildNodes.Count;
                    }
                }
            }

            return result;
        }
        public order(string id ,string passwd)
        {
            string userInfo = "";
            int status_code = 0;
            my_api = new FubonE01API.Fubon_Mananger_API_2();
            status_code =my_api.eLogin(id.ToUpper(), passwd, ref userInfo);
            if (status_code == 0)
            {
                MsgKey = my_api.Find_MsgKey_by_ID(id.ToUpper(), 1);
            }
           

        }

         public bool setCertificate(string ca_id,string ca_passwd,string ca_path) {
            bool isok = false;
            string userInfo = "";

            if (my_api.Ekey_AddPreSignData(ca_id.ToUpper(), ca_passwd, ca_path, ref userInfo))
            {
                isok = true;
            }
            else
            {
                isok = false;
            }
            log(" Ekey_AddPreSignData()：" + userInfo);
            return isok;
        }

        public string fOrder(string commID_YM,string bs, string qty)
        {
            //MsgKey 分公司帳號(F026000995XXXX)，可由登入後 MSGXML 讀取的到
            //string MsgKey = "";
            //TDate 交易日
            string TDate = "";
            //ProductType 商品別｛0 期貨／ 1 選擇權｝
            string ProductType = "0";
            //CommID 商品代碼
            string CommID = "MXF";
            //CommID_EP 參考價期貨為空白
            string CommID_EP = "";
            //CommID_YM 年月(EX：200901)
            string CommID_YM = commID_YM;
            //CommID_CP C：Call／P：Put(期貨為空白期貨為空白)
            string CommID_CP = "";
            //BS 買賣別｛B：：買進／S：：賣出
            string BS = bs;
            //PriceType 價位別｛0：限價 4：市價 ／24：範圍市價｝
            string PriceType = "24";
            //Price 委託價格 市價為空白
            string Price = "";
            //Qty 口數
            string Qty = qty;
            //Offset 倉別｛｛0：新倉／1：平倉／2：自動倉／4：當沖｝
            string Offset = "2";
            //Cond 委託別｛R：ROD／F：FOK／I：IOC｝｝
            string Cond = "I";


            // 回傳值1：交易日
            string TradeDay = "";

            // 回傳值2：MSGXML
            string UserInfo = "";

            // 宣告一個變數叫ret 會存放等等呼叫method回傳回來的數字
            int ret = 0;
            string PriceMatch = "0";
            string OrderNo = "";

            // 回傳值負值為失敗，其餘成功，失敗請參考錯誤代碼表
            if (my_api != null)
            {
                ret = my_api.eTDate("F", ref TradeDay, ref UserInfo);
                log("eTDate()：" + UserInfo);
                if (ret >= 0)
                {
                    TDate = TradeDay;

                    my_api.efOrder(MsgKey, TDate, ProductType, CommID, CommID_EP,
                            CommID_YM, CommID_CP, BS, PriceType, Price, Qty, Offset, Cond, ref UserInfo);
                    log("efOrder()：" + UserInfo);
                    OrderNo = readMSGXmlAttributesValue(UserInfo, "Row", "OrderNo");
                    UserInfo = "";
                    System.Threading.Thread.Sleep(2000);
                    int code = my_api.efMatch(MsgKey, ref UserInfo);
                   
                    PriceMatch = readMSGXmlAttributesValue(UserInfo, "Row", "PriceMatch", "OrderNo", OrderNo);
                    log(code.ToString() + "  efMatch()："  + PriceMatch +" " + OrderNo);

                }

                


            }

            return PriceMatch;
        }

        public string getMatch()
        {

            string UserInfo = "";
          
            int code = my_api.efMatch(MsgKey,ref UserInfo);
            log(code.ToString() + " efMatch()：" + UserInfo);
        
            return UserInfo;

        }


        private int _PositionQty = 0 ;
        private string _PositionBS = "";

        public int PositionQty {
            get { return _PositionQty; }
        }
        public string PositionBS {
            get { return _PositionBS; }
        }

        



        public void getPosition()
        {
            // 回傳值2：MSGXML
            string UserInfo = "";
            string result = "";
            _PositionQty = 0;
            _PositionBS = "";

            my_api.efPosition(MsgKey, ref UserInfo);
            log("getPosition()：" + UserInfo);
            result = readMSGXmlAttributesValue(UserInfo, "Row", "Qty");
            int qty = 0;

            if (result.Trim().Length > 0)
            {
                try
                {
                    qty = int.Parse(result);
                }
                catch {
                    qty = 0;
                }
            }
            _PositionQty = qty;

            result = readMSGXmlAttributesValue(UserInfo, "Row", "BS");
            _PositionBS = result;

        }


        
        // 查詢-權益
        public string getQuity()
        {
            // 回傳值2：MSGXML
            string UserInfo = "";
            string result = "";
            int status_code  = 0;

            status_code = my_api.efEquity(MsgKey, "TWD",ref UserInfo);
            if(UserInfo.Length>0)
                 result = readMSGXmlAttributesValue(UserInfo, "Row", "F1");
            log("getQuity()："+UserInfo);
            return result;
        }

    }
}
