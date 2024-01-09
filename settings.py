import pygame
import os

pygame.init()

INITIAL_SIZE = pygame.display.get_desktop_sizes()[0]

ENVIRONMENT_SPRITES = {
    file.replace('.png', ''): os.path.join('Sprites', 'Environment', file)
    for file in os.listdir(os.path.join('Sprites', 'Environment'))
}

ENEMY_SPRITES = {
    file.replace('.png', ''): os.path.join('Sprites', 'Enemies', file)
    for file in os.listdir(os.path.join('Sprites', 'Enemies'))
}
