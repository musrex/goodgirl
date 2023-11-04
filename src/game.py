import pyglet
import pymunk
from levels import *
import time
import random
from pyglet import shapes

class Game:
    def __init__(self,window):
        self.window = window
        
        self.bg_music = pyglet.media.load('../assets/music/background.wav')
        self.bg_player = pyglet.media.Player()
        self.bg_player.queue(self.bg_music)
        self.bg_player.eos_action = 'loop'
        self.bg_player.play()

        self.space = pymunk.Space()
        self.space.gravity = (0, -981)

        self.game_area_width = self.window.width
        self.game_area_height = int(self.game_area_width / 2.35)
        self.ball_count = 3

        self.game_area_left = self.window.width / 2 - self.game_area_width / 2
        self.game_area_right = self.game_area_left + self.game_area_width 
        self.game_area_bottom = self.window.height / 2 - self.game_area_height / 2
        self.game_area_top = self.game_area_bottom + self.game_area_height

        self.left_boundary = self.game_area_left
        self.right_boundary = self.game_area_right
        self.top_boundary = self.game_area_top
        self.bottom_boundary = self.game_area_bottom 

        self.setup_floor()
        
        self.load_sprites()

        self.level = Level(self.space)
        self.player = Player(self, self.space, position=(50, self.game_area_bottom))
        self.fly = Fly(self, self.space, position=(self.game_area_width - 100, self.game_area_bottom + 1))
        
        self.setup_collision_handlers()
        
        self.window.on_draw = self.on_draw

        self.setup_ui()
        self.toy = None
        self.window.push_handlers(self.player.on_mouse_press, self.player.on_mouse_release)
        

        self.window.on_close = self.on_close
        
        self.setup()

    def load_sprites(self):
        self.fly_image = pyglet.image.load('../assets/sprites/fly.png')
        self.grass_image = pyglet.image.load('../assets/sprites/grass.png')
        self.tree_image = pyglet.image.load('../assets/sprites/tree.png')
        self.player_image = pyglet.image.load('../assets/sprites/player.png')

        self.tree_sprites = []
        number_of_trees = 5
        for _ in range(number_of_trees):
            tree_x = random.randint(self.game_area_left, self.game_area_right)
            tree_sprite = pyglet.sprite.Sprite(self.tree_image, 
                                                x=tree_x,
                                                y=self.game_area_bottom)

            tree_sprite.scale = random.randrange(1, 5)
            
            # Set opacity based on the scale.
            if tree_sprite.scale == 1:
                tree_sprite.opacity = 80
            elif tree_sprite.scale == 2:
                tree_sprite.opacity = 130
            elif tree_sprite.scale == 3:
                tree_sprite.opacity = 200
            elif tree_sprite.scale == 4:
                tree_sprite.opacity = 255
            
            self.tree_sprites.append(tree_sprite)
        
        self.grass_sprites = []
        for i in range(0, self.game_area_width, self.grass_image.width):
            grass_sprite = pyglet.sprite.Sprite(self.grass_image,
                                                x=self.game_area_left + i,
                                                y=self.game_area_bottom)
            self.grass_sprites.append(grass_sprite)
        


    def setup_ui(self):
        self.game_name_label = pyglet.text.Label('Good Girl, Fly!',
                                                 font_name='Sans Serif',
                                                 font_size=36,
                                                 x=self.game_area_left + 10,
                                                 y=self.window.height - 10,
                                                 anchor_x='left', anchor_y='top')
        
        self.ball_count_label = pyglet.text.Label(f'Ball Count: {self.ball_count}',
                                                  font_name='Sans Serif',
                                                  font_size=24,
                                                  x=self.window.width - 10,
                                                  y=self.window.height - 10,
                                                  anchor_x='right', anchor_y='top')

        self.fly_excitement_label = pyglet.text.Label(f'Fly\'s Excitement: {self.fly.excitement}',
                                                      font_name='Sans Serif',
                                                      font_size=24,
                                                      x=self.window.width - 10,
                                                      y=self.window.height - 40,
                                                      anchor_x='right', anchor_y='top')

    def update_ui(self):
        self.ball_count_label.text = f'Ball Count: {self.ball_count}'
        self.fly_excitement_label.text = f'Fly\'s Excitement: {self.fly.excitement}'


    def create_toy(self, position, impulse):
        self.toy = Toy(self, self.space, position)
        self.toy.apply_force(impulse)

    def ball_lost(self):
        self.ball_count -= 1
        if self.ball_count <= 0:
            self.handle_fail()

    def handle_fail(self):
        self.bg_player.pause()
        self.game_over = True
        self.fail_label = pyglet.text.Label('Fly has run away!\nPress R to Restart',
                                            font_name='Sans Serif',
                                            font_size=36,
                                            x=self.window.width / 2,
                                            y=self.window.height / 2,
                                            anchor_x='center', anchor_y='center',
                                            multiline=True, width=400,
                                            color=(255,255,255,255))
    
    def restart_game(self):
        self.bg_player.play()
        self.game_over = False
        self.ball_count = 3
        self.fly.excitement = 5
        self.fly.body.position = self.fly.original_position
        self.fly.body.velocity = (0,0)

    def setup(self):
        pyglet.clock.schedule_interval(self.update, 1/60.0) 
    
    def setup_floor(self):
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
        floor_shape.collision_type = 1
        self.space.add(floor_body, floor_shape)


    def update(self, dt):
        # update game logic
        self.space.step(dt)
        self.player.update()
        self.fly.update()
        if self.toy is not None:
            self.toy.update()
            self.fly.set_target_to_ball()

        if not self.game_area_left < self.fly.body.position.x < self.game_area_right or \
           not self.game_area_bottom < self.fly.body.position.y < self.game_area_top:
            self.handle_fail()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.R:
            self.restart_game()

    def render(self):
        import pyglet.gl as gl
        
        gl.glClearColor(0,0,0,0) 
       
        self.window.clear()

        if hasattr(self, 'game_over') and self.game_over:
            self.fail_label.draw()
        else:
            game_area = shapes.Rectangle(
                x=self.window.width / 2 - self.game_area_width / 2,
                y=self.window.height / 2 - self.game_area_height / 2,
                width=self.game_area_width,
                height=self.game_area_height,
                color=(135,206,235)
                )
            game_area.draw()
        
             
            for tree_sprite in self.tree_sprites:
                tree_sprite.draw()

            for grass_sprite in self.grass_sprites:
                grass_sprite.draw()

            self.level.draw()
            self.player.draw()
            self.fly.draw()
            if self.toy is not None:
                self.toy.draw()
            self.game_name_label.draw()
            self.ball_count_label.draw()
            self.fly_excitement_label.draw()

    def on_draw(self):
        self.render()

    def setup_collision_handlers(self):
        handler = self.space.add_collision_handler(1, 2)
        handler.begin = self.handle_ball_floor_collision
        
        fly_floor_handler = self.space.add_collision_handler(3, 1)
        fly_floor_handler.begin = self.fly.handle_ground_collision


    def handle_ball_floor_collision(self, arbiter, space, data):
        ball_shape = arbiter.shapes[1]
        ball = ball_shape.body.data
        ball.has_bounced()
        return True

    
    def on_close(self):
        self.bg_player.pause()
        self.bg_player.delete()

        self.window.close()

