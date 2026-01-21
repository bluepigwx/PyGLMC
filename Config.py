import glm
import numpy as np

# 窗口配置
WINDOW_RES = (1024, 768)


# 控制配置
MOVE_SPEED = 0.01
MOUSE_SENSITIVITY = 0.2
PITCH_MAX = 89

# 相机配置
NEAR_CULL = 0.1
FAR_CULL = 2000.0
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV


#Chunk配置
CHUNK_WIDHT = 16
CHUNK_HEIGHT = 16
CHUNK_LENGHTH = 16
