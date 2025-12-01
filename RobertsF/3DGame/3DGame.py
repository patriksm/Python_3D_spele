from random import choice, uniform
from ursina import *
from classes.Gun import Gun
from classes.Environment import Environment
from classes.Player import Player
from classes.GameFunctions import GameFunctions
from classes.Ufo import Ufo

direction = 0.06
platform_scale = 3
destroyed_targets_count = 0

app = Ursina()

blocks = []
for i in range(7):
    block = Entity(
        model = 'cube',
        position = (0, 1.1 + i, 10 + platform_scale*i),
        texture = "assets/floor/weathered_planks_diff_2k.jpg",
        collider = 'box',
        scale = (platform_scale, 0.5, platform_scale),
        texture_scale=(1, 1)
    )
    block.speed = uniform(0.5, 0.8)
    block.direction = choice([direction, -direction])
    blocks.append(block)


message = Text(
        text=f"Targets destroyed: {destroyed_targets_count}",
        scale=1,
        font='assets/font/Game_Font.ttf',
        position = (-.88, .47)
    )

environment = Environment()
player = Player()
game_functions = GameFunctions(player=player, blocks=blocks, environment=environment, message=message)
game_functions.spawn_targets()

gun = Gun(parent=camera)

cow = Entity(
    model="/assets/models/cow.glb",
    position=(30, 0, 5),
    scale=1.5,
    rotation=(0, 180, 0),
    collider='mesh'
)

def update():
    environment.update()
    gun.shooting()
    game_functions.moveBlocks()
    player.set_walking()
    player.set_jumping()

def input(key):
    if(key == "q"):
        quit()

app.run()