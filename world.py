import block_type
import chunk
import config
import texture_mgr
import random
import models.plant
import models.cactus
import math


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

        self.chunks = {}

        for x in range(2):
            for z in range(2):
                chunk_position = (x - 1, -1, z - 1)

                new_chunk = chunk.Chunk(self, chunk_position)

                for i in range(config.CHUNK_WIDHT):
                    for j in range(config.CHUNK_HEIGHT):
                        for k in range(config.CHUNK_LENGHTH):
                            if j == 15:
                                new_chunk.blocks[i][j][k] = random.choices([0, 9, 10], [20, 2, 1])[0]
                            elif j == 14:
                                new_chunk.blocks[i][j][k] =2
                            elif j >10:
                                new_chunk.blocks[i][j][k] = 4
                            else:
                                new_chunk.blocks[i][j][k] = 5

                
                self.chunks[chunk_position] = new_chunk

        for _, c in self.chunks.items():
            c.update_subchunk_mesh()
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
        if chunk_pos not in self.chunks:
            return 0
        
        cur_chunk = self.chunks[chunk_pos]
        return cur_chunk.blocks[bx][by][bz]
    
    
    def get_chunk_position(self, wposition):
        """
        世界坐标到chunk之间的转换
        """
        wx, wy, wz = wposition
        return (
            math.floor(wx / config.CHUNK_WIDHT),
            math.floor(wy / config.CHUNK_HEIGHT),
            math.floor(wz / config.CHUNK_LENGHTH)
        )
        
        
    def get_block_pos_in_chunk(self, wpostion):
        """
        获得block在自己所在chunk中的相对位置
        """
        wx, wy, wz = wpostion
        return (
            int(wx % config.CHUNK_WIDHT),
            int(wy % config.CHUNK_HEIGHT),
            int(wz % config.CHUNK_LENGHTH)
        )
        
    
    def is_opaque_block(self, wposition):
        """
        指定世界坐标的block是否为不透明体
        """
        wx, wy, wz = wposition
        block_num = self.get_block_number(wx, wy, wz)
        
        block_type = self.block_types[block_num]
        if not block_type:
            return False
        
        return not block_type.transparent
    
    
    def set_block(self, wposition, block_num):
        """
        外部修改block的接口
        """
        wx, wy, wz = wposition
        
        chunk_position = self.get_chunk_position(wposition)
        if chunk_position not in self.chunks:
            if block_num == 0:
                return # 在虚空位置删除方块忽略
            
            #创建新的chunk
            self.chunks[chunk_position] = chunk.Chunk(self, chunk_position)
            
        if self.get_block_number(wx, wy, wz) == block_num:
            return
        
        blx, bly, blz = self.get_block_pos_in_chunk(wposition)
        self.chunks[chunk_position].blocks[blx][bly][blz] = block_num
        self.chunks[chunk_position].update_at_position((wx, wy, wz))
        self.chunks[chunk_position].update_mesh()
        
        cx, cy, cz = chunk_position
        # 如果修改到邻居chunk了，那么相邻的chunk也需要作出修改
        def try_update_chunk_at_position(chunk_position, position):
            if chunk_position in self.chunks:
                self.chunks[chunk_position].update_at_position(position)
                self.chunks[chunk_position].update_mesh()

        if blx == config.CHUNK_WIDHT - 1:
            try_update_chunk_at_position((cx + 1, cy, cz), (wx + 1, wy, wz))
        if blx == 0:
            try_update_chunk_at_position((cx - 1, cy, cz), (wx - 1, wy, wz))

        if bly == config.CHUNK_HEIGHT - 1:
            try_update_chunk_at_position((cx, cy + 1, cz), (wx, wy + 1, wz))
        if bly == 0:
            try_update_chunk_at_position((cx, cy - 1, cz), (wx, wy - 1, wz))

        if blz == config.CHUNK_LENGHTH - 1:
            try_update_chunk_at_position((cx, cy, cz + 1), (wx, wy, wz + 1))
        if blz == 0:
            try_update_chunk_at_position((cx, cy, cz - 1), (wx, wy, wz - 1))



    def draw(self):
        for _, c in self.chunks.items():
            c.draw()










