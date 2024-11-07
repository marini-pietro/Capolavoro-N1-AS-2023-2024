from noise import noise2, noise3
from random import random
from world_objects.voxel import Voxel
from settings import *

@njit
def get_height(x, z) -> int:
    # island mask
    island = 1 / (pow(0.0025 * math.hypot(x - CENTER_XZ, z - CENTER_XZ), 20) + 0.0001)
    island = min(island, 1)

    # amplitude
    a1 = CENTER_Y
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125

    # frequency
    f1 = 0.005
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    if noise2(0.1 * x, 0.1 * z) < 0:
        a1 /= 1.07

    height = 0
    height += noise2(x * f1, z * f1) * a1 + a1
    height += noise2(x * f2, z * f2) * a2 - a2
    height += noise2(x * f4, z * f4) * a4 + a4
    height += noise2(x * f8, z * f8) * a8 - a8

    height = max(height,  noise2(x * f8, z * f8) + 2)
    height *= island

    return int(height)

@njit
def get_index(pos: list[int]) -> int:
    """Get the index of a voxel in the voxels array from a given position."""
    x, y, z = pos
    return x + y * CHUNK_SIZE + z * CHUNK_AREA

def set_voxel_id(voxels: list[list[Voxel]], x: int, y: int, z: int, wx: int, wy: int, wz: int, world_height: int) -> None:

    voxel_id: int = AIR # Set to air (default value)

    if wy < world_height - 1: # If not at the top of the world minus 1
        # Create caves
        if (noise3(wx * 0.09, wy * 0.09, wz * 0.09) > 0 and noise2(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10): # Noise for caves
            voxel_id = AIR  # Set to air
        else:
            voxel_id = STONE # Else set to stone
    else:
        rng = int(7 * random()) # Random number between 0 and 6
        ry = wy - rng # Random height
        if SNOW_LVL <= ry < world_height: # If the height is between the snow level and the world height
            voxel_id = SNOW # Set to snow

        elif STONE_LVL <= ry < SNOW_LVL: # If the height is between the stone level and the snow level
            voxel_id = STONE # Set to stone

        elif DIRT_LVL <= ry < STONE_LVL: # If the height is between the dirt level and the stone level
            voxel_id = DIRT # Set to dirt

        elif GRASS_LVL <= ry < DIRT_LVL: # If the height is between the grass level and the dirt level
            voxel_id = GRASS # Set to grass

        else: # If the height is below the grass level
            voxel_id = SAND # Set to sand

    # Set the voxel id
    voxels[get_index(pos=(x, y, z))].id = voxel_id

    # If the world is less than the dirt level place a tree
    if wy < DIRT_LVL:
        place_tree(voxels=voxels, voxel_id=voxel_id, pos=(x, y, z))

def place_tree(voxels: list[Voxel], pos: glm.vec3, voxel_id: int) -> None:
    x, y, z = pos # Unpack the position
    rnd: float = random() # Random number between 0 and 1
    if voxel_id != GRASS or rnd > TREE_PROBABILITY: # If the voxel id is not grass or the random number is greater than the tree probability
        return None # Return None
    if y + TREE_HEIGHT >= CHUNK_SIZE: # If the height of the tree is greater than the chunk size
        return None # Return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE: # If the width of the tree is greater than the chunk size
        return None # Return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE: # If the width of the tree is greater than the chunk size
        return None # Return None

    # Set the voxel under the tree to dirt
    voxels[get_index(pos=(x, y, z))].id = DIRT

    # Generate leaves
    m: int = 0
    for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
        k: int = iy % 2
        rng: int = int(random() * 2)
        for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
            for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                if (ix + iz) % 4:
                    voxels[get_index(pos=(x + ix + k, y + iy, z + iz + k))].id = LEAVES
        m += 1 if n > 0 else 3 if n > 1 else 0

    # Generate trunk
    for iy in range(1, TREE_HEIGHT - 2):
        voxels[get_index(pos=(x, y + iy, z))].id = WOOD

    # Generate leaves at the top of the tree
    voxels[get_index(pos=(x, y + TREE_HEIGHT - 2, z))].id = LEAVES
