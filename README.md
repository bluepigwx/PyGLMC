# PyGLMC

场景Scene对象包含所有体素数据，但为了优化一次渲染提交的数据，把场景切割成了多个Chunk区块，一次往显卡提交的数据是一个可见Chunk的全部定点数据，
而不是整个场景的定点数据，因此场景结构表示为：
Scene:
    Chunk1
        ChunkMesh1
        Voxel1
    Chunk2
        ChunkMesh2
        Voxel2
        