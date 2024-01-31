from creatures import Factory, Spritesheet
import map
import random
import pygame
import os


class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(x, y, 70, 70)
        self.occupied = False
        self.sprite = None

    def return_occupied(self):
        return self.occupied

    def return_hitbox(self):
        return self.hitbox

    def return_coords(self):
        return [self.x, self.y]

    def return_sprite(self):
        return self.sprite


class Barrel(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.occupied = True
        self.sprite = pygame.transform.scale_by(
            pygame.image.load(os.path.join('Sprites', 'Environment', 'Obstacles', 'Barrel.png')), 2)


class Trap(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.spritesheet = Spritesheet(pygame.image.load(
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
        self.tiles = []

    def draw_grid(self):
        for tile in self.tiles:
            if tile.return_occupied():
                pygame.draw.rect(self.win, (255, 0, 0), tile.return_hitbox(), 1)
            else:
                pygame.draw.rect(self.win, (255, 0, 0), tile.return_hitbox(), 1)

    def generate(self):
        for x in range(24):
            for y in range(15):
                if [x, y] in map.OBSTACLE_MAP:
                    if random.randint(1, 10) == 1:
                        tile = Trap(x * 70, y * 70)
                    else:
                        tile = Barrel(x * 70, y * 70)
                else:
                    tile = Tile(x * 70, y * 70)
                self.tiles.append(tile)

        # for coords in map.ENEMY_MAP:
        #     self.add_enemy('Slime', coords[0], coords[1], 1)

    def draw_obstacles(self):

        for tile in self.tiles:
            if tile.return_sprite() is not None:
                self.win.blit(tile.return_sprite(), tile.return_coords())

        # for trap in self.traps:
        #     sprite = trap.return_sprite()
        #     coords = trap.return_coords()
        #     self.win.blit(sprite, coords)


    def add_enemy(self, name, x, y, difficulty):
        self.enemies.append(Factory(name, x, y, difficulty))

    def draw_enemies(self, x, y):
        for enemy in self.enemies:
            enemy.move(x, y)
            sprite = enemy.return_sprite()
            coords = enemy.return_coords()
            self.win.blit(sprite, coords)

    def draw_enemy_hitboxes(self):
        for enemy in self.enemies:
            enemy.draw_hitbox()
