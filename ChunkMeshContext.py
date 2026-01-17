from Mesh import *
import glm
from OpenGL.GL import *
from Shader import *
import Config



class ChunkMeshContext(CreateMeshContext):
    def __init__(self, Chunk):
        super().__init__()

        self.Chunk = Chunk


    def GetChunkIndex(self, WorldVoxelPos):
        wx, wy, wz = WorldVoxelPos
        cx = wx // Config.CHUNK_SIZE
        cy = wy // Config.CHUNK_SIZE
        cz = wz // Config.CHUNK_SIZE
        if not (0 <= cx < Config.WORLD_CHUNK_W and 0 <= cy < Config.WORLD_H and 0 <= cz < Config.WORLD_CHUNK_D):
            return -1

        index = cx + Config.WORLD_CHUNK_W * cz + Config.WORLD_AREA * cy
        return index


    def IsVoid(self, LocalVoxelPos, WorldVoxelPos):
        # 目标ChunkIndex可能是当前体素所在的Chunk，也可能是邻居Chunk
        TargetChunkIndex = self.GetChunkIndex(WorldVoxelPos)
        if TargetChunkIndex ==-1:
            return False    #触到世界边际了
        
        # 目标Chunk的体素集合
        TargetChunkVoxels = self.Chunk.Scene.Chunks[TargetChunkIndex]
        x, y, z = LocalVoxelPos
        # xyz坐标对CHUN_SIZE取模，如果是到了邻居Chunk的体素坐标里，那么就开始重头计算
        # 例如x=31，在自己的Chunk边缘，如果x=32，那么取模后则在邻居Chunk的开始第一格
        TargetVoxelIndex = x % Config.CHUNK_SIZE + z % Config.CHUNK_SIZE * Config.CHUNK_SIZE + y % Config.CHUNK_SIZE * Config.CHUNK_AREA
        if TargetChunkVoxels.Voxels[TargetVoxelIndex]:
            return False    # 有东西了
        
        return True


    def AddData(self, index, *vertexArray):
        for vertex in vertexArray:
            for attr in vertex:
                self.Vertices[index] = attr
                index += 1
        
        return index
        

    def GenVertices(self):
        self.Vertices = np.empty(Config.CHUNK_VOL * 18 * 5, dtype='uint8')
        NumVerticeAttr = 0
        index = 0

        # 为每一个暴露在空气中没有被阻挡的体素格子生成顶点属性数据
        for x in range(Config.CHUNK_SIZE):
            for y in range(Config.CHUNK_SIZE):
                for z in range(Config.CHUNK_SIZE):
                    VoxelIndex = self.Chunk.Voxels[x + Config.CHUNK_SIZE * z + Config.CHUNK_AREA * y]

                    # 空格子跳过
                    if not VoxelIndex:
                        continue

                    #转换到世界坐标
                    cx, cy, cz = self.Chunk.Position
                    wx = x + cx * Config.CHUNK_SIZE
                    wy = y + cy * Config.CHUNK_SIZE
                    wz = z + cz * Config.CHUNK_SIZE

                    # top face
                    if self.IsVoid((x, y + 1, z), (wx, wy + 1, wz)):
                         # format: x, y, z, VoxelIndex, face_id
                        v0 = (x    , y + 1, z    , VoxelIndex, 0)
                        v1 = (x + 1, y + 1, z    , VoxelIndex, 0)
                        v2 = (x + 1, y + 1, z + 1, VoxelIndex, 0)
                        v3 = (x    , y + 1, z + 1, VoxelIndex, 0)
                        index = self.AddData(index, v0, v3, v2, v0, v2, v1)
                    
                    # bottom face
                    if self.IsVoid((x, y - 1, z), (wx, wy - 1, wz)):
                        v0 = (x    , y, z    , VoxelIndex, 1)
                        v1 = (x + 1, y, z    , VoxelIndex, 1)
                        v2 = (x + 1, y, z + 1, VoxelIndex, 1)
                        v3 = (x    , y, z + 1, VoxelIndex, 1)
                        index = self.AddData(index, v0, v2, v3, v0, v1, v2)

                    # right face
                    if self.IsVoid((x + 1, y, z), (wx + 1, wy, wz)):
                        v0 = (x + 1, y    , z    , VoxelIndex, 2)
                        v1 = (x + 1, y + 1, z    , VoxelIndex, 2)
                        v2 = (x + 1, y + 1, z + 1, VoxelIndex, 2)
                        v3 = (x + 1, y    , z + 1, VoxelIndex, 2)
                        index = self.AddData(index, v0, v1, v2, v0, v2, v3)

                    # left face
                    if self.IsVoid((x - 1, y, z), (wx - 1, wy, wz)):
                        v0 = (x, y    , z    , VoxelIndex, 3)
                        v1 = (x, y + 1, z    , VoxelIndex, 3)
                        v2 = (x, y + 1, z + 1, VoxelIndex, 3)
                        v3 = (x, y    , z + 1, VoxelIndex, 3)
                        index = self.AddData(index, v0, v2, v1, v0, v3, v2)

                    # back face
                    if self.IsVoid((x, y, z - 1), (wx, wy, wz - 1)):
                        v0 = (x,     y,     z, VoxelIndex, 4)
                        v1 = (x,     y + 1, z, VoxelIndex, 4)
                        v2 = (x + 1, y + 1, z, VoxelIndex, 4)
                        v3 = (x + 1, y,     z, VoxelIndex, 4)
                        index = self.AddData(index, v0, v1, v2, v0, v2, v3)

                    # front face
                    if self.IsVoid((x, y, z + 1), (wx, wy, wz + 1)):
                        v0 = (x    , y    , z + 1, VoxelIndex, 5)
                        v1 = (x    , y + 1, z + 1, VoxelIndex, 5)
                        v2 = (x + 1, y + 1, z + 1, VoxelIndex, 5)
                        v3 = (x + 1, y    , z + 1, VoxelIndex, 5)
                        index = self.AddData(index, v0, v2, v1, v0, v3, v2)

        self.Vertices = self.Vertices[:index + 1]
        return self.Vertices


    def GenShaderProgram(self):
        self.Program = Shader("Shaders/ChunkVertexShader.vs", "Shaders/ChunkFragmentShader.fs")
        return self.Program

    def GenVAO(self):
        self.GenVertices()

        stride = 5

        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.Vertices.nbytes, self.Vertices.ptr, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_UNSIGNED_BYTE, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 1, GL_UNSIGNED_BYTE, GL_FALSE, stride, ctypes.c_void_p(3))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 1, GL_UNSIGNED_BYTE, GL_FALSE, stride, ctypes.c_void_p(4))
        glEnableVertexAttribArray(2)

        #unbind
        glBindBuffer(0)
        glBindVertexArray(0)

        return self.VAO