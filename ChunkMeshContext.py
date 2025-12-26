from Mesh import *
import glm
from OpenGL.GL import *
from Shader import *


class ChunkMeshContext(CreateMeshContext):
    def __init__(self):
        super().__init__()

    def GenVertices(self):
        self.Vertices = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint8')

    def GenShaderProgram(self):
        pass

    def GenVAO(self):
        pass