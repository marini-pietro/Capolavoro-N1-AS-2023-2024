#version 330 core

// Input texture coordinates
layout (location = 0) in vec2 in_tex_coord_0;
// Input vertex position
layout (location = 1) in vec3 in_position;

// Uniform matrices for transformations
uniform mat4 m_proj;  // Projection matrix
uniform mat4 m_view;  // View matrix
uniform mat4 m_model; // Model matrix
// Uniform mode identifier to select marker color
uniform uint mode_id;

// Array of marker colors: red and blue
const vec3 marker_colors[2] = vec3[2](vec3(1, 0, 0), vec3(0, 0, 1));

// Output variables to the fragment shader
out vec3 marker_color; // Marker color
out vec2 uv;           // Texture coordinates

void main() {
    // Pass the input texture coordinates to the fragment shader
    uv = in_tex_coord_0;
    // Select the marker color based on the mode_id
    marker_color = marker_colors[mode_id];
    // Transform the vertex position by the model, view, and projection matrices
    // The position is slightly scaled and translated to adjust the marker size and position
    gl_Position = m_proj * m_view * m_model * vec4((in_position - 0.5) * 1.01 + 0.5, 1.0);
}