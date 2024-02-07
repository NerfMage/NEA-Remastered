import creatures
import map
import random
import pygame
import os

TILES = []


def get_surrounding(tile):
    row = tile.get_row()
    column = tile.get_column()
    surrounding = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 22 > column + i >= 0 and 15 > row + j >= 0:
                surrounding.append(TILES[column + i][row + j])

    return surrounding

class Tile:
    def __init__(self, x, y, column, row):
        self.x = x
        self.y = y
        self.column = column
        self.row = row
        self.hitbox = pygame.Rect(x, y, 70, 70)
        self.occupied = False
        self.sprite = None

    def get_column(self):
        return self.column

    def get_row(self):
        return self.row

    def return_occupied(self):
        return self.occupied

    def return_hitbox(self):
        return self.hitbox

    def return_coords(self):
        return [self.x, self.y]

    def return_sprite(self):
        return self.sprite

    def __str__(self):
        return str(self.row) + str(self.column)


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

        for enemy in self.enemies:
            pygame.draw.rect(self.win, (0, 0, 255), enemy.get_tile().return_hitbox())

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

        # for coords in map.ENEMY_MAP:
        #     enemy = Factory('Slime', coords[0] * 70 + 35, coords[1] * 70 + 35, 1)
        #     self.enemies.append(enemy)
        self.enemies.append(creatures.Factory('Slime', 35, 35, 1))

    def draw_obstacles(self):
        for column in TILES:
            for tile in column:
                if tile.return_sprite() is not None:
                    self.win.blit(tile.return_sprite(), tile.return_coords())

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.move(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            sprite = enemy.return_sprite()
            coords = enemy.return_coords()
            self.win.blit(sprite, coords)

    def draw_enemy_hitboxes(self):
        for enemy in self.enemies:
            pygame.draw.rect(self.win, (0, 255, 0), enemy.return_hitbox())
