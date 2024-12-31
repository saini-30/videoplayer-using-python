
class KeyboardMouseControl:
    def __init__(self, player, volume_slider, speed_slider, progress, root):
        self.player = player
        self.volume_slider = volume_slider
        self.speed_slider = speed_slider
        self.progress = progress
        self.root = root

        self.is_hovering_volume = False
        self.is_hovering_speed = False

        # Bind keyboard events
        self.root.bind_all("<Left>", self.global_left_key_handler)
        self.root.bind_all("<Right>", self.global_right_key_handler)
        self.root.bind("<Home>", self.global_home_key_handler)
        self.root.bind("<End>", self.global_end_key_handler)
        self.root.bind("<space>", self.space_key_handler)

        # Bind "m" key press and release events
        self.root.bind("<KeyPress-m>", self.m_key_pressed)
        self.root.bind("<KeyRelease-m>", self.m_key_released)

        # Bind mouse hover events for sliders
        self.volume_slider.bind("<Enter>", self.on_volume_slider_hover)
        self.volume_slider.bind("<Leave>", self.on_slider_leave)
        self.speed_slider.bind("<Enter>", self.on_speed_slider_hover)
        self.speed_slider.bind("<Leave>", self.on_slider_leave)

        # Bind click event for the progress bar
        self.progress.bind("<Button-1>", self.on_progress_bar_click)

    def global_left_key_handler(self, event):
        """Handle Left arrow key event to adjust volume, speed, or forward/rewind 10 seconds"""
        if self.is_hovering_volume:
            volume = self.volume_slider.get() - 1
            self.volume_slider.set(max(0, volume))  # Prevent going below 0
            self.player.audio_set_volume(self.volume_slider.get())
        elif self.is_hovering_speed:
            speed = self.speed_slider.get() - 0.05
            self.speed_slider.set(max(0.5, speed))  # Prevent going below 0.5x
            self.player.set_rate(self.speed_slider.get())
        else:
            # If the mouse is not over volume or speed, control 10 seconds backward
            self.rewind_10s()

    def global_right_key_handler(self, event):
        """Handle Right arrow key event to adjust volume, speed, or forward/rewind 10 seconds"""
        if self.is_hovering_volume:
            volume = self.volume_slider.get() + 1
            self.volume_slider.set(min(100, volume))  # Prevent going above 100
            self.player.audio_set_volume(self.volume_slider.get())
        elif self.is_hovering_speed:
            speed = self.speed_slider.get() + 0.05
            self.speed_slider.set(min(2.0, speed))  # Prevent going above 2.0x
            self.player.set_rate(self.speed_slider.get())
        else:
            # If the mouse is not over volume or speed, control 10 seconds forward
            self.forward_10s()

    def global_home_key_handler(self, event):
        """Handle Home key event to rewind 10 seconds"""
        self.rewind_10s()

    def global_end_key_handler(self, event):
        """Handle End key event to forward 10 seconds"""
        self.forward_10s()

    def space_key_handler(self, event):
        """Handle spacebar key event to toggle play/pause"""
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()

    def m_key_pressed(self, event):
        """Handle 'm' key press event to set speed to 1.7x"""
        self.player.set_rate(1.5)

    def m_key_released(self, event):
        """Handle 'm' key release event to set speed back to normal"""
        self.player.set_rate(1.0)

    def on_volume_slider_hover(self, event):
        """Set the flag when mouse is hovering over the volume slider"""
        self.is_hovering_volume = True

    def on_speed_slider_hover(self, event):
        """Set the flag when mouse is hovering over the speed slider"""
        self.is_hovering_speed = True

    def on_slider_leave(self, event):
        """Reset flags when mouse leaves the slider area"""
        self.is_hovering_volume = False
        self.is_hovering_speed = False

    def on_progress_bar_click(self, event):
        """Handle click on progress bar to seek to the clicked position"""
        progress_width = self.progress.winfo_width()
        click_x = event.x  # X position of the click on the progress bar
        click_position = click_x / progress_width  # Calculate the position as a ratio (0 to 1)

        # Set the time in the video according to the click position
        video_length = self.player.get_length() / 1000  # Length of the video in seconds
        seek_time = click_position * video_length  # Calculate the time to seek to

        self.player.set_time(int(seek_time * 1000))  # Set the player's time in milliseconds

    def rewind_10s(self):
        """Rewind the video by 10 seconds"""
        current_time = self.player.get_time()
        self.player.set_time(max(0, current_time - 10000))  # Rewind by 10 seconds, ensuring not to go below 0

    def forward_10s(self):
        """Forward the video by 10 seconds"""
        current_time = self.player.get_time()
        self.player.set_time(current_time + 10000)  # Forward by 10 seconds
