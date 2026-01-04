#version 330 core

out vec4 FragmentColor;

uniform vec4 OurColor;

// 注意uniform变量如果在编译shader时被判定没有被使用过，可能会被编译器优化掉
// 如果接下来在运行时去访问这个变量就会访问不到了
uniform sampler2D TextureUnit0;
uniform sampler2D TextureUnit1;

in vec2 TexCoord;


void main()
{

    //FragmentColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
    //FragmentColor = OurColor;

    vec4 Color1 = texture(TextureUnit0, TexCoord);
    vec4 Color2 = texture(TextureUnit1, TexCoord);

    FragmentColor = mix(Color1, Color2, 0.5);
}