from settings import *
import numpy as np

def save_vertex_data_to_file(vertex_data, filename):
    """
    Saves vertex data to a file in a readable format, including headers.

    Args:
        vertex_data (ndarray): The 1D array containing vertex data.
        filename (str): The name of the file to save the data to.
    """
    with open(filename, 'w') as file:
        # Write the header line
        header = "x, y, z, voxel_id, face_id\n"
        file.write(header)
        
        # Write the vertex data
        for i in range(0, len(vertex_data), 5):  # Assuming format_size is 5 (x, y, z, voxel_id, face_id)
            line = f"{vertex_data[i]:3}, {vertex_data[i+1]:3}, {vertex_data[i+2]:3}, {vertex_data[i+3]:3}, {vertex_data[i+4]:3}\n"
            file.write(line)


def is_void(voxel_pos, chunk_voxels):
    
    """
    Determines if a voxel at a given position is void (i.e., has an ID of 0).

    Args:
        voxel_pos (tuple): A tuple (x, y, z) representing the position of the voxel within the chunk.
        chunk_voxels (list): A flat list representing the voxel data of the chunk.

    Returns:
        bool: True if the voxel is void (ID of 0), False otherwise.
    """
    
    x, y, z = voxel_pos
    if 0 <= x < CHUNK_SIZE and 0 <= y < CHUNK_SIZE and 0 <= z < CHUNK_SIZE: # Check if voxel is within chunk size
        if chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]: # Check if the voxel has a ID of 1 or more.
            return False
    return True

def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index

def build_chunk_mesh(chunk_voxels, format_size):
    
    """
    Builds a mesh for a chunk of voxels.
    Args:
        chunk_voxels (ndarray): A 3D array representing the voxel data of the chunk.
        format_size (int): The size of the format for each vertex attribute.
    Returns:
        ndarray: A 1D array containing the vertex data for the chunk mesh.
    The function iterates through each voxel in the chunk and checks if the voxel is not empty.
    For each non-empty voxel, it checks the visibility of each face (top, bottom, right, left, back, front).
    If a face is visible (i.e., adjacent voxel is empty), it adds the vertex data for that face to the vertex_data array.
    The vertex data includes the position (x, y, z), voxel_id, and face_id.
    The function returns the vertex_data array truncated to the actual size of the data.
    """
    
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint8')
    # Maximum number of faces rendered per voxel is 3 so 18 vertices total, and 5 attributes per vertex
    index = 0
    
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x+CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue
                
                # Face Culling
                # Render only faces of cubes that are visible.
                
                # Top Face
                if is_void((x,y + 1, z), chunk_voxels):
                    # format: x, y, z, voxel_id, face_id
                    v0 = (x    , y + 1, z    , voxel_id, 0)
                    v1 = (x + 1, y + 1, z    , voxel_id, 0)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = (x    , y + 1, z + 1, voxel_id, 0)
                    
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)
                
                # Bottom face
                if is_void((x,y-1, z), chunk_voxels):
                    v0 = (x    , y    , z    , voxel_id, 1)
                    v1 = (x + 1, y    , z    , voxel_id, 1)
                    v2 = (x + 1, y    , z + 1, voxel_id, 1)
                    v3 = (x    , y    , z + 1, voxel_id, 1)
                    
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)
                
                # Right face
                if is_void((x + 1, y, z), chunk_voxels):

                    v0 = (x + 1, y    , z    , voxel_id, 2)
                    v1 = (x + 1, y + 1, z    , voxel_id, 2)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = (x + 1, y    , z + 1, voxel_id, 2)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face
                if is_void((x - 1, y, z), chunk_voxels):

                    v0 = (x, y    , z    , voxel_id, 3)
                    v1 = (x, y + 1, z    , voxel_id, 3)
                    v2 = (x, y + 1, z + 1, voxel_id, 3)
                    v3 = (x, y    , z + 1, voxel_id, 3)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face
                if is_void((x, y, z - 1), chunk_voxels):

                    v0 = (x,     y,     z, voxel_id, 4)
                    v1 = (x,     y + 1, z, voxel_id, 4)
                    v2 = (x + 1, y + 1, z, voxel_id, 4)
                    v3 = (x + 1, y,     z, voxel_id, 4)

                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Front face
                if is_void((x, y, z + 1), chunk_voxels):

                    v0 = (x    , y    , z + 1, voxel_id, 5)
                    v1 = (x    , y + 1, z + 1, voxel_id, 5)
                    v2 = (x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = (x + 1, y    , z + 1, voxel_id, 5)

                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
                    
    #save_vertex_data_to_file(vertex_data, "vertex_data.txt")
    #print("Vertex data has been saved to vertex_data.txt")
    
    return vertex_data[:index+1]