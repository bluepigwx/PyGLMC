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
        wx, wy, wz = world_voxel_pos
        cx = wx // CHUNK_SIZE
        cy = wy // CHUNK_SIZE
        cz = wz // CHUNK_SIZE
        if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
            return -1

        index = cx + WORLD_W * cz + WORLD_AREA * cy
        return index

    def IsVoid(self, LocalVoxelPos, WorldVoxelPos):
        # 目标ChunkIndex可能是当前体素所在的Chunk，也可能是邻居Chunk
        TargetChunkIndex = self.GetChunkIndex(WorldVoxelPos)
        if not TargetChunkIndex:
            return False    #触到世界边际了
        
        # 目标Chunk的体素集合
        TargetChunkVoxels = self.Chunk.Scene.Chunks[TargetChunkIndex]
        x, y, z = LocalVoxelPos
        # xyz坐标对CHUN_SIZE取模，如果是到了邻居Chunk的体素坐标里，那么就开始重头计算
        # 例如x=31，在自己的Chunk边缘，如果x=32，那么取模后则在邻居Chunk的开始第一格
        TargetVoxelIndex = x % Config.CHUNK_SIZE + 
                            z % Config.CHUNK_SIZE * Config.CHUNK_SIZE + 
                            y % Config.CHUNK_SIZE * Config.CHUNK_AREA
        
        if TargetChunkVoxels[TargetVoxelIndex]:
            return False    # 有东西了
        
        return True
        

        

    def GenVertices(self):
        self.Vertices = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint8')
        NumVerticeAttr = 0

        # 为每一个暴露在空气中没有被阻挡的体素格子生成顶点属性数据
        for x in range(Config.CHUNK_SIZE):
            for y in range(Config.CHUNK_SIZE):
                for z in range(Config.CHUNK_SIZE):
                    VoxelIndex = self.Chunk.Voxels[x + Config.CHUNK_SIZE*Z + Config.CHUNK_AREA]

                    # 空格子跳过
                    if not VoxelIndex:
                        continue

                    #转换到世界坐标
                    cx, cy, cz = self.Chunk.Position
                    wx = x + cx * Config.CHUNK_SIZE
                    wy = y + cy * Config.CHUNK_SIZE
                    wz = z + cz * Config.CHUNK_SIZE





                    


    def GenShaderProgram(self):
        pass

    def GenVAO(self):
        pass