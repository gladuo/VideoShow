using System;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Navigation;
using Windows.Media.Capture;
using Windows.ApplicationModel;
using System.Threading.Tasks;
using Windows.System.Display;
using Windows.Graphics.Display;
using Windows.Media.MediaProperties;
using Windows.UI.Core;
using Windows.Storage;

// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=234238

namespace Demo
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class Camera
    {
        private MediaCapture _mediaCapture;
        private bool _isPreviewing;
        private DisplayRequest _displayRequest;
        LowLagMediaRecording _mediaRecording;
        public Camera()
        {
            this.InitializeComponent();
            StartPreviewAsync();
            Application.Current.Suspending += Application_Suspending;

            double MaxTime = MediaPlayer.NaturalDuration.TimeSpan.TotalMilliseconds;
            if (MediaPlayer.Position.TotalMilliseconds == MaxTime && MediaPlayer.Position.TotalMilliseconds >10)
            {
                Finish();

            }
            
        }

        private async void Finish()
        {
            await _mediaRecording.StopAsync();
            await _mediaRecording.FinishAsync();
        }

        private async void Application_Suspending(object sender, SuspendingEventArgs e)
        {
            // Handle global application events only if this page is active
            if (Frame.CurrentSourcePageType == typeof(Camera))
            {
                var deferral = e.SuspendingOperation.GetDeferral();
                await CleanupCameraAsync();
                deferral.Complete();
            }
        }

        private async void StartPreviewAsync()
        {
            try
            {

                _mediaCapture = new MediaCapture();
                await _mediaCapture.InitializeAsync();

                PreviewControl.Source = _mediaCapture;
                await _mediaCapture.StartPreviewAsync();
                _isPreviewing = true;

                _displayRequest.RequestActive();
                DisplayInformation.AutoRotationPreferences = DisplayOrientations.Landscape;
            }
            catch (UnauthorizedAccessException)
            {
                // This will be thrown if the user denied access to the camera in privacy settings
                System.Diagnostics.Debug.WriteLine("The app was denied access to the camera");
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine("MediaCapture initialization failed. {0}", ex.Message);
            }
        }
        private async Task CleanupCameraAsync()
        {
            if (_mediaCapture != null)
            {
                if (_isPreviewing)
                {
                    await _mediaCapture.StopPreviewAsync();
                }

                await Dispatcher.RunAsync(CoreDispatcherPriority.Normal, () =>
                {
                    PreviewControl.Source = null;
                    if (_displayRequest != null)
                    {
                        _displayRequest.RequestRelease();
                    }
                });

                _mediaCapture.Dispose();
                _mediaCapture = null;
            }

        }
        protected override async void OnNavigatedFrom(NavigationEventArgs e)
        {
            await CleanupCameraAsync();
        }

        private void Load()
        {
            var newUri = new Preview.InternalUri() { Url = new Uri("http://139.198.3.216/guoamo.mp4") };
            MediaPlayer.Source = newUri.Url;
            MediaPlayer.Position = TimeSpan.FromSeconds(0);
            MediaPlayer.Volume = 0;
            MediaPlayer.AutoPlay = true;
            MediaPlayer.Play();
        }

        private void StartButton_OnClick(object sender, RoutedEventArgs e)
        {
            BothPlay();
        }

        private async void BothPlay()
        {
            var myVideos = await StorageLibrary.GetLibraryAsync(Windows.Storage.KnownLibraryId.Videos);
            StorageFile file = await myVideos.SaveFolder.CreateFileAsync("video.mp4", CreationCollisionOption.GenerateUniqueName);
            _mediaRecording = await _mediaCapture.PrepareLowLagRecordToStorageFileAsync(
                    MediaEncodingProfile.CreateMp4(VideoEncodingQuality.Auto), file);
            await _mediaRecording.StartAsync();
            Load();
        }

        private void StopButton_OnClick(object sender, RoutedEventArgs e)
        {
            BothStop();
        }

        private async void BothStop()
        {
            await _mediaRecording.StopAsync();
            MediaPlayer.Stop();
        }

        private void MediaPlayer_MediaOpened(object sender, RoutedEventArgs e)
        {

        }
    }
}
