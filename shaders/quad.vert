#version 330 core

// Vertex position input
layout (location = 0) in vec3 in_position; // Vertex position

// Color input
layout (location = 1) in vec3 in_color; // Vertex color

// Output color to fragment shader
out vec3 color;

void main() {
    color = in_color;  // Assign the input color to the output color
    gl_Position = vec4(in_position, 1.0); // Convert the 3D position to 4D homogeneous coordinates
}

