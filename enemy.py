from ursina import *
import time
enemy_list = []
enemy_counter = 0
class Enemy(Entity):
    def __init__(self):
        super().__init__()

        self.name = 'enemy'

        self.animator = Animator({'walk': None, 'jump' : None, 'idle': None})
        self.origin_y = -.5
        self.model = "cube"
        self.color = color.white
        self.texture = Texture("textures/enemy0.png")
        self.collider = "box"
        self.gravity = 1
        self.jump_duration = .5
        self.jumpHeight = 4
        self.grounded = True
        self.jumping = False
        self.jumpTimer = 0
        self.walking = True
        self.jumpsLeft = 1
        self.blocksMoved = 0
        self.movementSpeed = 0.050
        self.movementDistance = 8
        self.air_time = 0
        self.start_time = time.time()
        self.animator.state = 'idle'
        self.isDead = False
        self.turnAround = False
        self.uniqueID = enemy_counter
        self.active = False

        #self.y = 2
        ray = boxcast(self.world_position, self.down, distance = 10, ignore = (self, ), thickness = 1)
        if ray.hit:
            self.y = ray.world_point[1] + .01
    def move(self, movement):
        self.x += movement
        self.blocksMoved += abs(movement)
    def update(self):

        if self.active:
            self.walking = self.grounded

            if not self.grounded:
                self.animator.state = 'jump'
            elif self.walking:
                self.animator.state = 'walk'
            jump_ray = boxcast(self.world_position+(0,.05,0), self.down, ignore = (self, ), thickness = .9)
            #print(jump_ray.distance)
            if jump_ray.distance <= .1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                self.y = jump_ray.world_point[1] + .5
                return
            else:
                self.grounded = False
            if not self.grounded and not self.jumping and self.jumpTimer % 60 == 0:
                self.grounded = True
                self.jump()
                self.air_time += time.dt
            else:
                self.jumpTimer += 1
                if self.y > 87:
                    self.y -= .5
            if raycast(origin = self.world_position, direction = self.down, ignore=(self,), distance = .5).hit != True:
                self.y -= .5
            self.move(self.movementSpeed)
            right_collision = raycast(self.position+Vec3(0,.05, 0), self.right, .5, ignore=(self, ), debug=True)
            left_collision = raycast(self.position+Vec3(0, -.05, 0), self.left, .5, ignore=(self, ), debug=True)
            if self.blocksMoved >= self.movementDistance or right_collision.hit or left_collision.hit:
                self.blocksMoved = 0
                self.movementSpeed = -self.movementSpeed
                self.turnAround = not self.turnAround

    def jump(self):

        if not self.grounded:
            return
        if hasattr(self, 'y_animator'):
            self.y_animator.pause()
        self.jumping = True
        self.grounded = False
        max_height = self.y + self.jumpHeight
        duration = self.jump_duration
        hit_above = boxcast(self.position+(0,1.99,0), self.up, ignore = (self, ), thickness = .9)
        if hit_above.hit:
            max_height = min(0.80 + self.y + hit_above.distance, max_height)
            duration *= max_height / (self.y + self.jumpHeight)
        self.animate_y(max_height, duration, resolution=30, curve=curve.out_expo)
        invoke(self.start_fall, delay = duration)
    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False
    def land(self):
        self.air_time = 0
        self.grounded = True
# Enemy 0 has lateral movement (Goomba-like) -
# hits from above and below kill enemy,
# running into the character causes damage to character
class Enemy_Type_Zero(Enemy):
    def __init__(self):
        super().__init__()
        self.texture = Texture("textures/enemy0.png")
    def move(self, movement):
        super().move(movement)
    def update(self):
        if self.active:
            if raycast(origin = self.world_position, direction = self.down, ignore=(self,), distance = .5).hit != True:
                self.y -= .5
            self.move(self.movementSpeed)
            right_collision = raycast(self.position+Vec3(0,.05, 0), self.right, .5, ignore=(self, ), debug=True)
            left_collision = raycast(self.position+Vec3(0, -.05, 0), self.left, .5, ignore=(self, ), debug=True)
            if self.blocksMoved >= self.movementDistance or right_collision.hit or left_collision.hit:
                self.blocksMoved = 0
                self.movementSpeed = -self.movementSpeed
                self.turnAround = not self.turnAround
            self.check_if_death()
    def jump(self):
        pass
    # enemy type zero can be hit from above and below
    # if it never jumps how can it be killed from below? just going to check for above
    def check_if_death(self):
        if raycast(origin=self.position, distance=.5, direction=self.up, ignore=(self,)).hit:
            enemy_list[self.uniqueID] = " "
            destroy(self)


    def start_fall(self):
        pass
    def land(self):
        pass

