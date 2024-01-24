import pygame
import os
from creatures import Spritesheet


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


class Trap(Obstacle):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.sprite = pygame.image.load(os.path.join('Sprites', 'Environment', 'Obstacles', name + '.png'))
        self.spritesheet = Spritesheet(self.sprite, 32, 32, 4, 2)
        self.activated = False

    def return_sprite(self):
        if self.activated:
            self.spritesheet.update()

        return self.spritesheet.get_image()
