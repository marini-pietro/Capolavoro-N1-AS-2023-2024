from base_mesh import BaseMesh  # Import the BaseMesh class
from pygltflib import GLTF2  # Import the GLTF2 class
import numpy as np  # Import numpy

class PlayerMesh(BaseMesh):
    def __init__(self):
        super().__init__()
        self.vertex_data, self.vbo_format = self.load_gltf("assets/player.glb")
        self.program = None
        self.attrs = ("in_position", "in_normal", "in_texcoord_0")
        self.vao = self.get_vao()

    def get_vertex_data(self) -> np.array:
        """Method that returns the vertex data of the player mesh."""
        
        return self.vertex_data

    def load_gltf(self, file_path: str):
        """Method that loads a GLTF file and returns the first mesh and buffer format."""
        
        # Load the GLTF file
        gltf = GLTF2().load(file_path)
        
        # Get the first mesh
        mesh = gltf.meshes[0]
        
        # Get the accessor for the vertex positions
        position_accessor = gltf.accessors[mesh.primitives[0].attributes.POSITION]
        
        # Get the buffer view for the accessor
        buffer_view = gltf.bufferViews[position_accessor.bufferView]
        
        # Get the buffer
        buffer = gltf.buffers[buffer_view.buffer]
        
        # Extract the binary data
        data = np.frombuffer(buffer.data, dtype=np.uint8, count=buffer_view.byteLength, offset=buffer_view.byteOffset)
        
        # Interpret the data based on the accessor's component type and type
        component_type = position_accessor.componentType
        type = position_accessor.type
        count = position_accessor.count
        
        # Map the component type to a numpy dtype
        component_type_map = {
            5120: np.int8,
            5121: np.uint8,
            5122: np.int16,
            5123: np.uint16,
            5125: np.uint32,
            5126: np.float32
        }
        
        dtype = component_type_map[component_type]
        
        # Determine the number of components per element
        type_map = {
            "SCALAR": 1,
            "VEC2": 2,
            "VEC3": 3,
            "VEC4": 4,
            "MAT2": 4,
            "MAT3": 9,
            "MAT4": 16
        }
        
        num_components = type_map[type]
        
        # Reshape the data to the correct format
        vertex_data = data.view(dtype).reshape((count, num_components))
        
        buffer_format = {
            "component_type": dtype,
            "num_components": num_components,
            "count": count
        }
        
        return mesh, buffer_format

    def extract_vertex_data(self, gltf, mesh):
        """Helper method to extract vertex data from a mesh."""
        
        # Get the accessor for the vertex positions
        position_accessor = gltf.accessors[mesh.primitives[0].attributes.POSITION]
        
        # Get the buffer view for the accessor
        buffer_view = gltf.bufferViews[position_accessor.bufferView]
        
        # Get the buffer
        buffer = gltf.buffers[buffer_view.buffer]
        
        # Extract the binary data
        data = np.frombuffer(buffer.data, dtype=np.uint8, count=buffer_view.byteLength, offset=buffer_view.byteOffset)
        
        # Interpret the data based on the accessor's component type and type
        component_type = position_accessor.componentType
        type = position_accessor.type
        count = position_accessor.count
        
        # Map the component type to a numpy dtype
        component_type_map = {
            5120: np.int8,
            5121: np.uint8,
            5122: np.int16,
            5123: np.uint16,
            5125: np.uint32,
            5126: np.float32
        }
        
        dtype = component_type_map[component_type]
        
        # Determine the number of components per element
        type_map = {
            "SCALAR": 1,
            "VEC2": 2,
            "VEC3": 3,
            "VEC4": 4,
            "MAT2": 4,
            "MAT3": 9,
            "MAT4": 16
        }
        
        num_components = type_map[type]
        
        # Reshape the data to the correct format
        vertex_data = data.view(dtype).reshape((count, num_components))
        
        return vertex_data