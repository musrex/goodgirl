import pyglet
from game import Game

def main():
    window = pyglet.window.Window(800, 600, 'Good Girl, Fly!')
    game = Game(window)
    pyglet.app.run()

if __name__ == "__main__":
    main()


