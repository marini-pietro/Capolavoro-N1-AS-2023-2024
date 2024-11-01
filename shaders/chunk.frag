#version 330 core

layout (location = 0) out vec4 fragColor; // Output variable containing the color of the fragment

const vec3 gamma = vec3(2.2); // Gamma correction
const vec3 inv_gamma = 1 / gamma; // Inverse gamma correction

uniform sampler2DArray u_texture_array_0; // Texture array
uniform vec3 bg_color; // Background color
uniform float water_line; // Threshold for water line

// Input variables
in vec2 uv; // Texture coordinates
in float shading; // Shading factor
in vec3 frag_world_pos; // Fragment position in world space

flat in int face_id; // Face id
flat in int voxel_id; // Voxel id

void main() {
    vec2 face_uv = uv;
    // Adjust texture coordinates based on face id
    face_uv.x = uv.x / 3.0 - min(face_id, 2) / 3.0;

    // Sample the texture color from the texture array
    vec3 tex_col = texture(u_texture_array_0, vec3(face_uv, voxel_id)).rgb;
    
    // Apply gamma correction to the texture color
    tex_col = pow(tex_col, gamma);

    // Apply shading to the texture color
    tex_col *= shading;

    // If below water line, tint the screen blue
    if (frag_world_pos.y < water_line) tex_col *= vec3(0.0, 0.3, 1.0);

    // Apply fog
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w; // Divide by w to get the distance from the camera
    // Apply fog by linearly interpolating between the texture color and the background color based on the distance from the camera
    tex_col = mix(tex_col, bg_color, (1.0 - exp2(-0.00001 * fog_dist * fog_dist))); // Increase the -0.00001 constant to make the fog denser

    // Apply inverse gamma correction to convert color back into SRGB space
    tex_col = pow(tex_col, inv_gamma);
    // Set the final fragment color with full opacity
    fragColor = vec4(tex_col, 1.0);
}