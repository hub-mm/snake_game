# ./elements/snake.py

from constant_variables import constants


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = constants.BODY_PARTS
        self.coordinates = []
        self.squares = []

        start_x = int((constants.GAME_WIDTH / 2) / constants.SPACE_SIZE) * constants.SPACE_SIZE
        start_y = int((constants.GAME_HEIGHT / 2) / constants.SPACE_SIZE) * constants.SPACE_SIZE

        for i in range(self.body_size):
            self.coordinates.append([start_x - i * constants.SPACE_SIZE, start_y])

        for index, (x_coord, y_coord) in enumerate(self.coordinates):
            color = constants.HEAD_COLOR if index == 0 else constants.SNAKE_COLOR

            square = self.canvas.create_rectangle(
                x_coord,
                y_coord,
                x_coord + constants.SPACE_SIZE,
                y_coord + constants.SPACE_SIZE,
                fill=color, outline=color, tags='snake'
            )
            self.squares.append(square)