import pygame as pg
from OpenGL.GL import *
import glm
import config
import texture_mgr
import block_type
import shader
import camera
import controller


class Application:
    def __init__(self):
        self._run = False


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

        self._texture_mgr = texture_mgr.TextureMgr(16, 16, 256)
        self._texture_mgr.init()

        self._grass = block_type.BlockType(self._texture_mgr, "grass", {"top": "grass", "bottom": "dirt", "sides": "grass_side"})

        self._texture_mgr.gen_mipmap()

        #上传数据
        self._vao = glGenVertexArrays(1)
        glBindVertexArray(self._vao)

        #定点数据
        self._vertices_bo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._vertices_bo)
        glBufferData(GL_ARRAY_BUFFER, self._grass.vertices.nbytes, self._grass.vertices.ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(0)
        #纹理坐标
        self._tex_coord_bo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._tex_coord_bo)
        glBufferData(GL_ARRAY_BUFFER, self._grass.texcoord.nbytes, self._grass.texcoord.ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(1)
        #光照数据
        self._shading_value_bo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self._shading_value_bo)
        glBufferData(GL_ARRAY_BUFFER, self._grass.shading_values.nbytes, self._grass.shading_values.ptr, GL_STATIC_DRAW)
        glVertexAttribPointer(2, 1, GL_FLOAT, GL_FALSE, 1 * glm.sizeof(glm.float32), None)
        glEnableVertexAttribArray(2)
        #数组数据
        self._ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self._ibo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self._grass.indices.nbytes, self._grass.indices.ptr, GL_STATIC_DRAW)

        self._shader = shader.Shader("shaders/vertex_shader.vs", "shaders/fragment_shader.fs")
        self._shader.use()

        self._shader_sampler_location = self._shader.get_uniform("texture_array_sampler")

        self._camera = camera.Camera()
        self._camera.bind_shader(self._shader)

        self._controller = controller.Controller()
        self._controller.bind_camera(self._camera)
        

    def run(self):
        while self._run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._run = False
            
            delta = self._clock.tick()

            self._update(delta)

            self._begin_render()
            self._draw(delta)
            self._end_render()


    def _update(self, delta):
        self._controller.update(delta)

    def _begin_render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def _end_render(self):
        pg.display.flip()


    def _draw(self, delta):
        self._shader.use()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D_ARRAY, self._texture_mgr.texture_array)
        glUniform1i(self._shader_sampler_location, 0)

        glBindVertexArray(self._vao)
        glDrawElements(GL_TRIANGLES, len(self._grass.indices), GL_UNSIGNED_INT, None)


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