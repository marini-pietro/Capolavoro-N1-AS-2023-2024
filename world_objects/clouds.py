from settings import *
from meshes.cloud_mesh import CloudMesh

class Clouds:
    def __init__(self, app):
        self.engine = engine # Get app object reference
        self.mesh = CloudMesh(app) # Get mesh

    def update(self):
        self.mesh.program['u_time'] = self.engine.time # Update uniform time in shader  

    def render(self):
        self.mesh.render() # Render