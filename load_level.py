from ursina import *
# from ursina.prefabs.platformer_controller_2d import PlatformerController2d
from PC2d import PlatformerController2d
from ursina.prefabs.health_bar import HealthBar
import csv
import enemy
import threading
import time
import sys
import item as itemClass
# the following is basically main
# but ursina didn't like having a main

began = False

app = Ursina()

def dist(a, b):
    return abs(sqrt((b.x-a.x)**2 + (b.y-a.y)**2))

def build_level(start, stop, spawn_entities):
    global enemy_counter
    global flag_coords
    enemies = []
    done = False
    global enemy_positions
    print('Start:', start, 'Stop:', stop)
    global end
    if stop > end:
        stop = end
    # no unique blocks -- loads floor everywhere there's a character
    for i in range(0,len(level)):
        for j in range(start, stop):
            if spawn_entities:
                if level[i][j] != '':
                        # enemy type 0
                        if level[i][j] == '0' or level[i][j] == '7':
                            enemy.create_enemy(0,j,-i+100)
                        # enemy type 1
                        elif level[i][j] == '1' or level[i][j] == '5':
                            enemy.create_enemy(1,j,-i+100)
                        # enemy type 2
                        elif level[i][j] == '2' or level[i][j] == '6':
                            enemy.create_enemy(2,j,-i+100)
                        # enemy type 3
                        elif level[i][j] == '3':
                            enemy.create_enemy(3,j,-i+100)
                        # enemy type 4
                        elif level[i][j] == '4' or level[i][j] == '8':
                            enemy.create_enemy(4,j,-i+100)
            else:
                if level[i][j] != '':
                    # dead box
                    if level[i][j] == '@':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture = Texture("textures/deadblock1.png")
                        )
                    # single coin box
                    elif level[i][j] == 'A':
                        item.append('A')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/itemblock1.png")
                        )
                    # power up
                    elif level[i][j] == 'B':
                        item.append('B')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/itemblock1.png")
                        )
                    # star
                    elif level[i][j] == 'C':
                        item.append('C')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/itemblock1.png")
                        )
                    # 1 up
                    elif level[i][j] == 'D':
                        item.append('D')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/itemblock1.png")
                        )
                    # coin
                    elif level[i][j] == 'E':
                        item.append('E')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/coin.png"),
                            scale=(1,1)
                        )
                    # hidden PowerUp
                    elif level[i][j] == 'F':
                        item.append('F')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture = Texture("blank.png"),
                            scale=(1,1)
                        )
                    # hidden star
                    elif level[i][j] == 'G':
                        item.append('G')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture = Texture("blank.png"),
                            scale=(1,1)
                        )
                    # hidden 1up
                    elif level[i][j] == 'H':
                        item.append('H')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture = Texture("blank.png"),
                            scale=(1,1)
                        )
                    # Fire Floor
                    elif level[i][j] == 'O':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture = Texture("textures/fire.png")
                        )
                    # pipe
                    elif level[i][j] == 'P' or  level[i][j] == '|':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture = Texture("textures/pipe.png")
                        )
                    # stone - color 1
                    elif level[i][j] == 'a':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture = Texture("textures/stone.png")
                        )
                    # block - color 1
                    elif level[i][j] == 'b':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture = Texture("textures/block1.png")
                        )
                    # brick - color 1
                    elif level[i][j] == 'c':
                        item.append('c')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/brick.png")

                        )
                    # multi-coin box
                    elif level[i][j] == 'd':
                        item.append('d')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/brick.png")

                        )
                    # power up
                    elif level[i][j] == 'e':
                        item.append('e')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/brick.png")

                        )
                    # star
                    elif level[i][j] == 'f':
                        item.append('f')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/brick.png")

                        )
                    # 1up
                    elif level[i][j] == 'g':
                        item.append('g')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture=Texture("textures/brick.png")

                        )
                    # dead box
                    elif level[i][j] == 'h':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.white,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/deadblock1.png"),
                            scale=(1,1)
                        )
                    # vine
                    elif level[i][j] == 'i':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            scale=(1,1),
                            texture = Texture("textures/block1.png")
                        )
                    # stone color 2
                    elif level[i][j] == 'j':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/stone2.png"),
                            scale=(1,1)
                        )
                    # block color 2
                    elif level[i][j] == 'k':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/block2.png"),
                            scale=(1,1)
                        )
                    # brick color 2
                    elif level[i][j] == 'l':
                        item.append('l')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/brick2.png"),
                            scale=(1,1)
                        )
                    # multi coin box color 2
                    elif level[i][j] == 'm':
                        item.append('m')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/brick2.png"),
                            scale=(1,1)
                        )
                    # power up color 2
                    elif level[i][j] == 'n':
                        item.append('n')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/brick2.png"),
                            scale=(1,1)
                        )
                    # star color 2
                    elif level[i][j] == 'o':
                        item.append('o')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/brick2.png"),
                            scale=(1,1)
                        )
                    # 1up color 2
                    elif level[i][j] == 'p':
                        item.append('p')
                        positionx.append(j)
                        positiony.append(-i+100)
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/brick2.png"),
                            scale=(1,1)
                        )
                    # dead box color 2
                    elif level[i][j] == 'q':
                        Entity(
                            name = 'normal',
                            model='cube',
                            color=color.dark_gray,
                            collider='box',
                            ignore=False,
                            position=(j, -i+100),
                            texture=Texture("textures/deadblock2.png"),
                            scale=(1,1)
                        )
                    # flagpole
                    elif level[i][j] == '~':
                            Flag = Entity(
                                model='cube',
                                color=color.red,
                                collision=False,
                                collider=None,
                                ignore=False,
                                #always_on_top=True,
                                position=(j, -i+100),
                                texture=Texture("textures/flag.png"),
                                scale=(1,1)
                            )
                            flag_coords = [j, -i+100]

