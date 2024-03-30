import astar
import creatures
import map
import system
import random
import pygame
import os
import items

pygame.font.init()

TILES = []  # 2D array for all the Tiles in the current Room
FONT = pygame.font.Font('ArcadeFont.ttf', 30)


def get_surrounding(tile) -> list:
    """
    Function used to find surrounding tiles of a given tile
    :param tile: The given tile
    :return: List of all surrounding tiles
    """
    row = tile.get_row()
    column = tile.get_column()
    surrounding = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if 23 >= (column + i) >= 0 and 14 >= (row + j) >= 0:
                if TILES[column + i][row + j] != tile and not tile.return_occupied():
                    surrounding.append(TILES[column + i][row + j])

    return surrounding


def get_left(tile):
    """
    :param tile: The given Tile
    :return: The Tile to the left of the given Tile, if it exists
    """
    if tile.get_column() > 0:
        return TILES[tile.get_column() - 1][tile.get_row()]
    else:
        return None


def get_right(tile):
    """
    :param tile: The given Tile
    :return: The Tile to the right of the given Tile, if it exists
    """
    if tile.get_column() < 23:
        return TILES[tile.get_column() + 1][tile.get_row()]
    else:
        return None


def get_up(tile):
    """
    :param tile: The given Tile
    :return: The Tile above the given Tile, if it exists
    """
    if tile.get_row() > 0:
        return TILES[tile.get_column()][tile.get_row()-1]
    else:
        return None


def get_down(tile):
    """
    :param tile: The given Tile
    :return: The Tile to below the given Tile, if it exists
    """
    if tile.get_row() < 14:
        return TILES[tile.get_column()][tile.get_row() + 1]
    else:
        return None


class Tile:
    def __init__(self, x, y, column, row, room):
        """
        A class for each 70x70px tile in the level
        :param x: The x-coordinate
        :param y: The y-coordinate
        :param column: Its column number
        :param row: Its row number
        :param room: The room the tile is part of
        """
        self.x = x
        self.y = y
        self.column = column
        self.row = row
        self.room = room
        self.hitbox = pygame.Rect(x, y, 70, 70)
        self.loot = []
        self.occupied = False
        self.sprite = None

    def get_column(self) -> int:
        """
        :return: The Tile's column in the TILES array
        """
        return self.column

    def get_row(self) -> int:
        """
        :return: The Tile's row in the TILES array
        """
        return self.row

    def return_occupied(self) -> bool:
        """
        :return: If the Tile is traversable or not
        """
        return self.occupied

    def get_hitbox(self) -> pygame.Rect:
        """
        :return: The rectangle that the Tile covers
        """
        return self.hitbox

    def get_coords(self) -> list[int, int]:
        """
        :return: The Tiles physical coordinates as [x, y]
        """
        return [self.x, self.y]

    def get_center(self, coord) -> int:
        """
        :param coord: Either x or y, dependingon desired coordinate
        :return: Either the x or y cooridnate of the Tile's center
        """
        if coord == 'x':
            return self.hitbox.centerx
        elif coord == 'y':
            return self.hitbox.centery

    def return_sprite(self) -> pygame.Surface:
        """
        :return: The Tile's sprite, in its current state (if animated)
        """
        return self.sprite

    def get_map_coords(self) -> list[int, int]:
        """
        :return: The Tile's row and column as list, format [column, row]
        """
        return [self.column, self.row]

    def get_enemies(self) -> list:
        """
        :return: A list of all the Enemies whose hitbox touches the Tile
        """
        temp = []
        for enemy in self.room.get_enemies():
            if self.hitbox.colliderect(enemy.get_hitbox()):
                temp.append(enemy)
        return temp

    def add_loot(self, item):
        """
        Method that adds droppable loot to the Tile so tht it can be picked up by the Player
        :param item: The item that was dropped
        """
        self.loot.append(item)

    def get_loot(self) -> list:
        """
        :return: The list of all items that have been dropped on the Tile
        """
        return self.loot

    def take_loot(self):
        """
        Adds all items dropped on the Tile to the Player
        Only works on Gold at the moment as it is the only dropped item
        """
        for item in self.loot:
            if isinstance(item, items.Gold):
                system.PLAYER.add_gold(item.get_value())
                self.loot.remove(item)
                del item  # Deletes the item to save memory

    def __str__(self) -> str:
        """
        Causes the coordinates of the Tile to be returned when printing the objecet
        Allows for easier debuggin
        :return: The Tile's map coordinates as a string
        """
        return str(self.column) + str(self.row)


