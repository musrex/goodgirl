import pyglet
import pymunk

class Game:
    def __init__(self,window):
        self.window = window
        self.space = pymunk.Space()
        self.level = Level(self.space)
        self.fly = Fly(self.space, position=(100, 100))
        self.toy = Toy(self.space, position=(200, 200))
        self.player = Player(self.space, position=(50, 50))
        self.setup()

    def setup(self):
        pyglet.clock.schedule_interval(self.update, 1/60.0) 
        self.window.push_hnadlers(self.on_key_press)
        # load assets, initialize game state, etc

    def update(self, dt):
        # update game logic
        self.space.step(dt)
        self.player.update()
        self.fly.update()
        self.toy.update()

        # check for win/fail conditions

    def render(self):
        # render game objects
        pass


