from typing import Optional

import pygame.sprite

from wordy.base.game import Game, Player, Move, Controller, LetterBag
from wordy.base.board import Board
from wordy.graphics.tile import Tile


class HumanController(Controller):

    def __init__(self, name, word_dict):
        super().__init__()

        self.finished_move = False
        self.hand_tiles = pygame.sprite.LayeredUpdates()
        self.name = name
        self.word_dict = word_dict
        self.empty_spots = [0, 1, 2, 3, 4, 5, 6]
        self.move = None

    def new_hand(self, letter_bag: LetterBag):
        i = 0
        s: Tile
        for s in self.hand_tiles.sprites():
            letter_bag.return_tile(s.l)
            self.empty_spots.append(i)
            self.hand_tiles.remove(s)
            i += 1
        self.draw_tiles(letter_bag)

    def end_turn(self, cur_board: Board, letter_bag: LetterBag):
        try:
            first_word = cur_board.num_tiles() == 0
            middle_flag = False
            start_x, start_y = 14, 14
            end_x, end_y = 0, 0
            tile_places = {}
            s: Tile
            for s in self.hand_tiles.sprites():
                if s.forming_word:
                    if s.grid_spot[0] < start_x:
                        start_x = int(s.grid_spot[0])
                    if s.grid_spot[0] > end_x:
                        end_x = int(s.grid_spot[0])
                    if s.grid_spot[1] < start_y:
                        start_y = int(s.grid_spot[1])
                    if s.grid_spot[1] > end_y:
                        end_y = int(s.grid_spot[1])
                    if s.grid_spot in tile_places or cur_board.tile_at(s.grid_spot):
                        raise ValueError()
                    if s.grid_spot == (7, 7):
                        middle_flag = True
                    tile_places[s.grid_spot] = s.l
            if start_y == 14 and start_x == 14 and end_y == 0 and end_x == 0:
                hand_letters = []
                for tile in self.hand_tiles:
                    hand_letters.append(tile.l)
                self.move = Move(hand_letters, [], {})
                self.finished_move = True
                return

            if not middle_flag and first_word:
                raise ValueError()

            if start_y != end_y and start_x != end_x:
                raise ValueError()

            new_board = cur_board.place_tiles(tile_places)
            intersect_flag = False
            for pos, tile in tile_places.items():
                # If a tile being placed is next to an existing tile, it intersects
                if cur_board.tile_at((pos[0] + 1, pos[1])) or cur_board.tile_at((pos[0] - 1, pos[1])) or cur_board.tile_at((pos[0], pos[1] + 1)) or cur_board.tile_at((pos[0], pos[1] - 1)):
                    intersect_flag = True
                    break

            # If there are tiles from the start of the placed tiles to the end, then it is continuous
            if start_y == end_y:
                # Horizontal words
                for x in range(start_x, end_x):
                    if not new_board.tile_at((x, start_y)):
                        raise ValueError()
            elif start_x == end_x:
                # Vertical words
                for y in range(start_y, end_y):
                    if not new_board.tile_at((start_x, y)):
                        raise ValueError()

            if not first_word and not intersect_flag:
                raise ValueError()
            
            for word in cur_board.get_words(tile_places):
                if not self.word_dict.test_word(word.word):
                    raise ValueError()

            s: Tile
            for s in self.hand_tiles.sprites():
                if s.forming_word:
                    self.hand_tiles.remove(s)
                    self.empty_spots.append(s.prev_spot[1] - 3)
            self.draw_tiles(letter_bag)
            hand_letters = []
            for tile in self.hand_tiles:
                hand_letters.append(tile.l)
            self.move = Move(hand_letters, cur_board.get_words(tile_places), tile_places)
            print(self.move)
            self.finished_move = True

        except ValueError:
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
            self.finished_move = False
            return self.move
        else:
            pass
