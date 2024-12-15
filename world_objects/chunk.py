from settings import *
from meshes.chunk_mesh import ChunkMesh

class Chunk:
    def __init__(self,app):
        self.app = app
        self.chunk_array: np.array = self.build_voxels()
        self.mesh: ChunkMesh = None
        self.build_mesh()
        
    def build_mesh(self):
        self.mesh = ChunkMesh(self)
        
    def render(self):
        self.mesh.render()
    
    def build_voxels(self):
        # Empty Chunk, voxel id: 0-255 for different block, 0 for empty space
        chunk_array = np.zeros(CHUNK_VOL, dtype='uint8')
        
        # Fill chunk
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    chunk_array[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (
                        x + y + z if int(glm.simplex(glm.vec3(x,y,z)*0.1)+1) else 0  # Generate a simplex noise value at the 3D position and multiplies by 0.1 to scale coordinates smoothly.
                        )
                    # Instead of storing the positions as 3D array (x,y,z). We iterate through each voxel like a list
                    # using an index.
        self.save_chunk_voxels(array=chunk_array)
        return chunk_array
    
    def save_chunk_voxels(self,array, filename="chunk_voxels.txt"):
        with open(filename, "w") as f:
            for y in range(CHUNK_SIZE):
                f.write(f"Layer {y}:\n")
                for z in range(CHUNK_SIZE):
                    row = [
                        array[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                        for x in range(CHUNK_SIZE)
                    ]
                    f.write(" ".join(map(str, row)) + "\n")
                f.write("\n")