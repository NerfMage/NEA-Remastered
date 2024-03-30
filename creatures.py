import pygame
import os
import random
import rooms
import astar
import system
import items


def Factory(enemy, *args) -> object:
    """
    A function to return the appropriate subcalss based on an input
    :param enemy: The subclass name
    :param args: The subcalss arguments
    :return: The subclass object
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
        Function that updates the spritesheet by moving on to the next frame
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
        # 'cuts out' the relevant frame from the Spritesheet
        image.blit(self.sheet, (0, 0), (self.width * (self.frame // self.speed), 0, self.width, self.height))
        image = pygame.transform.scale_by(image, self.scale)
        if self.direction == 'l':
            image = pygame.transform.flip(image, True, False)  # Flips the image horizontally

        return image.convert_alpha()

    def get_frame(self) -> int:
        """
        :return: The current frame count
        """
        return self.frame

    def get_len(self) -> int:
        """
        :return: The length of the animation, in frames
        """
        return self.frame * self.speed


class Creature:
    def __init__(self, hitbox, speed, health):
        """
        A superclass for all the enemies and the Player
        :param hitbox: A Pygame.Rect for the objects' hitbox
        :param speed: An integer value for the number of pixels moved per frame
        :param health: An integer representing how much damage the creature can take before dying
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
        """
        :return: The pygame rectangle that governsthe Creature's collisions
        """
        return self.hitbox

    def return_sprite(self) -> pygame.Surface:
        """
        :return: Image from the Spritesheet after updating
        """
        self.spritesheets[self.state].update()
        return self.spritesheets[self.state].get_image()

    def hit(self, damage: int):
        """
        Method that causes the creature to take damage and reduce its current health
        :param damage: The integer value representing the damge received
        """
        self.current_health -= damage

    def is_dead(self) -> bool:
        """
        :return: If the Creature is alive or dead, based on their current hit points
        """
        if self.current_health <= 0:
            return True
        else:
            return False

    def heal(self, value: int):
        """
        Increases the Creature's current hit points by given value
        :param value: Hit points to be recovered
        """
        self.current_health += value
        # Prevents current health exceeding max health
        if self.current_health > self.max_health:
            self.current_health = self.max_health


