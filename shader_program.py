from settings import *

class ShaderProgram:
    def __init__(self, engine):
        self.engine = engine
        self.ctx = engine.ctx
        self.player = engine.player
        # Assign shader programs
        self.chunk = self.get_program(shader_name='chunk')
        self.voxel_marker = self.get_program(shader_name='voxel_marker')
        self.water = self.get_program(shader_name='water')
        self.clouds = self.get_program(shader_name='clouds')
        self.player_program = self.get_program(shader_name='player')
        # Set uniforms 
        self.set_uniforms_on_init()

    def set_uniforms_on_init(self):
        # Chunk uniforms
        self.chunk['m_proj'].write(self.player.m_proj)
        self.chunk['m_model'].write(glm.mat4())
        self.chunk['u_texture_array_0'] = 1 # Assign texture location consult textures.py for more information
        self.chunk['bg_color'].write(BG_COLOR)
        self.chunk['water_line'] = WATER_LINE

        # Voxel marker uniforms
        self.voxel_marker['m_proj'].write(self.player.m_proj)
        self.voxel_marker['m_model'].write(glm.mat4())
        self.voxel_marker['u_texture_0'] = 0 # Assign texture location consult textures.py for more information

        # Water uniforms
        self.water['m_proj'].write(self.player.m_proj) 
        self.water['u_texture_0'] = 2 # Assign texture location consult textures.py for more information
        self.water['water_area'] = WATER_AREA
        self.water['water_line'] = WATER_LINE
        self.water['bg_color'].write(BG_COLOR)

        # Clouds uniforms
        self.clouds['m_proj'].write(self.player.m_proj)
        self.clouds['center'] = CENTER_XZ
        self.clouds['bg_color'].write(BG_COLOR)
        self.clouds['cloud_scale'] = CLOUD_SCALE 

        # Player uniforms
        self.player_program['m_proj'].write(self.player.m_proj)
        self.player_program['m_model'].write(glm.mat4())
        self.player_program['u_texture_0'] = 3 # Assign texture location consult textures.py for more information

    def update(self):
        # Update view matrices
        self.chunk['m_view'].write(self.player.m_view)
        self.voxel_marker['m_view'].write(self.player.m_view)
        self.water['m_view'].write(self.player.m_view)
        self.clouds['m_view'].write(self.player.m_view)
        self.player_program['m_view'].write(self.player.m_view)

    def get_program(self, shader_name):
        """Loads shader program from .vert or .frag files in the shaders folder."""	
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader) # Create shader program
        return program
