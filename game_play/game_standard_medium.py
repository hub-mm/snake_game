# ./game_play/game_standard_medium.py

from game_play import game_mode
from constant_variables import constants
from elements import snake
from elements import food

from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk


class Game:
    def __init__(self):
        # Initialize game variables
        self.direction = 'right'
        self.score = 0
        self.speed = constants.SPEED

        # Initialize the main window
        self.window = Tk()
        self.window.title('SnaKeGamE')
        self.window.resizable(False, False)

        # Initialize the style
        style = ttk.Style()

        # Use the 'default' theme as a base
        style.theme_use('default')

        # Configure a new style 'Yes.TButton'
        style.configure(
            'Yes.TButton',
            background=constants.BACKGROUND_COLOR,
            foreground=constants.HEAD_COLOR,
            font=('consolas', 16, 'bold'),
            borderwidth=2,
            focusthickness=2,
            focuscolor='none'
        )

        # Map the style for different states
        style.map(
            'Yes.TButton',
            background=[('active', constants.BACKGROUND_COLOR)],
            foreground=[('active', constants.SNAKE_COLOR)]
        )

        # Configure a new style 'No.TButton'
        style.configure(
            'No.TButton',
            background=constants.BACKGROUND_COLOR,
            foreground=constants.FOOD_COLOR,
            font=('consolas', 16, 'bold'),
            borderwidth=2,
            focusthickness=2,
            focuscolor='none'
        )

        # Map the style for different states
        style.map(
            'No.TButton',
            background=[('active', constants.BACKGROUND_COLOR)],
            foreground=[('active', constants.SNAKE_COLOR)]
        )

        # Configure a new style 'Menu.TButton'
        style.configure(
            'menu.TButton',
            background=constants.BACKGROUND_COLOR,
            foreground='blue',
            font=('consolas', 16, 'bold'),
            borderwidth=2,
            focusthickness=2,
            focuscolor='none'
        )

        # Map the style for different states
        style.map(
            'menu.TButton',
            background=[('active', constants.BACKGROUND_COLOR)],
            foreground=[('active', constants.SNAKE_COLOR)]
        )

        # Create label and canvas
        self.label = Label(
            self.window,
            text=f"Score: {self.score}\tHighscore: {Game.read_highscore()}",
            font=('consolas', 30)
        )
        self.label.pack()

        self.canvas = Canvas(
            self.window,
            bg=constants.BACKGROUND_COLOR,
            height=constants.GAME_HEIGHT,
            width=constants.GAME_WIDTH
        )
        self.canvas.pack()

        # Update window and center it on the screen
        self.window.update()

        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Bring the window to the front and make active window
        self.window.focus_force()

        # Create snake and food objects
        self.snake = snake.Snake(self.canvas)
        self.food = food.Food(self.canvas, self.snake)

        # Initialise attribute for wave effect
        self.segment_color_index = None

        # Bind keys to change direction
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<a>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<d>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<w>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))
        self.window.bind('<s>', lambda event: self.change_direction('down'))

        # Start the game loop
        self.next_turn()

        self.window.mainloop()

    def next_turn(self, *args):
        x_coord, y_coord = self.snake.coordinates[0]

        # Determine the new position of the head based on the direction
        if self.direction == 'up':
            y_coord -= constants.SPACE_SIZE
        elif self.direction == 'down':
            y_coord += constants.SPACE_SIZE
        elif self.direction == 'left':
            x_coord -= constants.SPACE_SIZE
        elif self.direction == 'right':
            x_coord += constants.SPACE_SIZE

        # Insert new head position at the beginning of the coordinates list
        self.snake.coordinates.insert(0, [x_coord, y_coord])

        # Create new square for the head with HEAD_COLOR
        square = self.canvas.create_rectangle(
            x_coord,
            y_coord,
            x_coord + constants.SPACE_SIZE,
            y_coord + constants.SPACE_SIZE,
            fill=constants.HEAD_COLOR,
            outline=constants.BACKGROUND_COLOR
        )
        self.snake.squares.insert(0, square)

        # Change the color of the previous head to body color
        if len(self.snake.squares) > 1:
            self.canvas.itemconfig(self.snake.squares[1], fill=constants.SNAKE_COLOR)

        if self.segment_color_index is not None:
            if self.segment_color_index < len(self.snake.squares):
                part = self.snake.squares[self.segment_color_index]
                self.canvas.itemconfig(part, fill=constants.FOOD_COLOR)
                self.segment_color_index += 1
            else:
                self.segment_color_index = None

        # Check if snake has eaten the food
        if x_coord == self.food.coordinates[0] and y_coord == self.food.coordinates[1]:
            self.score += 1
            self.speed = max(self.speed - 2, 20)

            self.label.config(text=f"Score: {self.score}\tHighscore: {Game.read_highscore()}")

            # Start wave effect from head
            self.segment_color_index = 0

            # Delete the old food and create a new one
            self.canvas.delete('food')
            self.food = food.Food(self.canvas, self.snake)
        else:
            # Remove the last part of the snake's tail
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        # Check for collisions
        if self.check_collision():
            self.game_over()
        else:
            # Continue the game
            self.window.after(self.speed, self.next_turn, *args)

    def change_direction(self, new_direction):
        if new_direction == 'left' and self.direction != 'right':
            self.direction = new_direction
        elif new_direction == 'right' and self.direction != 'left':
            self.direction = new_direction
        elif new_direction == 'up' and self.direction != 'down':
            self.direction = new_direction
        elif new_direction == 'down' and self.direction != 'up':
            self.direction = new_direction

    def check_collision(self):
        x_coord, y_coord = self.snake.coordinates[0]

        # Check collision with walls
        if x_coord < 0 or x_coord + constants.SPACE_SIZE > constants.GAME_WIDTH:
            return True
        elif y_coord < 0 or y_coord + constants.SPACE_SIZE > constants.GAME_HEIGHT:
            return True

        # Check collision with self
        for body_part in self.snake.coordinates[1:]:
            if x_coord == body_part[0] and y_coord == body_part[1]:
                return True

        return False

    def game_over(self):
        highscore = Game.read_highscore()

        if highscore < self.score:
            self.write_highscore()
            highscore = self.score

        # Display Game Over message
        self.canvas.delete(ALL)
        self.canvas.create_text(
            self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2 - 50,
            font=('consolas', 70),
            text='GAME OVER',
            fill='RED',
            tags='game_over'
        )
        self.canvas.create_text(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2 + 50,
            font=('consolas', 30),
            text=f"High Score: {highscore}",
            fill='WHITE',
            tags='highscore'
        )

        # Prompt play again
        self.window.after(200, self.ask_play_again)

    def ask_play_again(self):
        # Create a new top-level window
        dialog = tk.Toplevel(self.window)
        dialog.title('Play Again?')
        dialog.resizable(False, False)
        dialog.configure(bg=constants.BACKGROUND_COLOR)

        # Set dialog size and position it in the center of the main window
        dialog_width = 500
        dialog_height = 250
        main_x = self.window.winfo_x()
        main_y = self.window.winfo_y()
        main_width = self.window.winfo_width()
        main_height = self.window.winfo_height()
        pos_x = main_x + (main_width // 2) - (dialog_width // 2)
        pos_y = main_y + (main_height // 3) - (dialog_height // 2)
        dialog.geometry(f"{dialog_width}x{dialog_height}+{pos_x}+{pos_y}")

        # Make the dialog modal
        dialog.transient(self.window)
        dialog.grab_set()

        message = tk.Label(
            dialog,
            text='Do you want to play again?',
            fg=constants.HEAD_COLOR,
            bg=constants.BACKGROUND_COLOR,
            font=('consolas', 24, 'bold')
        )
        message.pack(pady=20)

        # Add button frame
        buttons_frame = tk.Frame(dialog, bg=constants.BACKGROUND_COLOR)
        buttons_frame.pack(pady=10)

        # Custom 'Yes' button using ttk with 'Black.TButton' style
        yes_button = ttk.Button(
            buttons_frame,
            text='Yes',
            command=lambda: self.restart_game_custom(dialog),
            style='Yes.TButton',
            width=10
        )
        yes_button.pack(side='right', padx=5)

        # Custom 'No' button using ttk with 'Black.TButton' style
        no_button = ttk.Button(
            buttons_frame,
            text='No',
            command=lambda: self.close_game(dialog),
            style='No.TButton',
            width=10
        )
        no_button.pack(side='left', padx=5)

        # Add button frame row below
        buttons_frame_below = tk.Frame(dialog, bg=constants.BACKGROUND_COLOR)
        buttons_frame_below.pack(pady=10)

        # Custom 'Menu' button using ttk with 'Black.TButton' style
        menu_button = ttk.Button(
            buttons_frame_below,
            text='Menu',
            command=lambda: self.open_menu(dialog),
            style='menu.TButton',
            width=20
        )
        menu_button.pack(padx=5)

        # Set focus to the 'Yes' button
        yes_button.focus_set()

        # Bind the Enter key to the 'Yes' button
        dialog.bind('<Return>', lambda event: self.restart_game_custom(dialog))

        # Optionally, bind the Escape key to the 'No' button
        dialog.bind('<Escape>', lambda event: self.close_game(dialog))

    def restart_game_custom(self, dialog):
        dialog.destroy()
        self.restart_game()

    def close_game(self, dialog):
        dialog.destroy()
        self.window.destroy()

    def open_menu(self, dialog):
        dialog.destroy()
        self.window.destroy()
        game_mode.GameMode()

    def restart_game(self):
        # Reset variables
        self.direction = 'right'
        self.score = 0
        self.speed = constants.SPEED
        self.segment_color_index = None
        self.label.config(text=f"Score: {self.score}\tHighscore: {Game.read_highscore()}")

        # Clear canvas
        self.canvas.delete(ALL)

        # Bring the window to the front and make active window
        self.window.focus_force()

        # Recreate snake and food object
        self.snake = snake.Snake(self.canvas)
        self.food = food.Food(self.canvas, self.snake)

        # Restart game loop
        self.next_turn()

    def write_highscore(self):
        # Write highscore to txt file
        with open('./score/highscore_standard_medium.txt', 'w') as txt_score:
            txt_score.write(f"{self.score}")

    @staticmethod
    def read_highscore():
        # Read highscore from txt file
        try:
            with open('./score/highscore_standard_medium.txt', 'r') as txt_score:
                highscore = int(txt_score.read())
                return highscore
        except (FileNotFoundError, ValueError):
            # If file doesn't exist or contains invalid data
            return 0