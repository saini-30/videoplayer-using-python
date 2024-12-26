import vlc
import tkinter as tk
from tkinter import filedialog, Button, Frame, Scale, HORIZONTAL, OptionMenu, StringVar

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

    def setup_ui(self):
        """Set up the UI with buttons to control playback"""
        # Video progress slider
        self.progress_slider = Scale(self.root, from_=0, to=1000, orient=HORIZONTAL, command=self.set_position, resolution=0.1, label="Progress")
        self.progress_slider.pack(fill=tk.X, padx=10, pady=10)

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

        # Crop size options
        self.crop_options = ["16:9", "4:3", "1:1", "21:9"]
        self.selected_crop = StringVar(self.root)
        self.selected_crop.set(self.crop_options[0])  # Set default crop size

        self.crop_menu = OptionMenu(button_frame, self.selected_crop, *self.crop_options, command=self.set_crop)
        self.crop_menu.pack(side=tk.LEFT, padx=5)

        # Update the progress slider periodically
        self.update_progress()

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

    def set_crop(self, crop_size):
        """Set the crop size of the VLC player"""
        self.player.video_set_crop_geometry(crop_size)

    def forward_10s(self):
        """Forward the video by 10 seconds"""
        current_time = self.player.get_time()
        self.player.set_time(current_time + 10000)  # Forward by 10 seconds

    def rewind_10s(self):
        """Rewind the video by 10 seconds"""
        current_time = self.player.get_time()
        self.player.set_time(max(0, current_time - 10000))  # Rewind by 10 seconds, ensuring not to go below 0

    def set_position(self, position):
        """Set the position of the video"""
        length = self.player.get_length()
        self.player.set_time(int(float(position) * length / 1000))

    def update_progress(self):
        """Update the progress slider periodically"""
        if self.player.is_playing():
            length = self.player.get_length()
            current_time = self.player.get_time()
            if length > 0:
                position = current_time * 1000 / length
                self.progress_slider.set(position)
        self.root.after(1000, self.update_progress)

if __name__ == "__main__":
    root = tk.Tk()
    app = VLCPlayerApp(root)
    root.mainloop()