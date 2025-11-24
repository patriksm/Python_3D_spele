from ursina.prefabs.health_bar import HealthBar
import random
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController


app = Ursina()

# Configuration
WALL_HEIGHT = 8
GROUND_SIZE = 100
WALL_TEXTURE = 'Bricks052_2K-JPG/Bricks052_2K-JPG_Color.jpg'
PLAYER_SPEED = 20
BLOCK_UPDATE_DISTANCE = 50

random.seed(0)
window.vsync = True


# ======================================================
#  DAMAGE FLOATING TEXT
# ======================================================
class DamageText(Text):
    def __init__(self, value, position):
        super().__init__(
            text=f"-{value}",
            color=color.red,
            position=position,
            scale=10,
            origin=(8, 8),
            world_parent=scene
        )
        self.animate_position(self.position + Vec3(1, 1, 1), duration=1)
        self.fade_out(duration=1)
        destroy(self, delay=1.1)


# ======================================================
#  GUN CLASS
# ======================================================
class Gun(Entity):

    def __init__(self, **kwargs):
        super().__init__(
            parent=camera,
            model='cartoon_rifle.glb',
            position=(.1, -.60, .20),
            rotation=(-8, -10, 0),
            scale=.1,
            color=color.gold,
            flip_faces=True,
            **kwargs
        )

        self.on_cooldown = False
        self.cooldown_time = 0.12
        self.recoil_amount = 4

        # store original rotation_z so we can reset recoil cleanly
        self._orig_rotation_z = self.rotation_z

        # Barrel offset relative to gun model
        self.barrel_offset = Vec3(0.9, 0.9, 2)

        self.muzzle_flash = Entity(
            parent=self,
            model='quad',
            color=color.yellow,
            world_scale=0.45,
            enabled=False,
            position=self.barrel_offset
        )

        # simple Audio-based gunshot
        self.gunshot = Audio('single-gunshot-54-40780.mp3',
                             volume=0.8, autoplay=False)

    # ----------------------------------------------
    # SHOOT
    # ----------------------------------------------
    def shoot(self):

        if self.on_cooldown:
            return

        self.on_cooldown = True

        # Sound
        if self.gunshot:  # play if available
            try:
                self.gunshot.play()
            except Exception:
                pass

        # Flash
        self.muzzle_flash.enabled = True
        invoke(self.muzzle_flash.disable, delay=0.05)

        # Recoil (random horizontal kick)
        self.rotation_z += random.uniform(-self.recoil_amount,
                                          self.recoil_amount)
        # reset to original rotation after short delay
        invoke(lambda: setattr(self, 'rotation_z',
               self._orig_rotation_z), delay=0.1)

        # Raycast from the gun barrel (use world_position + offsets)
        barrel_world = self.world_position + self.up * \
            self.barrel_offset.y + self.forward * self.barrel_offset.z
        hit = raycast(camera.world_position, camera.forward,
                      distance=200, ignore=(player, gun))

        if hit.hit and hasattr(hit.entity, "hp"):
            hit.entity.hp -= 10

        invoke(self._reset_cooldown, delay=self.cooldown_time)

    def _reset_cooldown(self):
        self.on_cooldown = False


# ======================================================
#  WORLD ENTITIES
# ======================================================
shootables_parent = Entity()
mouse.traverse_target = shootables_parent

# --- Audio ---
walk = Audio('walking-sound-effect.mp3', volume=1, autoplay=False, loop=False)
jump_sound = Audio('jumplanding.mp3', volume=1, autoplay=False, loop=False)
hit_sound = Audio('080998_bullet-hit-39870.mp3',
                  volume=0.6, autoplay=False, loop=False)

# --- Ground ---
ground = Entity(
    model='plane',
    texture='Grass008_2K-JPG/Grass008_2K-JPG_Color.jpg',
    collider='mesh',
    scale=(GROUND_SIZE, 1, GROUND_SIZE),
    texture_scale=(GROUND_SIZE/5, GROUND_SIZE/5)
)

# --- Car ---
car = Entity(
    model='transformers_rotf_psp_ratchet.glb',
    position=(-40, 0.3, -16),
    rotation=(0, 88, 0),
    collider='box',
    scale=(1, .9, 1)
)
# --- Text ---
msg = Text(
    scale=2,
    position=(-0.9, 0.5)
)

# --- Trees ---
trees = []
for pos in [(39, 0, 39), (-39, 0, -39), (39, 0, -39), (-39, 0, 39)]:
    trees.append(Entity(
        model='linden_tree.glb',
        position=pos,
        scale=(3, 2, 3),
        collider=None
    ))
trees = []
for pos in [(25, 0, 43), (-23, 0, -43), (20, 0, -43), (-22, 0, 43)]:
    trees.append(Entity(
        model='spruce_trees.glb',
        position=pos,
        scale=(.4, .4, .4),
        collider=None
    ))
trees = []
for pos in [(21, 0, 25), (-18, 0, -33), (15, 0, -33), (-18, 0, 33)]:
    trees.append(Entity(
        model='blue_spruce_tree.glb',
        position=pos,
        scale=(1, 1, 1),
        collider=None
    ))
trees = []
for pos in [(-48, 0, -9), (-33, 0, -33), (-42, 0, -9), (-38, 0, -9), (-34, 0, -9)]:
    trees.append(Entity(
        model='real_bush.glb',
        position=pos,
        scale=(.03, .02, .03),
        collider=None
    ))
trees = []
for pos in [(-44, 0, 12), (-35, 0, -4), (-40, 0, 4), (-25, 0, 6), (-25, 0, 20)]:
    trees.append(Entity(
        model='pine_tree.glb',
        position=pos,
        scale=(5, 4, 5),
        collider=None
    ))
