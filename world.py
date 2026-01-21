import block_type
import chunk
import config
import texture_mgr
import random
import models.plant
import models.cactus


class World:
    def __init__(self):
        self.texture_mgr = texture_mgr.TextureMgr(16, 16, 256)
        self.texture_mgr.init()

        # 注册所有的方块类型
        self.block_types = [None] # 0 -- 空气
        self.block_types.append(block_type.BlockType(self.texture_mgr, "cobblestone", {"all": "cobblestone"}))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "grass", {"top": "grass", "bottom": "dirt", "sides": "grass_side"}))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "grass_block", {"all": "grass"}))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "dirt", {"all": "dirt"}))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "stone", {"all": "stone"}))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "sand", {"all": "sand"}))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "planks", {"all": "planks"}))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "log", {"top": "log_top", "bottom": "log_top", "sides": "log_side"}))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "daisy", {"all": "daisy"}, models.plant))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "rose", {"all": "rose"}, models.plant))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "cactus", {"top": "cactus_top", "bottom": "cactus_bottom", "sides": "cactus_side"}, models.cactus,))
        self.block_types.append(block_type.BlockType(self.texture_mgr, "dead_bush", {"all": "dead_bush"}, models.plant))
        
        self.texture_mgr.gen_mipmap()

        self._chunks = {}

        for x in range(2):
            for z in range(2):
                chunk_position = (x - 1, -1, z - 1)

                new_chunk = chunk.Chunk(self, chunk_position)

                for i in range(config.CHUNK_WIDHT):
                    for j in range(config.CHUNK_HEIGHT):
                        for k in range(config.CHUNK_LENGHTH):
                            if j == 15:
                                new_chunk.blocks[i][j][k] = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 12, 11])
                            elif j == 14:
                                new_chunk.blocks[i][j][k] = random.choice([6, 2, 2, 2, 2, 2])
                            elif j >12:
                                new_chunk.blocks[i][j][k] = random.choice([0, 6])
                            else:
                                new_chunk.blocks[i][j][k] = random.choice([0, 0, 5])

                
                self._chunks[chunk_position] = new_chunk

        for _, c in self._chunks.items():
            c.update_mesh()


    def get_block_number(self, x, y, z):
        """
        获得指定世界坐标的方块类型
        """
        cx = x // config.CHUNK_WIDHT
        cy = y // config.CHUNK_HEIGHT
        cz = z // config.CHUNK_LENGHTH

        bx = x % config.CHUNK_WIDHT
        by = y % config.CHUNK_HEIGHT
        bz = z % config.CHUNK_LENGHTH

        # 检查 chunk 是否存在，如果不存在返回 0（空气）
        chunk_pos = (cx, cy, cz)
        if chunk_pos not in self._chunks:
            return 0
        
        cur_chunk = self._chunks[chunk_pos]
        return cur_chunk.blocks[bx][by][bz]


    def draw(self):
        for _, c in self._chunks.items():
            c.draw()










