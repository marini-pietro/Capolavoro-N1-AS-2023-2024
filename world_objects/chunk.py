import random
from settings import *
from meshes.chunk_mesh import ChunkMesh
from terrain_gen import *
from world_objects.voxel import Voxel

class Chunk:
    def __init__(self, world, position):
        self.engine = world.engine
        self.world = world
        self.position: glm.vec3 = position # Position of the chunk in the world (0, 0, 0) is the top left corner of the world and (0, 0, CHUNK_SIZE) is the one to its right
        self.m_model: glm.mat4x4 = self.get_model_matrix()
        self.voxels: list[Voxel] = [Voxel(position_in_chunk=(x, y, z), chunk_pos=self.position)
                                    for x in range(CHUNK_SIZE)
                                    for y in range(CHUNK_SIZE)
                                    for z in range(CHUNK_SIZE)]
        self.mesh: ChunkMesh = None
        self.is_empty: bool = True

        self.center: glm.vec3 = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum: bool = self.engine.player.frustum.is_on_frustum

    def get_model_matrix(self) -> glm.mat4x4:
        """
        Get the model matrix for the chunk.

        Returns:
            glm.mat4x4: The model matrix for the chunk.
        """

        m_model: glm.mat4x4 = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self) -> None:
        """
        Set the uniform variables for the chunk (model matrix).
        """
        self.mesh.program['m_model'].write(self.m_model) # Write the model matrix to the shader

    def build_mesh(self) -> None:
        self.mesh: ChunkMesh = ChunkMesh(self)

    def render(self) -> None:
        if not self.is_empty and self.is_on_frustum(self): # If the chunk is not empty and is on the frustum
            self.set_uniform() # Update uniform variables (in this case, the model matrix)
            self.mesh.render() # Render the chunk

    def build_voxels(self):
        
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE # Get the world coordinates of the chunk
        self.generate_terrain(self.voxels, cx, cy, cz) # Generate the terrain for the chunk

        if np.any(self.voxels): # If the chunk is not empty
            self.is_empty = False # Set the chunk as not empty

    def get_voxel(self, voxel_pos) -> int:
        """Get the voxel at the given position."""
        for voxel in self.voxels:
            if voxel.position_in_chunk == voxel_pos:
                return voxel
        return None

    def generate_terrain(self, voxels: list[Voxel], cx: int , cy: int, cz: int) -> None:

        for x in range(CHUNK_SIZE):
            wx: int = x + cx
            for z in range(CHUNK_SIZE):
                wz: int = z + cz
                world_height: int = get_height(wx, wz)
                local_height: int = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    set_voxel_id(voxels=voxels, x=x, y=y, z=z, wx=wx, wy=wy, wz=wz, world_height=world_height)
