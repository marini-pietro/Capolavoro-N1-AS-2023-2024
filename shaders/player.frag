#version 330 core

// Input variables from the vertex shader
in vec3 frag_normal;
in vec2 frag_texcoord;

// Uniforms for lighting and texture
uniform sampler2D u_texture_0;

// Output color
out vec4 frag_color;

void main()
{
    // Normalize the normal vector
    vec3 normal = normalize(frag_normal);
    
    // Sample the texture
    vec4 tex_color = texture(u_texture_0, frag_texcoord);
    
    // Calculate the final color
    frag_color = vec4(tex_color.rgb, tex_color.a);
}