using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Text;
using System.Threading.Tasks;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;

// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=234238

namespace Demo
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class Home : Page
    {
        public List<Item> Items { get; set; }
        RootObject data1 = DataContractJsonDeserializer<RootObject>(1);
        RootObject data2 = DataContractJsonDeserializer<RootObject>(2);
        RootObject data3 = DataContractJsonDeserializer<RootObject>(3);
        public Home()
        {
            this.InitializeComponent();
            Items = new List<Item>();

            AddItems();
            GridView.ItemsSource = Items;
            //这里的信息要缓冲下载下来
        }

        void AddItems()
        {
            Items.Add(new Item() { Uid = data1.Uid, Title = data1.Title, Subtitle = data1.Subtitle, Image = data1.Image, Address = data1.Address});
            Items.Add(new Item() { Uid = data2.Uid, Title = data2.Title, Subtitle = data2.Subtitle, Image = data2.Image, Address = data2.Address });
            Items.Add(new Item() { Uid = data3.Uid, Title = data3.Title, Subtitle = data3.Subtitle, Image = data3.Image, Address = data3.Address });
            Items.Add(new Item() { Uid = 4, Title = "测试用例", Subtitle = "For invoke, set IsItemClickEnabled", Image = "Assets/desk_007.jpg" });
            Items.Add(new Item() { Uid = 5, Title = "测试用例", Subtitle = "For invoke, set IsItemClickEnabled", Image = "Assets/desk_007.jpg" });
            Items.Add(new Item() { Uid = 6, Title = "测试用例", Subtitle = "For invoke, set IsItemClickEnabled", Image = "Assets/desk_007.jpg" });
            Items.Add(new Item() { Uid = 7, Title = "测试用例", Subtitle = "For invoke, set IsItemClickEnabled", Image = "Assets/desk_007.jpg" });
            Items.Add(new Item() { Uid = 8, Title = "测试用例", Subtitle = "For invoke, set IsItemClickEnabled", Image = "Assets/desk_007.jpg" });
            Items.Add(new Item() { Uid = 9, Title = "测试用例", Subtitle = "For invoke, set IsItemClickEnabled", Image = "Assets/desk_007.jpg" });
            Items.Add(new Item() { Uid = 10, Title = "测试用例", Subtitle = "For invoke, set IsItemClickEnabled", Image = "Assets/desk_007.jpg" });

        }

        public static RootObject DataContractJsonDeserializer<RootObject>(int uid)
        {
            //var http = new HttpClient();
            //var url = String.Format("json/{0}.json", uid);
            //var response = await http.GetAsync(url);
            var url = String.Format("json/{0}.txt", uid);
            var str = File.ReadAllText(url);
            var serializer = new DataContractJsonSerializer(typeof(RootObject));
            var ms = new MemoryStream(Encoding.UTF8.GetBytes(str));
            var data = (RootObject)serializer.ReadObject(ms);

            return data;
        }

        [DataContract]
        public class RootObject
        {
            [DataMember]
            public int Uid { get; set; }
            [DataMember]
            public string Image { get; set; }
            [DataMember]
            public string Title { get; set; }
            [DataMember]
            public string Subtitle { get; set; }
            [DataMember]
            public string Address { get; set; }
            
        }



        public class Item
        {
            public int Uid { get; set; }
            public string Title { get; set; }
            public string Subtitle { get; set; }
            public string Image { get; set; }
            public string Address { get; set; }
            //这里的图片要调用缩略图API

        }

        private void GridView_OnItemClick(object sender, ItemClickEventArgs e)
        {
            Frame.Navigate(typeof(Preview),(e.ClickedItem as Item)?.Address);
        }
    }
}
