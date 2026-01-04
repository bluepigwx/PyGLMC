
import glm
import Config


class Camera:
    def __init__(self):
        aspect_ratio = Config.SCREEN_WIDHT / Config.SCREEN_HEIGHT
        self.ProjecMat = glm.perspective(Config.V_FOV, aspect_ratio, Config.NEAR_CULL, Config.FAR_CULL)
        self.ViewMat = glm.mat4()

    def MakeViewMat(self, position, forward, up):
        self.ViewMat = glm.lookAt(position, forward, up)


