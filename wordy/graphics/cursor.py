import pygame


class Cursor(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.rect.Rect(1, 1, 1, 1)
