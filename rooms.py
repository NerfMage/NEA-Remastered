import creatures
import obstacles
import map


class Room:
    def __init__(self, difficulty):
        """
        A class to hold all the objects in one level
        :param difficulty: The difficulty scalar of all the enemies in the room
        """
        self.difficulty = difficulty
        self.obstacles = []
        self.enemies = []

    def add_enemy(self, name, x, y, difficulty):
        self.enemies.append(creatures.Factory(name, x, y, difficulty))

    def draw_enemies(self, win, x, y):
        for enemy in self.enemies:
            enemy.move(x, y)
            sprite = enemy.return_sprite()
            coords = enemy.return_coords()
            win.blit(sprite, coords)

    def add_obstacles(self):
        for coords in map.MAP:
            self.obstacles.append(obstacles.Obstacle('Barrel', coords[0], coords[1]))

    def draw_obstacles(self, win):
        for obstacle in self.obstacles:
            sprite = obstacle.return_sprite()
            coords = obstacle.return_coords()
            win.blit(sprite, coords)
