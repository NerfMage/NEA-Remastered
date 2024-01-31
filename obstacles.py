import pygame
import os
from creatures import Spritesheet


class Trap(Obstacle):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.sprite = pygame.image.load(os.path.join('Sprites', 'Environment', 'Obstacles', name + '.png'))
        self.spritesheet = Spritesheet(self.sprite, 32, 32, 4, 2)
        self.hitbox = (x + 16, y + 16, 32, 24)
        self.activated = False

    def return_sprite(self):
        if self.activated:
            self.spritesheet.update()

        return self.spritesheet.get_image()
