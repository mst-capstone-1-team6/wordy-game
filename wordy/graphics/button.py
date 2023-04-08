import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, text):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        pygame.sprite.Sprite.__init__(self)

        if text == "END TURN":
            self.image = pygame.transform.scale(pygame.image.load("assets/letter/Wood/EndTurn.png"),
                                            (self.width, self.height))
        elif text == "NEW HAND":
            self.image = pygame.transform.scale(pygame.image.load("assets/letter/Wood/NewHand.png"),
                                                (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

