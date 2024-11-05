from settings import CHUNK_SIZE, VOXEL_SIZE

class Voxel:
    def __init__(self, chunk_pos = (0, 0, 0), position_in_chunk = (0, 0, 0)):
        self.id: int = None
        self.position_in_chunk = position_in_chunk
        self.world_position = self.get_world_position(chunk_pos)
    
    def get_world_position(self, chunk_position) -> tuple:
        """Get the world position of the voxel."""
        x, y, z = chunk_position
        vx, vy, vz = self.position_in_chunk
        return (x * CHUNK_SIZE + vx, y * CHUNK_SIZE + vy, z * CHUNK_SIZE + vz)
    
    def get_bounding_box(self):
        x, y, z = self.world_position
        return (x, y, z, x + VOXEL_SIZE, y + VOXEL_SIZE, z + VOXEL_SIZE)