#version 330 core

// Output variable to store the final color of the fragment
layout (location = 0) out vec4 fragColor;

// Input variable to receive the color from the vertex shader
in vec3 color;

void main() {
    // Set the fragment color to the input color with full opacity (alpha = 1.0)
    fragColor = vec4(color, 1.0);
}