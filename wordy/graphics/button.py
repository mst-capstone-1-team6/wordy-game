import pygame


class Button(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, text):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        pygame.sprite.Sprite.__init__(self)

        if text == "END TURN":
            self.image = pygame.transform.scale(pygame.image.load("assets/letter/NewWood/EndTurn.png"),
                                                (self.width, self.height))
        elif text == "NEW HAND":
            self.image = pygame.transform.scale(pygame.image.load("assets/letter/NewWood/NewHand.png"),
                                                (self.width, self.height))
        elif text == "Arrow":
            self.image = pygame.transform.scale(pygame.image.load("assets/letter/NewWood/Arrow.png"),
                                                (self.width, self.height))
        elif text == "Continue":
            self.image = pygame.transform.scale(pygame.image.load("assets/letter/NewWood/Continue.png"),
                                                (self.width, self.height))
        elif text == "Rematch":
            self.image = pygame.transform.scale(pygame.image.load("assets/letter/NewWood/Rematch.png"),
                                                (self.width, self.height))
        elif text == "Menu":
            self.image = pygame.transform.scale(pygame.image.load("assets/letter/NewWood/Menu.png"),
                                                (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

