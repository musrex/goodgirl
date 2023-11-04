import pyglet
from game import Game

def main():
    window = pyglet.window.Window(fullscreen=True, caption='Good Girl, Fly!')
    game = Game(window)
    pyglet.app.run()

if __name__ == "__main__":
    main()


