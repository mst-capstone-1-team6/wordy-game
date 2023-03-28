import pygame

from typing import Tuple


class Tile(pygame.sprite.Sprite):
    piece_size = (50, 50)
    l = ""
    off_x, off_y = 0, 0
    dragging = False
    grid_lock = True
    grid_spot: Tuple[int, int] = (0, 0)
    prev_spot: Tuple[int, int] = (0, 0)
    forming_word = False
    board_tile = False

    def __init__(self, grid_pos: Tuple[int, int], letter, board):
        pygame.sprite.Sprite.__init__(self)

        self.board_tile = board
        self.l = letter

        self.image = pygame.transform.scale(pygame.image.load("assets/letter/Wood/letter_" + letter + ".png"), self.piece_size)

        self.rect = self.image.get_rect()
        self.grid_spot = grid_pos
        self.rect.size = self.piece_size

        self.rect.x = (self.piece_size[0] * grid_pos[0])
        self.rect.y = (self.piece_size[1] * grid_pos[1])

        self.prev_spot = self.grid_spot

    def update(self, display):
        if self.grid_lock:
            self.rect.x = (self.piece_size[0] * (self.grid_spot[0]))
            self.rect.y = (self.piece_size[1] * (self.grid_spot[1]))
        if self.forming_word:
            pygame.draw.lines(display, (255, 0, 0), True, (self.rect.topleft, self.rect.bottomleft, self.rect.bottomright, self.rect.topright), 3)

