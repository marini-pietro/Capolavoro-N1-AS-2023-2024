from settings import *
from numba import uint8

@njit # Use numba to accelerate this function that mainly contains calculations
def get_ao(local_pos: glm.vec3, world_pos: glm.vec3, world_voxels: np.array, plane: str) -> tuple[int, int, int, int]:
    """Generate ambient occlusion values for a voxel face.

    Args:
        local_pos (glm.vec3): Local voxel position.
        world_pos (glm.vec3): Global voxel position.
        world_voxels (np array): Voxel data of the world.
        plane (str): Plane of the face. 

    Returns:
        tuple: Tuple or four ambient occlusion values (integers) that determine whether ambient occlusion should be applied to that corner or not. 
    """

    x, y, z = local_pos
    wx, wy, wz = world_pos

    if plane == 'Y': # Y plane
        a = is_void((x    , y, z - 1), (wx    , wy, wz - 1), world_voxels)
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
        c = is_void((x - 1, y, z    ), (wx - 1, wy, wz    ), world_voxels)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
        e = is_void((x    , y, z + 1), (wx    , wy, wz + 1), world_voxels)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
        g = is_void((x + 1, y, z    ), (wx + 1, wy, wz    ), world_voxels)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)

    elif plane == 'X': # X plane
        a = is_void((x, y    , z - 1), (wx, wy    , wz - 1), world_voxels)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
        c = is_void((x, y - 1, z    ), (wx, wy - 1, wz    ), world_voxels)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
        e = is_void((x, y    , z + 1), (wx, wy    , wz + 1), world_voxels)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)
        g = is_void((x, y + 1, z    ), (wx, wy + 1, wz    ), world_voxels)
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)

    else:  # Z plane
        a = is_void((x - 1, y    , z), (wx - 1, wy    , wz), world_voxels)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
        c = is_void((x    , y - 1, z), (wx    , wy - 1, wz), world_voxels)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels)
        e = is_void((x + 1, y    , z), (wx + 1, wy    , wz), world_voxels)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
        g = is_void((x    , y + 1, z), (wx    , wy + 1, wz), world_voxels)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

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
def get_chunk_index(world_voxel_pos) -> int:
    wx, wy, wz = world_voxel_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE
    if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
        return -1

    index = cx + WORLD_W * cz + WORLD_AREA * cy
    return index

@njit
def is_void(local_voxel_pos, world_voxel_pos, world_voxels) -> bool:
    chunk_index = get_chunk_index(world_voxel_pos)
    if chunk_index == -1:
        return False
    chunk_voxels = world_voxels[chunk_index]

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
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels) -> np.array:
    vertex_data: np.array = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint32')
    index: int = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if not voxel_id: # Skip if the voxel is empty
                    continue

                # voxel world position
                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    # get ao values
                    ao = get_ao((x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane='Y')
                    flipped = ao[1] + ao[3] > ao[0] + ao[2] # Determine if the face should be flipped

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
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao((x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane='Y')
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
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao((x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane='X')
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
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao((x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane='X')
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
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao((x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane='Z')
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
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao((x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane='Z')
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