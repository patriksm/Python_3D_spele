from ursina import *

class Bullet(Entity):
    def __init__(self, parent, position):
        super().__init__(
            parent = parent,
            model = Cylinder(resolution=16, radius=0.5, height=1, direction=(0,0,1)),
            color = color.hex("#30a8db"),
            position = position,
            rotation = (0, 0, 0),
            scale=50
        )
        self.world_parent = scene

        # Cast a ray from the camera to the cursor
        hit_info = raycast(camera.world_position, camera.forward, distance=1000, ignore=[self, parent])
        if mouse.hovered_entity:
            target_point = mouse.world_point
        elif hit_info.hit:
            target_point = hit_info.point 
        else: # if nothing is hit - set target to very far positioned camera
            target_point = camera.world_position + camera.forward * 1000

        self.velocity = (target_point - self.position).normalized() * 20 
        invoke(destroy, self, delay=2)

    def find_target(self):
        hit_info = mouse.hovered_entity
        return hit_info if hit_info else None

    def update(self):
        self.position += self.velocity * time.dt