def whatToSpawn(xposition, yposition, item):
    global coin_s
    global mushroom_s
    global oneUP_s
    global star_s
    global flower_s
    global multicoin_s
    if item == 'A':
        itemClass.create_item("coin",xposition,yposition+1)
        coin_s = True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))

    elif item == 'B':
        if player.health == 1:
            itemClass.create_item("mushroom",xposition, yposition+1)
            mushroom_s = True
            Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
        elif player.health == 2 or player.health == 3:
            # spawn a mushroom, but change the player if they run into it at 2 or 3 health.
            itemClass.create_item("flower",xposition, yposition+1)
            flower_s = True
            Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'C':
        #spawn star
        itemClass.create_item("star",xposition,yposition+1)
        star_s = True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'D':
        itemClass.create_item("1up",xposition,yposition+1)
        oneUP_s=True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'E':
        itemClass.create_item("coin",xposition,yposition+1)
        coin_s = True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'F':
        if player.health == 1:
            itemClass.create_item("mushroom",xposition, yposition+1)
            mushroom_s = True
            Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
        elif player.health == 2 or player.health == 3:
            itemClass.create_item("flower",xposition, yposition+1)
            flower_s = True
            Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'G':
        #spawn star
        itemClass.create_item("star",xposition,yposition+1)
        star_s = True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'H':
        itemClass.create_item("1up",xposition,yposition+1)
        oneUP_s=True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'c':
        #block can be broken/disapear
        Entity(
            model='cube',
            color=color.light_gray,
            collision=False,
            collider=None,
            ignore=True,
            always_on_top=True,
            position=(xposition,yposition),
            scale=(1,1))
    elif item == 'd':
        #multicoin block
        itemClass.create_item("multicoin",xposition,yposition+1)
        multicoin_s = True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'e':
        if player.health == 1:
            itemClass.create_item("mushroom",xposition, yposition+1)
            mushroom_s = True
            Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))

        elif player.health == 2 or player.health == 3:
            itemClass.create_item("flower",xposition, yposition+1)
            flower_s = True
            Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))

    elif item == 'f':
        #spawn star
        itemClass.create_item("star",xposition,yposition+1)
        star_s = True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'g':
        itemClass.create_item("1up",xposition,yposition+1)
        oneUP_s=True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock1.png"),
            scale=(1,1))
    elif item == 'l':
        #block can be broken/disapear
        Entity(
            model='cube',
            color=color.light_gray,
            collision=False,
            collider=None,
            ignore=True,
            always_on_top=True,
            position=(xposition,yposition),
            scale=(1,1))
    elif item == 'm':
        #multicoin block
        itemClass.create_item("multicoin",xposition,yposition+1)
        multicoin_s = True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock2.png"),
            scale=(1,1))
    elif item == 'n':
        if player.health == 1:
            itemClass.create_item("mushroom",xposition, yposition+1)
            mushroom_s = True
            Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock2.png"),
            scale=(1,1))

        elif player.health == 2 or player.health == 3:
            itemClass.create_item("flower",xposition, yposition+1)
            flower_s = True
            Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock2.png"),
            scale=(1,1))

    elif item == 'o':
        #spawn star
        itemClass.create_item("star",xposition,yposition+1)
        star_s = True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock2.png"),
            scale=(1,1))
    elif item == 'p':
        itemClass.create_item("1up",xposition,yposition+1)
        oneUP_s=True
        Entity(
            model='cube',
            color=color.white,
            collision=True,
            collider=None,
            ignore=False,
            always_on_top=True,
            position=(xposition,yposition),
            texture=Texture("textures/deadblock2.png"),
            scale=(1,1))

