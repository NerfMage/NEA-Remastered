import pygame
import os
import random
import rooms
import astar
import system


def Factory(enemy, *args):
    """
    A function to return the appropriate subcalss based on an n
    :param enemy: the subclass name
    :param args: the subcalss arguments
    :return: the subclass object
    """

    localisers = {
        "Slime": Slime
    }

    return localisers[enemy](*args)


class Spritesheet:
    def __init__(self, sheet, width, height, length, scale, speed, direction):
        """
        A class to animate spritesheets
        :param sheet: The image file of the sheet
        :param width: The width of each frame
        :param height: The height of each frame
        :param length: The number of frame on the sheet
        :param scale: The scale factor for the sprite to be enlarged by
        :param speed: Scales down the speed of the animation to make it more visible
        :param direction: States whether the sprite is facing left or right
        """
        self.sheet = sheet
        self.width = width
        self.height = height
        self.length = length
        self.scale = scale
        self.speed = speed
        self.direction = direction
        self.frame = 0

    def update(self):
        """
        Function that updates the spritesheet
        :return: None
        """
        self.frame += 1
        # Increments frame counter by 1
        if self.frame == (self.length * self.speed):
            # Resets when reaching the end of the spritesheet strip
            self.frame = 0

    def get_image(self) -> pygame.Surface:
        """"
        :return: Current frame from Spritesheet as an image
        """
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), (self.width * (self.frame // self.speed), 0, self.width, self.height))
        image = pygame.transform.scale_by(image, self.scale)
        if self.direction == 'l':
            image = pygame.transform.flip(image, True, False)

        return image.convert_alpha()

    def get_frame(self):
        return self.frame

    def get_len(self):
        return self.frame * self.speed


class Creature:
    def __init__(self, hitbox, speed, health):
        """
        A superclass for all the enemies and the player
        :param hitbox: a Pygame.Rect for the objects' hitbox
        :param speed: an integer value for the number of pixels moved per frame
        """
        self.hitbox = hitbox
        self.speed = speed
        self.spritesheets = {}
        self.state = 'run_left'
        self.max_health = health
        self.current_health = self.max_health

    def get_tile(self):
        """
        :return: the tile that the Creature is currently occupying
        """
        for column in rooms.TILES:
            for tile in column:
                if pygame.Rect.colliderect(self.hitbox, tile.get_hitbox()) and not tile.return_occupied():
                    return tile

    def get_hitbox(self) -> pygame.Rect:
        return self.hitbox

    def return_sprite(self) -> pygame.Surface:
        """
        :return: Image from the Spritesheet
        """
        self.spritesheets[self.state].update()
        return self.spritesheets[self.state].get_image()

    def hit(self, damage: int):
        self.current_health -= damage

    def is_dead(self):
        if self.current_health <= 0:
            return True
        else:
            return False


class Player(Creature):
    def __init__(self, x, y):
        super().__init__(pygame.Rect(x, y, 40, 70), 10, 300)
        # Dict containing all the spritesheets for the Player's animations
        self.spritesheets = {
            'idle_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Idle.png')), 128, 128, 6, 1.5, 1, 'r'),
            'idle_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Idle.png')), 128, 128, 6, 1.5, 1, 'l'),
            'run_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Run.png')), 128, 128, 8, 1.5, 1, 'r'),
            'run_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Run.png')), 128, 128, 8, 1.5, 1, 'l'),
            'attack_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Attack.png')), 128, 128, 4, 1.5, 2, 'r'),
            'attack_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Attack.png')), 128, 128, 4, 1.5, 2, 'l'),
            'secondary_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Secondary.png')), 128, 128, 5, 1.5, 2, 'r'),
            'secondary_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Secondary.png')), 128, 128, 5, 1.5, 2, 'l'),
            'dash_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Dash.png')), 128, 128, 4, 1.5, 2, 'r'),
            'dash_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Player', 'Dash.png')), 128, 128, 4, 1.5, 2, 'l'),
        }
        self.health_bar = pygame.Rect(10, 980, 400, 60)
        self.cooldowns = {
            'secondary': [30, 30],
            'dash': [15, 15],
        }

    def get_coords(self) -> list:
        """
        :return: The coordinates that the sprite needs to be drawn to in order for the hitbox to be centered
        """
        if self.state in ['run_right', 'idle_right', 'attack_right', 'secondary_right', 'dash_right']:
            return [self.hitbox.x - 40, self.hitbox.y - 110]
        elif self.state in ['run_left', 'idle_left', 'attack_left', 'secondary_left', 'dash_left']:
            return [self.hitbox.x - 110, self.hitbox.y - 110]

    def move(self, key):
        if self.state in ['idle_left', 'idle_right', 'run_left', 'run_right']:
            if key[pygame.K_w] and rooms.get_up(self.get_tile()) is not None \
                    and not rooms.get_up(self.get_tile()).return_occupied():
                self.hitbox.y -= self.speed
                if self.state == 'idle_right':
                    self.state = 'run_right'
                elif self.state == 'idle_left':
                    self.state = 'run_left'
            if key[pygame.K_s] and rooms.get_down(self.get_tile()) is not None \
                    and not rooms.get_down(self.get_tile()).return_occupied():
                self.hitbox.y += self.speed
                if self.state == 'idle_right':
                    self.state = 'run_right'
                elif self.state == 'idle_left':
                    self.state = 'run_left'

            if key[pygame.K_a]:
                self.state = 'run_left'
                if rooms.get_left(self.get_tile()) is not None and \
                        not rooms.get_left(self.get_tile()).return_occupied():
                    self.hitbox.x -= self.speed
            if key[pygame.K_d]:
                self.state = 'run_right'
                if rooms.get_right(self.get_tile()) is not None and \
                        not rooms.get_right(self.get_tile()).return_occupied():
                    self.hitbox.x += self.speed

            if key[pygame.K_e] and self.cooldowns['secondary'][0] >= self.cooldowns['secondary'][1]:
                if self.state in ['idle_right', 'run_right']:
                    self.state = 'secondary_right'
                if self.state in ['idle_left', 'run_left']:
                    self.state = 'secondary_left'
                self.cooldowns['secondary'][0] = 0

            if key[pygame.K_SPACE] and self.cooldowns['dash'][0] >= self.cooldowns['dash'][1]:
                if key[pygame.K_a]:
                    self.state = 'dash_left'
                    self.cooldowns['dash'][0] = 0
                elif key[pygame.K_d]:
                    self.state = 'dash_right'
                    self.cooldowns['dash'][0] = 0

            if not any([key[pygame.K_w], key[pygame.K_a], key[pygame.K_s], key[pygame.K_d]]):
                if self.state == 'run_right':
                    self.state = 'idle_right'
                elif self.state == 'run_left':
                    self.state = 'idle_left'

        if self.state in ['attack_left', 'attack_right'] and \
                self.spritesheets[self.state].get_frame() == self.spritesheets[self.state].get_len():
            self.spritesheets[self.state].update()
            if self.state == 'attack_left':
                self.state = 'idle_left'
            if self.state == 'attack_right':
                self.state = 'idle_right'

        if self.state in ['secondary_left', 'secondary_right'] and \
                self.spritesheets[self.state].get_frame() == self.spritesheets[self.state].get_len():
            self.spritesheets[self.state].update()
            self.secondary_attack()
            if self.state == 'secondary_left':
                self.state = 'idle_left'
            if self.state == 'secondary_right':
                self.state = 'idle_right'

        if self.state in ['dash_left', 'dash_right'] and \
                self.spritesheets[self.state].get_frame() == self.spritesheets[self.state].get_len():
            self.spritesheets[self.state].update()
            if self.state == 'dash_left':
                self.state = 'run_left'
            if self.state == 'dash_right':
                self.state = 'run_right'
        elif self.state in ['dash_left', 'dash_right']:
            self.dash()

        if isinstance(self.get_tile(), rooms.Trap):
            self.get_tile().activate()

        for value in self.cooldowns.values():
            value[0] += 1

    def basic_attack(self):
        enemies = []

        for enemy in self.get_tile().get_enemies():
            enemies.append(enemy)

        if self.state in ['run_right', 'idle_right']:
            self.state = 'attack_right'
            try:
                for enemy in rooms.get_right(self.get_tile()).get_enemies():
                    enemies.append(enemy)
            except AttributeError:
                pass
        elif self.state in ['run_left', 'idle_left']:
            self.state = 'attack_left'
            try:
                for enemy in rooms.get_left(self.get_tile()).get_enemies():
                    enemies.append(enemy)
            except AttributeError:
                pass

        for enemy in enemies:
            enemy.hit(25)

    def secondary_attack(self):
        enemies = []
        if self.state == 'secondary_right':
            try:
                for enemy in self.get_tile().get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_right(self.get_tile()).get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_down(self.get_tile()).get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_up(self.get_tile()).get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_up(rooms.get_right(self.get_tile())).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

                for enemy in rooms.get_down(rooms.get_right(self.get_tile())).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

            except AttributeError:
                pass

        elif self.state == 'secondary_left':
            try:
                for enemy in self.get_tile().get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_left(self.get_tile()).get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_down(self.get_tile()).get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_up(self.get_tile()).get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_up(rooms.get_left(self.get_tile())).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

                for enemy in rooms.get_down(rooms.get_left(self.get_tile())).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

            except AttributeError:
                pass

        for enemy in enemies:
            enemy.hit(50)

    def dash(self):
        if self.state == 'dash_left':
            if rooms.get_left(self.get_tile()) is not None and \
                    not rooms.get_left(self.get_tile()).return_occupied():
                self.hitbox.x -= 3 * self.speed

        if self.state == 'dash_right':
            if rooms.get_right(self.get_tile()) is not None and \
                    not rooms.get_right(self.get_tile()).return_occupied():
                self.hitbox.x += 3 * self.speed

        for enemy in self.get_tile().get_enemies():
            enemy.hit(5)

    def get_healthbar(self):
        self.health_bar = self.health_bar = pygame.Rect(10, 980, 400 * (self.current_health / self.max_health), 60)
        return self.health_bar

    def get_cooldowns(self):
        return self.cooldowns

    def get_tile(self):
        """
        :return: the tile that the Creature is currently occupying
        """
        for column in rooms.TILES:
            for tile in column:
                if tile.get_hitbox().collidepoint(self.hitbox.center):
                    return tile


