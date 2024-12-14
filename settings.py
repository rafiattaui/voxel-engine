from numba import njit # Python compiler to speed up numerical computations
import numpy as np
import glm # Mathematics library for OpenGL (Vectors, Matrices, Transformations)
import math

# Resolution
WIN_RES = glm.vec2(1600, 900)

# Colors
BG_COLOR = glm.vec3(0.1, 0.16, 0.25)