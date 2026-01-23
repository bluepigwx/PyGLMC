import pygame as pg
from OpenGL.GL import *
import config
import shader
import camera
import controller
import world
import hit
import math
import glm


class Application:
    def __init__(self):
        self._run = False
        
        self.holding = 7
        self._mouse_grabbed = True  # 鼠标锁定状态


    def init(self):
        pg.init()

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

        pg.display.set_mode(config.WINDOW_RES, pg.OPENGL | pg.DOUBLEBUF)

        glClearColor(0.1, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)

        self._clock = pg.time.Clock()
        self._run = True

        self._world = world.World()
        print(f"try load map data")
        self._world.load_map()
        print(f"try build shaders")
        self._shader = shader.Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
        self._shader.use()

        self._shader_sampler_location = self._shader.get_uniform("texture_array_sampler")

        print(f"init camera")
        self._camera = camera.Camera()
        self._camera.bind_shader(self._shader)

        print(f"init controller")
        self._controller = controller.Controller()
        self._controller.bind_camera(self._camera)
        

    def run(self):
        while self._run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    self._process_mouse_down(event)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        # 切换鼠标锁定状态
                        self._mouse_grabbed = not self._mouse_grabbed
                        pg.event.set_grab(self._mouse_grabbed)
                        pg.mouse.set_visible(not self._mouse_grabbed)
                    elif event.key == pg.K_h:
                        self._controller._position = glm.vec3(0, 100, 10)
                    elif event.key == pg.K_1:
                        self.holding = 1
                    elif event.key == pg.K_2:
                        self.holding = 2
                    elif event.key == pg.K_3:
                        self.holding = 3
                    elif event.key == pg.K_4:
                        self.holding = 4
                    elif event.key == pg.K_5:
                        self.holding = 5
                    elif event.key == pg.K_6:
                        self.holding = 6
                    elif event.key == pg.K_7:
                        self.holding = 7
                    elif event.key == pg.K_8:
                        self.holding = 8
                    elif event.key == pg.K_9:
                        self.holding = 9
            
            delta = self._clock.tick()

            self._update(delta)

            self._begin_render()
            self._draw(delta)
            self._end_render()
            
    def _process_mouse_down(self, mouse_event):
        button = mouse_event.button
        
        def hit_callback(cur_block, next_block):
            if button == 1:
                #右键
                print(f"放置方块在 {cur_block}")
                self._world.set_block(cur_block, self.holding)
            elif button == 3:
                #左键
                print(f"击中方块 {next_block}")
                self._world.set_block(next_block, 0)

        # 将角度制转换为弧度制
        rotate_yaw = math.radians(self._controller._yaw)
        rotate_pitch = math.radians(self._controller._pitch)
        hit_ray = hit.Hit_ray(self._world, (rotate_yaw, rotate_pitch), self._controller._position)
        while hit_ray.distance < hit.HIT_RANGE:
            if hit_ray.step(hit_callback):
                break


    def _update(self, delta):
        self._controller.update(delta)


    def _begin_render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    def _end_render(self):
        pg.display.flip()


    def _draw(self, delta):
        self._shader.use()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self._world.texture_mgr.texture_array)
        glUniform1i(self._shader_sampler_location, 0)

        self._world.draw()


    def exit(self):
        if not self._run:
            return
        
        pg.quit()


if __name__ == "__main__":
    try:
        app = Application()

        app.init()

        app.run()

        app.exit()
    except Exception as e:
        print(f"{e}")