from random import uniform
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# --- Settings ---
wall_height = 6
ground_size = 120
wall_texture = 'Bricks052_2K-JPG/Bricks052_2K-JPG_Color.jpg'

# --- Audio ---
walk = Audio('walking-sound-effect.mp3', volume=1, autoplay=False, loop=False)
jump_sound = Audio('jumplanding.mp3', volume=1, autoplay=False, loop=False)

# --- Ground ---
ground = Entity(
    model='plane',
    texture='Grass008_2K-JPG/Grass008_2K-JPG_Color.jpg',
    collider='mesh',
    scale=(ground_size, 1, ground_size),
    texture_scale=(ground_size/5, ground_size/5)
)

# --- Car ---
car = Entity(
    model='transformers_rotf_psp_ratchet.glb',
    position=(-10, 0.3, -10),
    collider='box',
    scale=(1, 1, 1)
)

# --- Tree ---
tree = Entity(
    model='linden_tree.glb',
    position=(39, 0, 39),
    collider='box',
    scale=(3, 2, 1),
)

# --- House ---
house = Entity(
    model='wooden_cottage_house_psx.glb',
    position=(-20, 0, -25),
    collider='box',
    scale=(70, 50, 70),
)

# --- Moving Blocks ---
blocks = []
dirs = []
for i in range(10):
    b = Entity(
        model='cube',
        position=(10, 1 + i, 10 + 5*i),
        texture='white_cube',
        collider='box',
        scale=(5, 0.5, 5)
    )
    blocks.append(b)
    dirs.append(uniform(-1, 1))

# --- Walls ---
half = ground_size / 2
wall_thickness = 1
walls = [
    Entity(model='cube', position=(0, wall_height/2, -half),
           scale=(ground_size, wall_height, wall_thickness),
           collider='box', texture=wall_texture, texture_scale=(30, 2.2)),
    Entity(model='cube', position=(0, wall_height/2, half),
           scale=(ground_size, wall_height, wall_thickness),
           collider='box', texture=wall_texture, texture_scale=(30, 2.2)),
    Entity(model='cube', position=(-half, wall_height/2, 0),
           scale=(wall_thickness, wall_height, ground_size),
           collider='box', texture=wall_texture, texture_scale=(30, 2.2)),
    Entity(model='cube', position=(half, wall_height/2, 0),
           scale=(wall_thickness, wall_height, ground_size),
           collider='box', texture=wall_texture, texture_scale=(30, 2.2))
]

# --- Player ---
player = FirstPersonController(speed=20)
player.cursor.visible = False
editor_camera = EditorCamera(enabled=False, ignore_paused=True)

# --- Custom Sky ---
skybox = Entity(
    model='sphere',
    texture='NightSkyHDRI008_4K/NightSkyHDRI008_4K_TONEMAPPED.jpg',
    scale=1000,
    double_sided=True

)
window.fullscreen = False

# --- Jump Tracking ---
was_on_ground = player.grounded


# --- Update Loop ---
def update():
    global was_on_ground

    # Move blocks
    for i, b in enumerate(blocks):
        b.x += dirs[i] * time.dt * 3
        if b.x > 15 or b.x < 5:
            dirs[i] *= -1

    # Walking sound
    walking = held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']
    if walking and player.grounded and not walk.playing:
        walk.play()
    elif (not walking or not player.grounded) and walk.playing:
        walk.stop()

    # Landing sound
    if player.grounded and not was_on_ground:
        jump_sound.play()

    was_on_ground = player.grounded


# --- Input Handling ---
def input(key):
    if key == 'q':
        quit()


# --- Start the app ---
app.run()
