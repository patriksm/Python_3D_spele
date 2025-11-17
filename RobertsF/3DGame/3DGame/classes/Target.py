from ursina import *

class Target(Entity):
    def __init__(self, x, y, z):
        super().__init__(
            model='cube',
            color = color.gold,
            parent = scene,
            texture = 'white_cube',
            scale = (1, 2, 1), 
            position = (x, y, z),
            collider = 'mesh'
        )