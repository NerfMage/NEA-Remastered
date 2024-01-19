import pygame
import os


class Obstacle:
    def __init__(self, name, x, y):
        self.sprite = None
        self.sprite = pygame.image.load(os.path.join('Sprites', 'Environment', 'Obstacles', name+'.png'))
        self.sprite = pygame.transform.scale_by(self.sprite, 2)
        self.x, self.y = x, y

    def return_sprite(self):
        return self.sprite

    def return_coords(self):
        return self.x, self.y
