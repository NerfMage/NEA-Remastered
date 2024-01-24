import pygame
import os
from rooms import Room


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
            os.path.join('Sprites', 'Environment', 'Floor.png')), [1680, 1050])

        # SLIME TEST
        self.current_room = Room(1)
        self.current_room.generate()

    def run(self):
        while self.running:

            self.win.blit(self.bg, (0, 0))
            self.current_room.draw_enemies(self.win, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            self.current_room.draw_obstacles(self.win)
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

            self.clock.tick_busy_loop(20)
