import numpy as np

class BaseMesh:
    def __init__(self):
        # In OpenGL, we send data about vertices to the GPU through a vertex buffer
        # This sets up the format of this buffer for rendering
        
        # OpenGL context
        self.ctx = None
        # Shader program
        self.program = None
        # Vertex buffer data type format: "3f 3f", defines how data is structured in memory, using 3 floating-point values
        self.vbo_format = None
        # Attribute names according to format: ("in_position", "in_color")
        self.attrs: tuple[str, ...] = None
        # Vertex array object, configures interpretation of vertex buffer and links it to shader.
        self.vao = None
    
    def get_vertex_data(self) -> np.array: ...
    
    def get_vao(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array( # The VAO binds the VBO to the shaders and sets up how the vertex data will be interpreted in the shaders.
            self.program, [(vbo, self.vbo_format, *self.attrs)], skip_errors = True
        )
        return vao
    

    # VBO stores information to define a 3D object to be sent to the GPU
    # VAO defines how vertex data in a VBO is used so the GPU can remember the state of the VBO configuration.
    
    def render(self):
        self.vao.render()