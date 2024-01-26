import pygame
import os
from creatures import Spritesheet


class Obstacle:
    def __init__(self, name, x, y):
        self.sprite = None
        self.sprite = pygame.image.load(os.path.join('Sprites', 'Environment', 'Obstacles', name+'.png'))
        self.sprite = pygame.transform.scale_by(self.sprite, 2)
        self.hitbox = (x + self.sprite.get_width()*0.2, y + self.sprite.get_height()*0.2,
                       self.sprite.get_width()*0.6, self.sprite.get_height()*0.6)
        self.x, self.y = x, y

    def return_sprite(self):
        return self.sprite

    def return_coords(self):
        return self.x, self.y

    def draw_hitbox(self):
        win = pygame.display.get_surface()
        pygame.draw.rect(win, (255, 0, 0), self.hitbox)


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
