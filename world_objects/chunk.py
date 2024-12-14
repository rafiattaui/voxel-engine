from settings import *
from meshes.chunk_mesh import ChunkMesh

class Chunk:
    def __init__(self,app):
        self.app = app
        self.voxels: np.array = self.build_voxels()
        self.mesh: ChunkMesh = None
        self.build_mesh()
        
    def build_mesh(self):
        self.mesh = ChunkMesh(self)
        
    def render(self):
        self.mesh.render()
    
    def build_voxels(self):
        # Empty Chunk, voxel id: 0-255 for different block, 0 for empty space
        voxels = np.zeros(CHUNK_VOL, dtype='uint8')
        
        # Fill chunk
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (
                        x + y + z if int(glm.simplex(glm.vec3(x,y,z)*0.1)+1) else 0  # Generate a simplex noise value at the 3D position and multiplies by 0.1 to scale coordinates smoothly.
                        )
                    # Instead of storing the positions as 3D array (x,y,z). We iterate through each voxel like a list
                    # using an index.
        return voxels