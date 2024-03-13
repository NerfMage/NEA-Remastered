import pygame
import os
import rooms
import creatures
import gui

PLAYER = creatures.Player(70, 70)
WIN = pygame.display.set_mode([1680, 1050], pygame.FULLSCREEN)
STATE = 'menu'


class System:
    def __init__(self):
        """
        Class to run the game itself and manage all the objects
        """
        # Creates a surface that sprites can be drawn to
        self.clock = pygame.time.Clock()
        # Loads the background image sprite and scales it to fit screen resolution
        self.bg = pygame.transform.scale(pygame.image.load(
            os.path.join('Sprites', 'Environment', 'Floor.png')).convert_alpha(), [1680, 1050])

        self.current_room = rooms.Room(1)

    def new_run(self):
        self.current_room = rooms.Room(1)
        PLAYER.heal(999)

    def run(self):
        """
        Runs the game, using the current Room
        :return: None
        """
        global STATE
        while STATE != 'quit':
            if STATE == 'game_running':

                WIN.blit(self.bg, (0, 0))
                # self.current_room.draw_grid()

                PLAYER.move(pygame.key.get_pressed())

                rooms.draw_obstacles()
                # self.current_room.draw_enemy_hitboxes()
                self.current_room.draw_creatures()
                # self.current_room.draw_grid()
                # self.current_room.draw_player_hitbox()

                if self.current_room.check_win():
                    if PLAYER.get_tile() == self.current_room.get_door():
                        WIN.fill((0, 0, 0))
                        pygame.display.update()
                        pygame.time.delay(750)
                        self.current_room = self.current_room.next_room()

                if PLAYER.is_dead():
                    STATE = 'dead'

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # Quits the program
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Quits the program if escape key is pressed
                            STATE = 'game_paused'

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        PLAYER.basic_attack()

                pygame.time.Clock.tick(self.clock, 20)

            elif STATE == 'game_paused':

                gui.pause_menu()
                pygame.display.update()

            elif STATE == 'menu':

                gui.main_menu()
                pygame.display.update()

                if STATE == 'game_running':
                    self.new_run()

            elif STATE == 'dead':

                gui.death_menu()
                pygame.display.update()

        PLAYER.save_data()
