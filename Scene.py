import Config
import numpy as np
from Chunk import Chunk


class Scene:
    """
    按区块Chunk来分管场景，尽量减少一次性投递到显卡的数据
    """
    def __init__(self):
        # 场景的初始分区
        self.Chunks = [None for _ in Config.WORLD_VOL]
        # 每个分区包含的体素数据，使用uint8支持2^8种不同的体素类型
        # 初始化一个二维数组，用来按ChunkId为索引来存放场景中各个Chunk的体素
        self.Voxels = np.empty([Config.WORLD_VOL, Config.CHUNK_VOL], dtype="uint8")


    def BuildChunk(self):
        for cx in Config.WORLD_CHUNK_W:
            for cy in Config.WORLD_CHUNK_H:
                for cz in Config.WORLD_CHUNK_D:
                    ChunkIndex = cx + Config.WORLD_CHUNK_W * cz + Config.WORLD_AREA * cy
                    NewChunk = Chunk(self, cx, cy, cz)
                    self.Chunks[ChunkIndex] = NewChunk
                    
                    self.Voxels[ChunkIndex] = NewChunk.BuildVoxels()

                    NewChunk.BuildMesh()


    def Render(self):
        for Chunk in self.Chunks:
            Chunk.Render()

