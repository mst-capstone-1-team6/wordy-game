import pygame


class Tile(pygame.sprite.Sprite):
    piece_size = (50, 50)
    l = ""
    off_x, off_y = 0, 0
    dragging = False
    grid_lock = True
    grid_spot = (0, 0)
    prev_spot = (0, 0)
    forming_word = False
    locked = False

    def __init__(self, pos_x, pos_y, letter):
        pygame.sprite.Sprite.__init__(self)

        self.l = letter
        self.image = pygame.transform.scale(pygame.image.load("assets/letter/Wood/letter_" + letter + ".png"), self.piece_size)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y
        self.rect.size = self.piece_size

        self.rect.x = (self.piece_size[0] * (int(self.rect.centerx / self.piece_size[0])))
        self.rect.y = (self.piece_size[1] * (int(self.rect.centery / self.piece_size[1])))
        self.grid_spot = ((self.rect.x / self.piece_size[0]), (self.rect.y / self.piece_size[1]))
        self.prev_spot = self.grid_spot

    def update(self, display):
        if self.grid_lock:
            self.rect.x = (self.piece_size[0] * (int(self.rect.centerx / self.piece_size[0])))
            self.rect.y = (self.piece_size[1] * (int(self.rect.centery / self.piece_size[1])))
            self.grid_spot = ((self.rect.x / self.piece_size[0]), (self.rect.y / self.piece_size[1]))
