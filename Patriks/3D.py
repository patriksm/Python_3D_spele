from random import uniform
from ursina import *
from ursina.prefabs.first_person_controller \
import FirstPersonController

app = Ursina()

ground = Entity(
    model = 'plane',
    texture = 'grass',
    collider = 'mesh',
    scale = (100, 1, 100)
)

siena_prieksa = Entity(
    model = 'cube',
    position = (0, 5, 50),
    scale = (100, 10, 1),
    collider = 'box',
    texture = 'textures\siena_prieksa.jpg', 
    texture_scale=(3.6,0.72),
)

masina = Entity(
    model = 'redCar.glb',
    position = (-40, 0, 10),
    collider = 'box',
    scale = (2, 2, 2),
)

masina = Entity(
    model = 'mapleTree.glb',
    position = (-40, 0, 25),
    collider = 'box',
    scale = (0.1, 0.1, 0.1),
)

bloki = []
directions = []
for i in range(10):
    r = uniform(-2, 2)
    bloks = Entity(
        model = 'cube',
        position = (r, 1 + i, 1 + 5*i),
        texture = 'white_cube',
        collider = 'box',
        scale = (5, 0.5, 5)
    )
    bloki.append(bloks)
    if r < 0: 
        directions.append(1);
    else:
        directions.append(-1)


player = FirstPersonController(
    speed = 15,
    collider = 'box',
    position = (40, 0, -45)
)
player.cursor.visible  = True

sky = Sky()

window.fullscreen = False

walk = Audio(
    'assets\walking.mp3',
    loop = False,
    autoplay = False
)

jump = Audio(
    'assets\jumping.mp3',
    loop = False,
    autoplay = False
)

def update():
    i = 0
    for bloks in bloki:
        bloks.x -= directions[i] * time.dt 
        if abs(bloks.x) > 5:
            directions[i] *= -1
        if bloks.intersects().hit: 
            player.x -= directions[i] * time.dt        
        i += 1

    walking = held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']
    if walking:
        if not walk.playing: 
            walk.play()
    else:
        if walk.playing:
            walk.stop()

def input(key):
    if(key == 'q'):
        quit()
    if(key == 'space'):
        if not jump.playing:
            jump.play()

app.run()