#version 330 core

layout (location=0) in vec3 position;
layout (location=1) in vec3 tex_coord;

uniform mat4 view_mat;
uniform mat4 proj_mat;

out vec3 interpolated_tex_coords;

void main()
{
    interpolated_tex_coords = tex_coord;
    gl_Position = proj_mat * view_mat * vec4(position, 1.0f);
}