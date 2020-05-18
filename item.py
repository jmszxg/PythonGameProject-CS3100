from ursina import *
item_counter = 0
item_list = []
class Item (Entity):
    def __init__(self):
        super().__init__()
        self.blocksMoved = 0
        self.model = "cube"
        self.collider = "box"
        self.color = color.white
        self.texture = Texture("textures/coin.png")
        self.movementSpeed = 0.2
        self.movementDistance = 8
        self.gravity = 1
        self.uniqueID = item_counter
        self.turnAround = False
        ray = boxcast(self.world_position, self.down, distance = 10, ignore = (self, ), thickness = 1)
        if ray.hit:
            self.y = ray.world_point[1] + .01
    def update(self):
        self.move(self.movementSpeed)
        right_collision = raycast(self.position+Vec3(0,.05, 0), self.right, .5, ignore=(self, ), debug=True)
        left_collision = raycast(self.position+Vec3(0, -.05, 0), self.left, .5, ignore=(self, ), debug=True)
        if self.blocksMoved >= self.movementDistance or right_collision.hit or left_collision.hit:
            self.blocksMoved = 0
            self.movementSpeed = -self.movementSpeed
            self.turnAround = not self.turnAround

    def delete(self):
        destroy(self)
    def move(self, movement):
        self.x += movement
        self.blocksMoved += abs (movement)

class Coin (Item):
    def __init__(self):
        super().__init__()
        self.created = True
    def update(self):
        pass
    def delete(self):
        destroy(self)

class OneUp(Item):
    def __init__(self):
        super().__init__()
        self.created = True
        self.texture = Texture("textures/1up.jpg")
    def update(self):
        super().update()
        if raycast(origin = self.world_position, direction = self.down, ignore=(self,), distance= .5).hit != True:
            self.y -= .5
    def delete(self):
        destroy(self)
class Star(Item):
    def __init__(self):
        super().__init__()
        self.texture = Texture("textures/star.jpg")
        self.created = True
    def update(self):
        super().update()
        if raycast(origin = self.world_position, direction = self.down, ignore=(self,), distance= .5).hit != True:
            self.y -= .5
    def delete(self):
        destroy(self)
class PowerUp(Item):
    def __init__(self):
        super().__init__()
        self.created = True
        self.texture = Texture("textures/mushroom.jpg")
    def update(self):
        super().update()
        if raycast(origin = self.world_position, direction = self.down, ignore=(self,), distance= .5).hit != True:
            self.y -= .5
    def delete(self):
        destroy(self)
class Flower(Item):
    def __init__(self):
        super().__init__()
        self.created = True
        self.texture = Texture("textures/flower.png")
    def update(self):
        pass
    def delete(self):
        destroy(self)

class MultiCoin (Item):
    def __init__(self):
        super().__init__()
        self.created = True
        self.texture = Texture("textures/pot_gold.jpg")
    def update(self):
        pass
    def delete(self):
        destroy(self)

def create_item(type, x, y):
    global item_counter
    global item_list
    if type == "coin":
        currItem = Coin()
    elif type == "1up":
        currItem = OneUp()
    elif type == "star":
        currItem = Star()
    elif type == "mushroom":
        currItem = PowerUp()
    elif type == "flower":
        currItem = Flower()
    elif type == "multicoin":
        currItem = MultiCoin()    
    currItem.x = x
    currItem.y = y
    item_counter += 1
    item_list.append(currItem)
    return currItem