def restart_level(app):
    app.restart()

endText = dedent('''
Congratulations! You have beaten this level. ''')
deadText = dedent('''
You died. Oh well. DMSP. ''')
timeUPtext = dedent('''
You ran out of time. DMSP. ''')

# we can probably specify background texture in window
window.color = color.light_gray
window.display_moves = 'colliders'

camera.orthographic = True

camera.fov = 16
enemy_counter = 0
enemies = []
enemy_positions = []
level = []
flag_coords = []
frames_passed = 0
boxes = []
item = []
positionx = []
positiony = []
coin_spawn = 0
coin_s = False
oneUP_s = False
star_s = False
mushroom_s = False
flower_s = False
multicoin_s = False


Song = Audio(sound_file_name='Leek Spin',
   autoplay=True,
   loop=True
 )

# maybe we should add user input to specify the file level
# it would be really easy to do the same with user data (coins/lives) too
file = ""
if len(sys.argv) == 1:
    print("Defaulting...")
    file  = "mario2-1.csv"
elif len(sys.argv) == 2:
    print("Opening file...")
    file = sys.argv[1]
else:
    print("Must pass in one file name to load file. Defaulting...")
    file = "mario2-1.csv"
with open(file) as csvDataFile:
    csvFile = csv.reader(csvDataFile)
    exclude_empty_rows = True
    for row in csvFile:
        if exclude_empty_rows:
            if not all([i == '' for i in row]):
                level.append(row)
                exclude_empty_rows = False
        else:
            level.append(row)

# todo: add up arrow functionality... I hate space bar
player = PlatformerController2d(
    color=color.white,
    y=1,
)
player.x = 0
player.y = 87
player.y = raycast(player.world_position, player.down).world_point[1]
player.texture = Texture("textures/pat_small.png")

