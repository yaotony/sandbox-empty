
using System.Windows.Forms;

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace FubonAPIDemoPro
{
     class Program
    {
        /// <summary>
        /// 應用程式的主要進入點。
        /// </summary>

        public static void Main(string[] args)
        {

            if (args.Length == 0)
            {

                Application.EnableVisualStyles();
                Application.SetCompatibleTextRenderingDefault(false);
                Application.Run(new Form1());



            }
            else
            {


                string cate = "";
                string id = "H122192596";
                string pw = "tony0429";
                string path = "C:\\CAFubon\\H122192596\\H122192596.pfx";
                // order  , view
                cate = args[0];
                order o = new order(id, pw);
                switch (cate)
                {
                    case "order":
                        string yymm = args[1];
                        string bs = args[2];
                        string qty = args[3];

                        string price = "0";

                        if (o.setCertificate(id, pw, path))
                        {
                            price = o.fOrder(yymm, bs, qty);
                        }
                        Console.WriteLine(price);
                        break;
                    case "viewQty":
                        o.getPosition();
                        Console.WriteLine(o.PositionQty);
                        break;
                    case "viewBS":
                        o.getPosition();
                        Console.WriteLine(o.PositionBS);
                        break;
                    case "quity":
                        string quity = o.getQuity();
                        Console.WriteLine(quity);

                        break;
                    case "match":
                        string msg = o.getMatch();
                        Console.WriteLine(msg);

                        break;
                }



            }



        }
    }
}