from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# --- Settings ---
wall_height = 6
ground_size = 40
# make sure the file exists!
wall_texture = 'rough_plaster_brick_02_2k.blend/textures/rough_plaster_brick_02_diff_2k.jpg'


# --- Audio ---
walk = Audio('walking-sound-effect.mp3', volume=1, autoplay=False, loop=False)
jump = Audio('jumplanding.mp3', volume=1, autoplay=False, loop=False)

# --- Ground ---
ground = Entity(
    model='plane',
    texture='grass',
    collider='mesh',
    scale=(ground_size, 1, ground_size)
)

# --- Walls ---
half = ground_size / 2
wall_thickness = 1

walls = [
    # Front wall (in front of the player, so negative Z)
    Entity(model='cube', position=(0, wall_height/2, -half),
           scale=(ground_size, wall_height, wall_thickness),
           collider='box', texture=wall_texture, texture_scale=(5, 2)),

    # Back wall
    Entity(model='cube', position=(0, wall_height/2, half),
           scale=(ground_size, wall_height, wall_thickness),
           collider='box', texture=wall_texture, texture_scale=(5, 2)),

    # Left wall
    Entity(model='cube', position=(-half, wall_height/2, 0),
           scale=(wall_thickness, wall_height, ground_size),
           collider='box', texture=wall_texture, texture_scale=(5, 2)),

    # Right wall
    Entity(model='cube', position=(half, wall_height/2, 0),
           scale=(wall_thickness, wall_height, ground_size),
           collider='box', texture=wall_texture, texture_scale=(5, 2)),
]

# --- Player ---
player = FirstPersonController(speed=15)
player.cursor.visible = False

# --- Sky ---
sky = Sky()
skybox = Entity(
    model='eclipse_skybox',
    texture='eclipse_skybox_texture',
    scale=100,
    double_sided=True
)


window.fullscreen = False

# --- Update ---


def update():
    walking = held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']
    if walking:
        if not walk.playing:
            walk.play()
    else:
        if walk.playing:
            walk.stop()

# --- Input ---


def input(key):
    if key == 'q':
        quit()
    elif key == 'space':
        jump.play()


app.run()
