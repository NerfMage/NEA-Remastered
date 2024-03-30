import pygame
import os
import rooms
import creatures
import gui

PLAYER = creatures.Player(70, 70)  # Creates an instance of the Player class for the user to control
WIN = pygame.display.set_mode([1680, 1050], pygame.FULLSCREEN)  # Creats a window for the program to display to
STATE = 'menu'  # Variable that controls what GUI should be displayed


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

        self.current_room = rooms.Room(1)  # The Room the Plyer is currently on

    def new_run(self):
        """
        Starts a new run for the Player
        Heals the Player to full health and resets the current_room to a Room of difficulty 1
        """
        self.current_room = rooms.Room(1)
        PLAYER.heal(999)

    def run(self):
        """
        Runs the game, using the current_room
        Draws to screen based on STATE global
        Commented code is debuggin functions
        Contains the main game loop, operating at a set FPS
        """
        global STATE
        while STATE != 'quit':
            if STATE == 'game_running':

                WIN.blit(self.bg, (0, 0))
                # self.current_room.draw_grid()

                PLAYER.move(pygame.key.get_pressed())  # Takes user input for movement and abilites

                rooms.draw_obstacles()  # Draws all obstacles in the Room to screen
                # self.current_room.draw_enemy_hitboxes()
                self.current_room.draw_creatures()
                # self.current_room.draw_grid()
                # self.current_room.draw_player_hitbox()

                if self.current_room.check_win():
                    if PLAYER.get_tile() == self.current_room.get_door():
                        # Moves on to next level if the Door is open
                        WIN.fill((0, 0, 0))
                        pygame.display.update()
                        pygame.time.delay(750)  # Small time delay before drawing new Room to prevent disorientation
                        self.current_room = self.current_room.next_room()

                if PLAYER.is_dead():  # Changes to death screen if the Player dies
                    STATE = 'dead'

                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        # Quits the program
                        pygame.quit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            # Pauses the program if escape key is pressed
                            STATE = 'game_paused'

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        PLAYER.basic_attack()

                pygame.time.Clock.tick(self.clock, 20)  # Caps FPS at a set amount

            # GUIS #
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

        # Saves all Player data when the game ends
        PLAYER.save_data()
