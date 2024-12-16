from settings import *
from meshes.chunk_mesh import ChunkMesh

class Chunk:
    def __init__(self,world,position):
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True
        
    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model
    
    def set_uniform(self):
        self.mesh.program['m_model'].write(self.m_model)
        
    def build_mesh(self):
        self.mesh = ChunkMesh(self)
        
    def render(self):
        if not self.is_empty:
            self.set_uniform()
            self.mesh.render()
    
    def build_voxels(self):
        # Empty Chunk, voxel id: 0-255 for different block, 0 for empty space
        voxels = np.zeros(CHUNK_VOL, dtype='uint8')
        
        # Fill chunk
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE # This is the origin of the chunk in world space.
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                # To get the absolute position of the voxel in world space, you combine the chunk's world-space origin (cx) with the voxel's local position (x):
                # world-space x-coordinate (wx)=chunk origin (cx)+local position (x)
                # world-space x-coordinate (wx)=chunk origin (cx)+local position (x)
                wx = x + cx # This converts the local position of the voxel within the chunk to world space.
                wz = z + cz
                world_height = int(glm.simplex(glm.vec2(wx,wz) * 0.01) * 32 + 32) # Use simplex noise to generate height variations based on wx,wz,
                # Scales the noise output to a range of [-32, +32] and then shifts it to [0, 64], representing terrain heights.
                local_height = min(world_height - cy, CHUNK_SIZE)
                # Converts the global height (world_height) into chunk-local space (relative to the chunk’s vertical position).
                # min(world_height - cy, CHUNK_SIZE): Ensures the height doesn’t exceed the chunk’s vertical bounds (CHUNK_SIZE).
                
                for y in range(local_height):
                    wy = y + cy # convert chunk-space y to world-space y
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = wy + 1
                    # Instead of storing the positions as 3D array (x,y,z). We iterate through each voxel like a list
                    # using an index.
        # self.save_chunk_voxels(array=voxels)
        if np.any(voxels): # Prevent rendering of chunks with no voxels.
            self.is_empty = False
        return voxels
    
    def save_chunk_voxels(self,array, filename="voxels.txt"):
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