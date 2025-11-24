
from ursina import *
from classes.Bullet import Bullet

def_position = Vec3(.4, -.35, .7)
def_rotation = Vec3(0, -180, 0)

class Gun(Entity):
    def __init__(self, parent):
        super().__init__(
            model="/assets/models/gun.glb",
            parent = parent,
            position = def_position,
            rotation = def_rotation,
            scale= .001
        )
        self.shooting = False
    
    def set_recoil(self):
        self.shooting = True
        self.animate_rotation(Vec3(5, -180, 0), 0.01)
        self.animate_position(Vec3(.4, -.35, .65), 0.01)
        self.set_ammo_particle()
        invoke(self.reset_recoil, delay = .15)
        print('Ow! That hurt!')
    
    def reset_recoil(self):
        self.animate_position(def_position, 0.05)
        self.animate_rotation(def_rotation, 0.01)
        self.shooting = False

    def set_ammo_particle(self):
        Bullet(parent=self, position=Vec3(-75, 200, -500))