class Player(Creature):
    def __init__(self, x, y):
        """
        Class for the user's plyable character
        :param x: starting x-coord
        :param y: starting y-coord
        """
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
        # A pygame rectangle representing the portion of health the player has left
        self.health_bar = pygame.Rect(10, 980, 400, 60)
        # Dict containing the cooldowns for all player abilities as a 2d array [current count, reset count]
        self.cooldowns = {
            'secondary': [30, 30],
            'dash': [15, 15],
        }
        # Player data imported from text file
        self.data = open('data', 'r+')
        self.gold = int(''.join(filter(str.isdigit, self.data.readlines()[0])))

    def get_coords(self) -> list:
        """
        :return: The coordinates that the sprite needs to be drawn to in order for the hitbox to be centered
        """
        if self.state in ['run_right', 'idle_right', 'attack_right', 'secondary_right', 'dash_right']:
            return [self.hitbox.x - 40, self.hitbox.y - 110]
        elif self.state in ['run_left', 'idle_left', 'attack_left', 'secondary_left', 'dash_left']:
            return [self.hitbox.x - 110, self.hitbox.y - 110]

    def get_gold(self) -> int:
        """
        :return: The amount of gold the Player has
        """
        return self.gold

    def move(self, key):
        """
        Method that takes a key input from the user and maps it to a game action
        Updates the Player's sprite based on the state attribute
        Controls cooldowns
        :param key: The dictionary containing all button inputs from that frame, given by pygame
        """
        if self.state in ['idle_left', 'idle_right', 'run_left', 'run_right']:
            # Basic movement inputs
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

            # Secondary Attck input
            if key[pygame.K_e] and self.cooldowns['secondary'][0] >= self.cooldowns['secondary'][1]:
                if self.state in ['idle_right', 'run_right']:
                    self.state = 'secondary_right'
                if self.state in ['idle_left', 'run_left']:
                    self.state = 'secondary_left'
                self.cooldowns['secondary'][0] = 0

            # Dash input
            if key[pygame.K_SPACE] and self.cooldowns['dash'][0] >= self.cooldowns['dash'][1]:
                if key[pygame.K_a]:
                    self.state = 'dash_left'
                    self.cooldowns['dash'][0] = 0
                elif key[pygame.K_d]:
                    self.state = 'dash_right'
                    self.cooldowns['dash'][0] = 0

            # Idle if there was no movement input
            if not any([key[pygame.K_w], key[pygame.K_a], key[pygame.K_s], key[pygame.K_d]]):
                if self.state == 'run_right':
                    self.state = 'idle_right'
                elif self.state == 'run_left':
                    self.state = 'idle_left'

        # Updating animations for attacks #
        if self.state in ['attack_left', 'attack_right'] and \
                self.spritesheets[self.state].get_frame() == self.spritesheets[self.state].get_len():
            # Changes state if animation has ended
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

        # Activates Traps if stepped on
        if isinstance(self.get_tile(), rooms.Trap):
            self.get_tile().activate()

        # Takes all the dropped items on the current Tile
        self.get_tile().take_loot()

        # Updates cooldown counter
        for value in self.cooldowns.values():
            value[0] += 1

    def basic_attack(self):
        """
        Damages all Enemies on the current Tile and the horizontally adjacent Tile in the direction
        that the Player is facing
        """
        enemies = []  # Temporary list toensure no Enemies are damaged twice if they are on 2 Tiles

        for enemy in self.get_tile().get_enemies():
            enemies.append(enemy)

        # Try Except is easier than checking if adjacent Tile exists
        if self.state in ['run_right', 'idle_right']:
            self.state = 'attack_right'
            try:
                for enemy in rooms.get_right(self.get_tile()).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)
            except AttributeError:
                pass
        elif self.state in ['run_left', 'idle_left']:
            self.state = 'attack_left'
            try:
                for enemy in rooms.get_left(self.get_tile()).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)
            except AttributeError:
                pass

        # Damages all enemies
        for enemy in enemies:
            enemy.hit(25)

    def secondary_attack(self):
        """
        Damages all enemies in a semicircle in the direction that the Player is facing
        Works similarly to primary_attack()
        """
        enemies = []  # Temp list to prevent Enemies being damaged twice
        if self.state == 'secondary_right':
            try:
                # Adding each Enemy that occupies a Tile in the semicircle to the temp
                for enemy in self.get_tile().get_enemies():
                    enemies.append(enemy)

                for enemy in rooms.get_right(self.get_tile()).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

                for enemy in rooms.get_down(self.get_tile()).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

                for enemy in rooms.get_up(self.get_tile()).get_enemies():
                    if enemy not in enemies:
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
                    if enemy not in enemies:
                        enemies.append(enemy)

                for enemy in rooms.get_down(self.get_tile()).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

                for enemy in rooms.get_up(self.get_tile()).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

                for enemy in rooms.get_up(rooms.get_left(self.get_tile())).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

                for enemy in rooms.get_down(rooms.get_left(self.get_tile())).get_enemies():
                    if enemy not in enemies:
                        enemies.append(enemy)

            except AttributeError:
                pass

        # Damages the enemies
        for enemy in enemies:
            enemy.hit(50)

    def dash(self):
        """
        Moves the Player a set distance, horizontally and then damages each Enemy at the new occupied Tile
        """
        if self.state == 'dash_left':
            if rooms.get_left(self.get_tile()) is not None and \
                    not rooms.get_left(self.get_tile()).return_occupied():
                self.hitbox.x -= 3 * self.speed  # Horizontal movement scales with Player speed

        if self.state == 'dash_right':
            if rooms.get_right(self.get_tile()) is not None and \
                    not rooms.get_right(self.get_tile()).return_occupied():
                self.hitbox.x += 3 * self.speed

        # Damagin Enemies on the occupied Tile
        for enemy in self.get_tile().get_enemies():
            enemy.hit(5)

    def get_healthbar(self) -> pygame.Rect:
        """
        :return: The part of the health bar that represents remaining health
        """
        self.health_bar = pygame.Rect(10, 980, 400 * (self.current_health / self.max_health), 60)
        return self.health_bar

    def get_cooldowns(self) -> dict:
        """
        :return: The dictionary containing all the information on the Player ability cooldownns
        """
        return self.cooldowns

    def add_gold(self, value: int):
        """
        Gives the Player gold
        :param value: The amount of gold to be added
        """
        self.gold += value

    def get_tile(self):
        """
        :return: the tile that the Creature is currently occupying
        """
        for column in rooms.TILES:
            for tile in column:
                if tile.get_hitbox().collidepoint(self.hitbox.center):
                    return tile

    def save_data(self):
        """
        Saves the Player's data back to the text file
        Must be written in exact smae order os taht it is readable
        """
        self.data.seek(0)
        self.data.write('GOLD = {}'.format(self.gold))
        self.data.close()  # Closing the file saves the data


