from random import choice, uniform
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

wall_height = 30
ground_size = 100
spawn_area = (ground_size - 20)
wall_texture = 'assets/wall/brick_crosswalk_diff_2k.jpg'
jabami_tree_path = "assets/models/jabami_tree_v3.glb"

direction = 0.06
platform_scale = 3

app = Ursina()

ground = Entity(
    model='plane',
    texture='grass',
    collider='mesh',
    scale=(ground_size, 1, ground_size)
)

def CreateWall(position, scale, texture):
    return Entity(
        model='cube',
        collider='box',
        position=position,
        scale=scale,
        texture=texture,
        texture_scale=(5, 2.5)
    )

wall_F = CreateWall((0, wall_height/2, ground_size/2), (ground_size, wall_height, 1), wall_texture)
wall_B = CreateWall((0, wall_height/2, -ground_size/2), (ground_size, wall_height, 1), wall_texture)
wall_R = CreateWall((-ground_size/2, wall_height/2, 0), (1, wall_height, ground_size), wall_texture)
wall_L = CreateWall((ground_size/2, wall_height/2, 0), (1, wall_height, ground_size), wall_texture)

def CreateTree(position, scale, model = jabami_tree_path):
    tree = Entity(
        model=model,
        position=position,
        scale=scale,
    )
    # apply custom collider for tree trunk
    Entity(parent=tree, position=(0,0.5,0), scale=(0.3,4,0.3), collider='box')

def CreateRandomTree(r, x, y, model = jabami_tree_path):
    CreateTree(position=(x, -.2, y), scale=(r, r, r), model=model)

for i in range(5):
    CreateRandomTree(r=uniform(1, 2), x=uniform(-spawn_area/2, spawn_area/2), y=uniform(-spawn_area/2, 0))

player = FirstPersonController(
    height=2
)
player.cursor.visible = True

player.walk_sound = Audio(
    'assets\sounds\sound_walking01.mp3',
    loop=True,
    autoplay=False,
    volume=.4
)

player.jump_sound = Audio(
    'assets\sounds\sound_jump.mp3',
    loop=False,
    autoplay=False,
    volume=.4
)

blocks = []
for i in range(7):
    r = uniform(-2, 2)
    block = Entity(
        model = 'cube',
        position = (0, 1 + i, 10 + platform_scale*i),
        texture = 'white_cube',
        collider = 'box',
        scale = (platform_scale, 0.5, platform_scale)
    )
    block.speed = uniform(0.5, 0.8)
    block.direction = choice([direction, -direction])
    blocks.append(block)

sky = Sky()

def update():
    moveBlocks()
    walking()
    jumping()


def moveBlocks():
    for block in blocks:
        block.x += block.direction * block.speed
        if block.x >= 10:
            block.direction = -direction
        elif block.x <= -10:
            block.direction = direction

        #check collision with block entitiy and apply movement direction to player.
        ray = raycast(player.position, Vec3(0,-1,0), distance=1, ignore=[player])
        if ray.hit and ray.entity == block:
            player.x += ray.entity.direction * ray.entity.speed

def walking():
    walking = held_keys['a'] or held_keys['s'] or held_keys['d'] or held_keys['w']
    if walking:
        if not player.walk_sound.playing:
            player.walk_sound.play()
    else:
        if player.walk_sound.playing:
           player.walk_sound.stop()

def jumping():
    jumping = held_keys['space']
    if jumping:
        if not player.jump_sound.playing:
            player.jump_sound.play()
    else:
        if player.jump_sound.playing:
            player.jump_sound.stop()

def input(key):
    if(key == "q"):
        quit()

app.run()