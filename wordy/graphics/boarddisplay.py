import pygame


class BoardDisplay(pygame.sprite.Sprite):

    board_size = 15
    piece_size = 30

    def __init__(self, pos_x, pos_y, board_size, piece_size):
        pygame.sprite.Sprite.__init__(self)

        self.board_size = board_size
        self.piece_size = piece_size

        self.image = pygame.transform.scale(pygame.image.load("assets/letter/Marble/grid.png"), (self.piece_size*self.board_size, self.piece_size*self.board_size))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x, pos_y
        self.rect.size = (self.piece_size*self.board_size, self.piece_size*self.board_size)
