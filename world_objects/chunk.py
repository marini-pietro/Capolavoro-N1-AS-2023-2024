import random
from settings import *
from meshes.chunk_mesh import ChunkMesh
from terrain_gen import *

class Chunk:
    def __init__(self, world, position):
        self.engine = world.engine
        self.world = world
        self.position: glm.vec3 = position
        self.m_model: glm.mat4x4 = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty: bool = True

        self.center: glm.vec3 = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum: bool = self.engine.player.frustum.is_on_frustum

    def get_model_matrix(self):
        """
        Get the model matrix for the chunk.

        Returns:
            glm.mat4x4: The model matrix for the chunk.
        """

        m_model: glm.mat4x4 = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        """
        Set the uniform variables for the chunk (model matrix).
        """
        self.mesh.program['m_model'].write(self.m_model)

    def build_mesh(self):
        self.mesh: ChunkMesh = ChunkMesh(self)

    def render(self):
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        voxels = np.zeros(CHUNK_VOL, dtype='uint8')

        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE
        self.generate_terrain(voxels, cx, cy, cz)

        if np.any(voxels):
            self.is_empty = False
        return voxels

    @staticmethod
    @njit
    def generate_terrain(voxels, cx, cy, cz):
        for x in range(CHUNK_SIZE):
            wx = x + cx
            for z in range(CHUNK_SIZE):
                wz = z + cz
                world_height = get_height(wx, wz)
                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)
