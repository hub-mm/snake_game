# ./game_play/game_mode.py

from game_play import game_standard_easy
from game_play import game_standard_medium
from game_play import game_standard_hard
from constant_variables import constants

from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk


class GameMode:
    def __init__(self):
        # Initialize new window
        self.window = Tk()
        self.window.title('SnaKeGamE')
        self.window.resizable(False, False)

        self.label = Label(
            self.window,
            text="SnaKe",
            font=('consolas', 30),
        )
        self.label.pack()

        # Initialize the style
        style = ttk.Style()

        # Use the 'default' theme as a base
        style.theme_use('default')

        # Configure 'easy.TButton' style
        style.configure(
            'easy.TButton',
            background=constants.BACKGROUND_COLOR,
            foreground=constants.HEAD_COLOR,
            font=('consolas', 16, 'bold'),
            borderwidth=2,
            focusthickness=2,
            focuscolor='none'
        )

        # Map the style for different states
        style.map(
            'easy.TButton',
            background=[('active', constants.BACKGROUND_COLOR)],
            foreground=[('active', constants.SNAKE_COLOR)]
        )

        # Configure 'medium.TButton' style
        style.configure(
            'medium.TButton',
            background=constants.BACKGROUND_COLOR,
            foreground='blue',
            font=('consolas', 16, 'bold'),
            borderwidth=2,
            focusthickness=2,
            focuscolor='none'
        )

        # Map the style for different states
        style.map(
            'medium.TButton',
            background=[('active', constants.BACKGROUND_COLOR)],
            foreground=[('active', constants.SNAKE_COLOR)]
        )

        # Configure 'hard.TButton' style
        style.configure(
            'hard.TButton',
            background=constants.BACKGROUND_COLOR,
            foreground=constants.FOOD_COLOR,
            font=('consolas', 16, 'bold'),
            borderwidth=2,
            focusthickness=2,
            focuscolor='none'
        )

        # Map the style for different states
        style.map(
            'hard.TButton',
            background=[('active', constants.BACKGROUND_COLOR)],
            foreground=[('active', constants.SNAKE_COLOR)]
        )

        # Create label and canvas
        self.canvas = Canvas(
            self.window,
            bg=constants.BACKGROUND_COLOR,
            height=constants.GAME_HEIGHT,
            width=constants.GAME_WIDTH
        )
        self.canvas.pack()

        # Update window to ensure accurate geometry
        self.window.update_idletasks()

        # Get main window dimensions and screen dimensions
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calculate position to center the main window on the screen
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Bring the window to the front and make it active
        self.window.focus_force()

        # Create a new top-level window (dialog)
        self.dialog = tk.Toplevel(self.window)
        self.dialog.title('Choose Your Game Mode')
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=constants.BACKGROUND_COLOR)

        # Update main window again to ensure geometry is up-to-date
        self.window.update_idletasks()

        # Set dialog size
        dialog_width = 500
        dialog_height = 250

        # Calculate position to center the dialog on the main window
        main_x = self.window.winfo_x()
        main_y = self.window.winfo_y()
        main_width = self.window.winfo_width()
        main_height = self.window.winfo_height()

        pos_x = main_x + (main_width // 2) - (dialog_width // 2)
        pos_y = main_y + (main_height // 3) - (dialog_height // 2)
        self.dialog.geometry(f"{dialog_width}x{dialog_height}+{pos_x}+{pos_y}")

        # Make the dialog modal
        self.dialog.transient(self.window)
        self.dialog.grab_set()

        # Add UI elements to the dialog
        message = tk.Label(
            self.dialog,
            text='Choose Your Game Mode',
            fg=constants.HEAD_COLOR,
            bg=constants.BACKGROUND_COLOR,
            font=('consolas', 24, 'bold')
        )
        message.pack(pady=20)

        # Add button frame
        buttons_frame = tk.Frame(self.dialog, bg=constants.BACKGROUND_COLOR)
        buttons_frame.pack(pady=10)

        # Custom 'Easy' button using ttk with 'easy.TButton' style
        easy_button = ttk.Button(
            buttons_frame,
            text='Easy',
            command=self.start_easy_game,
            style='easy.TButton',
            width=10
        )
        easy_button.pack(side='left', padx=5)

        # Custom 'Medium' button using ttk with 'medium.TButton' style
        medium_button = ttk.Button(
            buttons_frame,
            text='Medium',
            command=self.start_medium_game,
            style='medium.TButton',
            width=10
        )
        medium_button.pack(side='left', padx=5)

        # Custom 'Hard' button using ttk with 'hard.TButton' style
        hard_button = ttk.Button(
            buttons_frame,
            text='Hard',
            command=self.start_hard_game,
            style='hard.TButton',
            width=10
        )
        hard_button.pack(side='left', padx=5)

        # Start the main event loop
        self.window.mainloop()

    def start_easy_game(self):
        self.destroy_windows()
        game_standard_easy.Game()

    def start_medium_game(self):
        self.destroy_windows()
        game_standard_medium.Game()

    def start_hard_game(self):
        self.destroy_windows()
        game_standard_hard.Game()

    def destroy_windows(self):
        if self.dialog.winfo_exists():
            self.dialog.destroy()

        if self.window.winfo_exists():
            self.window.destroy()