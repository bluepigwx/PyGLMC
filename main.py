import pygame as pg
from OpenGL.GL import *
import glm
from Shader import *


def LoadTexture(image_path: str) -> int:
    """
    Args:
        image_path: Path to the image file
        
    Returns:
        Texture ID, or 0 if failed
    """
    try:
        
        image_surface = pg.image.load(image_path)
        
        width = image_surface.get_width()
        height = image_surface.get_height()
        
        image_surface = image_surface.convert_alpha()
        
        image_data = pg.image.tostring(image_surface, "RGBA", True)
        
        # Generate texture
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Upload texture data to GPU
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            image_data
        )
        
        # Generate mipmaps
        glGenerateMipmap(GL_TEXTURE_2D)
        
        # Unbind texture
        glBindTexture(GL_TEXTURE_2D, 0)
        
        print(f"Texture loaded: {image_path} ({width}x{height})")
        return texture_id
        
    except Exception as e:
        print(f"Failed to load texture {image_path}: {e}")
        return 0


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

        self.TriangleShader = Shader("Shaders/VertexShader.vs", "Shaders/FragmentShader.fs")
        if not self.TriangleShader.IsValid:
            raise RuntimeError(f"Create Shader failed")
        
        # 构建四边角形
        Vertices = glm.array(glm.float32,
                             -0.5, -0.5, 0.0,   0.0, 0.0,
                              0.5, -0.5, 0.0,   1.0, 0.0,
                              0.5,  0.5, 0.0,   1.0, 1.0,
                              -0.5, 0.5, 0.0,   0.0, 1.0
                             )
        
        Indices = glm.array(glm.uint32,
                            0, 1, 2,
                            0, 2, 3
                            )
        
        Vertices2 = glm.array(glm.float32,
        -0.5, -0.5, -0.5,  0.0, 0.0,
         0.5, -0.5, -0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5,  0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 0.0,

        -0.5, -0.5,  0.5,  0.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
         0.5,  0.5,  0.5,  1.0, 1.0,
        -0.5,  0.5,  0.5,  0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,

        -0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5, -0.5,  1.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        -0.5,  0.5,  0.5,  1.0, 0.0,

         0.5,  0.5,  0.5,  1.0, 0.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5,  0.5,  0.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 0.0,

        -0.5, -0.5, -0.5,  0.0, 1.0,
         0.5, -0.5, -0.5,  1.0, 1.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
         0.5, -0.5,  0.5,  1.0, 0.0,
        -0.5, -0.5,  0.5,  0.0, 0.0,
        -0.5, -0.5, -0.5,  0.0, 1.0,

        -0.5,  0.5, -0.5,  0.0, 1.0,
         0.5,  0.5, -0.5,  1.0, 1.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
         0.5,  0.5,  0.5,  1.0, 0.0,
        -0.5,  0.5,  0.5,  0.0, 0.0,
        -0.5,  0.5, -0.5,  0.0, 1.0
        )

        self.VAOHandle = glGenVertexArrays(1)
        glBindVertexArray(self.VAOHandle)

        # 多边形数据
        self.VBOHandle = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBOHandle)
        glBufferData(GL_ARRAY_BUFFER, Vertices2.nbytes, Vertices2.ptr, GL_STATIC_DRAW)

        self.EBOHandle = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBOHandle)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, Indices.nbytes, Indices.ptr, GL_STATIC_DRAW)

        # Position attribute (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5*glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)

        # Texture coordinate attribute (location = 1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5*glm.sizeof(glm.float32), 
                            ctypes.c_void_p(3*glm.sizeof(glm.float32)))
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        # Load texture
        self.TextureHandle = LoadTexture("Pic/Wall.png")
        if self.TextureHandle == 0:
            raise RuntimeError(f"Load Pic Wall failed")

        self.TextureHandle1 = LoadTexture("Pic/Rock.png")
        if self.TextureHandle1 == 0:
            raise RuntimeError(f"Load Pic Rock failed")
        
        glEnable(GL_DEPTH_TEST)


    def BeginRender(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    def EndRender(self):
        pg.display.flip()


    def Draw(self):

        CubePositions = [
        glm.vec3( 0.0,  0.0,  0.0),
        glm.vec3( 2.0,  5.0, -15.0),
        glm.vec3(-1.5, -2.2, -2.5),
        glm.vec3(-3.8, -2.0, -12.3),
        glm.vec3( 2.4, -0.4, -3.5),
        glm.vec3(-1.7,  3.0, -7.5),
        glm.vec3( 1.3, -2.0, -2.5),
        glm.vec3( 1.5,  2.0, -2.5),
        glm.vec3( 1.5,  0.2, -1.5),
        glm.vec3(-1.3,  1.0, -1.5)
        ]

        # 使用Shader中的unifor变量一定要先use shader
        self.TriangleShader.Use()
        self.TriangleShader.Uniform1i("TextureUnit0", 0)
        self.TriangleShader.Uniform1i("TextureUnit1", 1)

        # self.TriangleShader.Uniform4f("OurColor", 1.0, 1.0, 1.0, 1.0)

        # Bind texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.TextureHandle)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.TextureHandle1)

        for i in range(len(CubePositions)):
            
            Model = glm.mat4(1.0)
            View = glm.mat4(1.0)
            Projection = glm.mat4(1.0)

            Rotation = pg.time.get_ticks() / 1000
            Model = glm.translate(Model, CubePositions[i])
            Model = glm.rotate(Model, Rotation, glm.vec3(0.0, 1.0, 1.0))
            View = glm.translate(View, glm.vec3(0.0, 0.0, -5.0))
            Projection = glm.perspective(glm.radians(45.0), 1024 / 768, 0.1, 100.0)
 
            self.TriangleShader.UniformMat4fv("Model", Model)
            self.TriangleShader.UniformMat4fv("View", View)
            self.TriangleShader.UniformMat4fv("Projection", Projection)

            glBindVertexArray(self.VAOHandle)
            glDrawArrays(GL_TRIANGLES, 0, 36)
        
        #glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)


    def Run(self):
        Running = True

        while Running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Running = False

            self.BeginRender()

            self.Draw()

            self.EndRender()

            self.clock.tick(60)


    def Finish(self):
        glDeleteVertexArrays(1, (self.VAOHandle,))
        glDeleteBuffers(1, (self.VBOHandle,))
        glDeleteBuffers(1, (self.EBOHandle,))
        
        if hasattr(self, 'TextureHandle') and self.TextureHandle > 0:
            glDeleteTextures(1, (self.TextureHandle,))
        
        self.TriangleShader.Release()

        pg.quit()



if __name__ == "__main__":

    try:
        app = SDLApp()

        app.SetupRender()

        app.Run()
    except Exception as e:
        print(str(e))

    finally:
        app.Finish()