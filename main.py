# ./main.py

from tkinter import *
import random
from time import sleep

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOUR = '#00FF00'
FOOD_COLOUR = '#FF0000'
BACKGROUND_COLOUR = '#000000'

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x_cord, y_cord in self.coordinates:
            square = canvas.create_rectangle(x_cord, y_cord, x_cord + SPACE_SIZE, y_cord + SPACE_SIZE,
                                             fill=SNAKE_COLOUR, outline=BACKGROUND_COLOUR, tags='snake')
            self.squares.append(square)

class Food:
    def __init__(self):
        x_cord = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
        y_cord = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x_cord, y_cord]

        canvas.create_oval(x_cord, y_cord, x_cord + SPACE_SIZE, y_cord + SPACE_SIZE,
                           fill=FOOD_COLOUR, outline=BACKGROUND_COLOUR, tags='food')

def next_turn(snake_obj, food_obj):
    x_cord, y_cord = snake_obj.coordinates[0]

    if direction == 'up':
        y_cord -= SPACE_SIZE
    elif direction == 'down':
        y_cord += SPACE_SIZE
    elif direction == 'left':
        x_cord -= SPACE_SIZE
    elif direction == 'right':
        x_cord += SPACE_SIZE

    snake_obj.coordinates.insert(0, (x_cord, y_cord))

    square = canvas.create_rectangle(x_cord, y_cord, x_cord + SPACE_SIZE, y_cord + SPACE_SIZE,
                                     fill=SNAKE_COLOUR, outline=SNAKE_COLOUR)

    snake_obj.squares.insert(0, square)

    if x_cord == food_obj.coordinates[0] and y_cord == food_obj.coordinates[1]:
        global score

        score += 1
        label.config(text=f"Score: {score}")

        canvas.delete('food')
        food_obj = Food()

    else:

        del snake_obj.coordinates[-1]
        canvas.delete(snake_obj.squares[-1])
        del snake_obj.squares[-1]

    if check_collision(snake_obj):
        game_over()
    else:
        window.after(SPEED, next_turn, snake_obj, food_obj)

def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collision(snake_obj):
    x_cord, y_cord = snake_obj.coordinates[0]

    if x_cord < 0 or x_cord >= GAME_WIDTH:
        return True
    elif y_cord < 0 or y_cord >= GAME_HEIGHT:
        return True

    for body_part in snake_obj.coordinates[1:]:
        if x_cord == body_part[0] and y_cord == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() /2,
                       font=('consolas', 70), text='GAME OVER', fill='RED', tags='game_over')

window = Tk()
window.title('Snake Game')
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text=f"Score {score}", font=('consolas', 40))
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