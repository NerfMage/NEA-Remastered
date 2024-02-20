import creatures
import map
import random
import pygame
import os

TILES = []


def get_surrounding(tile) -> list:
    """
    Function that returns all surrounding tiles for a given tile
    :param tile: The given tile
    :return: List of all surrounding tiles
    """
    row = tile.get_row()
    column = tile.get_column()
    surrounding = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 22 > column + i >= 0 and 15 > row + j >= 0:
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

        self.g = 0
        self.h = 999
        self.f = 0
        self.parent = None

    def set_g(self, g):
        self.g = g
        self.f = self.g + self.h

    def set_h(self, h):
        self.h = h
        self.f = self.g + self.h

    def get_h(self):
        return self.h

    def get_f(self):
        return self.f

    def get_g(self):
        return self.g

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_column(self):
        return self.column

    def get_row(self):
        return self.row

    def return_occupied(self):
        return self.occupied

    def return_hitbox(self):
        return self.hitbox

    def get_coords(self):
        return [self.x, self.y]

    def return_center(self):
        return [self.hitbox.centerx, self.hitbox.centery]

    def return_sprite(self):
        return self.sprite

    def __str__(self):
        return str(self.row) + str(self.column)


def manhattan(start: Tile, end: Tile):
    dist_x = abs(end.return_center()[0] - start.return_center()[0])
    dist_y = abs(end.return_center()[1] - start.return_center()[1])

    return dist_x + dist_y


def astar(start: Tile, end: Tile):
    currentNode = start
    openList = [currentNode]
    closedList = []

    while currentNode != end:
        openList.remove(currentNode)
        closedList.append(currentNode)

        for tile in get_surrounding(currentNode):
            if tile not in closedList and not tile.return_occupied():
                if tile not in openList:
                    tile.set_parent(currentNode)
                    # tile.set_g(manhattan(start, tile))
                    tile.set_h(manhattan(tile, end))
                    openList.append(tile)
                # else:
                #     if tile.get_g() < (currentNode.get_g() + manhattan(currentNode, tile)):
                #         tile.set_parent(currentNode)
                #         tile.set_g(currentNode.get_g() + manhattan(currentNode, tile))

        currentNode = openList[-1]
        for tile in openList:
            if tile.get_h() < currentNode.get_h():
                currentNode = tile

    path = []

    while currentNode.get_parent() is not None:
        path.append(currentNode.get_parent())
        currentNode = currentNode.get_parent()

    return path


class Barrel(Tile):
    def __init__(self, x, y, row,  column):
        super().__init__(x, y, row, column)
        self.occupied = True
        self.sprite = pygame.transform.scale_by(
            pygame.image.load(os.path.join('Sprites', 'Environment', 'Obstacles', 'Barrel.png')), 2)


class Trap(Tile):
    def __init__(self, x, y, row, column):
        super().__init__(x, y, row, column)
        self.spritesheet = creatures.Spritesheet(pygame.image.load(
            os.path.join('Sprites', 'Environment', 'Obstacles', 'Bear_Trap.png')), 32, 32, 4, 2)
        self.sprite = self.spritesheet.get_image()
        self.activated = False


class Room:
    def __init__(self, difficulty):
        """
        A class to hold all the objects in one level
        :param difficulty: The difficulty scalar of all the enemies in the room
        """
        self.win = pygame.display.get_surface()
        self.difficulty = difficulty
        self.enemies = []

    def draw_grid(self):
        for column in TILES:
            for tile in column:
                if tile.return_occupied():
                    pygame.draw.rect(self.win, (255, 0, 0), tile.return_hitbox())
                else:
                    pygame.draw.rect(self.win, (255, 0, 0), tile.return_hitbox(), 1)

        for i in get_surrounding(self.enemies[0].get_tile()):
            pygame.draw.rect(self.win, (0, 0, 255), i.return_hitbox())

        pygame.draw.rect(self.win, (50, 50, 50), TILES[10][10].return_hitbox())

        for tile in astar(self.enemies[0].get_tile(), TILES[10][10]):
            pygame.draw.rect(self.win, (50, 50, 50), tile.return_hitbox())

    def generate(self):
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

        for coords in map.ENEMY_MAP:
            enemy = creatures.Factory('Slime', coords[0] * 70 + 35, coords[1] * 70 + 35, 1)
            self.enemies.append(enemy)

    def draw_obstacles(self):
        for column in TILES:
            for tile in column:
                if tile.return_sprite() is not None:
                    self.win.blit(tile.return_sprite(), tile.get_coords())

    def draw_enemies(self):
        for enemy in self.enemies:
            sprite = enemy.return_sprite()
            coords = enemy.get_coords()
            self.win.blit(sprite, coords)

    def draw_enemy_hitboxes(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.win, (0, 255, 0), enemy.return_hitbox())
