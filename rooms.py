import creatures


class Room:
    def __init__(self, difficulty):
        """
        A class to hold all the objects in one level
        :param difficulty: The difficulty scalar of all teh enemies in the room
        """
        self.difficulty = difficulty
        self.obstacles = []
        self.enemies = []

    def add_enemy(self):
        self.enemies.append(creatures.Slime('Green', 100, 100, 1))

    def draw_enemies(self, win):
        for enemy in self.enemies:
            sprite = enemy.return_sprite()
            coords = enemy.return_coords()
            win.blit(sprite, coords)
