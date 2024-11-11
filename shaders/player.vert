#version 330 core

// Uniforms for transformation matrices
uniform mat4 m_model;
uniform mat4 m_view;
uniform mat4 m_proj;

// Input attributes from the vertex buffer
layout(location = 0) in vec3 in_position;
layout(location = 1) in vec3 in_normal;
layout(location = 2) in vec2 in_texcoord_0;

// Output variables to the fragment shader
out vec3 frag_normal;
out vec2 frag_texcoord;

void main()
{
    // Transform the vertex position
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
    
    // Pass the normal and texture coordinates to the fragment shader
    frag_normal = in_normal;
    frag_texcoord = in_texcoord_0;
}