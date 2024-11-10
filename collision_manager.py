from settings import CHUNK_SIZE
import glm

class CollisionManager:
    def __init__(self, size, engine, detection_radius):
        self.size = size
        self.detect_radius = detection_radius
        self.engine = engine

    def check_collision(self, desired_position) -> bool: #TODO: Finish this function
        bounding_box = self.get_bounding_box(desired_position = desired_position) # Get the bounding box the player would have if it moved to the desired position
        current_chunk = self.engine.scene.world.get_chunk(self.get_chunk_coordinates(position = desired_position)) # Get the chunk the player is in
        surrounding_voxels = self.get_surrounding_voxels(chunk=current_chunk, position=desired_position) # Get the surrounding voxels of the player
        
        for voxel in surrounding_voxels: # For each voxel in the surrounding voxels
            voxel_bounding_box = voxel.get_bounding_box()
            if self.is_colliding(bounding_box, voxel_bounding_box): 
                print("Collision detected")
                return True

        return False
    
    def get_surrounding_voxels(self, chunk, position) -> list:
        """Get the surrounding voxels of the entity."""
        x, y, z = position
        voxels = []
        for i in range(-self.detect_radius, self.detect_radius):
            for j in range(-self.detect_radius, self.detect_radius):
                for k in range(-self.detect_radius, self.detect_radius): 
                    voxel = chunk.get_voxel((x + i, y + j, z + k)) # Get the voxel at the given position
                    if voxel: voxels.append(voxel) # If the voxel is not empty, add it to the list
        return voxels

    def is_colliding(self, box1, box2) -> bool: 
        """Check if two bounding boxes are colliding."""	
        x1_min, y1_min, z1_min, x1_max, y1_max, z1_max = box1
        x2_min, y2_min, z2_min, x2_max, y2_max, z2_max = box2
        return (x1_min < x2_max and x1_max > x2_min and
                y1_min < y2_max and y1_max > y2_min and
                z1_min < z2_max and z1_max > z2_min)

    def get_chunk_coordinates(self, position) -> glm.vec3:
        """Get the chunk coordinates the entity is in."""
        x, y, z = position
        chunk_x: int = int(x // CHUNK_SIZE)
        chunk_y: int = int(y // CHUNK_SIZE)
        chunk_z: int = int(z // CHUNK_SIZE)
        return glm.vec3(chunk_x, chunk_y, chunk_z)
    
    def get_bounding_box(self, desired_position) -> tuple:
        """Get the bounding box of the player."""
        x, y, z = desired_position
        w, h, d = self.size
        return (x, y, z, x + w, y + h, z + d)