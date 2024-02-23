import pygame
import os
import random
import rooms
import astar


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
        """
        Function that updates the spritesheet
        :return: None
        """
        self.frame += 1
        # Increments frame counter by 1
        if self.frame == self.length:
            # Resets when reaching the end of the spritesheet strip
            self.frame = 0

    def get_image(self) -> pygame.Surface:
        """"
        :return: Current frame from Spritesheet as an image
        """
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), (self.width * self.frame, 0, self.width, self.height))
        image = pygame.transform.scale_by(image, self.scale)

        return image


class Creature:
    def __init__(self, hitbox):
        """
        A superclass for all the enemies and the player
        :param hitbox: a Pygame.Rect for the objects' hitbox
        """
        self.hitbox = hitbox

    def get_tile(self):
        """
        :return: the tile that the Creature is currently occupying
        """
        for column in rooms.TILES:
            for tile in column:
                if pygame.Rect.colliderect(self.get_hitbox(), tile.get_hitbox()) and not tile.return_occupied():
                    return tile

    def get_hitbox(self) -> pygame.Rect:
        return self.hitbox


class Enemy(Creature):
    def __init__(self, difficulty, speed, health, hitbox):
        """
        Class for all the enemies in the game
        Inherits from Creature class
        :param difficulty: Scalar to increase class difficulty as the game continues
        :param speed: Number of pixels moved per frame
        :param health: Hit points that the Enemy can recive before dying
        :param hitbox: Pygame Rect that governs all collisions
        """
        super().__init__(hitbox)
        self.difficulty = difficulty
        self.droppable = []
        self.speed = speed
        self.health = health
        self.state = None

    def move(self, dest):
        """
        Method to move the Enemy after each frame, uses astar algorithm
        :param dest: The target Tile
        :return: None
        """
        if len(astar.astar(self.get_tile(), dest)) > 1:
            tile = astar.astar(self.get_tile(), dest)[-2]
            # Selects the nearest tile on the path to the destination other than its own tile

            if astar.manhattan(self.get_tile(), dest) > 75:
                # Checks if the nemy is close enough to the destination to make and attack
                dist_x = self.hitbox.centerx - tile.get_center('x')
                dist_y = self.hitbox.centery - tile.get_center('y')
                tot_dist = ((dist_x ** 2) + (dist_y ** 2)) ** 0.5
                scale_factor = self.speed / tot_dist
                self.hitbox.x -= dist_x * scale_factor
                self.hitbox.y -= dist_y * scale_factor


class Slime(Enemy):
    def __init__(self, x, y, difficulty):
        """
        Class for the Slime enemy
        :param x: Starting x coord
        :param y: Starting y coord
        :param difficulty: Starting difficulty
        """
        super().__init__(difficulty, 5, 10, pygame.Rect(x, y, 50, 30))

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
        self.hitbox.center = [x, y]

    def return_sprite(self) -> pygame.Surface:
        """
        :return: Image from the Spritesheet
        """
        self.spritesheets[self.state].update()
        return self.spritesheets[self.state].get_image()

    def get_coords(self) -> list:
        """
        :return: The coordinates that the sprite needs to be drawn to in order for the hitbox to be centered
        """
        return [self.hitbox.x - 45, self.hitbox.y - 100]