class Player:
    def __init__(self, game, space, position):
        self.game = game
        self.space = space
        
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = position
        
        self.width = 25
        self.height = 100
        rectangle_points = [(-self.width/2, -self.height/2),
                            (-self.width/2, self.height/2),
                            (self.width/2, self.height/2),
                            (self.width/2, -self.height/2)]
        self.shape = pymunk.Poly(self.body, rectangle_points)  # Define the physics shape
        self.shape.elasticity = 0.0
        self.shape.friction = 1
        self.shape.collision_type = 4
        self.space.add(self.body, self.shape)
        
        self.sprite = pyglet.sprite.Sprite(game.player_image, 
                                           x=position[0], 
                                           y=position[1])        
        self.sprite.scale = 1.5
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

        if time_elapsed > 0:
            dx = self.throw_end_pos[0] - self.throw_start_pos[0]
            dy = self.throw_end_pos[1] - self.throw_start_pos[1]
            impulse = (dx / time_elapsed, dy / time_elapsed)
        
            self.game.create_toy(self.body.position, impulse)
            self.game.fly.set_target_to_ball()

    def draw(self):
        self.sprite.x, self.sprite.y = self.body.position
        self.sprite.draw()

    def update(self):
        x, y = self.body.position 

    
class Toy:
    def __init__(self, game, space, position):
        self.game = game
        self.space = space

        self.body = pymunk.Body(1, float('inf')) # 1 is mass, pymunk.inf is inertia
        self.body.position = position

        self.body.data = self
        
        self.shape = pymunk.Circle(self.body, 10) # 10 is radius
        self.shape.elasticity = 0.75
        self.shape.friction = 0.4
        self.shape.collision_type = 2

        self.space.add(self.body, self.shape)

        self.bounce_count = 0

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
            self.game.update_ui()

    def has_bounced(self):
        self.bounce_count += 1
    
