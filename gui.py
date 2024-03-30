import pygame
import system

pygame.init()
pygame.font.init()

FONT = pygame.font.Font('ArcadeFont.ttf', 40)


def pause_menu():
    """
    Function to display the pause menu on screen
    Changes game state based on button presses
    Contains buttons to resume and quit to main menu
    """
    mouse_pos = pygame.mouse.get_pos()  # Gets the mouse coordinates each frame
    menu_text = FONT.render('Game Paused', True, (255, 255, 255))  # Text at the top of the screen

    resume_text = FONT.render('Resume', True, (14, 229, 236))
    resume_button = resume_text.get_rect(x=750, y=500)  # Creates a rectangle around the text to act as a button

    quit_text = FONT.render('Quit To Main Menu', True, (14, 229, 236))
    quit_button = quit_text.get_rect(x=550, y=700)

    # Draws elements to screen
    system.WIN.fill((0, 0, 0))
    system.WIN.blit(menu_text, (650, 200))
    system.WIN.blit(resume_text, (750, 500))
    system.WIN.blit(quit_text, (550, 700))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # Allows usee of escape button to unpause as well as mouse clicks
            if event.key == pygame.K_ESCAPE:
                system.STATE = 'game_running'

        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.collidepoint(mouse_pos):
                system.STATE = 'menu'

            elif resume_button.collidepoint(mouse_pos):
                system.STATE = 'game_running'


def main_menu():
    """
    Function to display the main menu to screen
    Changes game state based on button presses
    Contains play and quit game buttons
    """
    mouse_pos = pygame.mouse.get_pos()
    menu_text = FONT.render('Main Menu', True, (255, 255, 255))

    play_text = FONT.render('Play', True, (14, 229, 236))
    play_button = play_text.get_rect(x=775, y=500)

    quit_text = FONT.render('Quit Game', True, (14, 229, 236))
    quit_button = quit_text.get_rect(x=675, y=700)

    system.WIN.fill((0, 0, 0))
    system.WIN.blit(menu_text, (675, 200))
    system.WIN.blit(play_text, (775, 500))
    system.WIN.blit(quit_text, (675, 700))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.collidepoint(mouse_pos):
                system.STATE = 'quit'

            elif play_button.collidepoint(mouse_pos):
                system.STATE = 'game_running'


def death_menu():
    """
    Function to display the death screen when the Player dies
    Changes game state based on button presses
    Contains return to menu and quit game buttons
    """
    mouse_pos = pygame.mouse.get_pos()
    menu_text = FONT.render('You Died', True, (255, 0, 0))

    back_text = FONT.render('Back to Main Menu', True, (14, 229, 236))
    back_button = back_text.get_rect(x=525, y=500)

    quit_text = FONT.render('Quit Game', True, (14, 229, 236))
    quit_button = quit_text.get_rect(x=675, y=700)

    system.WIN.fill((0, 0, 0))
    system.WIN.blit(menu_text, (675, 200))
    system.WIN.blit(back_text, (525, 500))
    system.WIN.blit(quit_text, (675, 700))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if quit_button.collidepoint(mouse_pos):
                system.STATE = 'quit'

            elif back_button.collidepoint(mouse_pos):
                system.STATE = 'menu'
