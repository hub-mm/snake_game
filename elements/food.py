# ./elements/food.py

from constant_variables import constants
import random


class Food:
    def __init__(self, canvas, snake):
        self.canvas = canvas
        self.snake = snake
        while True:
            x_coord = random.randint(0, int((constants.GAME_WIDTH / constants.SPACE_SIZE) - 1)) * constants.SPACE_SIZE
            y_coord = random.randint(0, int((constants.GAME_HEIGHT / constants.SPACE_SIZE) - 1)) * constants.SPACE_SIZE
            self.coordinates = [x_coord, y_coord]

            if self.coordinates not in self.snake.coordinates:
                break

        self.canvas.create_oval(
            x_coord, y_coord, x_coord + constants.SPACE_SIZE, y_coord + constants.SPACE_SIZE,
            fill=constants.FOOD_COLOR, outline=constants.BACKGROUND_COLOR, tags='food'
        )