import vlc
import tkinter as tk
from tkinter import filedialog, Button, Frame, Scale, HORIZONTAL

class VLCPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VLC Media Player Control")
        self.root.geometry("800x600")  # Set the size of the window
        
        # VLC MediaPlayer setup
        self.player = vlc.MediaPlayer()

        self.speed_is_2x = False  # Track the current playback speed

        # Create a frame to hold the VLC video
        self.video_frame = Frame(self.root, bg="black", width=800, height=450)
        self.video_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Setup UI components
        self.setup_ui()

        # Bind spacebar key event to play/pause
        self.root.bind("<space>", self.space_key_handler)
        # Bind Home, End, Left, and Right keys globally
        self.root.bind_all("<Home>", self.global_home_key_handler)
        self.root.bind_all("<End>", self.global_end_key_handler)
        self.root.bind_all("<Left>", self.global_left_key_handler)
        self.root.bind_all("<Right>", self.global_right_key_handler)
        # Bind "m" key press and release events
        self.root.bind("<KeyPress-m>", self.m_key_pressed)
        self.root.bind("<KeyRelease-m>", self.m_key_released)

    def setup_ui(self):
        """Set up the UI with buttons to control playback"""
        button_frame = Frame(self.root)
        button_frame.pack(pady=10)

        self.load_button = Button(button_frame, text="Load Video", command=self.load_video)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.back_button = Button(button_frame, text="<< 10s", command=self.rewind_10s)
        self.back_button.pack(side=tk.LEFT, padx=5)
        self.back_button.bind("<Left>", lambda event: self.rewind_10s())
        self.back_button.bind("<Home>", lambda event: self.rewind_10s())

        self.play_pause_button = Button(button_frame, text="Play", command=self.play_pause)
        self.play_pause_button.pack(side=tk.LEFT, padx=5)

        self.forward_button = Button(button_frame, text="10s >>", command=self.forward_10s)
        self.forward_button.pack(side=tk.LEFT, padx=5)
        self.forward_button.bind("<Right>", lambda event: self.forward_10s())
        self.forward_button.bind("<End>", lambda event: self.forward_10s())

        # Volume slider
        self.volume_slider = Scale(button_frame, from_=0, to=100, orient=HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_slider.set(50)  # Set initial volume to 50%
        self.volume_slider.pack(side=tk.LEFT, padx=5)
        self.volume_slider.bind("<Left>", self.decrease_volume)
        self.volume_slider.bind("<Right>", self.increase_volume)
        self.volume_slider.bind("<Home>", self.decrease_volume)
        self.volume_slider.bind("<End>", self.increase_volume)
        self.volume_slider.bind("<Enter>", lambda event: self.volume_slider.focus_set())
        self.volume_slider.bind("<Leave>", lambda event: self.root.focus_set())

        # Speed slider
        self.speed_slider = Scale(button_frame, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Speed", command=self.set_speed)
        self.speed_slider.set(1.0)  # Set initial speed to normal (1.0x)
        self.speed_slider.pack(side=tk.LEFT, padx=5)
        self.speed_slider.bind("<Left>", self.decrease_speed)
        self.speed_slider.bind("<Right>", self.increase_speed)
        self.speed_slider.bind("<Home>", self.decrease_speed)
        self.speed_slider.bind("<End>", self.increase_speed)
        self.speed_slider.bind("<Enter>", lambda event: self.speed_slider.focus_set())
        self.speed_slider.bind("<Leave>", lambda event: self.root.focus_set())

    def load_video(self):
        """Load a video using VLC and play it"""
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.wmv")])

        if file_path:
            media = vlc.Media(file_path)
            self.player.set_media(media)

            # Set the parent window for the VLC player (embed in Tkinter window)
            if self.player.get_fullscreen():
                self.player.set_fullscreen(False)  # Exit fullscreen if it's in fullscreen mode

            # Set video output to the Tkinter frame (using hwnd for Windows)
            self.player.set_hwnd(self.video_frame.winfo_id())  # Use this on Windows to embed in Tkinter

            self.player.play()
            self.play_pause_button.config(text="Pause")  # Set button text to "Pause" when video starts playing

            # Set the VLC player to fullscreen
            self.player.set_fullscreen(True)

    def play_pause(self):
        """Toggle play/pause"""
        if self.player.is_playing():
            self.play_pause_button.config(text="Play")
            self.player.pause()
        else:
            self.play_pause_button.config(text="Pause")
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

    def space_key_handler(self, event):
        """Handle spacebar key event to toggle play/pause"""
        self.play_pause()

    def global_home_key_handler(self, event):
        """Handle global Home key event to rewind 10 seconds"""
        if self.root.focus_get() not in [self.volume_slider, self.speed_slider]:
            self.rewind_10s()

    def global_end_key_handler(self, event):
        """Handle global End key event to forward 10 seconds"""
        if self.root.focus_get() not in [self.volume_slider, self.speed_slider]:
            self.forward_10s()

    def global_left_key_handler(self, event):
        """Handle global Left key event to rewind 10 seconds"""
        if self.root.focus_get() not in [self.volume_slider, self.speed_slider]:
            self.rewind_10s()

    def global_right_key_handler(self, event):
        """Handle global Right key event to forward 10 seconds"""
        if self.root.focus_get() not in [self.volume_slider, self.speed_slider]:
            self.forward_10s()

    def m_key_pressed(self, event):
        """Handle 'm' key press event to set speed to 1.7x"""
        self.player.set_rate(1.7)

    def m_key_released(self, event):
        """Handle 'm' key release event to set speed back to normal"""
        self.player.set_rate(1.0)

    def decrease_volume(self, event):
        """Decrease the volume by 5 units"""
        current_volume = self.volume_slider.get()
        self.volume_slider.set(max(0, current_volume - 5))

    def increase_volume(self, event):
        """Increase the volume by 5 units"""
        current_volume = self.volume_slider.get()
        self.volume_slider.set(min(100, current_volume + 5))

    def decrease_speed(self, event):
        """Decrease the speed by 0.1 units"""
        current_speed = self.speed_slider.get()
        self.speed_slider.set(max(0.5, current_speed - 0.1))

    def increase_speed(self, event):
        """Increase the speed by 0.1 units"""
        current_speed = self.speed_slider.get()
        self.speed_slider.set(min(2.0, current_speed + 0.1))

if __name__ == "__main__":
    root = tk.Tk()
    app = VLCPlayerApp(root)
    root.mainloop()