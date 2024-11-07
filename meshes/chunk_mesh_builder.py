from settings import *
from numba import uint8

@njit # Use numba to accelerate this function that mainly contains calculations
def get_ao(local_pos: tuple[int], world_pos: tuple[int], world_voxels_ids: np.array, plane: str) -> tuple[int, int, int, int]:
    """
    Generate ambient occlusion values for a voxel face.

    Args:
        local_pos (tuple[int]): Voxel position in the chunk.
        world_pos (tuple[int]): Voxel position in the world.
        world_voxels (np array): Voxel data of the world.
        plane (str): Plane of the face. 

    Returns:
        tuple: Tuple or four ambient occlusion values (integers) that determine whether ambient occlusion should be applied to that corner or not. 
    """

    x, y, z = local_pos
    wx, wy, wz = world_pos

    if plane == 'Y': # Y plane
        a = is_void(local_voxel_pos=(x    , y, z - 1), world_voxel_pos=(wx    , wy, wz - 1), world_voxels_ids=world_voxels_ids)
        b = is_void(local_voxel_pos=(x - 1, y, z - 1), world_voxel_pos=(wx - 1, wy, wz - 1), world_voxels_ids=world_voxels_ids)
        c = is_void(local_voxel_pos=(x - 1, y, z    ), world_voxel_pos=(wx - 1, wy, wz    ), world_voxels_ids=world_voxels_ids)
        d = is_void(local_voxel_pos=(x - 1, y, z + 1), world_voxel_pos=(wx - 1, wy, wz + 1), world_voxels_ids=world_voxels_ids)
        e = is_void(local_voxel_pos=(x    , y, z + 1), world_voxel_pos=(wx    , wy, wz + 1), world_voxels_ids=world_voxels_ids)
        f = is_void(local_voxel_pos=(x + 1, y, z + 1), world_voxel_pos=(wx + 1, wy, wz + 1), world_voxels_ids=world_voxels_ids)
        g = is_void(local_voxel_pos=(x + 1, y, z    ), world_voxel_pos=(wx + 1, wy, wz    ), world_voxels_ids=world_voxels_ids)
        h = is_void(local_voxel_pos=(x + 1, y, z - 1), world_voxel_pos=(wx + 1, wy, wz - 1), world_voxels_ids=world_voxels_ids)

    elif plane == 'X': # X plane
        a = is_void(local_voxel_pos=(x, y    , z - 1), world_voxel_pos=(wx, wy    , wz - 1), world_voxels_ids=world_voxels_ids)
        b = is_void(local_voxel_pos=(x, y - 1, z - 1), world_voxel_pos=(wx, wy - 1, wz - 1), world_voxels_ids=world_voxels_ids)
        c = is_void(local_voxel_pos=(x, y - 1, z    ), world_voxel_pos=(wx, wy - 1, wz    ), world_voxels_ids=world_voxels_ids)
        d = is_void(local_voxel_pos=(x, y - 1, z + 1), world_voxel_pos=(wx, wy - 1, wz + 1), world_voxels_ids=world_voxels_ids)
        e = is_void(local_voxel_pos=(x, y    , z + 1), world_voxel_pos=(wx, wy    , wz + 1), world_voxels_ids=world_voxels_ids)
        f = is_void(local_voxel_pos=(x, y + 1, z + 1), world_voxel_pos=(wx, wy + 1, wz + 1), world_voxels_ids=world_voxels_ids)
        g = is_void(local_voxel_pos=(x, y + 1, z    ), world_voxel_pos=(wx, wy + 1, wz    ), world_voxels_ids=world_voxels_ids)
        h = is_void(local_voxel_pos=(x, y + 1, z - 1), world_voxel_pos=(wx, wy + 1, wz - 1), world_voxels_ids=world_voxels_ids)

    else:  # Z plane
        a = is_void(local_voxel_pos=(x - 1, y    , z), world_voxel_pos=(wx - 1, wy    , wz), world_voxels_ids=world_voxels_ids)
        b = is_void(local_voxel_pos=(x - 1, y - 1, z), world_voxel_pos=(wx - 1, wy - 1, wz), world_voxels_ids=world_voxels_ids)
        c = is_void(local_voxel_pos=(x    , y - 1, z), world_voxel_pos=(wx    , wy - 1, wz), world_voxels_ids=world_voxels_ids)
        d = is_void(local_voxel_pos=(x + 1, y - 1, z), world_voxel_pos=(wx + 1, wy - 1, wz), world_voxels_ids=world_voxels_ids)
        e = is_void(local_voxel_pos=(x + 1, y    , z), world_voxel_pos=(wx + 1, wy    , wz), world_voxels_ids=world_voxels_ids)
        f = is_void(local_voxel_pos=(x + 1, y + 1, z), world_voxel_pos=(wx + 1, wy + 1, wz), world_voxels_ids=world_voxels_ids)
        g = is_void(local_voxel_pos=(x    , y + 1, z), world_voxel_pos=(wx    , wy + 1, wz), world_voxels_ids=world_voxels_ids)
        h = is_void(local_voxel_pos=(x - 1, y + 1, z), world_voxel_pos=(wx - 1, wy + 1, wz), world_voxels_ids=world_voxels_ids)

    ao: tuple[int, int, int, int] = (a + b + c), (g + h + a), (e + f + g), (c + d + e)
    return ao

