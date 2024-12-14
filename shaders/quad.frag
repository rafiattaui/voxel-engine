#version 330 core

// Declare the output color of the fragment shader
layout (location = 0) out vec4 FragColor;  // The color output of the fragment shader (vec4: RGBA)

// Declare the input color to the fragment shader, passed from the vertex shader
in vec3 color;  // A 3D vector representing the RGB color of the fragment

void main() {
    // Set the fragment color by converting the RGB input to a RGBA output
    FragColor = vec4(color, 1.0);  // The input color is converted to a vec4 with alpha set to 1.0 (fully opaque)
}