# Enemy 1 has lateral movement (Koopa-like) -
# hits from below kill enemy, hits from above stun or
# transform enemy such that a second hit kills
class Enemy_Type_One(Enemy):
    def __init__(self):
        super().__init__()
        self.texture = Texture("textures/enemy1.png")
        self.type = 1
        self.numAllowedHits = 2
    # movement shouldn't have to chance since it has similar
    # lateralness as type 0.
    def move(self, movement):
        super().move(movement)
    def update(self):
        if self.active:
            # if it hasn't been stunned it can move

            if self.numAllowedHits == 2:
                self.move(self.movementSpeed)
                right_collision = raycast(self.position+Vec3(0,.05, 0), self.right, .5, ignore=(self, ), debug=True)
                left_collision = raycast(self.position+Vec3(0, -.05, 0), self.left, .5, ignore=(self, ), debug=True)
                if self.blocksMoved >= self.movementDistance or right_collision.hit or left_collision.hit:
                    self.blocksMoved = 0
                    self.movementSpeed = -self.movementSpeed
            self.check_if_death()
    def jump(self):
        pass
    def check_if_death(self):
        if raycast(origin=self.position, distance=.5, direction=self.up, ignore=(self, )).hit:
            self.numAllowedHits = self.numAllowedHits - 1
            if self.numAllowedHits == 0:
                enemy_list[self.uniqueID] = " "
                destroy(self)
    def start_fall(self):
        pass
    def land(self):
        pass



# Enemy 2 has lateral and vertical movement -
# hits from above convert into Enemy 1s,
# cannot be hit from below
class Enemy_Type_Two(Enemy):
    def __init__(self):
        super().__init__()
        self.color = color.white
        self.texture = Texture("textures/enemy2_left.png")
        self.type = 2
    def move(self, movement):
        super().move(movement)
    def jump(self):
        super().jump()
    def start_fall(self):
        super().start_fall()
    def land(self):
        super().land()
    def update(self):
        if self.active:
            if raycast(origin = self.world_position, direction = self.down, ignore=(self,), distance = .5).hit != True:
                self.y -= .5
            # currently set
            super().update()
            self.check_if_death()
            if(self.turnAround):
                self.texture = Texture("textures/enemy2_left.png")
            else:
                self.texture = Texture("textures/enemy2_right.png")
    def check_if_death(self):
        if raycast(origin=self.position, distance=.5, direction=self.up, ignore=(self, )).hit:
            enemy_list[self.uniqueID] = " "
            destroy(self)


# Enemy 3 has lateral movement and cannot be killed
# via attack (like buzzy beetle), hits from above or
# below stun/transform
class Enemy_Type_Three(Enemy_Type_Zero):
    def __init__(self):
        super().__init__()
        self.stunned = False

    def move(self, movement):
        super().move(movement)
    def update(self):
        if self.active:
            if raycast(origin = self.world_position, direction = self.down, ignore=(self,), distance = .5).hit != True:
                self.y -= .5
            if self.stunned == False:
                super().update()
            if(self.stunned):
                self.texture = Texture("textures/pot_gold.jpg")
            elif(self.turnAround):
                self.texture = Texture("textures/enemy2_left.png")
            else:
                self.texture = Texture("textures/enemy2_right.png")
    def start_fall(self):
        pass
    def land(self):
        pass
    def jump(self):
        pass
    # doesn't actually die, but still use this function to "stun"
    def check_if_death(self):
        if raycast(origin=self.position, distance=.5, direction=self.up, ignore=(self, )).hit:
            self.stunned = True


# Enemy 4 has minimal lateral movement and vertical
# movement but has attack (hammer brothers), hits from
# above or below kill enemy
class Enemy_Type_Four(Enemy):
    def __init__(self):
        super().__init__()
    def move(self, movement):
        super().move(movement)
    def jump(self):
        super().jump()
    def start_fall(self):
        super().start_fall()
    def land(self):
        super().land()
    def update(self):
        if self.active:
            if raycast(origin = self.world_position, direction = self.down, ignore=(self,), distance = .5).hit != True:
                self.y -= .5
            # currently set
            super().update()
            self.check_if_death()
    def check_if_death(self):
        if raycast(origin=self.position, distance=.5, direction=self.up, ignore=(self, )).hit:
            enemy_list[self.uniqueID] = " "
            destroy(self)



def create_enemy(type, x, y):
    global enemy_list
    global enemy_counter
    if type == 0:
        currenemy = Enemy_Type_Zero()
    elif type == 1:
        currenemy = Enemy_Type_One()
    elif type == 2:
        currenemy = Enemy_Type_Two()
    elif type == 3:
        currenemy = Enemy_Type_Three()
    elif type == 4:
        currenemy = Enemy_Type_Four()
    currenemy.x = x
    currenemy.y = y
    enemy_counter += 1
    enemy_list.append(currenemy)
    return currenemy
