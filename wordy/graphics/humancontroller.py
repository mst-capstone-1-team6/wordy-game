from typing import Optional

import pygame.sprite

from wordy.base.game import Game, Player, Move, Controller, LetterBag, WordPlacement
from wordy.base.board import Board
from wordy.graphics.tile import Tile


class HumanController(Controller):
    word_placement: WordPlacement

    def __init__(self, name):
        super().__init__()

        self.finished_move = False
        self.hand_tiles = pygame.sprite.LayeredUpdates()
        self.name = name
        self.empty_spots = [0, 1, 2, 3, 4, 5, 6]

    def new_hand(self, letter_bag: LetterBag):
        i = 0
        s: Tile
        for s in self.hand_tiles.sprites():
            letter_bag.return_tile(s.l)
            self.empty_spots.append(i)
            self.hand_tiles.remove(s)
            i += 1
        self.draw_tiles(letter_bag)

    def end_turn(self, cur_board: Board):
        try:
            first_word = cur_board.num_tiles()==0
            middle_flag = False
            start_x, start_y = 14, 14
            end_x, end_y = 0, 0
            tile_places = {}
            s: Tile
            for s in self.hand_tiles.sprites():
                if s.forming_word:
                    if s.grid_spot[0] < start_x:
                        start_x = s.grid_spot[0]
                    if s.grid_spot[0] > end_x:
                        end_x = s.grid_spot[0]
                    if s.grid_spot[1] < start_y:
                        start_y = s.grid_spot[1]
                    if s.grid_spot[1] > end_y:
                        end_y = s.grid_spot[1]
                    if s.grid_spot in tile_places or cur_board.tile_at(s.grid_spot):
                        raise ValueError
                    if s.grid_spot == (7, 7):
                        middle_flag = True
                    tile_places[s.grid_spot] = s.l
            if start_y==14 and start_x==14 and end_y==0 and end_x==0:
                self.word_placement = None
                self.finished_move = True

            if not middle_flag and first_word:
                raise ValueError

            if start_y!=end_y and start_x!=end_x:
                raise ValueError

            print(cur_board.get_words(tile_places))

            self.word_placement = WordPlacement(tile_places, (start_x, start_y), (start_x, end_y), "hello")

            s: Tile
            for s in self.hand_tiles.sprites():
                if s.forming_word:
                    self.hand_tiles.remove(s)
                    self.empty_spots.append(s.prev_spot[1]-3)
            self.finished_move = True
        except ValueError or TypeError:
            self.return_tiles()

    def draw_tiles(self, letter_bag: LetterBag):
        for i in self.empty_spots:
            self.hand_tiles.add(Tile((17, 3 + i), letter_bag.get_tile(), False))
        self.empty_spots = []

    def return_tiles(self):
        s: Tile
        for s in self.hand_tiles.sprites():
            if s.forming_word:
                s.grid_spot = s.prev_spot
                s.forming_word = False

    def make_move(self, game: Game, player: Player) -> Optional[Move]:
        if self.finished_move:
            move = Move([], self.word_placement)
            self.finished_move = False
            return move
        else:
            pass
