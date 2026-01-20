#version 330 core

uniform sampler2DArray texture_array_sampler;

out vec4 fragment_colour;

in vec3 interpolated_tex_coords;
in float interpolated_shading_value;

void main(void) 
{
	fragment_colour = texture(texture_array_sampler, interpolated_tex_coords) * interpolated_shading_value;
}