@njit
def pack_data(x, y, z, voxel_id, face_id, ao_id, flipped):
    """
    Function to pack voxel data.
    """

    # x: 6bit  y: 6bit  z: 6bit  voxel_id: 8bit  face_id: 3bit  ao_id: 2bit  flipped: 1bit (boolean)
    a, b, c, d, e, f, g = x, y, z, voxel_id, face_id, ao_id, flipped

    b_bit, c_bit, d_bit, e_bit, f_bit, g_bit = 6, 6, 8, 3, 2, 1
    fg_bit = f_bit + g_bit
    efg_bit = e_bit + fg_bit
    defg_bit = d_bit + efg_bit
    cdefg_bit = c_bit + defg_bit
    bcdefg_bit = b_bit + cdefg_bit

    packed_data = (
        a << bcdefg_bit |
        b << cdefg_bit |
        c << defg_bit |
        d << efg_bit |
        e << fg_bit |
        f << g_bit | g
    )
    return packed_data

@njit
def get_chunk_index(world_voxel_pos: tuple[int, int, int]) -> int:
    wx, wy, wz = world_voxel_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
        return -1

    index = cx + WORLD_W * cz + WORLD_AREA * cy
    return index

@njit
def is_void(local_voxel_pos: tuple[int, int, int], world_voxel_pos: tuple[int, int, int], world_voxels_ids: list[int]) -> bool:
    chunk_index: int = get_chunk_index(world_voxel_pos)
    if chunk_index == -1:
        return False
    chunk_voxels = world_voxels_ids[chunk_index]

    x, y, z = local_voxel_pos
    voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA

    if chunk_voxels[voxel_index]:
        return False
    return True

@njit
def add_data(vertex_data, index, *vertices) -> bool: # Add vertices to the vertex data array
    for vertex in vertices:
        vertex_data[index] = vertex
        index += 1
    return index

