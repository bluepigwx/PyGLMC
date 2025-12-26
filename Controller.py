
from Camera import Camera
import glm
import pygame as pg
import Config

class Controller:
    """
    接受外部输入，根据上下文作用于不同对象上，通常是控制相机与角色
    """
    def __init__(self):
        self.Position = glm.vec3()
        self.Yaw = 0
        self.Pitch = 0

        self.Up = glm.vec3(0, 1, 0)
        self.Right = glm.vec3(1, 0, 0)
        self.Forward = glm.vec3(0, 0, -1)
    
        self.Camare = Camera()

    def Update(self, delta):
        self.KeyboradControle(delta)
        self.MouseControle()

        self.Forward.x = glm.cos(self.Yaw) * glm.cos(self.Pitch)
        self.Forward.y = glm.sin(self.Pitch)
        self.Forward.z = glm.sin(self.Yaw) * glm.cos(self.Pitch)
        self.Forward = glm.normalize(self.Forward)

        self.Right = glm.normalize(glm.cross(self.Forward, glm.vec3(0, 1, 0)))
        self.Up = glm.normalize(glm.cross(self.Right, self.Forward))

        self.Camare.MakeViewMat(self.Position, self.Position-self.Forward, self.Up)


    def _MoveForward(self, Vel):
        self.Position -= self.Forward * Vel

    def _MoveBack(self, Vel):
        self.Position += self.Forward * Vel

    def _MoveRight(self, Vel):
        self.Position -= self.Right * Vel

    def _MoveLeft(self, Vel):
        self.Position += self.Right * Vel

    def _RotateYaw(self, delta):
        self.Yaw += delta


    def _RotatePitch(self, delta):
        self.Pitch += delta
        self.Pitch = glm.clamp(self.Pitch, -Config.PITCH_MAX, Config.PITCH_MAX)


    def KeyboradControle(self, delta):
        KeyStates = pg.key.get_pressed()
        # 后面改到InputComponent里面
        Vel = Config.MOVE_SPEED * delta
        if KeyStates[pg.K_w]:
            self._MoveForward(Vel)
        if KeyStates[pg.K_a]:
            self._MoveLeft(Vel)
        if KeyStates[pg.K_s]:
            self._MoveBack(Vel)
        if KeyStates[pg.K_d]:
            self._MoveRight(Vel)


    def MouseControle(self):
        # 后面改到InputComponent里面
        Mouse_dx, Mouse_dy = pg.mouse.get_rel()
        if Mouse_dx:
            self._RotateYaw(Mouse_dx * 0.002)
        if Mouse_dy:
            self._RotatePitch(Mouse_dy * 0.002)

