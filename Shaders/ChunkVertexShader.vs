#version 330 core

layout (location=0) in ivec3 position;
layout (location=1) in int voxelIndex;
layout (location=2) in int FaceId;

uniform mat4 modelMat;
uniform mat4 viewMat;
uniform mat4 projMat;

out vec3 voxelColor;

// 给体素整点颜色
vec3 hash31(float p)
{
    vec3 p3 = fract(vec3(p * 21.2) * vec3(0.1031, 0.1030, 0.0973));
    p3 += dot(p3, p3.yzx + 33.33);
    return fract((p3.xxy + p3.yzz) * p3.zyx) + 0.05;
}


void main()
{
    voxelColor = hash31(voxelIndex);
    gl_Position = projMat * viewMat * modelMat * vec4(position, 1);
}