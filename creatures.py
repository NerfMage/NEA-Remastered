import pygame
import os


class Spritesheet:
    def __init__(self, sheet, width, height, length, scale):
        """
        A class to animate spritesheets
        :param sheet: The image file of the sheet
        :param width: The width of each frame
        :param height: The height of each frame
        :param length: The number of frame on the sheet
        :param scale: The scale factor for the sprite to be enlarged by
        """
        self.sheet = sheet
        self.width = width
        self.height = height
        self.length = length
        self.scale = scale
        self.frame = 0

    def get_image(self):
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), (128 * self.frame, 0, self.width, self.height))
        image = pygame.transform.scale_by(image, self.scale)

        self.frame += 1
        if self.frame == self.length:
            self.frame = 0

        return image


class Creature:
    def __init__(self, x, y):
        """
        A superclass for all the enemies and the player
        :param x,y : The coordinates of teh creature
        """
        self.x = x
        self.y = y


class Enemy(Creature):
    def __init__(self, x, y, difficulty):
        """
        A subclass for all enemies to inherit from
        :param difficulty: An integer to scale the health and damage of the enemy as the run progresses
        """
        super().__init__(x, y)
        self.difficulty = difficulty
        self.droppable = []


class Slime(Enemy):
    def __init__(self, colour, x, y, difficulty):
        super().__init__(x, y, difficulty)

        # Dict containing all the spritesheets for the Slime's animations
        self.spritesheets = {
            'move_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Enemies', 'Slime', colour, 'Move_Right.png')), 128, 128, 7, 1),
            'move_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Enemies', 'Slime', colour, 'Move_Left.png')), 128, 128, 7, 1)
        }

        # Stats
        self.health = 10
        self.damage = 10

        self.state = 'move_right'

    def return_sprite(self):
        return self.spritesheets[self.state].get_image()

    def return_coords(self):
        return self.x, self.y
