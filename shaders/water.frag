#version 330 core

// Output variable to store the final color of the fragment
layout (location = 0) out vec4 fragColor;

// Constants for gamma correction
const vec3 gamma = vec3(2.2);      // Gamma correction factor
const vec3 inv_gamma = 1 / gamma;  // Inverse gamma correction factor

// Input texture coordinates from the vertex shader
in vec2 uv;

// Uniform variables
uniform sampler2D u_texture_0; // Texture sampler
uniform vec3 bg_color; // Background color

void main() {
    // Sample the texture color using the texture coordinates
    vec3 tex_col = texture(u_texture_0, uv).rgb;
    // Apply gamma correction to the texture color
    tex_col = pow(tex_col, gamma);

    // Calculate fog distance based on fragment depth
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w;
    // Calculate alpha value for water transparency
    float alpha = mix(0.5, 0.0, 1.0 - exp(-0.00002 * fog_dist * fog_dist)); // Increase the -0.000002 constant to make the water less transparent                                    
    // Apply fog by linearly interpolating between the texture color and the background color based on the distance from the camera
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist))); // Increase the -0.00001 constant to make the fog denser
    
    tex_col = pow(tex_col, inv_gamma); // Apply inverse gamma correction to convert color back to sRGB space
    fragColor = vec4(tex_col, alpha); // Set the final fragment color with the calculated alpha value
}