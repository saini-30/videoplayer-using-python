import tkinter as tk
from tkinter import filedialog, Button, Frame, Scale, HORIZONTAL, ttk

class UIComponents:
    def __init__(self, root, player):
        self.root = root
        self.player = player
        
        # Create a frame to hold the VLC video
        self.video_frame = Frame(self.root, bg="black", width=800, height=450)
        self.video_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Progress bar and time labels just below the video frame
        progress_frame = Frame(self.root)
        progress_frame.pack(pady=5, fill=tk.X)

        self.time_label = tk.Label(progress_frame, text="00:00:00")
        self.time_label.pack(side=tk.LEFT, padx=10)

        self.progress = ttk.Progressbar(progress_frame, orient="horizontal", mode="determinate")
        self.progress.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.total_time_label = tk.Label(progress_frame, text="00:00:00")
        self.total_time_label.pack(side=tk.LEFT, padx=10)

        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI with buttons to control playback"""
        button_frame = Frame(self.root)
        button_frame.pack(pady=10)

        self.load_button = Button(button_frame, text="Load Video", command=self.load_video)
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.back_button = Button(button_frame, text="<< 10s", command=self.rewind_10s)
        self.back_button.pack(side=tk.LEFT, padx=5)

        self.play_pause_button = Button(button_frame, text="Play", command=self.play_pause)
        self.play_pause_button.pack(side=tk.LEFT, padx=5)

        self.forward_button = Button(button_frame, text="10s >>", command=self.forward_10s)
        self.forward_button.pack(side=tk.LEFT, padx=5)

        # Volume slider
        self.volume_slider = Scale(button_frame, from_=0, to=100, orient=HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_slider.set(50)  # Set initial volume to 50%
        self.volume_slider.pack(side=tk.LEFT, padx=5)

        # Speed slider
        self.speed_slider = Scale(button_frame, from_=0.5, to=2.0, resolution=0.1, orient=HORIZONTAL, label="Speed", command=self.set_speed)
        self.speed_slider.set(1.0)  # Set initial speed to normal (1.0x)
        self.speed_slider.pack(side=tk.LEFT, padx=5)

    def load_video(self):
        """Load a video using VLC"""
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.wmv")])
        if file_path:
            self.player.load_video(file_path, self.video_frame.winfo_id())
            self.play_pause_button.config(text="Pause")  # Set button text to "Pause" when video starts playing

    def play_pause(self):
        """Toggle play/pause"""
        self.player.play_pause()
        if self.player.player.is_playing():
            self.play_pause_button.config(text="Pause")
        else:
            self.play_pause_button.config(text="Play")

    def set_volume(self, volume):
        """Set the volume of the VLC player"""
        self.player.set_volume(volume)

    def set_speed(self, speed):
        """Set the playback speed of the VLC player"""
        self.player.set_speed(speed)

    def forward_10s(self):
        """Forward the video by 10 seconds"""
        self.player.forward_10s()

    def rewind_10s(self):
        """Rewind the video by 10 seconds"""
        self.player.rewind_10s()

    def update_progress_bar(self):
        """Update progress bar and time labels"""
        if self.player.player.is_playing():
            length = self.player.get_length() / 1000  # in seconds
            current_time = self.player.get_time() / 1000  # in seconds
            self.progress['maximum'] = length
            self.progress['value'] = current_time

            # Update time labels in hh:mm:ss format
            self.time_label.config(text=self.format_time(current_time))
            self.total_time_label.config(text=self.format_time(length))
        self.root.after(1000, self.update_progress_bar)

    def format_time(self, seconds):
        """Format seconds as hh:mm:ss"""
        hours, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)
        return f"{int(hours):02}:{int(mins):02}:{int(secs):02}"