class Enemy(Creature):
    def __init__(self, difficulty, speed, health, damage, hitbox):
        """
        Class for all the enemies in the game
        Inherits from Creature class
        :param difficulty: Scalar to increase class difficulty as the game continues
        :param speed: Number of pixels moved per frame
        :param health: Hit points that the Enemy can receive before dying
        :param hitbox: Pygame Rect that governs all collisions
        """
        super().__init__(hitbox, speed, int(health * difficulty))
        self.difficulty = difficulty
        self.damage = int(damage * difficulty)
        self.health_bar = pygame.Rect(self.hitbox.x, self.hitbox.y - 20, 50, 10)
        self.under_bar = pygame.Rect(self.hitbox.x, self.hitbox.y - 20, 50, 10)

    def move(self, dest):
        """
        Method to move the Enemy after each frame, uses astar algorithm
        :param dest: The target Tile
        :return: None
        """
        if self.get_tile() is not None:
            if len(astar.astar(self.get_tile(), dest)) > 1:
                tile = astar.astar(self.get_tile(), dest)[-2]
                # Selects the nearest tile on the path to the destination other than its own tile

                if astar.manhattan(self.get_tile(), dest) > 75:
                    # Checks if the enemy is close enough to the destination to make and attack
                    dist_x = self.hitbox.centerx - tile.get_center('x')
                    dist_y = self.hitbox.centery - tile.get_center('y')
                    tot_dist = ((dist_x ** 2) + (dist_y ** 2)) ** 0.5
                    scale_factor = self.speed / tot_dist
                    self.hitbox.x -= dist_x * scale_factor
                    self.hitbox.y -= dist_y * scale_factor

                    if dist_x > 0:
                        self.state = 'move_right'
                    else:
                        self.state = 'move_left'

                else:
                    if self.state == 'move_right':
                        self.state = 'attack_left'
                    elif self.state == 'move_left':
                        self.state = 'attack_right'

        if self.spritesheets[self.state].get_frame() == self.spritesheets[self.state].get_len() \
                and astar.manhattan(self.get_tile(), dest) < 75:
            system.PLAYER.hit(5)

    def get_health_bar(self):
        self.health_bar = pygame.Rect(self.hitbox.x, self.hitbox.y - 20, 50 * (self.current_health / self.max_health),
                                      10)
        self.under_bar = pygame.Rect(self.hitbox.x, self.hitbox.y - 20, 50, 10)
        return self.under_bar, self.health_bar


