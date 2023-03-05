import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self):
        self.width = 100
        self.height = 50
        self.x = 540
        self.y = 540

        pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def update(self, display):
        pygame.draw.rect(display, (255, 0, 0), self.rect)
