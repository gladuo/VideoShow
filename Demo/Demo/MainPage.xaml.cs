using System;
using System.Collections.Generic;
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

// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=402352&clcid=0x409

namespace Demo
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class MainPage : Page
    {
        public MainPage()
        {
            this.InitializeComponent();
        }

        private void Hamburger_OnClick(object sender, RoutedEventArgs e)
        {
            SplitView.IsPaneOpen = !SplitView.IsPaneOpen;
        }

        private void IconsListBox_OnSelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (Duel.IsSelected)
            {
                Frame.Navigate(typeof(Duel));
            }
            if (Home.IsSelected)
            {
                Frame.Navigate(typeof(Home));
            }
            if (Achievement.IsSelected)
            {
                Frame.Navigate(typeof(Achievement));
            }
            if (Person.IsSelected)
            {
                Frame.Navigate(typeof(Person));
            }
        }
    }
}
