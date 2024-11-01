#version 330 core

layout (location = 0) out vec4 fragColor; //Output variable for fragment color

const vec3 cloud_color = vec3(1); //Color of the clouds (white)

uniform vec3 bg_color; //Background color

void main() {
    float fog_dist = gl_FragCoord.z / gl_FragCoord.w; // Divide by w to get the distance from the camera
    // Apply fog by linearly interpolating between the texture color and the background color based on the distance from the camera
    vec3 col = mix(cloud_color, bg_color, 1.0 - exp(-0.000001 * fog_dist * fog_dist)); // Increase the -0.00001 constant to make the fog denser

    fragColor = vec4(col, 0.8); //Output the color of the clouds (white with 80% opacity)
}