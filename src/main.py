import pyglet
from game import Game

def main():
    window = pyglet.window.Window(fullscreen=True, caption='Good Girl, Fly!')
    game = Game(window)
    window.push_handlers(game.on_key_press)
    pyglet.app.run()

if __name__ == "__main__":
    main()


