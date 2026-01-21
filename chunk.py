import config
from OpenGL.GL import *
import numpy as np


class Chunk:
    def __init__(self, world, position):
        self._position = position
        self._world_position_offset = (
            self._position[0] * config.CHUNK_WIDHT,
            self._position[1] * config.CHUNK_HEIGHT,
            self._position[2] * config.CHUNK_LENGHTH
        )

        self._world = world

        self.blocks = [
			[
				[0 for z in range(config.CHUNK_LENGHTH)]  # 初始化为0
				for y in range(config.CHUNK_HEIGHT)
			]
			for x in range(config.CHUNK_WIDHT)
		]

        self._init_raw_data()

        self._vao = glGenVertexArrays(1)
        # 定点缓冲
        self._vertex_vbo = glGenBuffers(1)
        # 纹理缓冲
        self._tex_coord_vbo = glGenBuffers(1)
        # 光照缓冲
        self._shading_vbo = glGenBuffers(1)
        # 索引缓冲
        self._indicat_vbo = glGenBuffers(1)


    def _init_raw_data(self):
        self._raw_mesh_vertex_position = []
        self._raw_mesh_tex_coord = []
        self._raw_mesh_shading_value = []

        self._mesh_index_counter = 0
        self._mesh_indicates = []

    
    def _add_face(self, faceid, block_type, wx, wy, wz):
        """
        将blocktype蓝图实例化为具体的方块
        """

        # 实例化定点
        vertex_positions = block_type.vertices[faceid].copy() #config.template_vertex_positions[faceid].copy()

        for i in range(4):
            vertex_positions[i*3 + 0] += wx
            vertex_positions[i*3 + 1] += wy
            vertex_positions[i*3 + 2] += wz

        self._raw_mesh_vertex_position.extend(vertex_positions)

        # 实例化索引
        indices = [0, 1, 2, 0, 2, 3]
        for i in range(6):
            indices[i] += self._mesh_index_counter

        self._mesh_indicates.extend(indices)
        self._mesh_index_counter += 4

        # 实例化纹理坐标
        self._raw_mesh_tex_coord.extend(block_type.texcoord[faceid])
        # 实例化光照
        self._raw_mesh_shading_value.extend(block_type.shading_values[faceid])


    def update_mesh(self):
        for c_x in range(config.CHUNK_WIDHT):
            for c_y in range(config.CHUNK_HEIGHT):
                for c_z in range(config.CHUNK_LENGHTH):
                    block_number = self.blocks[c_x][c_y][c_z]

                    if block_number:
                        block_type = self._world.block_types[block_number]
                        if not block_type:
                            continue

                        wx, wy, wz = (
                            self._world_position_offset[0] + c_x,
                            self._world_position_offset[1] + c_y,
                            self._world_position_offset[2] + c_z,
                        )

                        if not self._world.get_block_number(wx + 1, wy, wz):
                            self._add_face(0, block_type, wx, wy, wz)
                        if not self._world.get_block_number(wx - 1, wy, wz):
                            self._add_face(1, block_type, wx, wy, wz)
                        if not self._world.get_block_number(wx, wy + 1, wz):
                            self._add_face(2, block_type, wx, wy, wz)
                        if not self._world.get_block_number(wx, wy - 1, wz):
                            self._add_face(3, block_type, wx, wy, wz)
                        if not self._world.get_block_number(wx, wy, wz + 1):
                            self._add_face(4, block_type, wx, wy, wz)
                        if not self._world.get_block_number(wx, wy, wz - 1):
                            self._add_face(5, block_type, wx, wy, wz)

        # 啥都没生成出来，是有可能的，例如chunk被四面八方的chunk给包围住了并且不留空隙        
        if len(self._mesh_indicates) == 0:
            return

        # 上传几何数据
        glBindVertexArray(self._vao)
        # local =0 放置顶点缓冲数据
        glBindBuffer(GL_ARRAY_BUFFER, self._vertex_vbo)
        mesh_vertex_position = np.array(self._raw_mesh_vertex_position, np.float32)
        glBufferData(GL_ARRAY_BUFFER, mesh_vertex_position.nbytes, mesh_vertex_position, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * mesh_vertex_position.dtype.itemsize, None)
        glEnableVertexAttribArray(0)
        # local = 1 放置纹理坐标缓冲
        glBindBuffer(GL_ARRAY_BUFFER, self._tex_coord_vbo)
        tex_coord= np.array(self._raw_mesh_tex_coord, np.float32)
        glBufferData(GL_ARRAY_BUFFER, tex_coord.nbytes, tex_coord, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * tex_coord.dtype.itemsize, None)
        glEnableVertexAttribArray(1)
        # local =2 放置光照参数
        glBindBuffer(GL_ARRAY_BUFFER, self._shading_vbo)
        shading_value = np.array(self._raw_mesh_shading_value, np.float32)
        glBufferData(GL_ARRAY_BUFFER, shading_value.nbytes, shading_value, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 1 * shading_value.dtype.itemsize, None)
        glEnableVertexAttribArray(2)
        # 最后更新缩影
        indecates = np.array(self._mesh_indicates, np.uint32)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._indicat_vbo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indecates.nbytes, indecates, GL_STATIC_DRAW)

    
    def draw(self):
        if len(self._mesh_indicates) == 0:
            return
        
        glBindVertexArray(self._vao)
        glDrawElements(GL_TRIANGLES, len(self._mesh_indicates), GL_UNSIGNED_INT, None)



