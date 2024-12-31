import vlc

class VLCPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.video_length = 0  # Total video length in milliseconds

    def load_video(self, file_path, hwnd):
        """Load a video using VLC and play it"""
        media = vlc.Media(file_path)
        self.player.set_media(media)
        self.player.set_hwnd(hwnd)  # Set video output to the Tkinter frame (using hwnd for Windows)
        self.player.play()

    def play_pause(self):
        """Toggle play/pause"""
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    def set_volume(self, volume):
        """Set the volume of the VLC player"""
        self.player.audio_set_volume(int(volume))

    def set_speed(self, speed):
        """Set the playback speed of the VLC player"""
        self.player.set_rate(float(speed))

    def forward_10s(self):
        """Forward the video by 10 seconds"""
        current_time = self.player.get_time()
        self.player.set_time(current_time + 10000)  # Forward by 10 seconds

    def rewind_10s(self):
        """Rewind the video by 10 seconds"""
        current_time = self.player.get_time()
        self.player.set_time(max(0, current_time - 10000))  # Rewind by 10 seconds, ensuring not to go below 0

    def get_time(self):
        """Get the current time of the video"""
        return self.player.get_time()

    def get_length(self):
        """Get the length of the video"""
        return self.player.get_length()
