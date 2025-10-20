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

player = FirstPersonController(

)
player.cursor.visible  = True

sky = Sky()

window.fullscreen = True

walk = Audio(
    'assets\walking.mp3',
    loop = False,
    autoplay = False
)

def update():
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

app.run()