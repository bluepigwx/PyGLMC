
import numpy as np
import glm
import Config

class VexelBuilder:
    @staticmethod
    def BuildVoxel(Position):
        voxels = np.zeros(Config.CHUNK_VOL, dtype="uint8")

        cx, cy, cz = glm.ivec3(Position) * Config.CHUNK_SIZE

        for x in range(Config.CHUNK_SIZE):
            wx = x + cx
            for z in range(Config.CHUNK_SIZE):
                wz = z + cz
                world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)
                local_height = min(world_height - cy, Config.CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    voxels[x + Config.CHUNK_SIZE * z + Config.CHUNK_AREA * y] = wy + 1
        
        return voxels