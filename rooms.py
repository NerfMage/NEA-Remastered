import creatures
import obstacles
import map
import random


class Room:
    def __init__(self, difficulty):
        """
        A class to hold all the objects in one level
        :param difficulty: The difficulty scalar of all the enemies in the room
        """
        self.difficulty = difficulty
        self.obstacles = []
        self.traps = []
        self.enemies = []

    def add_enemy(self, name, x, y, difficulty):
        self.enemies.append(creatures.Factory(name, x, y, difficulty))

    def draw_enemies(self, win, x, y):
        for enemy in self.enemies:
            enemy.move(x, y)
            sprite = enemy.return_sprite()
            coords = enemy.return_coords()
            win.blit(sprite, coords)

    def add_obstacle(self, name, x, y):
        self.obstacles.append(obstacles.Obstacle(name, x, y))

    def add_trap(self, name, x, y):
        self.traps.append(obstacles.Trap(name, x, y))

    def generate(self):
        for coords in map.OBSTACLE_MAP:
            if random.randint(1, 10) == 1:
                self.add_trap('Bear_Trap', coords[0], coords[1])
            else:
                self.add_obstacle('Barrel', coords[0], coords[1])

        for coords in map.ENEMY_MAP:
            self.add_enemy('Slime', coords[0], coords[1], 1)

    def draw_obstacles(self, win):
        for trap in self.traps:
            sprite = trap.return_sprite()
            coords = trap.return_coords()
            win.blit(sprite, coords)

        for obstacle in self.obstacles:
            sprite = obstacle.return_sprite()
            coords = obstacle.return_coords()
            win.blit(sprite, coords)