trees = []
for pos in [(-44, 0, -4), (-44, 0, 20), (-32, 0, 12), (-35, 0, 20), (-25, 0, -7)]:
    trees.append(Entity(
        model='birch_tree.glb',
        position=pos,
        scale=(3, 2, 3),
        collider=None
    ))


house = Entity(
    model='wooden_cottage_house_psx.glb',
    position=(-30, 0, -26),
    collider=None,
    scale=(70, 50, 70)
)

# --- Moving Blocks ---
blocks = []
block_dirs = []

for i in range(9):
    b = Entity(
        model='cube',
        position=(8, 1 + i, 8 + 5 * i),
        texture='white_cube',
        collider='box',
        scale=(5, 0.5, 5)
    )
    blocks.append(b)

    # block movement direction (left/right)
    block_dirs.append(random.uniform(-0.03, 0.03))

# --- Walls ---
half = GROUND_SIZE / 2
wall_thickness = 1
walls = [
    Entity(model='cube', position=(0, WALL_HEIGHT/2, -half),
           scale=(GROUND_SIZE, WALL_HEIGHT, wall_thickness),
           collider='box', texture=WALL_TEXTURE, texture_scale=(30, 2.5)),
    Entity(model='cube', position=(0, WALL_HEIGHT/2, half),
           scale=(GROUND_SIZE, WALL_HEIGHT, wall_thickness),
           collider='box', texture=WALL_TEXTURE, texture_scale=(30, 2.5)),
    Entity(model='cube', position=(-half, WALL_HEIGHT/2, 0),
           scale=(wall_thickness, WALL_HEIGHT, GROUND_SIZE),
           collider='box', texture=WALL_TEXTURE, texture_scale=(30, 2.5)),
    Entity(model='cube', position=(half, WALL_HEIGHT/2, 0),
           scale=(wall_thickness, WALL_HEIGHT, GROUND_SIZE),
           collider='box', texture=WALL_TEXTURE, texture_scale=(30, 2.5))
]

# --- Extra Blocks ---
for i in range(25):
    Entity(
        model='cube',
        origin_y=-.4,
        scale=2,
        texture='brick',
        texture_scale=(3, 4),
        x=random.uniform(-16, 35),
        z=random.uniform(-13, 35) - 30,
        collider='box',
        scale_y=random.uniform(3, 4),
        color=color.hsv(0, 0, random.uniform(.9, 1))
    )


player = FirstPersonController(speed=PLAYER_SPEED, position=(0, 0, -30))
player.cursor.visible = True
editor_camera = EditorCamera(enabled=False, ignore_paused=True)

# --- Skybox ---
skybox = Entity(
    model='sphere',
    texture='NightSkyHDRI008_4K/NightSkyHDRI008_4K_TONEMAPPED.jpg',
    scale=1000,
    double_sided=True,
    rotation=(0, 180, 0)
)

gun = Gun()

was_on_ground = player.grounded


# ======================================================
#  ENEMY CLASS
# ======================================================
class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=shootables_parent,
            position=pos,
            model='cube',
            scale_y=.1,
            origin_y=-.1,
            color=color.light_gray,
            collider='box',
            **kwargs
        )
        self.health_bar = Entity(
            parent=self,
            y=1.2,
            model='cube',
            color=color.red,
            world_scale=(.1, .1, .1)
        )
        self.max_hp = 100
        self._hp = self.max_hp
        self.hp = self.max_hp
        self.destroyed = False

    def update(self):
        if self.destroyed:
            return

        dist = distance_xz(player.position, self.position)
        if dist > BLOCK_UPDATE_DISTANCE:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)
        self.look_at_2d(player.position, 'y')

        hit_info = raycast(self.world_position + Vec3(0, 1, 0),
                           self.forward, 30, ignore=(self,))
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 3

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        damage = self._hp - value
        self._hp = value

        if damage > 0:
            DamageText(damage, self.world_position + Vec3(0, 2.5, 0))
            original_color = self.color
            self.color = color.white
            hit_sound.play()
            invoke(lambda: setattr(self, 'color', original_color), delay=0.1)

        if value <= 0:
            self.destroyed = True
            self.collider = None
            self.enabled = False
            destroy(self, delay=.05)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


# Spawn Enemies
enemies = [Enemy(x=x * 4) for x in range(4)]


# ======================================================
#  UPDATE LOOP
# ======================================================

def update():
    for i, block in enumerate(blocks):

        # --- Move block ---
        block.x += block_dirs[i]

        # reverse direction at limits
        if block.x > 5:
            block_dirs[i] = -abs(block_dirs[i])
        if block.x < -5:
            block_dirs[i] = abs(block_dirs[i])

        # --- Check if player is standing on block ---
        on_top = (
            abs(player.x - block.x) < block.scale_x/2 and
            abs(player.z - block.z) < block.scale_z/2 and
            abs(player.y - (block.y + 0.3)) < 0.4
        )

        if on_top and player.grounded:
            # move player together with block
            player.x += block_dirs[i]

    msg.text = f"Youre position is: x = {int(player.x)}, y = {int(player.y)}, z = {int(player.z)}"

    # Walking sound
    walking = held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']
    if walking and player.grounded and not walk.playing:
        walk.play()
    elif (not walking or not player.grounded) and walk.playing:
        walk.stop()

    if player.grounded and not was_on_ground:
        jump_sound.play()

    # Shooting
    if held_keys['left mouse']:
        gun.shoot()


# ======================================================
#  PAUSE
# ======================================================
def pause_input(key):
    if key == 'tab':
        editor_camera.enabled = not editor_camera.enabled
        player.visible_self = editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        gun.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position
        application.paused = editor_camera.enabled


pause_handler = Entity(ignore_paused=True, input=pause_input)


def input(key):
    if key == 'q':
        quit()


app.run()