end = len(level[0])
load_point = end // 4
# leaving here in case we want to do threading, but it seems like it doesn't work.
build = threading.Thread(target=build_level, args=(load_point, end // 2, False))
build.start()
build_remaining = threading.Thread(target=build_level, args=(end // 2, end, False))
build_remaining.start()
build_level(0, load_point, False)
build_level(0, end, True)

for i in range(0,len(positionx)):
    boxes.append([positionx[i],positiony[i], item[i]])

boxes.sort()
print(boxes)

# makes the camera object
cameraObject = Entity(
    model='cube',
    color=color.salmon,
    collider='',
    ignore=True,
    position=player.position,
    scale=(1,1),
    texture=Texture('blank.png')
)

checkpoint = Entity(
    model='cube',
    color=color.white,
    collider = None,
    collision = False,
    position = ((len(level[0]))/2, -13+100),
    scale=(1,2),
    texture=Texture('textures/checkpoint.png')
)


# camera follows object
camera.add_script(SmoothFollow(target=cameraObject, offset=[0,1,-30], speed=4))
# object follows player's x movement


button = Button(text="Click to start!\n Up Arrow/Space bar: Jump\nLeft Arrow: Left\n Right Arrow: Right\nDown Arrow: Attack [ DISABLED :( ]", color = color.azure)
def input(key):
    global start_time
    global began
    if key == "left mouse down" and began == False:
        began = True
        start_time = time.time()
        player.points = 0
        destroy(button)
    if key == "right mouse down":
        if(player.health == 3):
            player.health = 1
        else:
            player.health += 1
        print(player.health)
start_time = time.time()
s_time=time.time()
print(enemy.enemy_list)
timePassed = "Time: 250"
timeText = Text(text=timePassed, origin = (6.45, -10))
livesText = Text(text="Lives: x", origin = (9, -13))
pointsText = Text(text="Points: xxxxx", origin = (5, -12))
coinsText = Text(text="Coins: xxx", origin = (6.45, -11))

# enemy_dist = []
def update():
    global s_time
    global coin_s
    global oneUP_s
    global star_s
    global mushroom_s
    global flower_s
    global multicoin_s
    global began
    if began:
        player.gain_points(1)
        points = ""
        coins = ""
        lives = "Lives: " + str(player.lives)
        if len(str(player.points)) <= 5:
            for i in range(5 - len(str(player.points))):
                points = "0" + points
        points += str(player.points)
        points = "Points: "  + points
        if len(str(player.coins)) <= 3:
            for i in range(3 - len(str(player.coins))):
                coins = "0" + coins
        coins += str(player.coins)
        coins = "Coins: "  + coins
        elapsed_time = int(time.time() - start_time)
        timePassed = "Time: " + str(250 - elapsed_time)

        #disable player if time is up
        if 250-elapsed_time <= 0:
            player.enabled = False
            endTextAppear = Text(text = timeUPtext)
            endTextAppear.create_background()

        timeText.text = timePassed
        coinsText.text = coins
        pointsText.text = points
        livesText.text = lives
        if player.x > cameraObject.x:
            cameraObject.x = player.x
        if player.y < cameraObject.y:
            cameraObject.y = player.y
        if(player.y < -20+100):
            player.lose_life(level, checkpoint, cameraObject)
        if (player.lives == 0):
            player.enabled = False
            endTextAppear = Text(text = deadText)
            endTextAppear.create_background()

        # disable the player if they pass the coordinates of the flag.
        if player.x >= flag_coords[0] and player.y >= flag_coords[1]:
            player.x = flag_coords[0] + 5
            player.enabled = False
            endTextAppear = Text(text = endText)
            endTextAppear.create_background()

        # check if the player has been hit by an enemy
        for i in range(0, len(enemy.enemy_list)):
            if(enemy.enemy_list[i] != ' '):
                enemy_dist = dist(player, enemy.enemy_list[i])
                if not enemy.enemy_list[i].active:
                    if enemy_dist <= load_point:
                        enemy.enemy_list[i].active = True
                if(enemy_dist < 1.2 and player.grounded and not player.invincible):
                    # print("hit")
                    player.lose_health(level, checkpoint, cameraObject)

        #if player is jumping and hits a box that has action, take action
        if player.jumping:
            for j in range(0,len(boxes)):
                if player.health == 1 and player.x <= boxes[j][0]+.45 and player.x >= boxes[j][0]-.45 and player.y+2>=boxes[j][1] and boxes[j][1]>=player.y:
                    whatToSpawn(boxes[j][0],boxes[j][1],boxes[j][2])
                    boxes.pop(j)
                    s_time=time.time()
                    break
                elif player.health >= 2 and player.x <= boxes[j][0]+.45 and player.x >= boxes[j][0]-.45 and player.y+3>=boxes[j][1] and boxes[j][1]>=player.y:
                    whatToSpawn(boxes[j][0],boxes[j][1],boxes[j][2])
                    boxes.pop(j)
                    s_time=time.time()
                    break

        #if one up has spawned wait till player touches it or its off screen
        if oneUP_s:
            if dist(player, itemClass.item_list[-1]) < 1.2 :
                player.lives+=1
                itemClass.item_list[-1].delete()
                oneUP_s=False
            elif dist(player, itemClass.item_list[-1]) >15:
                itemClass.item_list[-1].delete()
                oneUP_s=False

        #if coin has spawned remove after one second
        if coin_s:
            if int(time.time()-s_time)>=1:
                #player.add_coin()
                itemClass.item_list[-1].delete()
                coin_s=False
                player.get_coin()
        if multicoin_s:
            if int(time.time()-s_time)>=1:
                #player.add_coin()
                itemClass.item_list[-1].delete()
                multicoin_s=False
                player.get_coin()
                player.get_coin()
                player.get_coin()
                player.get_coin()
                player.get_coin()

        if mushroom_s:
            if dist(player, itemClass.item_list[-1]) < 1.2 :
                if player.health == 1:
                    player.health += 1
                elif player.health == 2 or player.health == 3:
                    player.gain_points(50)
                itemClass.item_list[-1].delete()
                mushroom_s=False
            elif dist(player, itemClass.item_list[-1]) >15:
                itemClass.item_list[-1].delete()
                mushroom_s=False
        if flower_s:
            if dist(player, itemClass.item_list[-1]) < 1.2:
                player.gain_points(100)
                if player.health != 3:
                    player.health += 1
                itemClass.item_list[-1].delete()
                flower_s = False
            elif dist(player, itemClass.item_list[-1]) > 15:
                itemClass.item_list[-1].delete()
                flower_s = False

        if star_s:
            if dist(player, itemClass.item_list[-1]) < 1.2 :
                player.invincible = True
                itemClass.item_list[-1].delete()
                star_s=False
            elif dist(player, itemClass.item_list[-1]) >15:
                itemClass.item_list[-1].delete()
                star_s=False

        if(player.invincible):
            player.color = color.green
        else:
            player.color = color.white

        # update sprite based on health
        if(player.health == 3 and player.texture != Texture("textures/pat_powered.png")):
            player.scale_y = 2
            player.texture = Texture("textures/pat_powered.png")
        if(player.health == 2 and player.scale_y != 2):
            player.scale_y = 2
            player.texture = Texture("textures/pat_tall.png")
        if(player.health == 1 and player.scale_y != 1):
            player.scale_y = 1
            player.texture = Texture("textures/pat_small.png")


        # check invincibility frames and update if necessary
        if(player.invincible == True):
            player.inv_ctr += 1
        if(player.inv_ctr % 60 == 0):
            player.invincible = False

    return

camera.smooth_follow.offset[0] = 3
camera.smooth_follow.offset[1] = 3

window.size = (window.fullscreen_size[0]//2, window.fullscreen_size[1]//2)
window.position = (int(window.size[0]), int(window.size[1]-(window.size[1]/2)))
window.borderless = False
window.fullscreen = False

input_handler.bind('right arrow', 'd')
input_handler.bind('left arrow', 'a')
input_handler.bind('up arrow', 'w')
input_handler.bind('down arrow', 's')


print(enemy.enemy_list)

app.run()