class Barrel(Tile):
    def __init__(self, x, y, row,  column,  room):
        """
        Class for all tiles in the map containing a Barrel obstacle
        :param x: x-coord
        :param y: y-coord
        :param row: Row in the tile map
        :param column: Column in the tile map
        :param room: The Room that the Tile belongs to
        """
        super().__init__(x, y, row, column, room)
        self.occupied = True  # Non-traversable Tile
        self.sprite = pygame.transform.scale_by(
            pygame.image.load(os.path.join('Sprites', 'Environment', 'Obstacles', 'Barrel.png')), 2)


class Trap(Tile):
    def __init__(self, x, y, row, column, room):
        """
        Class for all tiles in the map containing a trap
        :param x: x-coord
        :param y: y-coord
        :param row: Row in the tile map
        :param column: Column in the tile map
        :param room: The Room that the Tile belongs to
        """
        super().__init__(x, y, row, column, room)
        self.spritesheet = creatures.Spritesheet(pygame.image.load(
            os.path.join('Sprites', 'Environment', 'Obstacles', 'Bear_Trap.png')), 32, 32, 4, 2, 1, 'r')
        self.sprite = self.spritesheet.get_image()
        self.activated = False  # Boolean to ensure that the Trap cannot be activated multiple times

    def activate(self):
        """
        Updates the Spritesheet to makethe Trap animation play
        Damages the Player for a small amount
        """
        if not self.activated:
            self.activated = True
            system.PLAYER.hit(30 * self.room.difficulty)
            self.spritesheet.update()
            self.sprite = self.spritesheet.get_image()


class Door(Tile):
    def __init__(self, x, y, row, column, room):
        """
        Class for the Door Tile in the Room
        Each Room hs only one Door which leads to the next Room
        Door only opens when all Enemies have been defeated
        :param x: x-coord
        :param y: y-coord
        :param row: Row in the tile map
        :param column: Column in the tile map
        :param room: The Room that the Tile belongs to
        """
        super().__init__(x, y, row, column, room)
        self.spritesheet = creatures.Spritesheet(pygame.image.load(
            os.path.join('Sprites', 'Environment', 'Door.png')), 70, 70, 2, 1.5, 1, 'r')
        self.sprite = self.spritesheet.get_image()
        self.opened = False

    def open(self):
        """
        Opens the Door
        Updates the Door sprite to appear open to alert the Player
        """
        self.opened = True
        self.spritesheet.update()
        self.sprite = self.spritesheet.get_image()

    def is_open(self) -> bool:
        """
        :return: If the Door is open or not
        """
        return self.opened


def draw_grid():
    """
    Method to help with debugging
    Draws a grid that outlines all tiles on the map
    """
    for column in TILES:
        for tile in column:
            if tile.return_occupied():
                pygame.draw.rect(system.WIN, (255, 0, 0), tile.get_hitbox())
            else:
                pygame.draw.rect(system.WIN, (255, 0, 0), tile.get_hitbox(), 1)


def draw_obstacles():
    """
    Method that draws all obstacle sprites to their respective locations
    """
    for column in TILES:
        for tile in column:
            if tile.return_sprite() is not None:
                system.WIN.blit(tile.return_sprite(), tile.get_coords())

            for item in tile.get_loot():
                if isinstance(item, items.Gold):
                    pygame.draw.circle(system.WIN, (255, 215, 0),
                                       (item.get_coords()[0], item.get_coords()[1]), 10)


def draw_player_hitbox():
    """
    Debugging method that draws Player hitbox
    """
    pygame.draw.rect(system.WIN, (0, 0, 255), system.PLAYER.get_tile().get_hitbox())


