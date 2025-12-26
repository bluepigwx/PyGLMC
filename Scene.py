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
        # 每个分区包含的体素数据，支持2^8种不同的体素类型
        self.Voxels = np.empty([Config.WORLD_VOL, Config.CHUNK_VOL], dtype="uint8")

    def BuildChunk(self):
        for x in Config.WORLD_W:
            for y in Config.WORLD_H:
                for z in Config.WORLD_D:
                    ChunkIndex = x + Config.WORLD_W * z + Config.WORLD_AREA * y
                    NewChunk = Chunk(x, y, z)
                    self.Chunks[ChunkIndex] = NewChunk

                    self.Voxels[ChunkIndex] = NewChunk.BuildVoxels()

                    NewChunk.BuildMesh()


    def Render(self):
        for Chunk in self.Chunks:
            Chunk.Render()