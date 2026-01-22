# PyGLMC

场景World对象包含所有体素数据，但为了优化一次渲染提交的数据，把场景切割成了多个Chunk区块，一次往显卡提交的数据是一个可见Chunk的全部几何数据，而不是整个场景的定点数据，因此场景结构表示为：
World:
    Chunk1
        [SubChunk]
        ChunkMesh1
        Voxel1
    Chunk2
        [SubChunk]
        ChunkMesh2
        Voxel2

为什么将World场景划分为了Chunk，SubChunk，这是从CPU和GPU之间的性能平衡来考虑。但进行体素增删的时候，需要尽可能小的重建数据，这时候就需要在SubChunk上进行修改操作，否则需要重新整个Chunk的定点数据，当构建完数据往显卡发送数据的时候则更希望将整个Chunk作为一个整体发送过去，以减少DrawCall的调用次数。所以将一个Chunk划分为SubChunk（CPU友好）和ChunkMesh（GPU友好）分别用于程序的不同阶段
        