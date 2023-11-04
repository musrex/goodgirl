import pyglet
from pyglet import shapes

class Player:
    def __init__(self, space, position):
        self.space = space
        self.position = position
        # define physics
        # add to space

    def handle_input(self, symbol):
        # handle inputs
        pass
    
    def draw(self):
        square = shapes.Rectangle(self.position[0], self.position[1], 50, 50, color=(50, 225, 30))
        square.draw()

    def update(self):
        # update player state
        pass


