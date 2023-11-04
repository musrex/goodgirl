import pyglet
import pymunk
from levels import *
import time
# from player import *
# from fly import *
# from toy import *
from pyglet import shapes

class Game:
    def __init__(self,window):
        self.window = window

        self.game_area_width = self.window.width
        self.game_area_height = int(self.game_area_width / 2.35)

        self.game_area_left = self.window.width / 2 - self.game_area_width / 2
        self.game_area_right = self.game_area_left + self.game_area_width 
        self.game_area_bottom = self.window.height / 2 - self.game_area_height / 2
        self.game_area_top = self.game_area_bottom + self.game_area_height
        
        self.space = pymunk.Space()
        self.space.gravity = (0, -981)
        self.level = Level(self.space)
        self.fly = Fly(self, self.space, position=(self.game_area_width - 100, self.game_area_bottom))
        self.player = Player(self, self.space, position=(50, self.game_area_bottom))
        self.ball_count = 3

        self.window.on_draw = self.on_draw
        self.setup()

        self.toy = None
        self.window.push_handlers(self.player.on_mouse_press, self.player.on_mouse_release)

    def create_toy(self, position, impulse):
        self.toy = Toy(self, self.space, position)
        self.toy.apply_force(impulse)

    def ball_lost(self):
        self.ball_count -= 1
        if self.ball_count <= 0:
            self.handle_fail()

    def handle_fail(self):
        print("Game over! You've lost all your balls.")

    def setup(self):
        pyglet.clock.schedule_interval(self.update, 1/60.0) 

        #defining the floor
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(
                floor_body, 
                (self.game_area_left, self.game_area_bottom), 
                (self.game_area_right, self.game_area_bottom), 
                0.0
        )
        floor_shape.elasticity = 0.95
        floor_shape.friction = 0.9
        self.space.add(floor_body, floor_shape)


    def update(self, dt):
        # update game logic
        self.space.step(dt)
        self.player.update()
        self.fly.update()
        if self.toy is not None:
            self.toy.update()

        # check for win/fail conditions
        #if self.win_condition():
        #    self.handle_win()
        #elif self.fail_condition():
        #    self.handle_fail()

    def render(self):
        import pyglet.gl as gl
        
        gl.glClearColor(0,0,0,0) 
       
        self.window.clear()

        game_area = shapes.Rectangle(
                x=self.window.width / 2 - self.game_area_width / 2,
                y=self.window.height / 2 - self.game_area_height / 2,
                width=self.game_area_width,
                height=self.game_area_height,
                color=(255,255,255)
                )
        game_area.draw()
        
        self.level.draw()
        self.player.draw()
        self.fly.draw()
        if self.toy is not None:
            self.toy.draw()
        

    def on_draw(self):
        self.render()


class Player:
    def __init__(self, game, space, position):
        self.game = game
        self.space = space
        self.position = position
        self.height = 100

        self.is_throwing = False
        self.throw_start_pos = None
        self.throw_end_pos = None
        self.throw_start_time = None

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.is_throwing = True
            self.throw_start_pos = (x, y)
            self.throw_start_time = time.time()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT and self.is_throwing:
            self.is_throwing = False
            self.throw_end_pos = (x, y)
            self.throw_toy()

    def throw_toy(self):
        throw_end_time = time.time()
        time_elapsed = throw_end_time - self.throw_start_time

        dx = self.throw_end_pos[0] - self.throw_start_pos[0]
        dy = self.throw_end_pos[1] - self.throw_start_pos[1]
        impulse = (dx / time_elapsed, dy / time_elapsed)

        self.game.create_toy(self.position, impulse)

    def draw(self):
        square = shapes.Rectangle(#self.position[0], self.position[1], 50, 25, color=(50, 255, 30))
                x=self.position[0],
                y=self.position[1],
                width=25,
                height=self.height,
                color=(50, 225, 30) # green
        )
        square.draw()

    def update(self):
        x = max(self.position[0], self.game.game_area_left)
        x = min(x, self.game.game_area_right)
        y = max(self.position[1], self.game.game_area_bottom)
        y = min(y, self.game.game_area_top)
        self.position = (x, y)
    
class Toy:
    def __init__(self, game, space, position):
        self.game = game
        self.space = space

        self.body = pymunk.Body(1, float('inf')) # 1 is mass, pymunk.inf is inertia
        self.body.position = position
        
        self.shape = pymunk.Circle(self.body, 10) # 10 is radius
        self.shape.elasticity = 0.95
        self.shape.friction - 0.9

        self.space.add(self.body, self.shape)

    def draw(self):
        x, y = self.body.position
        circle = shapes.Circle(x, y, 5, color=(255, 50, 30)) # red
        circle.draw()
    
    def apply_force(self, force):
        self.body.apply_impulse_at_local_point(force)

    def update(self):
        x, y = self.body.position

        if x < self.game.game_area_left or x > self.game.game_area_right:
            self.game.ball_lost()
            self.space.remove(self.body, self.shape)
            self.game.toy = None

class Fly:
    def __init__(self, game, space, position):
        self.game = game
        self.space = space
        self.position = position
        # define physics body and shape
        # add to space

    def draw(self):
        square = shapes.Rectangle(#self.position[0], self.position[1], 50, 25, color=(50, 255, 30))
                x=self.position[0],
                y=self.position[1],
                width=45,
                height=15,
                color=(30, 30, 225) # blue
        )
        square.draw()
        square.draw()

    def update(self):
        x = max(self.position[0], self.game.game_area_left)
        x = min(x, self.game.game_area_right)
        y = max(self.position[1], self.game.game_area_bottom)
        y = min(y, self.game.game_area_top)
        self.position = (x, y)

        if self.game.toy is not None:
            ball_position = self.game.toy.body.position
            direction_to_ball = pymunk.Vec2d(ball_position - self.position)
            if direction_to_ball.length < chase_range:
                steering_force = direction_to_ball.normalized() * chase_speed
                self.body.apply_force(steering_force)

        if self.game.toy is not None and direction_to_ball < catch_threshold:
            self.catch_ball()

        if self.returning_ball:
            direction_to_player = pymunk.Vec2d(self.game.player.position - self.position)
            if direction_to_player.length > return_threshold:
                steering_force = direction_to_player.normalized() * return_speed
                self.body.apply_force(steering_force)
            else:
                self.returning_ball = False


    def catch_ball(self):
        self.game.space.remove(self.game.toy.body, self.game.toy.shape)
        self.game.toy = None

        self.returning_ball = True