class Fly:
    def __init__(self, game, space, position):
        self.game = game
        self.space = space
        
        self.sprite = pyglet.sprite.Sprite(game.fly_image, 
                                           x=position[0], 
                                           y=position[1])

        self.width = 45
        self.height = 15
        
        mass = 1
        moment = pymunk.moment_for_box(mass, (self.width, self.height))

        self.body = pymunk.Body(mass, moment)
        self.body.position = position 

        rectangle_points = [(-self.width/2, -self.height/2), 
                            (-self.width/2, self.height/2), 
                            (self.width/2, self.height/2),
                            (self.width/2, -self.height/2)]
        self.shape = pymunk.Poly(self.body, rectangle_points)
        self.shape.elasticity = 0.0
        self.shape.friction = 1.0
        self.shape.collision_type = 3

        self.space.add(self.body, self.shape)

        self.original_position = position
        self.target_position = position
        self.last_ball_catch_position = position
        self.boredom_factor = 0
        self.excited = False
        
        self.on_ground = True
        if self.on_ground:
            self.should_jump = True
        else:
            self.should_jump = False


        self.chase_speed = 25
        self.chase_range = 100
        self.catch_threshold = 100
        self.return_speed = 20
        self.return_threshold = 700
        self.excitement = 5
        self.max_excitement = 10
        self.excitement_increase = 1
        self.excitement_decrease = 1
        self.returning_ball = False


    def draw(self):
        self.sprite.x = self.body.position.x
        self.sprite.y = self.body.position.y
        self.sprite.draw()


    def update(self):
        print("Fly is updating")
        x , y = self.body.position

        self. boredom_factor += 0.009
        self.boredom_factor = min(self.boredom_factor, 1)

        direction_to_target = pymunk.Vec2d(*self.target_position - self.body.position)
       
        if self.returning_ball:
            print('check 1')
            self.boredom_factor -= 0.01
            distance_from_player = self.last_ball_catch_position.get_distance(self.game.player.body.position)
            direction_to_player = pymunk.Vec2d(*self.game.player.body.position - self.body.position)
            print(f"Distance from player :", distance_from_player)
            print(f"Direction to player :", direction_to_player)

            if distance_from_player > self.return_threshold:
                steering_force = direction_to_player.normalized() * self.return_speed
                self.body.apply_impulse_at_local_point(steering_force)
            else:
                self.returning_ball = False
                self.game.ball_count += 1

        elif self.game.toy is not None:
            print('check 2')
            self.boredom_factor -= 0.01
            ball_position = self.game.toy.body.position
            direction_to_target = pymunk.Vec2d(*ball_position - self.body.position)
            self.last_ball_catch_position = pymunk.Vec2d(*ball_position)
            if direction_to_target.length > 10:
                if random.random() > self.boredom_factor:
                    steering_force = direction_to_target.normalized() * self.chase_speed
                    self.body.apply_impulse_at_local_point(steering_force)

        if self.excitement > 5:
            print('excited')
            self.boredom_factor -= 0.01
            jitter_force = pymunk.Vec2d(random.uniform(-1, 1), random.uniform(-1, 1)) * self.chase_speed * 0.1
            self.body.apply_impulse_at_local_point(jitter_force)

        if self.game.toy is not None and direction_to_target.length < self.catch_threshold:
            print('check 3')
            self.boredom_factor -= 0.01
            self.catch_ball()

       # Boundary checks
        if x < self.game.game_area_left:
            x = self.game.game_area_left
            self.body.velocity = (0, self.body.velocity.y)
        elif x > self.game.game_area_right:
            x = self.game.game_area_right
            self.body.velocity = (0, self.body.velocity.y)

        if y < self.game.game_area_bottom:
            self.body.velocity = (self.body.velocity.x, max(self.body.velocity.y, 0))
        elif y > self.game.game_area_top:
            self.body.velocity = (self.body.velocity.x, max(self.body.velocity.y, 0))
        
        self.body.position = (x, y)

        max_jump_height = self.game.game_area_bottom + 100
        if y > max_jump_height:
            gravity_force = -981
            self.body.apply_force_at_local_point((0, gravity_force))

        if self.on_ground and self.should_jump:
            jump_force = 50
            self.body.apply_impulse_at_local_point((0, jump_force))
            self.on_ground = False
        
        self.game.update_ui()


    def handle_ground_collision(self, arbiter, space, data):
        self.on_ground = True
        return True

    def catch_ball(self):
        print('caught!')
        bounces = self.game.toy.bounce_count
        
        count = 0
        for i in range(bounces):
            count += 1
        print(f"Bounces: ", count)
        
        self.game.space.remove(self.game.toy.body, self.game.toy.shape)
        self.game.toy = None

        self.returning_ball = True

        if bounces == 0:
            self.excitement += self.excitement_increase
        elif bounces > 0:
            self.excitement -= self.excitement_decrease
        
        self.game.update_ui()

    def set_target_to_ball(self):
        if self.game.toy:
            ball_position = self.game.toy.body.position
            self.target_position = ball_position


