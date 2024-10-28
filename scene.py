from settings import *
import moderngl as mgl
from world import World
from world_objects.voxel_marker import VoxelMarker
from world_objects.water import Water
from world_objects.clouds import Clouds

class Scene:
    def __init__(self, engine):
        self.engine = engine
        self.world = World(self.engine)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)
        self.water = Water(engine)
        self.clouds = Clouds(engine)

    def update(self):
        self.world.update()
        self.voxel_marker.update()
        self.clouds.update()

    def render(self):
        # Render chunks
        self.world.render()

        # Render clouds and water without face culling because they are not fully opaque (not rendered faces will be visible if we use face culling)
        self.engine.ctx.disable(mgl.CULL_FACE)
        self.clouds.render()
        self.water.render()
        self.engine.ctx.enable(mgl.CULL_FACE) # Renable face culling

        # Voxel Selection Outline
        self.voxel_marker.render()
