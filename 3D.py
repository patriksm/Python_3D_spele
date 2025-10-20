from ursina import *
from ursina.prefabs.first_person_controller \
import FirstPersonController

app = Ursina()

player = FirstPersonController(

)

sky = Sky()

window.fullscreen = True

def input(key):
    if(key == 'q'):
        quit()

app.run()