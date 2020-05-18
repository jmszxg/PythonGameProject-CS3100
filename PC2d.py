# Variation of ursina's platformer_controller_2d.py
# edited by Brie

from ursina import *



class PlatformerController2d(Entity):
    def __init__(self, **kwargs):
        super().__init__()

        self.model = 'cube'
        self.origin_y = -.5
        self.scale_y = 2
        self.color = color.orange
        self.collider = 'box'

        self.lives = 3
        self.health = 1
        self.coins = 0
        self.points = 0
        self.invincible = False
        self.inv_ctr = 0

        self.animator = Animator({'idle' : None, 'walk' : None, 'jump' : None})
        # self.animation_state_machine.state = 'jump'
        # self.idle_animation = None
        # self.walk_animation = None
        # self.jump_animation = None
        # self.idle_animation = Entity(parent=self, model='cube', color=color.gray, origin_y=-.5, scale_z=2)
        # self.walk_animation = Animation(parent=self, texture='ursina_wink', color=color.red, origin_y=-.5, scale=(2,2), double_sided=True)
        # self.model = None

        self.walk_speed = 8
        self.walking = False
        self.velocity = 0
        self.jump_height = 4
        self.jump_duration = .5
        self.jumping = False
        self.max_jumps = 1
        self.jumps_left = self.max_jumps
        self.gravity = 1
        self.grounded = True
        self.air_time = 0

        self.y = 2
        ray = boxcast(self.world_position, self.down, distance=10, ignore=(self, ), thickness=1)
        if ray.hit:
            self.y = ray.world_point[1] + .01

        #camera.add_script(SmoothFollow(target=self, offset=[0,1,-30], speed=4))

        for key, value in kwargs.items():
            setattr(self, key, value)

        self._original_scale_x = self.scale_x


    def update(self):
        if raycast(self.position+Vec3(0,.05,0), self.right, .5, ignore=(self, ), debug=True).hit == False:
            self.x += self.velocity * time.dt * self.walk_speed

        self.walking = held_keys['a'] + held_keys['d'] > 0 and self.grounded

        # animations
        if not self.grounded:
            self.animator.state = 'jump'
        else:
            if self.walking:
                self.animator.state = 'walk'
            else:
                self.animator.state = 'idle'

        ray = boxcast(self.world_position+(0,.05,0), self.down, ignore=(self, ), thickness=.9)

        if ray.distance <= .1:
            if not self.grounded:
                self.land()
            self.grounded = True
            self.y = ray.world_point[1]
            return
        else:
            self.grounded = False

        # if not on ground and not on way up in jump, fall
        if not self.grounded and not self.jumping:
            self.y -= min(self.air_time, ray.distance-.05)
            self.air_time += time.dt*7


    def input(self, key):
        if key == 'space' or key=='up' or key=='w':
            self.jump()

        #if key == 'down' or key=='s':
            #self.attack()

        if key == 'd':
            self.velocity = 1
            self.scale_x = self._original_scale_x
        if key == 'd up':
            self.velocity = -held_keys['a']

        if key == 'a':
            self.velocity = -1
        if key == 'a up':
            self.velocity = held_keys['d']

        if key == 'finished':
            self.velocity = .25
            self.scale_x=self._original_scale_x

        if held_keys['d'] or held_keys['a']:
            self.scale_x = self._original_scale_x * self.velocity


    def jump(self):
        if not self.grounded:
            return

        if hasattr(self, 'y_animator'):
            self.y_animator.pause()
        self.jump_dust = Entity(model=Circle(), scale=.5, color=color.white33, position=self.position)
        self.jump_dust.animate_scale(3, duration=.3, curve=curve.linear)
        self.jump_dust.fade_out(duration=.2)
        destroy(self.jump_dust, 2.1)

        self.jumping = True
        #self.jumps_left -= 1
        self.grounded = False
        jump_sound=Audio(sound_file_name='Mario Jump Sound Effect', autoplay=True)

        max_height = self.y + self.jump_height
        duration = self.jump_duration
        hit_above = boxcast(self.position+(0,1.99,0), self.up, ignore=(self,), thickness=.9)
        if hit_above.hit:
            if self.health == 1:
                max_height = min(0.99+self.y+hit_above.distance, max_height)
                duration *=  max_height / (self.y+self.jump_height)
            elif self.health == 2 or self.health == 3:
                max_height = min(self.y+hit_above.distance, max_height)
                duration *=  max_height / (self.y+self.jump_height)

        self.animate_y(max_height, duration, resolution=30, curve=curve.out_expo)
        invoke(self.start_fall, delay=duration)


    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False

    def land(self):
        # print('land')
        self.air_time = 0
        self.jumps_left = self.max_jumps
        self.grounded = True
    def gain_points(self, points):
        if self.enabled:
            self.points += points

    def get_coin(self):
        self.coins += 1
        self.points += 50
        if(self.coins == 100):
            self.lives += 1
            self.coins = 0

    def lose_health(self, level, checkpoint, cameraObject):
        if(self.invincible == False):
            if(self.health == 3):
                self.health = 1
            else:
                self.health -= 1
            if(self.health == 0):
                self.lose_life(level, checkpoint, cameraObject)
            self.invincible = True

    def lose_life(self, level, checkpoint, cameraObject):
        deadText = dedent('''
        You died. Oh well. DMSP. ''')
        # this takes health straight from powered up to small. we can take this out if we want
        self.lives -= 1
        if(self.lives == 0):
            self.y = 87
            game_over=Audio('Rick Death', autoplay=True)
            self.enabled = False
            endTextAppear = Text(text = deadText)
            endTextAppear.create_background()
        self.respawn(level, checkpoint, cameraObject)

    def respawn(self, level, checkpoint, cameraObject):
        self.health = 1
        if (self.x >= (len(level[0])/2)):
            self.position = checkpoint.position
            cameraObject.x = self.x
            cameraObject.y = self.y
        elif (self.x < (len(level[0])/2)):
            self.x = 0
            self.y = 87
            cameraObject.x = self.x
            cameraObject.y = self.y

    #def attack(self):
        #if(self.health == 3):
            #intersection_marker = Entity(model='cube', scale=.2, color=color.red)
            #ray = boxcast(self.position+Vec3(2,0,0), self.right, 2, thickness=.3, debug=False)
            #intersection_marker.world_position = ray.world_point
            #intersection_marker.visible = ray.hit