class Enemy(Creature):
    def __init__(self, difficulty, speed, health, damage, hitbox, droppable):
        """
        Class for all the enemies in the game
        Inherits from Creature class
        :param difficulty: Scalar to increase class difficulty as the game continues
        :param speed: Number of pixels moved per frame
        :param health: Hit points that the Enemy can receive before dying
        :param hitbox: Pygame Rect that governs all collisions
        :param droppable: All the items the enemy can drop upon death
        """
        super().__init__(hitbox, speed, int(health * difficulty))  # Health scales with difficulty
        self.difficulty = difficulty
        self.damage = int(damage * difficulty)  # Damage scales with difficulty
        self.droppable = droppable
        self.health_bar = pygame.Rect(self.hitbox.x, self.hitbox.y - 20, 50, 10)
        self.under_bar = pygame.Rect(self.hitbox.x, self.hitbox.y - 20, 50, 10)

    def move(self, dest):
        """
        Method to move the Enemy after each frame, uses astar algorithm
        :param dest: The target Tile
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

        # Makes it so that the dmage dealt to the Player lines up with the animation
        if self.spritesheets[self.state].get_frame() == self.spritesheets[self.state].get_len() \
                and astar.manhattan(self.get_tile(), system.PLAYER.get_tile()) < 75:
            system.PLAYER.hit(5)

    def get_health_bar(self) -> tuple:
        """
        Gives the two rectangles that display the Enemy's health barto the user'
        :return: The 2 rectangles; under_bar, health_bar
        """
        self.health_bar = pygame.Rect(self.hitbox.x, self.hitbox.y - 20, 50 * (self.current_health / self.max_health),
                                      10)
        self.under_bar = pygame.Rect(self.hitbox.x, self.hitbox.y - 20, 50, 10)
        return self.under_bar, self.health_bar

    def hit(self, damage: int):
        """
        Slightly different to the Player's hit method
        Causes the Enemy to take damage and drop gold if they die
        :param damage: The amount of damage to be taken
        """
        self.current_health -= damage
        if self.is_dead():
            drop = random.choice(list(self.droppable.keys()))  # Picks a random item from droppables
            if drop == 'gold':
                value = int(self.droppable[drop] * self.difficulty)
                self.get_tile().add_loot(items.Gold(value, self.hitbox.x, self.hitbox.y))


class Slime(Enemy):
    def __init__(self, x, y, difficulty):
        """
        Class for the Slime enemy
        :param x: Starting x coord
        :param y: Starting y coord
        :param difficulty: Starting difficulty
        """
        super().__init__(difficulty, 5, 50, 20, pygame.Rect(x, y, 50, 30),
                         {'gold': 5})

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
