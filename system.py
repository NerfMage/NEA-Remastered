import pygame
import os
from rooms import Room
import creatures

PLAYER = creatures.Player(70, 70)


class System:
    def __init__(self):
        """
        Class to run the game itself and manage all the objects
        """
        # Creates a surface that sprites can be drawn to
        self.win = pygame.display.set_mode([1680, 1050], pygame.FULLSCREEN)
        self.running = True
        self.clock = pygame.time.Clock()
        # Loads the background image sprite and scales it to fit screen resolution
        self.bg = pygame.transform.scale(pygame.image.load(
            os.path.join('Sprites', 'Environment', 'Floor.png')).convert_alpha(), [1680, 1050])

        self.current_room = Room(1)

    def run(self):
        """
        Runs the game, using the current Room
        :return: None
        """
        while self.running:

            self.win.blit(self.bg, (0, 0))
            # self.current_room.draw_grid()

            PLAYER.move(pygame.key.get_pressed())

            self.current_room.draw_obstacles()
            # self.current_room.draw_enemy_hitboxes()
            self.current_room.draw_creatures()
            # self.current_room.draw_grid()
            # self.current_room.draw_player_hitbox()
            if self.current_room.check_win():
                if PLAYER.get_tile() == self.current_room.get_door():
                    self.win.fill((0, 0, 0))
                    pygame.display.update()
                    pygame.time.delay(750)
                    self.current_room = self.current_room.next_room()
                pass

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quits the program
                    pygame.quit()
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Quits the program if escape key is pressed
                        pygame.quit()
                        self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    PLAYER.basic_attack()

            pygame.time.Clock.tick(self.clock, 20)
