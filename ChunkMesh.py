from Mesh import *



class ChunkMesh(Mesh):
    def __init__(self):
        pass

    def Setup(self, Context):
        self.Program = Context.GenShaderProgram()
        self.VAO = Context.GenVAO()
    
    def Render(self):
        glBindVertexArray(self.VAO)
        glDrawArrays()