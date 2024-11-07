from settings import *
from world_objects.chunk import Chunk
from voxel_handler import VoxelHandler
from world_objects.voxel import Voxel

class World:
    def __init__(self, engine):
        self.engine = engine
        self.chunks = [None for _ in range(WORLD_VOL)] # Array to store all the chunks in the world
        self.voxels: list[list[Voxel]] = [[None for _ in range(CHUNK_VOL)] for _ in range(WORLD_VOL)]
        
        print(f"voxels type: {type(self.voxels)} and len: {len(self.voxels)}", flush=True)
        print(f"voxels[0] type: {type(self.voxels[0])} and len : {len(self.voxels[0])}", flush=True)
        print(f"voxels[0][0] type: {type(self.voxels[0][0])}", flush=True)
        print(f"total length: {len(self.voxels) * len(self.voxels[0])}", flush=True)
        print()

        self.build_chunks()     # Build all the chunks in the world  
        self.build_chunk_mesh() # Build the mesh for all the chunks in the world
        self.voxel_handler = VoxelHandler(self) # Create a voxel handler

    def update(self):
        self.voxel_handler.update()

    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_index = x + WORLD_W * z + WORLD_AREA * y # Index in which to store the chunk in the array that stores all the chunks in the world

                    self.chunks[chunk_index] = chunk # Put the newly created chunk in the array that stores all the chunks in the world

                    chunk.build_voxels() # Build the voxels for the chunk
                    print(f"type of chunk.voxels: {type(chunk.voxels)} with chunk index {chunk_index}", flush=True) 
                    print()
                    
                    self.voxels[chunk_index] = chunk.voxels # Put the voxels in the array that stores all the voxels in the world

    def build_chunk_mesh(self) -> None:
        """Build the mesh for all the chunks in the world."""	
        for chunk in self.chunks:
            chunk.build_mesh()

    def render(self):
        """Render all the chunks in the world."""
        for chunk in self.chunks:
            chunk.render()

    def get_chunk(self, coordinates) -> Chunk:
        """Get the chunk at the given coordinates."""
        for chunk in self.chunks:
            if chunk.position == coordinates:
                return chunk
