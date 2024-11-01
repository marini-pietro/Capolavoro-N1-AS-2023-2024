#version 330 core

// Output variable to store the final color of the fragment
layout (location = 0) out vec4 fragColor;

// Input variables from the vertex shader
in vec3 marker_color; // Marker color
in vec2 uv;           // Texture coordinates

// Uniform sampler for the texture
uniform sampler2D u_texture_0;

void main() {
    // Sample the texture color using the texture coordinates
    fragColor = texture(u_texture_0, uv);
    // Add the marker color to the sampled texture color
    fragColor.rgb += marker_color;
    // Set the alpha value based on the combined red and blue components
    // If the sum of red and blue components is greater than 1.0, set alpha to 0.0 (transparent)
    // Otherwise, set alpha to 1.0 (opaque)
    fragColor.a = (fragColor.r + fragColor.b > 1.0) ? 0.0 : 1.0;
}