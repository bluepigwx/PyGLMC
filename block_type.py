import config
import glm

class BlockType:
    """
    方块的蓝图定义类
    """
    def __init__(self, texture_mgr, name="unknow", block_face_textures={"all":"cobblestone"}):
        self._name = name
        self.vertices = config.vertex_positions
        self.indices = config.indices
        self.texcoord = glm.array(config.tex_coords)
        self.shading_values = config.shading_values

        def set_block_face(face_id, tex_layer):
            """
            设置方块的face_id使用哪个tex_layer
            """
            for i in range(4):
                self.texcoord[face_id * 12 + i * 3 + 2] = tex_layer

        for face in block_face_textures:
            texture_name = block_face_textures[face]
            tex_layer = texture_mgr.add_texture(texture_name)

            if face == "all":
                set_block_face(0, tex_layer)
                set_block_face(1, tex_layer)
                set_block_face(2, tex_layer)
                set_block_face(3, tex_layer)
                set_block_face(4, tex_layer)
                set_block_face(5, tex_layer)
            elif face == "sides":
                set_block_face(0, tex_layer)
                set_block_face(1, tex_layer)
                set_block_face(4, tex_layer)
                set_block_face(5, tex_layer)
            else:
                set_block_face(["right", "left", "top", "bottom", "front", "back"].index(face), tex_layer)