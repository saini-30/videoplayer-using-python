import vlc
import tkinter as tk
from tkinter import filedialog, Button, Frame

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
        self.video_frame.pack(padx=10, pady=10)

        # Setup UI components
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI with buttons to control playback"""
        self.load_button = Button(self.root, text="Load Video", command=self.load_video)
        self.load_button.pack(pady=10)

        self.play_pause_button = Button(self.root, text="Play", command=self.play_pause)
        self.play_pause_button.pack(pady=10)

        self.speed_button = Button(self.root, text="Toggle Speed", command=self.toggle_speed)
        self.speed_button.pack(pady=10)

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

    def play_pause(self):
        """Toggle play/pause"""
        if self.player.is_playing():
            self.player.pause()
            self.play_pause_button.config(text="Play")
        else:
            self.player.play()
            self.play_pause_button.config(text="Pause")

    def toggle_speed(self):
        """Toggle between normal speed (1x) and fast speed (2x)"""
        if self.speed_is_2x:
            # Set to normal speed
            self.player.set_rate(1.0)
            self.speed_button.config(text="Set Speed 2x")
        else:
            # Set to 2x speed
            self.player.set_rate(2.0)
            self.speed_button.config(text="Set Speed 1x")
        
        # Toggle the flag
        self.speed_is_2x = not self.speed_is_2x

if __name__ == "__main__":
    root = tk.Tk()
    app = VLCPlayerApp(root)
    root.mainloop()
