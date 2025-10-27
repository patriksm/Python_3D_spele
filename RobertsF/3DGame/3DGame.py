from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

wall_height = 30
ground_size = 100
wall_texture = 'assets/wall/brick_crosswalk_diff_2k.jpg'

app = Ursina()

ground = Entity(
    model='plane',
    texture='grass',
    collider='mesh',
    scale=(ground_size, 1, ground_size)
)

wall_F = Entity(
    model='cube',
    collider='box',
    position=(0, wall_height/2, ground_size/2),
    scale=(ground_size, wall_height, 1),
    texture=wall_texture,
    texture_scale=(5,2.5)
)

wall_B = Entity(
    model='cube',
    collider='box',
    position=(0, wall_height/2, -ground_size/2),
    scale=(ground_size, wall_height, 1),
    texture=wall_texture,
    texture_scale=(5,2.5)
)

wall_R = Entity(
    model='cube',
    collider='box',
    position=(-ground_size/2, wall_height/2, 0),
    scale=(1, wall_height, ground_size),
    texture=wall_texture,
    texture_scale=(5,2.5)
)

wall_L = Entity(
    model='cube',
    collider='box',
    position=(ground_size/2, wall_height/2, 0),
    scale=(1, wall_height, ground_size),
    texture=wall_texture,
    texture_scale=(5,2.5)
)

player = FirstPersonController(
    height=2
)
player.cursor.visible = True

player.walk_sound = Audio(
    'assets\sound_walking.mp3',
    loop=True,
    autoplay=False,
    volume=.4
)

player.jump_sound = Audio(
    'assets\sound_jump.mp3',
    loop=False,
    autoplay=False,
    volume=.4
)

sky = Sky()

def update():
    walking()
    jumping()

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