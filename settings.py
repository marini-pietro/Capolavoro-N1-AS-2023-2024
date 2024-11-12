from numba import njit
from random import randint
import numpy as np
import glm
import math
import pygame as pg

# OpenGL settings
MAJOR_VER, MINOR_VER = 3, 3
DEPTH_SIZE = 24
NUM_SAMPLES = 1  # antialiasing (increase for better quality)
ANISOTROPY_LEVEL = 32.0  # texture filtering
MAX_FPS = 60

# Resolution
RESOLUTIONS = {
    "8KUHD": glm.vec2(7680, 4320),
    "UHD": glm.vec2(3840, 2160),
    "QHD": glm.vec2(2560, 1440),
    "Full HD": glm.vec2(1920, 1080),
    "HD+": glm.vec2(1600, 900),
    "HD": glm.vec2(1280, 720),
    "SVGA": glm.vec2(800, 600)
}
WIN_RES = RESOLUTIONS["Full HD"]

# Seed for world gen (noise algorithm)
SEED = randint(0, 1000)

# Max raycasting distance
MAX_RAY_DIST = 6

# chunk
CHUNK_SIZE = 48 # Chunk size (width, height, depth) DO NOT MODIFY IT MESSED UP THE ISLAND MASK (IDK WHY)
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOL = CHUNK_AREA * CHUNK_SIZE
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# World dimnesions
WORLD_W, WORLD_H = 2, 2
WORLD_D = WORLD_W
WORLD_AREA = WORLD_W * WORLD_D
WORLD_VOL = WORLD_AREA * WORLD_H

# World center coordinates
CENTER_XZ = WORLD_W * H_CHUNK_SIZE
CENTER_Y = WORLD_H * H_CHUNK_SIZE

# Camera settings
ASPECT_RATIO = WIN_RES.x / WIN_RES.y 
FOV_DEG = 50 # Field of view degree value
V_FOV = glm.radians(FOV_DEG)  # Vertical FOV
H_FOV = 2 * math.atan(math.tan(V_FOV * 0.5) * ASPECT_RATIO)  # horizontal FOV
NEAR = 0.1 # Near plane distance from camera
FAR = 2000.0 # Far plane distance from camera
PITCH_MAX = glm.radians(89) # Max vertical rotations

# Physics settings
GRAVITY_STRENGTH = 0.5 # Gravity force

# Player controls
FORWARD_KEY = pg.K_w
BACKWARD_KEY = pg.K_s
LEFT_KEY = pg.K_a
RIGHT_KEY = pg.K_d
UP_KEY = pg.K_q
DOWN_KEY = pg.K_e

# Player settings
GAMEMODE = "SURVIVAL" # Creative or Survival
PLAYER_SPEED = 0.005 # Player movement speed
PLAYER_ROT_SPEED = 0.003 # Camera rotation speed
PLAYER_POS = glm.vec3(CENTER_XZ + 0.5, WORLD_H * CHUNK_SIZE + 0.5, CENTER_XZ + 0.5)
#PLAYER_POS = glm.vec3(CENTER_XZ, CHUNK_SIZE, CENTER_XZ) # Starting player position
PLAYER_WIDTH = 1
PLAYER_HEIGTH = 2
PLAYER_DEPTH = 1
MOUSE_SENSITIVITY = 0.002 # Mouse sensibility

# Standardized colors
BG_COLOR = glm.vec3(0.58, 0.83, 0.99) #Color used for the sky and when buffer is cleared

# Textures ID's
SAND = 1
GRASS = 2
DIRT = 3
STONE = 4
SNOW = 5
LEAVES = 6
WOOD = 7

# Terrain levels (at which heigth different types of terrain should take place)
SNOW_LVL = 54
STONE_LVL = 49
DIRT_LVL = 40
GRASS_LVL = 8
SAND_LVL = 7

# Tree settings
TREE_PROBABILITY = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# Tree settings
WATER_LINE = 5.6 # Heigth of water block
WATER_AREA = 5 * CHUNK_SIZE * WORLD_W # Area of water block

# Cloud settings
CLOUD_SCALE = 25 # Dimension
CLOUD_HEIGHT = WORLD_H * CHUNK_SIZE * 2 # Heigth of the clouds