@njit
def build_chunk_mesh(chunk_voxels_ids: list[int], format_size: str, chunk_pos: tuple[int, int, int], world_voxels_ids: list[int]) -> np.array:
    """
    Build the mesh data for a chunk.

    Parameters:
        chunk_voxels_ids (list[int]): Voxel ids of the chunk.
        format_size (str): Format size of the vertex data.
        chunk_pos (tuple[int, int, int]): Position of the chunk.
        world_voxels_ids (list[int]): Voxel ids of the world.

    Returns:
        np.array: Numpy array containing the vertex data.
    """

    vertex_data: np.array = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint32')
    index: int = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels_ids[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if not voxel_id: # Skip if the voxel is empty
                    continue

                # voxel world position
                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # top face
                if is_void(local_voxel_pos=(x, y + 1, z), world_voxel_pos=(wx, wy + 1, wz), world_voxels_ids=world_voxels_ids):
                    # get ao values
                    ao: tuple[int, int, int, int] = get_ao(local_pos=(x, y + 1, z), world_pos=(wx, wy + 1, wz), world_voxels_ids=world_voxels_ids, plane='Y')
                    flipped: bool = ao[1] + ao[3] > ao[0] + ao[2] # Determine if the face should be flipped

                    # format: x, y, z, voxel_id, face_id, ao_id, flipped
                    v0 = pack_data(x    , y + 1, z    , voxel_id, 0, ao[0], flipped)
                    v1 = pack_data(x + 1, y + 1, z    , voxel_id, 0, ao[1], flipped)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 0, ao[2], flipped)
                    v3 = pack_data(x    , y + 1, z + 1, voxel_id, 0, ao[3], flipped)

                    if flipped:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom face
                if is_void(local_voxel_pos=(x, y - 1, z), world_voxel_pos=(wx, wy - 1, wz), world_voxels_ids=world_voxels_ids):
                    ao = get_ao(local_pos=(x, y - 1, z), world_pos=(wx, wy - 1, wz), world_voxels_ids=world_voxels_ids, plane='Y')
                    flipped = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y, z    , voxel_id, 1, ao[0], flipped)
                    v1 = pack_data(x + 1, y, z    , voxel_id, 1, ao[1], flipped)
                    v2 = pack_data(x + 1, y, z + 1, voxel_id, 1, ao[2], flipped)
                    v3 = pack_data(x    , y, z + 1, voxel_id, 1, ao[3], flipped)

                    if flipped:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void(local_voxel_pos=(x + 1, y, z), world_voxel_pos=(wx + 1, wy, wz), world_voxels_ids=world_voxels_ids):
                    ao = get_ao(local_pos=(x + 1, y, z), world_pos=(wx + 1, wy, wz), world_voxels_ids=world_voxels_ids, plane='X')
                    flipped = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y    , z    , voxel_id, 2, ao[0], flipped)
                    v1 = pack_data(x + 1, y + 1, z    , voxel_id, 2, ao[1], flipped)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 2, ao[2], flipped)
                    v3 = pack_data(x + 1, y    , z + 1, voxel_id, 2, ao[3], flipped)

                    if flipped:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void(local_voxel_pos=(x - 1, y, z), world_voxel_pos=(wx - 1, wy, wz), world_voxels_ids=world_voxels_ids):
                    ao = get_ao(local_pos=(x - 1, y, z), world_pos=(wx - 1, wy, wz), world_voxels_ids=world_voxels_ids, plane='X')
                    flipped = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y    , z    , voxel_id, 3, ao[0], flipped)
                    v1 = pack_data(x, y + 1, z    , voxel_id, 3, ao[1], flipped)
                    v2 = pack_data(x, y + 1, z + 1, voxel_id, 3, ao[2], flipped)
                    v3 = pack_data(x, y    , z + 1, voxel_id, 3, ao[3], flipped)

                    if flipped:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void(local_voxel_pos=(x, y, z - 1), world_voxel_pos=(wx, wy, wz - 1), world_voxels_ids=world_voxels_ids):
                    ao = get_ao(local_pos=(x, y, z - 1), world_pos=(wx, wy, wz - 1), world_voxels_ids=world_voxels_ids, plane='Z')
                    flipped = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x,     y,     z, voxel_id, 4, ao[0], flipped)
                    v1 = pack_data(x,     y + 1, z, voxel_id, 4, ao[1], flipped)
                    v2 = pack_data(x + 1, y + 1, z, voxel_id, 4, ao[2], flipped)
                    v3 = pack_data(x + 1, y,     z, voxel_id, 4, ao[3], flipped)

                    if flipped:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)
                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front face
                if is_void(local_voxel_pos=(x, y, z + 1), world_voxel_pos=(wx, wy, wz + 1), world_voxels_ids=world_voxels_ids):
                    ao = get_ao(local_pos=(x, y, z + 1), world_pos=(wx, wy, wz + 1), world_voxels_ids=world_voxels_ids, plane='Z')
                    flipped = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x    , y    , z + 1, voxel_id, 5, ao[0], flipped)
                    v1 = pack_data(x    , y + 1, z + 1, voxel_id, 5, ao[1], flipped)
                    v2 = pack_data(x + 1, y + 1, z + 1, voxel_id, 5, ao[2], flipped)
                    v3 = pack_data(x + 1, y    , z + 1, voxel_id, 5, ao[3], flipped)

                    if flipped:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[:index + 1]