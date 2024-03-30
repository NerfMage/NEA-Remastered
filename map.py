import numpy as np
import noise
import random
# Library to visualise noise map:
# from PIL import Image as im

shape = (24, 15)  # The dimensions of the numpy array, set to 24x15 to represent Tiles
OBSTACLE_MAP = []  # Will hold coords of all obstacles given by the noise map
ENEMY_MAP = []  # Will hold coords of all the enemies given by the noise map
array = np.zeros(shape)  # Creates an array of 0s
scale = 5


def generate_map():
    """
    Procedure that generates a noise map and uses it to determine the positions of enemies and obstacles
    within the game
    Commented code is used to create a .png file of the noise map, for testing
    """
    seed = random.randint(0, 255)  # Picks a random seed to generate from
    # Resets the maps to re-generate the contents
    ENEMY_MAP.clear()
    OBSTACLE_MAP.clear()

    # Creats the perlin noise using the noise library
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

    # Selects the relevant coordinates to be added to the maps
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
