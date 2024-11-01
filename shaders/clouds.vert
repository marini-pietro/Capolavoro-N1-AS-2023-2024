#version 330 core

// Input vertex attribute: position of the vertex
layout (location = 0) in vec3 in_position;

// Uniform matrices for transformations
uniform mat4 m_proj; // Projection matrix
uniform mat4 m_view; // View matrix
uniform mat4 m_view_proj; // Combined view-projection matrix (not used in this shader)

// Uniform variables for cloud animation
uniform int center; // Center position for scaling and translation
uniform float u_time; // Time variable for animation
uniform float cloud_scale; // Scale factor for the clouds

void main() {
    vec3 pos = vec3(in_position); // Copy the input position to a local variable

    // Adjust the x and z coordinates relative to the center
    pos.xz -= center;
    pos.xz *= cloud_scale; // Scale the x and z coordinates
    pos.xz += center; // Translate back to the original position

    float time = 300 * sin(0.01 * u_time); // Calculate the time-based translation for cloud movement
    pos.xz += time; // Apply the time-based translation to the x and z coordinates

    // Transform the position to clip space using the projection and view matrices
    gl_Position = m_proj * m_view * vec4(pos, 1.0);
}