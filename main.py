from operator import iconcat
from tkinter import *
from tkinter import messagebox
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = '#06402B'
HEAD_COLOR = '#00FF00'
FOOD_COLOR = '#FF0000'
BACKGROUND_COLOR = '#000000'


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        start_x = int((GAME_WIDTH / 2) / SPACE_SIZE) * SPACE_SIZE
        start_y = int((GAME_HEIGHT / 2) / SPACE_SIZE) * SPACE_SIZE

        for i in range(self.body_size):
            self.coordinates.append([start_x - i * SPACE_SIZE, start_y])

        for index, (x_coord, y_coord) in enumerate(self.coordinates):
            color = HEAD_COLOR if index == 0 else SNAKE_COLOR

            square = self.canvas.create_rectangle(
                x_coord, y_coord, x_coord + SPACE_SIZE, y_coord + SPACE_SIZE,
                fill=color, outline=color, tags='snake'
            )
            self.squares.append(square)


class Food:
    def __init__(self, canvas, snake):
        self.canvas = canvas
        self.snake = snake
        while True:
            x_coord = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
            y_coord = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE
            self.coordinates = [x_coord, y_coord]

            if self.coordinates not in self.snake.coordinates:
                break

        self.canvas.create_oval(
            x_coord, y_coord, x_coord + SPACE_SIZE, y_coord + SPACE_SIZE,
            fill=FOOD_COLOR, outline=BACKGROUND_COLOR, tags='food'
        )


class Game:
    def __init__(self):
        # Initialize game variables
        self.direction = 'right'
        self.score = 0
        self.speed = SPEED

        # Initialize the main window
        self.window = Tk()
        self.window.title('SnaKeGamE')
        self.window.resizable(False, False)

        # Create label and canvas
        self.label = Label(self.window, text=f"Score: {self.score}\tHighscore: {Game.read_highscore()}",
                           font=('consolas', 30))
        self.label.pack()

        self.canvas = Canvas(self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
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
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas, self.snake)

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
            y_coord -= SPACE_SIZE
        elif self.direction == 'down':
            y_coord += SPACE_SIZE
        elif self.direction == 'left':
            x_coord -= SPACE_SIZE
        elif self.direction == 'right':
            x_coord += SPACE_SIZE

        # Insert new head position at the beginning of the coordinates list
        self.snake.coordinates.insert(0, [x_coord, y_coord])

        # Create new square for the head with HEAD_COLOR
        square = self.canvas.create_rectangle(
            x_coord, y_coord, x_coord + SPACE_SIZE, y_coord + SPACE_SIZE,
            fill=HEAD_COLOR, outline=BACKGROUND_COLOR
        )
        self.snake.squares.insert(0, square)

        # Change the color of the previous head to body color
        if len(self.snake.squares) > 1:
            self.canvas.itemconfig(self.snake.squares[1], fill=SNAKE_COLOR)

        if self.segment_color_index is not None:
            if self.segment_color_index < len(self.snake.squares):
                part = self.snake.squares[self.segment_color_index]
                self.canvas.itemconfig(part, fill=FOOD_COLOR)
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
            self.food = Food(self.canvas, self.snake)
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
        if x_coord < 0 or x_coord + SPACE_SIZE > GAME_WIDTH:
            return True
        elif y_coord < 0 or y_coord + SPACE_SIZE > GAME_HEIGHT:
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
        self.window.after(500, self.ask_play_again)

    def ask_play_again(self):
        response = messagebox.askyesno('Play Again?', 'Do you want to play again?')

        if response:
            self.restart_game()
        else:
            self.window.destroy()

    def restart_game(self):
        # Reset variables
        self.direction = 'right'
        self.score = 0
        self.speed = SPEED
        self.segment_color_index = None
        self.label.config(text=f"Score: {self.score}\tHighscore: {Game.read_highscore()}")

        # Clear canvas
        self.canvas.delete(ALL)

        # Bring the window to the front and make active window
        self.window.focus_force()

        # Recreate snake and food object
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas, self.snake)

        # Restart game loop
        self.next_turn()


    def write_highscore(self):
        # Write highscore to txt file
        with open('highscore.txt', 'w') as txt_score:
            txt_score.write(f"{self.score}")

    @staticmethod
    def read_highscore():
        # Read highscore from txt file
        try:
            with open('highscore.txt', 'r') as txt_score:
                highscore = int(txt_score.read())
                return highscore
        except (FileNotFoundError, ValueError):
            # If file doesn't exist or contains invalid data
            return 0

if __name__ == '__main__':
    game = Game()