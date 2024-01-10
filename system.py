import pygame
import settings


class System:
    def __init__(self):
        """
        Class to run teh game itself and manage all the objects
        """
        self.win = pygame.display.set_mode(settings.INITIAL_SIZE, pygame.FULLSCREEN)
        # Creates a surface that sprites can be drawn to
        self.running = True
        # Loads the background image sprite and scales it to fit screen resolution
        self.bg = pygame.transform.scale(pygame.image.load(
            settings.ENVIRONMENT_SPRITES['Floor']), settings.INITIAL_SIZE)

    def run(self):
        while self.running:

            self.win.blit(self.bg, (0, 0))
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
