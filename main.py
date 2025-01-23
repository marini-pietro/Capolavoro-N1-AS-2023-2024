try:
    from settings import *
    import moderngl as mgl
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1" #Hide pygame support prompt
    import pygame as pg
    del os
    import sys
    from shader_program import ShaderProgram
    from scene import Scene
    from player import Player
    from textures import Textures
except ImportError as e:
    import os
    os.system('pip install -r requirements.txt')
    from settings import *
    import moderngl as mgl
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1" #Hide pygame support prompt
    import pygame as pg
    del os
    import sys
    from shader_program import ShaderProgram
    from scene import Scene
    from player import Player
    from textures import Textures

class VoxelEngine:
    def __init__(self):
        pg.init()

        #Define API version
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, MAJOR_VER) 
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, MINOR_VER)
        
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE) #Set core profile (remove deprecated functions)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, DEPTH_SIZE) #Set depth size (precision of depth buffer, used to handle depth calculations)
        pg.display.gl_set_attribute(pg.GL_MULTISAMPLESAMPLES, NUM_SAMPLES) #Set number of samples for multisampling (antialiasing)

        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF) #Create pygame window
        self.ctx = mgl.create_context() #Create ModernGL context

        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND) #Enable flags inside of the context just created (depth test: pixels closer to the camera obscure the ones farther away)
        self.ctx.gc_mode = 'auto' #Set garbage collection to auto                                                           cull face: only render visible faces of objects
                                                                                                                          # blend: mix colors of objects based on alpha value (enable transparency)
        self.clock = pg.time.Clock() # Pygame clock object to track time
        self.delta_time = 0 #Time between frames
        self.time = 0 #Time for the start of the program

        pg.event.set_grab(True) #Set the window so that it grabs the mouse
        pg.mouse.set_visible(False) #Hide mouse when inside of window

        self.is_running = True # Flag to keep track if game should be running or not
        self.on_init() # Init all necessary objects

    def on_init(self): 
        """Method that initializes all the necessary objects."""

        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)

    def update(self):
        """
        Method that updates all the components of the game.
        Should be called each frame.
        """

        self.player.update() # Update player position and camera
        self.shader_program.update() # Update shaders
        self.scene.update() # Update objects in scene

        self.delta_time = self.clock.tick(MAX_FPS) # Limit FPS
        self.time = pg.time.get_ticks() * 0.001 # Get current time in seconds
        pg.display.set_caption(f'{self.clock.get_fps() :.0f}') # Update caption with FPS

    def render(self):
        """Method that clears the context buffer and renders all objects inside of scene."""
        
        self.ctx.clear(color=BG_COLOR) # Clear the context buffer
        self.scene.render() # Render the scene
        pg.display.flip() # Swap the buffers

    def handle_events(self):
        """Method that handles all the events in the game."""

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.is_running = False
            self.player.handle_event(event=event)

    def run(self):
        """Method that runs the game loop."""
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()

if __name__ == '__main__':
    engine = VoxelEngine()
    engine.run()