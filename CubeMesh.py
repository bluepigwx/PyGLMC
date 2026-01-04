from Mesh import *
from OpenGL.GL import *

class CubeMesh(Mesh):
    def __init__(self):
        pass

    def Setup(self, Context):
        self.Program = Context.GenShaderProgram()
        self.VAO = Context.GenVAO()

    def Render(self):
        glBindVertexArray(self.VAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)

