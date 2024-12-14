from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene

class VoxelEngine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3) # Define major version of OpenGL to use
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3) # Define minor version of OpenGL to use
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE) # Sets context profile to core profile to remove deprecated functions
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24) # Specifies size of depth buffer in bits, used for depth testing to determine which surfaces are in the most front relative to the camera

        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF) # pg.OPENGL enables OpenGL rendering, pg.DOUBLEBUF enables double buffering to improve performance by using two buffers: One for rendering and one for display, swapping out every frame
        self.ctx = mgl.create_context()
        
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND) # Experimental depth testing, color blending, polygon face culling
        self.ctx.gc_mode = 'auto' # Automatic garbage collection of unused objects
        
        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        
        self.is_running = True
        self.on_init()
        
    def on_init(self):
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)
        
    def update(self):
        self.shader_program.update()
        self.scene.update()
        
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f'Voxel Engine | FPS: {self.clock.get_fps():.0f}')
    
    def render(self):
        self.ctx.clear(color=BG_COLOR) # Clears depth buffer from previous frame for recalculation.
        self.scene.render()
        pg.display.flip()
    
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
    
    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()
    
if __name__ == '__main__':
    app = VoxelEngine()
    app.run()