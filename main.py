import pygame as pg
from OpenGL.GL import *


class App:
    def __init__(self):
        pg.init()
        
        # Set OpenGL version before creating window
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        
        pg.display.set_mode((1024, 768), pg.OPENGL|pg.DOUBLEBUF)

        self.clock = pg.time.Clock()

        glClearColor(0.1, 0.1, 0.1, 1)
        
        self.VAOHandle = glGenVertexArrays(1)
        glBindVertexArray(self.VAOHandle)
        self.VBOHandle = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBOHandle)


    def Run(self):
        Running = True

        while Running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    Running = False

            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()

            self.clock.tick(60)
        
        pg.quit()


if __name__ == "__main__":
    app = App()
    app.Run()