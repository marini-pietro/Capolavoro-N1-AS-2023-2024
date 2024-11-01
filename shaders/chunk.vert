#version 330 core

layout (location = 0) in uint packed_data; // Input packed data containing vertex information

// Variables to store unpacked vertex data
int x, y, z;
int ao_id;
int flip_id;

// Uniform matrices for transformations
uniform mat4 m_proj; // Projection matrix
uniform mat4 m_view; // View matrix
uniform mat4 m_model; // Model matrix

// Output variables to the fragment shader
flat out int voxel_id; // Voxel ID
flat out int face_id; // Face ID

//out vec3 voxel_color; // Uncomment if voxel color is needed
out vec2 uv; // Texture coordinates
out float shading; // Shading factor
out vec3 frag_world_pos; // Fragment position in world space

// Ambient occlusion values
const float ao_values[4] = float[4](0.1, 0.25, 0.5, 1.0);

// Shading values for each face
const float face_shading[6] = float[6](
    1.0, 0.5,  // Top and bottom faces
    0.5, 0.8,  // Right and left faces
    0.5, 0.8   // Front and back faces
);

// Texture coordinates for a quad
const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);

// Indices for texture coordinates based on face orientation and flip
const int uv_indices[24] = int[24](
    1, 0, 2, 1, 2, 3,  // Even face
    3, 0, 2, 3, 1, 0,  // Odd face
    3, 1, 0, 3, 0, 2,  // Even flipped face
    1, 2, 3, 1, 0, 2   // Odd flipped face
);

// Hash function to generate pseudo-random values
vec3 hash31(float p) {
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}

// Function to unpack the packed vertex data
void unpack(uint packed_data) {
    // Bit lengths and masks for unpacking
    uint b_bit = 6u, c_bit = 6u, d_bit = 8u, e_bit = 3u, f_bit = 2u, g_bit = 1u;
    uint b_mask = 63u, c_mask = 63u, d_mask = 255u, e_mask = 7u, f_mask = 3u, g_mask = 1u;
    // Bit shifts for unpacking
    uint fg_bit = f_bit + g_bit;
    uint efg_bit = e_bit + fg_bit;
    uint defg_bit = d_bit + efg_bit;
    uint cdefg_bit = c_bit + defg_bit;
    uint bcdefg_bit = b_bit + cdefg_bit;
    // Unpacking vertex data
    x = int(packed_data >> bcdefg_bit); // Extract x coordinate
    y = int((packed_data >> cdefg_bit) & b_mask); // Extract y coordinate
    z = int((packed_data >> defg_bit) & c_mask); // Extract z coordinate
    // Extract final data
    voxel_id = int((packed_data >> efg_bit) & d_mask); // Extract voxel ID
    face_id = int((packed_data >> fg_bit) & e_mask); // Extract face ID
    ao_id = int((packed_data >> g_bit) & f_mask); // Extract ambient occlusion ID
    flip_id = int(packed_data & g_mask); // Extract flip ID
}

void main() {
    unpack(packed_data); // Unpack the vertex data

    vec3 in_position = vec3(x, y, z); // Create the input position vector
    int uv_index = gl_VertexID % 6  + ((face_id & 1) + flip_id * 2) * 6; // Calculate the UV index

    uv = uv_coords[uv_indices[uv_index]]; // Set the texture coordinates

    shading = face_shading[face_id] * ao_values[ao_id]; // Calculate the shading factor

    frag_world_pos = (m_model * vec4(in_position, 1.0)).xyz; // Transform the position to world space

    gl_Position = m_proj * m_view * vec4(frag_world_pos, 1.0); // Calculate the final position in clip space
}