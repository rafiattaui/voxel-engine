from settings import *
from world_objects.chunk import Chunk

class World:
    def __init__(self,app):
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOL)] # Empty list equal to number of chunks, stores chunk objects.
        self.voxels = np.empty([WORLD_VOL, CHUNK_VOL], dtype='uint8') # Voxels stored in 2D array, and correspond to list of chunks.
        self.build_chunks()
        self.build_chunk_mesh()
        
    def build_chunks(self):
        for x in range(WORLD_W):
            for y in range(WORLD_H):
                for z in range(WORLD_D):
                    chunk = Chunk(self, position=(x,y,z))
                    
                    chunk_index = x + WORLD_W * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk # Stores the chunk class objects
                    
                    # Put the chunk voxels itself in a seperate array.
                    self.voxels[chunk_index] = chunk.build_voxels() # Calls upon the previous chunk object to build its voxels and store that array of voxels in the list.
                    
                    # Store voxel pointer in chunk to point to the voxels array in world class.
                    chunk.voxels = self.voxels[chunk_index]
    
    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh() # Call each chunk to build their meshes
    
    def update(self):
        pass
    
    def render(self):
        for chunk in self.chunks:
            chunk.render()