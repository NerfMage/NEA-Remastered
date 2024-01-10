import pygame
import settings


class Spritesheet:
    def __init__(self, sheet, width, height, length, scale):
        """
        A class to animate spritesheets
        :param sheet: The image file of the sheet
        :param width: The width of each frame
        :param height: The height of each frame
        :param length: The number of frame on the sheet
        :param scale: The scale factor for the sprite to be enlarged by
        """
        self.sheet = sheet
        self.width = width
        self.height = height
        self.length = length
        self.scale = scale
        self.frame = 0

    def get_image(self):
        image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), (128 * self.frame, 0, self.width, self.height))
        image = pygame.transform.scale_by(image, self.scale)

        self.frame += 1
        if self.frame == self.length:
            self.frame = 0

        return image


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
