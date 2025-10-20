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

def input(key):
    if(key == 'q'):
        quit()

app.run()