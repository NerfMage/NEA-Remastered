import numpy as np
# from PIL import Image as im
import noise
import random

shape1 = (40, 25)
OBSTACLE_MAP = []
ENEMY_MAP = []
array = np.zeros(shape1)
scale = 5
seed = random.randint(0, 255)

for i in range(shape1[0]):
    for j in range(shape1[1]):
        array[i][j] = noise.pnoise2(i/scale,
                                    j/scale,
                                    octaves=4,
                                    persistence=.5,
                                    lacunarity=3,
                                    repeatx=shape1[0],
                                    repeaty=shape1[1],
                                    base=seed)

for i in range(shape1[0]):
    for j in range(shape1[1]):
        if array[i][j] < -0.25:
            OBSTACLE_MAP.append([i*40, j*40])
        elif array[i][j] > 0.35:
            ENEMY_MAP.append([i*40, j*40])
