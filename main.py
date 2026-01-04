import pygame as pg
from OpenGL.GL import *
import glm
from Shader import *
from Controller import *
from Mesh import *
from CubeMesh import *
from TestContext import *


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
        self.Ctl = Controller()


    def SetupRender(self):
        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)

        TestCxt = TestCubeCreateContext()
        self.TestCube = CubeMesh()
        self.TestCube.Setup(TestCxt)
        
        # Load texture
        self.TextureHandle = LoadTexture("Pic/Wall.png")
        if self.TextureHandle == 0:
            raise RuntimeError(f"Load Pic Wall failed")

        self.TextureHandle1 = LoadTexture("Pic/Rock.png")
        if self.TextureHandle1 == 0:
            raise RuntimeError(f"Load Pic Rock failed")
        
        
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
        self.TestCube.Program.Use()
        self.TestCube.Program.Uniform1i("TextureUnit0", 0)
        self.TestCube.Program.Uniform1i("TextureUnit1", 1)

        # Bind texture
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.TextureHandle)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.TextureHandle1)

        for i in range(len(CubePositions)):
            
            Model = glm.mat4(1.0)

            Rotation = pg.time.get_ticks() / 1000
            Model = glm.translate(Model, CubePositions[i])
 
            self.TestCube.Program.UniformMat4fv("Model", Model)
  
            self.TestCube.Render()
        

        self.TestCube.Program.UniformMat4fv("View", self.Ctl.Camare.ViewMat)
        self.TestCube.Program.UniformMat4fv("Projection", self.Ctl.Camare.ProjecMat)


    def Run(self):
        Running = True

        while Running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Running = False

            delta = self.clock.tick()
            self.Ctl.Update(delta)

            self.BeginRender()

            self.Draw()

            self.EndRender()

            #self.clock.tick(60)


    def Finish(self):
        # Clean up textures
        if hasattr(self, 'TextureHandle') and self.TextureHandle > 0:
            glDeleteTextures(1, (self.TextureHandle,))
        
        if hasattr(self, 'TextureHandle1') and self.TextureHandle1 > 0:
            glDeleteTextures(1, (self.TextureHandle1,))
        
        # Clean up mesh resources (VAO, VBO are managed by TestCube)
        if hasattr(self, 'TestCube') and hasattr(self.TestCube, 'VAO'):
            glDeleteVertexArrays(1, (self.TestCube.VAO,))
        
        # Clean up shader program
        if hasattr(self, 'TestCube') and hasattr(self.TestCube, 'Program'):
            self.TestCube.Program.Release()

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
        