from ursina.prefabs.health_bar import HealthBar
from random import uniform
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

app = Ursina()

# --- Settings ---
wall_height = 8
ground_size = 100
wall_texture = 'Bricks052_2K-JPG/Bricks052_2K-JPG_Color.jpg'
random.seed(0)
Entity.default_shader = lit_with_shadows_shader

# --- Camera & Player ---
editor_camera = EditorCamera(enabled=False, ignore_paused=True)
player = FirstPersonController()

gun = Entity(
    model='cube',
    parent=camera,
    position=(.5, -.25, .25),
    scale=(.3, .2, 1),
    origin_z=-.5,
    color=color.red,
    on_cooldown=False
)

gun.muzzle_flash = Entity(
    parent=gun,
    z=1,
    world_scale=.5,
    model='quad',
    color=color.yellow,
    enabled=False
)

shootables_parent = Entity()
mouse.traverse_target = shootables_parent

# --- Audio ---
walk = Audio('walking-sound-effect.mp3', volume=1, autoplay=False, loop=False)
jump_sound = Audio('jumplanding.mp3', volume=1, autoplay=False, loop=False)
hit_sound = Audio('thud.mp3', volume=0.6, autoplay=False,
                  loop=False)  # <-- new sound

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
    position=(-20, 0.3, 18),
    collider='box',
    scale=(1, 1, 1)
)

# --- Trees ---
trees = []
for pos in [(39, 0, 39), (-39, 0, -39), (39, 0, -39), (-39, 0, 39)]:
    trees.append(Entity(
        model='linden_tree.glb',
        position=pos,
        collider='box',
        scale=(3, 2, 3)
    ))

# --- House ---
house = Entity(
    model='wooden_cottage_house_psx.glb',
    position=(-20, 0, 0),
    collider='box',
    scale=(70, 50, 70)
)

# --- Moving Blocks ---
blocks = []
dirs = []
for i in range(10):
    r = uniform(-2, 2)
    b = Entity(
        model='cube',
        position=(8, 1 + i, 8 + 5 * i),
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
           collider='box', texture=wall_texture, texture_scale=(30, 2.5)),
    Entity(model='cube', position=(0, wall_height/2, half),
           scale=(ground_size, wall_height, wall_thickness),
           collider='box', texture=wall_texture, texture_scale=(30, 2.5)),
    Entity(model='cube', position=(-half, wall_height/2, 0),
           scale=(wall_thickness, wall_height, ground_size),
           collider='box', texture=wall_texture, texture_scale=(30, 2.5)),
    Entity(model='cube', position=(half, wall_height/2, 0),
           scale=(wall_thickness, wall_height, ground_size),
           collider='box', texture=wall_texture, texture_scale=(30, 2.5))
]

# --- Extra Blocks ---
for i in range(25):
    Entity(
        model='cube',
        origin_y=-.4,
        scale=2,
        texture='brick',
        texture_scale=(3, 4),
        x=uniform(-16, 35),
        z=uniform(-13, 35) - 30,
        collider='box',
        scale_y=uniform(3, 4),
        color=color.hsv(0, 0, uniform(.9, 1))
    )

# --- Player ---
player = FirstPersonController(speed=20)
player.cursor.visible = False
editor_camera = EditorCamera(enabled=False, ignore_paused=True)

# --- Skybox ---
skybox = Entity(
    model='sphere',
    texture='NightSkyHDRI008_4K/NightSkyHDRI008_4K_TONEMAPPED.jpg',
    scale=1000,
    double_sided=True,
    rotation=(0, 180, 0)
)

window.fullscreen = True
was_on_ground = player.grounded


# --- Floating Damage Indicator ---
class DamageText(Text):
    def __init__(self, value, position):
        super().__init__(
            text=f"-{value}",
            color=color.red,
            position=position,
            scale=30,
            origin=(0, 0),
            world_parent=scene
        )
        self.animate_position(self.position + Vec3(0, 1, 0), duration=1)
        self.fade_out(duration=1)
        destroy(self, delay=1.1)


# --- Enemy Class ---
class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent=shootables_parent,
            model='cube',
            scale_y=2,
            origin_y=-.5,
            color=color.light_gray,
            collider='box',
            **kwargs
        )
        self.health_bar = Entity(
            parent=self,
            y=1.2,
            model='cube',
            color=color.red,
            world_scale=(1.5, .1, .1)
        )
        self.max_hp = 100
        self._hp = self.max_hp
        self.hp = self.max_hp

    def update(self):
        dist = distance_xz(player.position, self.position)
        if dist > 40:
            return
        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)
        self.look_at_2d(player.position, 'y')

        hit_info = raycast(self.world_position + Vec3(0, 1, 0),
                           self.forward, 30, ignore=(self,))
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        damage = self._hp - value
        self._hp = value

        if damage > 0:
            # Floating damage indicator
            DamageText(damage, self.world_position + Vec3(0, 2.5, 0))
            # White flash + thud sound
            original_color = self.color
            self.color = color.white
            hit_sound.play()  # <--- Play thud on hit
            invoke(setattr, self, 'color', original_color, delay=0.1)

        if value <= 0:
            destroy(self)
            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1


# --- Enemies ---
enemies = [Enemy(x=x * 4) for x in range(4)]


# --- Shooting ---
def shoot():
    if not gun.on_cooldown:
        gun.on_cooldown = True
        gun.muzzle_flash.enabled = True
        gun.rotation_z = random.uniform(-5, 5)

        from ursina.prefabs.ursfx import ursfx
        ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75),
               (0.3, 0.14), (0.6, 0.0)], volume=0.5,
              wave='noise', pitch=random.uniform(-13, -12),
              pitch_change=-12, speed=3.0)

        invoke(gun.muzzle_flash.disable, delay=.05)
        invoke(lambda: setattr(gun, 'rotation_z', 0), delay=.1)
        invoke(setattr, gun, 'on_cooldown', False, delay=.15)

        if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
            mouse.hovered_entity.hp -= 10
            mouse.hovered_entity.blink(color.red)


# --- Update Loop ---
def update():
    global was_on_ground

    # Moving blocks
    for i, b in enumerate(blocks):
        b.x += dirs[i] * time.dt * 3
        if b.x > 15 or b.x < 5:
            dirs[i] *= -1
        if b.intersects().hit:
            dirs[i] *= -1
            player.y += 5 * time.dt

    # Walking sound
    walking = held_keys['a'] or held_keys['d'] or held_keys['w'] or held_keys['s']
    if walking and player.grounded and not walk.playing:
        walk.play()
    elif (not walking or not player.grounded) and walk.playing:
        walk.stop()

    # Jump/Land sound
    if player.grounded and not was_on_ground:
        jump_sound.play()  # Landing
    elif not player.grounded and was_on_ground:
        jump_sound.play()  # Jumping

    was_on_ground = player.grounded

    # Shooting
    if held_keys['left mouse']:
        shoot()


# --- Pause ---
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


# --- Quit ---
def input(key):
    if key == 'q':
        quit()


app.run()
