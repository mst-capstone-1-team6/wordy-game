import pygame

from wordy.graphics.constants import DISPLAY_WIDTH, DISPLAY_HEIGHT
from wordy.graphics.titlescreen import TitleScreen


# reference: https://www.digitalocean.com/community/tutorials/how-to-install-pygame-and-create-a-template-for-developing-games-in-python-3


def main():

    pygame.init()

    game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pygame.display.set_caption("Wordy Game")

    game_screen = TitleScreen()

    try:
        while True:
            game_screen.update(game_display)
            game_screen = game_screen.next_screen()

            # TODO decide if we want to keep the call to update() here or if we should move it into Screen#update()
            pygame.display.update()
    finally:
        # A call to sys.exit would result in a SystemExit raised, but we will call pygame.quit() no matter what exception is raised
        pygame.quit()

