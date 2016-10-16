using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
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
    public sealed partial class Preview : Page
    {
        private bool _updatingMediaTimeline = false;
        public List<Rank> Ranks { get; set; }
        public ObservableCollection<Comment> Comments { get; set; }
        public Preview()
        {
            this.InitializeComponent();
            Load();
            GetRank();
            GetComment();

        }

        private void Slider_OnValueChanged(object sender, RangeBaseValueChangedEventArgs e)
        {
            if (!_updatingMediaTimeline && MediaPlayer.CanSeek)
            {
                TimeSpan duration = MediaPlayer.NaturalDuration.TimeSpan;
                int newPosition = (int)(duration.TotalSeconds * Slider.Value);
                MediaPlayer.Position=new TimeSpan(0,0,newPosition);
            }
        }

        private void Play_OnClick(object sender, RoutedEventArgs e)
        {
            MediaPlayer.Play();
        }

        private void Stop_OnClick(object sender, RoutedEventArgs e)
        {
            MediaPlayer.Stop();
        }

        private void Pause_OnClick(object sender, RoutedEventArgs e)
        {
            MediaPlayer.Pause();
        }

        public class InternalUri
        {
            public Uri Url { get; set; }
        }

        private void Load()
        {
            _updatingMediaTimeline = false;
            var newUri = new InternalUri() { Url = new Uri("http://139.198.3.216/guoamo.mp4") };
            MediaPlayer.Source = newUri.Url;
            MediaPlayer.Position = TimeSpan.FromSeconds(0);
            MediaPlayer.DownloadProgressChanged += (s, ee) =>
            {
                Download.Text = string.Format("下载{0:0.0%} ", MediaPlayer.DownloadProgress);
            };
            MediaPlayer.BufferingProgressChanged += (s, ee) =>
            {
                Buffering.Text = string.Format("缓冲{0:0.0%} ", MediaPlayer.BufferingProgress);
            };
            CompositionTarget.Rendering += (s, ee) =>
            {
                _updatingMediaTimeline = true;
                TimeSpan duration = MediaPlayer.NaturalDuration.TimeSpan;
                if (duration.TotalSeconds != 0)
                {
                    double percentComplete = MediaPlayer.Position.TotalSeconds / duration.TotalSeconds;
                    Slider.Value = percentComplete;
                    TimeSpan mediaTime = MediaPlayer.Position;
                    string text = string.Format("{0:00}:{1:00}", (mediaTime.Hours * 60) + mediaTime.Minutes,
                        mediaTime.Seconds);
                    if (Status.Text != text)
                    {
                        Status.Text = text;
                        _updatingMediaTimeline = false;
                    }
                }
            };
            MediaPlayer.Play();
        }
        public class Rank
        {
            public string Num { get; set; }
            public string Name { get; set; }
            public string Image { get; set; }
            public double Similiarity { get; set; }
        }

        public void GetRank()
        {
            Ranks = new List<Rank>();
            Ranks.Add(new Rank() { Num = "No.1", Name = "Yixiao Zhang", Image = "Assets/male-01.png" });
            Ranks.Add(new Rank() { Num = "No.2", Name = "Xingyu Tian", Image = "Assets/male-02.png" });
            Ranks.Add(new Rank() { Num = "No.3", Name = "Duo Chai", Image = "Assets/male-03.png" });
            Ranks.Add(new Rank() { Num = "No.4", Name = "Fangxing Xiong", Image = "Assets/male-01.png" });
            Ranks.Add(new Rank() { Num = "No.5", Name = "Letian Jiang", Image = "Assets/male-03.png" });
            Ranks.Add(new Rank() { Num = "No.6", Name = "Hillary Clinton", Image = "Assets/female-01.png" });
            Ranks.Add(new Rank() { Num = "No.7", Name = "Marie Curie", Image = "Assets/female-02.png" });
            Ranks.Add(new Rank() { Num = "No.8", Name = "Marie Curie", Image = "Assets/female-03.png" });
            Ranks.Add(new Rank() { Num = "No.9", Name = "Park Geun-hye", Image = "Assets/female-01.png" });
            Ranks.Add(new Rank() { Num = "No.10", Name = "Yoriko Kawaguch", Image = "Assets/female-03.png" });
            Ranks.Add(new Rank() { Num = "No.2889", Name = "You", Image = "Assets/male-01.png" });
            Ranklist.ItemsSource = Ranks;
        }

        public class Comment
        {
            public string Name { get; set; }
            public string _Comment { get; set; }
            public string Performance { get; set; }
        }

        public void GetComment()
        {
            Comments = new ObservableCollection<Comment>();
            Comments.Add(new Comment() { Name = "专家柴先生",Performance="183赞", _Comment = "87年前，我们的祖辈基于自由的构想和致力于实现人人平等的主张，在这个大陆上建立了一个新国家。如今，我们投身于一场伟大的内战，检验我们这个国家，或者其他任何拥有这种构想和主张的国家，是否能够永久存在。" });
            Comments.Add(new Comment() { Name = "开发团队", Performance = "15赞", _Comment = "我们在这个伟大的战场上相逢。我们将这块战场上的一小部分土地奉献给那些为了民族生存而献出他们生命的人们，以作为他们最后的安息之地。" });
            CommentList.ItemsSource = Comments;
        }

        private void CommitButton_OnClick(object sender, RoutedEventArgs e)
        {
            if (CommentTextBox.Text != "")
            {
                Comments.Add(new Comment() { Name = "用户", Performance = "0赞", _Comment = CommentTextBox.Text });
                CommentTextBox.Text = "";
            }
        }

        private void ButtonBase1_OnClick(object sender, RoutedEventArgs e)
        {
            Frame.Navigate(typeof(Camera));
        }

        private void ButtonBase2_OnClick(object sender, RoutedEventArgs e)
        {
            Frame.Navigate(typeof(Home));
        }

        private void VolumeSlider_OnValueChanged(object sender, RangeBaseValueChangedEventArgs e)
        {
            MediaPlayer.Volume = VolumeSlider.Value;
        }

        
    }


}
