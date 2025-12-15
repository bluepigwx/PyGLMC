import pygame as pg
from OpenGL.GL import *
import glm

VertexShaderSource = """#version 330 core
layout (location=0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0f);
}
"""


FragmentShaderSource = """#version 330 core
out vec4 FragmentColor;
void main()
{
    FragmentColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""


# 创建着色器
def CreateShader(ShaderCode: str, ShaderType: int)->int:
    ShaderHandle = glCreateShader(ShaderType)
    glShaderSource(ShaderHandle, ShaderCode)
    glCompileShader(ShaderHandle)

    Success = glGetShaderiv(ShaderHandle, GL_COMPILE_STATUS)
    if not Success:
        ErrorInfo = glGetShaderInfoLog(ShaderHandle)
        ShaderTypeName = "Vertex" if ShaderType == GL_VERTEX_SHADER else "Fragment"
        print(f"Create {ShaderTypeName} Shader failed: {ErrorInfo.decode()}")
        glDeleteShader(ShaderHandle)
        return -1

    return ShaderHandle



class SDLApp:
    def __init__(self):
        pg.init()
        
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((1024, 768), pg.OPENGL|pg.DOUBLEBUF)

        self.clock = pg.time.Clock()

    
    def SetupRender(self):
        glClearColor(0.1, 0.1, 0.1, 1)
        
        VSHandle = CreateShader(VertexShaderSource, GL_VERTEX_SHADER)
        FSHandle = CreateShader(FragmentShaderSource, GL_FRAGMENT_SHADER)
        if (VSHandle < 0 or FSHandle < 0):
            if VSHandle < 0:
                glDeleteShader(FSHandle)
            
            if FSHandle < 0:
                glDeleteShader(VSHandle)

            raise Exception(f"Create Shader Failed VS{VSHandle} FS{FSHandle}")

        ShaderProgram = glCreateProgram()
        glAttachShader(ShaderProgram, VSHandle)
        glAttachShader(ShaderProgram, FSHandle)
        glLinkProgram(ShaderProgram)
        Success = glGetProgramiv(ShaderProgram, GL_LINK_STATUS)

        glDeleteShader(VSHandle)
        glDeleteShader(FSHandle)

        if (not Success):
            ErrorInfo = glGetProgramInfoLog(ShaderProgram)
            raise Exception(f"Link Program Failed {ErrorInfo.decode()}")
        
        self.ShaderProgram = ShaderProgram

        # 构建三角形
        Vertices = glm.array(glm.float32,
                             -0.5, -0.5, 0.0,
                             0.5, -0.5, 0.0,
                             0.0, 0.5, 0.0
                             )

        self.VAOHandle = glGenVertexArrays(1)
        glBindVertexArray(self.VAOHandle)

        self.VBOHandle = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBOHandle)
        glBufferData(GL_ARRAY_BUFFER, Vertices.nbytes, Vertices.ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3*glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)


    def BeginRender(self):
        glClear(GL_COLOR_BUFFER_BIT)


    def EndRender(self):
        pg.display.flip()


    def Draw(self):
        glUseProgram(self.ShaderProgram)
        glBindVertexArray(self.VAOHandle)
        glDrawArrays(GL_TRIANGLES, 0, 3)


    def Run(self):
        Running = True

        self.SetupRender()

        while Running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Running = False

            self.BeginRender()

            self.Draw()

            self.EndRender()

            self.clock.tick(60)
        
        pg.quit()



if __name__ == "__main__":
    app = SDLApp()
    app.Run()