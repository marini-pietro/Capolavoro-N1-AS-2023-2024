from meshes.quad_mesh import QuadMesh
from settings import *

class Water:
    def __init__(self, game):
        self.app = game # Retrieve reference to game object
        self.mesh = QuadMesh(game) # Import standard quad mesh

    def render(self):
        self.mesh.render()
