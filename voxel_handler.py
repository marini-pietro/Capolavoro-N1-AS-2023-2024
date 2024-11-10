from settings import *
from meshes.chunk_mesh_builder import get_chunk_index

class VoxelHandler:
    def __init__(self, world):
        self.world = world
        self.engine = world.engine
        self.chunks = world.chunks

        # Variables to handle ray casting results
        self.chunk = None
        self.voxel_id = None
        self.voxel_index = None
        self.voxel_local_pos = None
        self.voxel_world_pos = None
        self.voxel_normal = None

        self.interaction_mode = 0  # 0: remove voxel   1: add voxel
        self.new_voxel_id = DIRT

    def add_voxel(self):
        if self.voxel_id:
            # check voxel id along normal
            result = self.get_voxel_info(self.voxel_world_pos + self.voxel_normal)

            # is the new place empty?
            if not result[0]:
                _, voxel_index, _, chunk = result
                chunk.voxels[voxel_index] = self.new_voxel_id
                chunk.mesh.rebuild()

                # was it an empty chunk
                if chunk.is_empty:
                    chunk.is_empty = False

    def rebuild_chunk(self, adj_voxel_pos):
        """Rebuild a chunk based identified by the a voxel position."""
        index = get_chunk_index(adj_voxel_pos) # Get chunk index
        if index != -1: # If chunk exists
            self.chunks[index].mesh.rebuild() # Rebuild mesh

    def rebuild_adjacent_chunks(self):
        lx, ly, lz = self.voxel_local_pos
        wx, wy, wz = self.voxel_world_pos

        if lx == 0:
            self.rebuild_chunk((wx - 1, wy, wz))
        elif lx == CHUNK_SIZE - 1:
            self.rebuild_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_chunk((wx, wy - 1, wz))
        elif ly == CHUNK_SIZE - 1:
            self.rebuild_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_chunk((wx, wy, wz - 1))
        elif lz == CHUNK_SIZE - 1:
            self.rebuild_chunk((wx, wy, wz + 1))

    def remove_voxel(self):
        """Remove a voxel from the world."""
        if self.voxel_id: # If voxel exists
            self.chunk.voxels[self.voxel_index] = 0 # Set voxel to air

            self.chunk.mesh.rebuild() # Rebuild mesh
            self.rebuild_adjacent_chunks() # Rebuild adjacent chunks

    def set_voxel(self):
        """Set a voxel in the world."""	
        if self.interaction_mode: # If interaction mode is set to add voxel
            self.add_voxel() # Add voxel
        else: # If interaction mode is set to remove voxel
            self.remove_voxel() # Remove voxel

    def switch_mode(self):
        """Switch between add and remove voxel mode."""
        self.interaction_mode = not self.interaction_mode # Switch mode

    def update(self):
        self.ray_cast()

    def ray_cast(self):
        """Ray casting algorithm to find the voxel the player is looking at."""
        # Start point of the ray
        x1, y1, z1 = self.engine.player.position # Player position
        # End point of the ray
        x2, y2, z2 = self.engine.player.position + self.engine.player.forward * MAX_RAY_DIST # Player position + forward vector * max ray distance

        current_voxel_pos = glm.ivec3(x1, y1, z1) # Current voxel position
        self.voxel_id = 0 # Voxel id
        self.voxel_normal = glm.ivec3(0) # Voxel normal
        step_dir = -1 

        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):

            result = self.get_voxel_info(voxel_world_pos=current_voxel_pos)
            if result[0]:
                self.voxel_id, self.voxel_index, self.voxel_local_pos, self.chunk = result
                self.voxel_world_pos = current_voxel_pos

                if step_dir == 0:
                    self.voxel_normal.x = -dx
                elif step_dir == 1:
                    self.voxel_normal.y = -dy
                else:
                    self.voxel_normal.z = -dz
                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_voxel_pos.x += dx
                    max_x += delta_x
                    step_dir = 0
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
            else:
                if max_y < max_z:
                    current_voxel_pos.y += dy
                    max_y += delta_y
                    step_dir = 1
                else:
                    current_voxel_pos.z += dz
                    max_z += delta_z
                    step_dir = 2
        return False

    def get_voxel_info(self, voxel_world_pos) -> tuple:
        """Get the voxel id of a voxel in the world."""
        cx, cy, cz = chunk_pos = voxel_world_pos / CHUNK_SIZE # Get chunk position

        if 0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D: # If chunk position is within world dimensions
            chunk_index = cx + WORLD_W * cz + WORLD_AREA * cy # Get chunk index
            chunk = self.chunks[chunk_index] # Get chunk

            lx, ly, lz = voxel_local_pos = voxel_world_pos - chunk_pos * CHUNK_SIZE # Get voxel local position

            voxel_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly # Get voxel index
            voxel_id = chunk.voxels[voxel_index] # Get voxel id

            return voxel_id, voxel_index, voxel_local_pos, chunk
        return 0, 0, 0, 0
