
import numpy as np
from ChunkMesh import ChunkMesh
import glm
import Config
from VoxelBuilder import VoxelBuilder
from ChunkMeshContext import *
from ChunkMesh import *
from Scene import *

class Chunk:
    """
    管理世界中的一个区块的体素数据以及他们的mesh渲染
    """
    def __init__(self, position):
        self.Voxels : np.array = None
        self.Mesh : ChunkMesh = None
        self.Scene : Scene = None
        self.Position = position
        self.MatModel = glm.translate(glm.mat4(), glm.vec3(self.Position) * Config.CHUNK_SIZE)

    def BuildVoxels(self):
        self.Voxels = VoxelBuilder.BuildVoxel(self.Position)

        Context = ChunkMeshContext(self)

        self.Mesh = ChunkMesh()
        self.Mesh.Setup(Context)


    def BuildMesh(self):
        pass

    def Render(self):
        self.Mesh.Render()