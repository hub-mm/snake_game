# ./main.py
from tkinter import *
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOUR = '#06402B'
HEAD_COLOUR = '#00FF00'
FOOD_COLOUR = '#FF0000'
BACKGROUND_COLOUR = '#000000'

# Global variables
direction = 'right'
score = 0

# Update the window to get the correct width and height
window = Tk()
window.title('Snake Game')
window.resizable(False, False)

label = Label(window, text=f"score: {score}", font=('consolas', 30))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.attributes('-topmost', True)
window.update()
window.attributes('-topmost', False)


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        start_x = int((GAME_WIDTH / 2) / SPACE_SIZE) * SPACE_SIZE
        start_y = int((GAME_HEIGHT / 2) / SPACE_SIZE) * SPACE_SIZE

        for i in range(self.body_size):
            self.coordinates.append([start_x - i * SPACE_SIZE, start_y])

        for index, (x_coord, y_coord) in enumerate(self.coordinates):
            colour = HEAD_COLOUR if index == 0 else SNAKE_COLOUR

            square = canvas.create_rectangle(
                x_coord, y_coord, x_coord + SPACE_SIZE, y_coord + SPACE_SIZE,
                fill=colour, outline=BACKGROUND_COLOUR, tags='snake'
            )
            self.squares.append(square)


class Food:
    def __init__(self):
        while True:
            x_coord = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
            y_coord = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE
            self.coordinates = [x_coord, y_coord]

            if self.coordinates not in snake.coordinates:
                break

        canvas.create_oval(
            x_coord, y_coord, x_coord + SPACE_SIZE, y_coord + SPACE_SIZE,
            fill=FOOD_COLOUR, outline=BACKGROUND_COLOUR, tags='food'
        )


def next_turn(snake_obj, food_obj):
    global direction, score, SPEED

    x_coord, y_coord = snake_obj.coordinates[0]

    if direction == 'up':
        y_coord -= SPACE_SIZE
    elif direction == 'down':
        y_coord += SPACE_SIZE
    elif direction == 'left':
        x_coord -= SPACE_SIZE
    elif direction == 'right':
        x_coord += SPACE_SIZE

    snake_obj.coordinates.insert(0, [x_coord, y_coord])

    square = canvas.create_rectangle(
        x_coord, y_coord, x_coord + SPACE_SIZE, y_coord + SPACE_SIZE,
        fill=HEAD_COLOUR, outline=BACKGROUND_COLOUR
    )
    snake_obj.squares.insert(0, square)

    if len(snake_obj.squares) > 1:
        canvas.itemconfig(snake_obj.squares[1], fill=SNAKE_COLOUR)

    if x_coord == food_obj.coordinates[0] and y_coord == food_obj.coordinates[1]:
        score += 1
        SPEED = max(SPEED - 2, 20)

        label.config(text=f"score: {score}")

        canvas.delete('food')
        food_obj = Food()
    else:
        del snake_obj.coordinates[-1]
        canvas.delete(snake_obj.squares[-1])
        del snake_obj.squares[-1]

    if check_collision():
        game_over()
    else:
        print(SPEED)
        window.after(SPEED, next_turn, snake_obj, food_obj)


def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def check_collision():
    x_coord, y_coord = snake.coordinates[0]

    if x_coord < 0 or x_coord + SPACE_SIZE > GAME_WIDTH:
        return True
    elif y_coord < 0 or y_coord + SPACE_SIZE > GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x_coord == body_part[0] and y_coord == body_part[1]:
            return True

    return False


def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2, canvas.winfo_height() /2,
        font=('consolas', 70), text='GAME OVER', fill='RED', tags='game_over'
    )


window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<s>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()