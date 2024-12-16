from numba import njit
import numpy as np
import glm
import math

# Resolution
WIN_RES = glm.vec2(1600, 900)

# Chunk
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE

# World
WORLD_W, WORLD_H = 8,3 # World width, height (8 Chunks wide, 3 chunks high)
WORLD_D = WORLD_W # World depth same as width making it a cube. (8 chunks deep.)
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# WORLD CENTER
CENTER_XZ = WORLD_W * H_CHUNK_SIZE # Calculate world center by multiplying the total number of chunks in the world with the size of each chunk divided by 2
CENTER_Y = WORLD_H * H_CHUNK_SIZE # Same for Y axis

# Camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)  # vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89)

# Player
PLAYER_SPEED = 0.05
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, WORLD_H * CHUNK_SIZE, CENTER_XZ)
MOUSE_SENSITIVITY = 0.002

# Colors
BG_COLOR = glm.vec3(0.1, 0.16, 0.25)