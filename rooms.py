import astar
import creatures
import map
import random
import pygame
import os

TILES = []


def get_surrounding(tile) -> list:
    """
    :param tile: The given tile
    :return: List of all surrounding tiles
    """
    row = tile.get_row()
    column = tile.get_column()
    surrounding = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 23 > (column + i) >= 0 and 14 > (row + j) >= 0:
                if TILES[column + i][row + j] != tile and not tile.return_occupied():
                    surrounding.append(TILES[column + i][row + j])

    return surrounding


class Tile:
    def __init__(self, x, y, column, row):
        """
        A class for each 70x70px tile in the level
        :param x: The x-coordinate
        :param y: The y-coordinate
        :param column: Its column number
        :param row: Its row number
        """
        self.x = x
        self.y = y
        self.column = column
        self.row = row
        self.hitbox = pygame.Rect(x, y, 70, 70)
        self.occupied = False
        self.sprite = None

    def get_column(self) -> int:
        return self.column

    def get_row(self) -> int:
        return self.row

    def return_occupied(self) -> bool:
        return self.occupied

    def get_hitbox(self) -> pygame.Rect:
        return self.hitbox

    def get_coords(self) -> list:
        return [self.x, self.y]

    def get_center(self, coord) -> int:
        if coord == 'x':
            return self.hitbox.centerx
        elif coord == 'y':
            return self.hitbox.centery

    def return_sprite(self) -> pygame.Surface:
        return self.sprite

    def __str__(self):
        return str(self.row) + str(self.column)


class Barrel(Tile):
    def __init__(self, x, y, row,  column):
        """
        Class for all tiles in the map containing a Barrel obstacles
        :param x: x-coord
        :param y: y-coord
        :param row: Row in the tile map
        :param column: Column in the tile map
        """
        super().__init__(x, y, row, column)
        self.occupied = True
        self.sprite = pygame.transform.scale_by(
            pygame.image.load(os.path.join('Sprites', 'Environment', 'Obstacles', 'Barrel.png')), 2)


class Trap(Tile):
    def __init__(self, x, y, row, column):
        """
        Class for all tiles in the map containing a trap
        :param x: x-coord
        :param y: y-coord
        :param row: Row in the tile map
        :param column: Column in the tile map
        """
        super().__init__(x, y, row, column)
        self.spritesheet = creatures.Spritesheet(pygame.image.load(
            os.path.join('Sprites', 'Environment', 'Obstacles', 'Bear_Trap.png')), 32, 32, 4, 2)
        self.sprite = self.spritesheet.get_image()
        self.activated = False


class Room:
    def __init__(self, difficulty, player):
        """
        A class to hold all the objects in one level
        :param difficulty: The difficulty scalar of all the enemies in the room
        """
        self.win = pygame.display.get_surface()
        self.difficulty = difficulty
        self.enemies = []
        self.player = player

    def draw_grid(self):
        """
        Method to help with debugging
        Draws a grid that outlines all tiles on the map
        :return: None
        """
        for column in TILES:
            for tile in column:
                if tile.return_occupied():
                    pygame.draw.rect(self.win, (255, 0, 0), tile.get_hitbox())
                else:
                    pygame.draw.rect(self.win, (255, 0, 0), tile.get_hitbox(), 1)

        pygame.draw.rect(self.win, (0, 0, 255), TILES[10][10].get_hitbox())

    def generate(self):
        """
        Generates the tileset of obstacles and traps then generates enemies
        Based on noise mapping
        :return: None
        """
        for x in range(24):
            column = []
            for y in range(15):
                if [x, y] in map.OBSTACLE_MAP:
                    if random.randint(1, 10) == 1:
                        tile = Trap(x * 70, y * 70, x, y)
                    else:
                        tile = Barrel(x * 70, y * 70, x, y)
                else:
                    tile = Tile(x * 70, y * 70, x, y)
                column.append(tile)
            TILES.append(column)

        # for coords in map.ENEMY_MAP:
        #     enemy = creatures.Factory('Slime', coords[0] * 70 + 35, coords[1] * 70 + 35, 1)
        #     self.enemies.append(enemy)

    def draw_obstacles(self):
        """
        Method that draws all obstacle sprites to their respective locations
        :return: None
        """
        for column in TILES:
            for tile in column:
                if tile.return_sprite() is not None:
                    self.win.blit(tile.return_sprite(), tile.get_coords())

    def draw_creatures(self):
        """
        Method that draws all creatures in the level to their respective locations
        :return: None
        """
        for enemy in self.enemies:
            enemy.move(TILES[0][0])
            # for tile in astar.astar(enemy.get_tile(), TILES[10][10]):
            #     pygame.draw.rect(self.win, (50, 50, 50), tile.get_hitbox())
            sprite = enemy.return_sprite()
            coords = enemy.get_coords()
            self.win.blit(sprite, coords)

        self.win.blit(self.player.return_sprite(), self.player.get_coords())

    def draw_enemy_hitboxes(self):
        """
        Debugging method that draws all enemy hitboxes
        :return: None
        """
        for enemy in self.enemies:
            pygame.draw.rect(self.win, (0, 255, 0), enemy.get_hitbox())

    def draw_player_hitbox(self):
        """
        Debugging method that draws player hitbox
        :return: None
        """
        pygame.draw.rect(self.win, (0, 0, 255), self.player.get_hitbox())
        pygame.draw.rect(self.win, (0, 0, 255), self.player.get_tile().get_hitbox())
