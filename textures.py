import pygame as pg
import moderngl as mgl
from settings import ANISOTROPY_LEVEL

class Textures:
    def __init__(self, engine):
        self.engine = engine # Get reference to engine object
        self.ctx = engine.ctx # Get reference to moderngl context

        # Load textures
        self.texture_0 = self.load('frame.png')
        self.texture_1 = self.load('water.png')
        self.texture_array_0 = self.load('tex_array_0.png', is_tex_array=True) # Load texture array

        # Assing locations to textures
        self.texture_0.use(location=0)
        self.texture_array_0.use(location=1)
        self.texture_1.use(location=2)

    def load(self, file_name, is_tex_array=False):
        """Load texture from file and return it."""
        pg_texture = pg.image.load(f'assets/{file_name}') # Load texture from file
        pg_texture = pg.transform.flip(pg_texture, flip_x=True, flip_y=False) # Flip texture on x axis (moderngl has origin in top left corner and pygame in upper left corner so we need to flip the texture)

        if is_tex_array: # If texture is a texture array
            num_layers = 3 * pg_texture.get_height() // pg_texture.get_width()  # 3 textures per layer
            texture = self.engine.ctx.texture_array( # Create texture array
                size=(pg_texture.get_width(), pg_texture.get_height() // num_layers, num_layers), # Set size
                components=4, # RGBA
                data=pg.image.tostring(pg_texture, 'RGBA') # Convert texture to string
            )
        else: # If texture is not a texture array
            texture = self.ctx.texture( # Create texture
                size=pg_texture.get_size(), # Set size
                components=4, # RGBA
                data=pg.image.tostring(pg_texture, 'RGBA', False) # Convert texture to string (False means that the pixel data should not be flipped vertically)
            )

        # Set texture filtering (they are complementary with each other but optional)
        
        # Set anisotropy level (filter textures so they look good at all angles at distances, the higher the samples the better the quality)
        max_anisotropy = self.ctx.info.get('GL_MAX_TEXTURE_MAX_ANISOTROPY', 0) # Get the maximum anisotropy level supported by the GPU (0 if not supported)
        texture.anisotropy = min(ANISOTROPY_LEVEL, max_anisotropy) if max_anisotropy != 0 else ANISOTROPY_LEVEL # Used min function to prevent anisotropy level from exceeding the maximum level supported by the GPU
        texture.build_mipmaps() # Generate mipmaps (lower resolutions versions of the textures that are meant to be rendered when the camera is farther away).
        texture.filter = (mgl.NEAREST, mgl.NEAREST) # Set nearest-neighbour filtering to both minification and magnification
        return texture