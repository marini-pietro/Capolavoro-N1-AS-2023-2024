#version 330 core

// Input vertex attributes
layout (location = 0) in vec2 in_tex_coord; // Texture coordinates
layout (location = 1) in vec3 in_position;  // Vertex position

// Uniform matrices for transformations
uniform mat4 m_proj;      // Projection matrix
uniform mat4 m_view;      // View matrix
uniform mat4 m_view_proj; // Combined view-projection matrix (not used in this shader)

// Uniform variables for water properties
uniform int water_area;   // Scale factor for the water area
uniform float water_line; // Height of the water line

// Output variable to pass texture coordinates to the fragment shader
out vec2 uv;

void main() {
    vec3 pos = in_position; // Copy the input position to a local variable

    // Scale and translate the x and z coordinates based on the water area
    pos.xz *= water_area;          // Scale the x and z coordinates
    pos.xz -= 0.33 * water_area;   // Translate the x and z coordinates

    // Adjust the y coordinate based on the water line height
    pos.y += water_line;

    // Scale the texture coordinates based on the water area
    uv = in_tex_coord * water_area;

    // Transform the position to clip space using the projection and view matrices
    gl_Position = m_proj * m_view * vec4(pos, 1.0);
}