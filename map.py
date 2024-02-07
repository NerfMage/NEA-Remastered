import numpy as np
# from PIL import Image as im
import noise
import random

shape = (24, 15)
OBSTACLE_MAP = []
ENEMY_MAP = []
array = np.zeros(shape)
scale = 5
seed = random.randint(0, 255)

for i in range(shape[0]):
    for j in range(shape[1]):
        array[i][j] = noise.pnoise2(i / scale,
                                    j / scale,
                                    octaves=4,
                                    persistence=.5,
                                    lacunarity=3,
                                    repeatx=shape[0],
                                    repeaty=shape[1],
                                    base=seed)

for i in range(shape[0]):
    for j in range(shape[1]):
        if array[i][j] < -0.2:
            OBSTACLE_MAP.append([i, j])
            # array[i][j] = 0
        elif array[i][j] > 0.25:
            ENEMY_MAP.append([i, j])
        # else:
            # array[i][j] = 1

# array = (array*255).astype(np.uint8)
#
# image = im.fromarray(array)
# image.show()
