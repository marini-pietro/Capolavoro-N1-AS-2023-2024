from settings import *
from world_objects.chunk import Chunk
from voxel_handler import VoxelHandler

class World:
    def __init__(self, engine):
        self.engine = engine
        self.chunks = [None for _ in range(WORLD_VOL)]
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8')
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def update(self):
        self.voxel_handler.update()

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # put the chunk voxels in a separate array
                    self.voxels[chunk_index] = chunk.build_voxels()

                    # get pointer to voxels
                    chunk.voxels = self.voxels[chunk_index]

    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def get_voxel_bounds(self, world_x, world_y, world_z) -> tuple:
        """
        Get the voxel bounding box for the given world position.
        """
        chunk_x, voxel_x = divmod(int(world_x), CHUNK_SIZE)
        chunk_y, voxel_y = divmod(int(world_y), CHUNK_SIZE)
        chunk_z, voxel_z = divmod(int(world_z), CHUNK_SIZE)

        chunk_index = chunk_x + WORLD_W * chunk_z + WORLD_AREA * chunk_y
        chunk = self.chunks[chunk_index]

        return chunk.get_voxel_bound_box(voxel_x, voxel_y, voxel_z)

    def render(self):
        for chunk in self.chunks:
            chunk.render()
    
    def get_voxel_id(self, voxel_world_pos):
        """Get the voxel id of a voxel in the world."""
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE  # Get chunk position

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D:  # If chunk position is within world dimensions
            chunk_index = int(cx) + WORLD_W * int(cz) + WORLD_AREA * int(cy)  # Get chunk index
            chunk = self.chunks[chunk_index]  # Get chunk

            lx, ly, lz = voxel_world_pos - chunk_pos * CHUNK_SIZE  # Get voxel local position

            voxel_index = int(lx) + CHUNK_SIZE * int(lz) + CHUNK_AREA * int(ly)  # Get voxel index
            voxel_id = chunk.voxels[voxel_index]  # Get voxel id

            return voxel_id
        return 0
