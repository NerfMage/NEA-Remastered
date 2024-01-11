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

    def add_enemy(self, name, x, y, difficulty):

        self.enemies.append(creatures.Factory(name, x, y, difficulty))

    def draw_enemies(self, win):
        for enemy in self.enemies:
            sprite = enemy.return_sprite()
            coords = enemy.return_coords()
            win.blit(sprite, coords)