class Room:
    def __init__(self, difficulty):
        """
        A class to hold all the objects in one level
        :param difficulty: The difficulty scalar of all the enemies in the room
        """
        self.door = None  # Will hold the Door Tile when it is created
        self.difficulty = difficulty
        self.enemies = []  # List of all the Enemies in the Room
        self.generate()

    def generate(self):
        """
        Generates the tileset of obstacles and traps then generates Enemies
        Based on noise mapping from map.py
        """
        TILES.clear()  # Resets the TILES array every time a new Room is created
        map.generate_map()  # Generates the ENEMY_MAP and OBSTACLE_MAP every time a new Room is created
        openList = []  # List of all possible coordinates for the Door
        for x in range(24):
            column = []
            for y in range(15):
                if [x, y] in map.OBSTACLE_MAP:
                    if random.randint(1, 10) == 1:  # 10% chance for a Barrel to become a Trap
                        tile = Trap(x * 70, y * 70, x, y, self)
                    else:
                        tile = Barrel(x * 70, y * 70, x, y, self)
                else:
                    if x == 23 or x == 0 or y == 0 or y == 14:
                        # Adds non-occupied Tiles from the border to the openList
                        openList.append([x, y])
                    tile = Tile(x * 70, y * 70, x, y, self)
                column.append(tile)
            TILES.append(column)

        doorCoord = random.choice(openList)  # Picks a random coordinate from the openList for the Door
        self.door = Door(doorCoord[0] * 70, doorCoord[1] * 70, doorCoord[0], doorCoord[1], self)
        TILES[doorCoord[0]][doorCoord[1]] = self.door  # Door added to TILES

        # Adds Enemies to the Room
        enemy_count = 0
        for coords in map.ENEMY_MAP:
            enemy = creatures.Factory('Slime', coords[0] * 70 + 35, coords[1] * 70 + 35, 1)
            self.enemies.append(enemy)
            enemy_count += 1
            if enemy_count == 12:  # Caps number of Enemies at 12 to save processing power and not overwhelm Player
                break

    def draw_creatures(self):
        """
        Method that draws all creatures in the level to their respective locations
        """

        # Draws the Player sprite
        system.WIN.blit(system.PLAYER.return_sprite(), system.PLAYER.get_coords())
        # Draws all Enemy sprites
        for enemy in self.enemies:
            if not enemy.is_dead():  # Doesn't draw dead Enemies
                enemy.move(system.PLAYER.get_tile())
                sprite = enemy.return_sprite()
                coords = enemy.get_coords()
                system.WIN.blit(sprite, coords)
                # Draws Enemy health bars
                pygame.draw.rect(system.WIN, (255, 0, 0), enemy.get_health_bar()[0])
                pygame.draw.rect(system.WIN, (0, 255, 0), enemy.get_health_bar()[1])

        # Draws the Player healthbar
        pygame.draw.rect(system.WIN, (255, 255, 255), (7, 977,  406, 66))
        pygame.draw.rect(system.WIN, (255, 0, 0), (10, 980, 400, 60))
        pygame.draw.rect(system.WIN, (0, 255, 0), system.PLAYER.get_healthbar())
        # Draws cooldown circles
        for i, values in enumerate(system.PLAYER.get_cooldowns().values()):
            pygame.draw.circle(system.WIN, (255, 255, 255), (1600 - 90 * i, 990), 40)
            if values[0] >= values[1]:
                pygame.draw.circle(system.WIN, (0, 0, 255), (1600 - 90 * i, 990), 35)

        # Draws gold count
        gold_text = FONT.render(str(system.PLAYER.get_gold()), True, (255, 215, 0))
        pygame.draw.circle(system.WIN, (255, 215, 0), (1550, 50), 20)
        system.WIN.blit(gold_text, (1580, 38))

    def draw_enemy_hitboxes(self):
        """
        Debugging method that draws all enemy hitboxes as green rectangles
        """
        for enemy in self.enemies:
            pygame.draw.rect(system.WIN, (0, 255, 0), enemy.get_hitbox())
            for tile in astar.astar(enemy.get_tile(), system.PLAYER.get_tile()):
                pygame.draw.rect(system.WIN, (50, 50, 50), tile.get_hitbox())

    def get_enemies(self) -> list:
        """
        :return: A list of all the live Enemies in the Room
        """
        temp = []
        for enemy in self.enemies:
            if not enemy.is_dead():
                temp.append(enemy)
        return temp

    def check_win(self) -> bool:
        """
        Method to check if the Player has 'beaten' the level or not
        :return: True if all Enemeies are dead, False otherwise
        """
        if any(not enemy.is_dead() for enemy in self.enemies):
            return False
        else:
            if not self.door.is_open():
                self.door.open()
            return True

    def next_room(self):
        """
        Method that creates the next Room in the run
        :return: A new Room object with higher difficulty
        """
        system.PLAYER.heal(int(50 * self.difficulty))  # Heals the Player slightly between Rooms
        return Room(self.difficulty + 0.5)

    def get_door(self) -> Door:
        """
        :return: The Room's Door Tile
        """
        return self.door