class Slime(Enemy):
    def __init__(self, x, y, difficulty):
        """
        Class for the Slime enemy
        :param x: Starting x coord
        :param y: Starting y coord
        :param difficulty: Starting difficulty
        """
        super().__init__(difficulty, 5, 50, 20, pygame.Rect(x, y, 50, 30))

        self.colour = random.choice(['Red', 'Green', 'Blue'])

        # Dict containing all the spritesheets for the Slime's animations
        self.spritesheets = {
            'move_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Enemies', 'Slime', self.colour, 'Move.png')), 128, 128, 7, 1, 1, 'r'),
            'move_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Enemies', 'Slime', self.colour, 'Move.png')), 128, 128, 7, 1, 1, 'l'),
            'attack_right': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Enemies', 'Slime', self.colour, 'Attack.png')), 128, 128, 4, 1, 3, 'r'),
            'attack_left': Spritesheet(pygame.image.load(os.path.join(
                'Sprites', 'Enemies', 'Slime', self.colour, 'Attack.png')), 128, 128, 4, 1, 3, 'l'),
        }

        # Stats
        self.damage = 10

        self.state = 'move_left'
        self.sprite = self.return_sprite()
        self.hitbox.center = [x, y]

    def get_coords(self) -> list:
        """
        :return: The coordinates that the sprite needs to be drawn to in order for the hitbox to be centered
        """
        if self.state == 'move_right':
            return [self.hitbox.x - 35, self.hitbox.y - 100]
        else:
            return [self.hitbox.x - 45, self.hitbox.y - 100]
