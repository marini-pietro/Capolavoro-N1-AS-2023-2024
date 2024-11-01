#version 330 core

// Input vertex attributes
layout (location = 0) in vec3 in_position; // Vertex position
layout (location = 1) in vec3 in_color;    // Vertex color

// Uniform matrices for transformations
uniform mat4 m_proj;  // Projection matrix
uniform mat4 m_view;  // View matrix
uniform mat4 m_model; // Model matrix

// Output variable to pass color to the fragment shader
out vec3 color;

void main() {
    // Pass the input color to the fragment shader
    color = in_color;

    // Transform the vertex position by the model, view, and projection matrices
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}