import pygame
import os
import random
import rooms


def Factory(enemy, *args):
    """
    A function to return the appropriate subcalss based on an input
    :param enemy: the subclass name
    :param args: the subcalss arguments
    :return: the subclass object
    """

    localisers = {
        "Slime": Slime
    }

    return localisers[enemy](*args)


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

    def update(self):
        self.frame += 1
        if self.frame == self.length:
            self.frame = 0

    def get_image(self):
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), (self.width * self.frame, 0, self.width, self.height))
        image = pygame.transform.scale_by(image, self.scale)

        return image


class Creature:
    def __init__(self):
        """
        A superclass for all the enemies and the player
        """
        self.hitbox = pygame.Rect

    def get_tile(self):
        for column in rooms.TILES:
            for tile in column:
                if tile.return_hitbox().collidepoint(self.hitbox.centerx, self.hitbox.centery):
                    return tile


class Enemy(Creature):
    def __init__(self, difficulty, speed, health):
        """
        A subclass for all enemies to inherit from
        :param difficulty: An integer to scale the health and damage of the enemy as the run progresses
        """
        super().__init__()
        self.difficulty = difficulty
        self.droppable = []
        self.speed = speed
        self.health = health
        self.state = None
        self.tile_index = [0][0]

    def move(self, x, y):
        dist_x = x - self.hitbox.centerx
        dist_y = y - self.hitbox.centery
        tot_dist = ((dist_x ** 2) + (dist_y ** 2)) ** 0.5

        if tot_dist < 5:
            pass
        else:
            scale_factor = self.speed / tot_dist

            self.hitbox.x += int(dist_x * scale_factor)
            self.hitbox.y += int(dist_y * scale_factor)


class Slime(Enemy):
    def __init__(self, x, y, difficulty):
        super().__init__(difficulty, 5, 10)

        self.colour = random.choice(['Red', 'Green', 'Blue'])

        # Dict containing all the spritesheets for the Slime's animations
        self.spritesheets = {
            'move_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Enemies', 'Slime', self.colour, 'Move_Right.png')), 128, 128, 7, 1),
            'move_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Enemies', 'Slime', self.colour, 'Move_Left.png')), 128, 128, 7, 1)
        }

        # Stats
        self.damage = 10

        self.state = 'move_left'
        self.sprite = self.return_sprite()
        self.hitbox = pygame.Rect(x, y, 50, 30)
        self.hitbox.center = [x, y]

    def return_sprite(self):
        self.spritesheets[self.state].update()
        return self.spritesheets[self.state].get_image()

    def get_coords(self):
        return [self.hitbox.x - 45, self.hitbox.y - 100]

    def return_hitbox(self):
        return self.hitbox
