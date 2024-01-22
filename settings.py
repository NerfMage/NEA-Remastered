import pygame
import numpy as np
import noise
import random
from PIL import Image as im

pygame.init()

INITIAL_SIZE = pygame.display.get_desktop_sizes()[0]
SEED = random.randint(0, 255)

ARRAY = np.zeros((INITIAL_SIZE[1], INITIAL_SIZE[0]))
MAP = []


for i in range(INITIAL_SIZE[1]):
    for j in range(INITIAL_SIZE[0]):
        ARRAY[i][j] = noise.pnoise2(i/150,
                                    j/150,
                                    octaves=4,
                                    persistence=.5,
                                    lacunarity=3,
                                    repeatx=INITIAL_SIZE[1],
                                    repeaty=INITIAL_SIZE[0],
                                    base=SEED)

for i in range(INITIAL_SIZE[1]):
    for j in range(INITIAL_SIZE[0]):
        if ARRAY[i][j] < -0.25 and i % 40 == 0 and j % 40 == 0:
            ARRAY[i][j] = 0
            MAP.append((i, j))
        elif ARRAY[i][j] > 0.25:
            ARRAY[i][j] = 0.5
        else:
            ARRAY[i][j] = 1

# array = (ARRAY*255).astype(np.uint8)
# image = im.fromarray(array)
# image.show()
