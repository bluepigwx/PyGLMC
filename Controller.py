import glm
import pygame as pg
import config

class Controller:
    """
    处理外部输入
    """
    def __init__(self):
        self._position = glm.vec3(0, 1, 10)
        self._right = glm.vec3(1, 0, 0)
        self._up = glm.vec3(0, 1, 0)
        self._forward = glm.vec3(0, 0, -1)

        self._yaw = -90
        self._pitch = 0
        
        self._update_vectors()

    def bind_camera(self, camera):
        self._camera = camera

    def _move_forward(self, value):
        self._position += self._forward * value

    def _move_right(self, value):
        self._position += self._right * value

    def _rotate_yaw(self, value):
        self._yaw += value

    def _rotate_pitch(self, value):
        self._pitch -= value
        self._pitch = glm.clamp(self._pitch, -config.PITCH_MAX, config.PITCH_MAX)

    def _keyboard_process(self, delta):
        key_states = pg.key.get_pressed()

        value = delta * config.MOVE_SPEED

        if key_states[pg.K_w]:
            self._move_forward(value)
        if key_states[pg.K_s]:
            self._move_forward(-value)
        if key_states[pg.K_a]:
            self._move_right(-value)
        if key_states[pg.K_d]:
            self._move_right(value)


    def _mouse_process(self):
        dx, dy = pg.mouse.get_rel()

        if dx:
            self._rotate_yaw(dx * config.MOUSE_SENSITIVITY)
        if dy:
            self._rotate_pitch(dy * config.MOUSE_SENSITIVITY)
        

    def _update_vectors(self):
        self._forward.x = glm.cos(glm.radians(self._yaw)) * glm.cos(glm.radians(self._pitch))
        self._forward.y = glm.sin(glm.radians(self._pitch))
        self._forward.z = glm.sin(glm.radians(self._yaw)) * glm.cos(glm.radians(self._pitch))
        
        self._forward = glm.normalize(self._forward)
        self._right = glm.normalize(glm.cross(self._forward, glm.vec3(0, 1, 0)))
        self._up = glm.normalize(glm.cross(self._right, self._forward))


    def update(self, delta):
        self._keyboard_process(delta)
        self._mouse_process()

        self._update_vectors()

        if self._camera:
            self._camera.update(self._position, self._forward, self._up)