import pygame
from pygame.locals import *
import sys

# reference: https://www.digitalocean.com/community/tutorials/how-to-install-pygame-and-create-a-template-for-developing-games-in-python-3


def main():

    pygame.init()

    display_width = 800
    display_height = 600

    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("Wordy Game")

    def event_handler():
        for event in pygame.event.get():
            if event.type == QUIT or (
                event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)
            ):
                pygame.quit()
                sys.exit(0)

    while True:
        event_handler()

        pygame.display.update()
