from typing import Optional, List, Tuple

import pygame.sprite

from wordy.base.board import Board, Position, Tile
from wordy.base.game import Game, Player, Move, Controller, LetterBag
from wordy.base.worddict import WordInfo



class AIController(Controller):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def draw_tiles(self, num_tiles: int, letter_bag: LetterBag):
        tiles = []
        for i in range(num_tiles):
            tiles.append(letter_bag.get_tile())
        return tiles

    def make_move(self, game: Game, player: Player) -> Optional[Move]:
        num_tiles = 7 - len(player.hand)
        hand_letters = self.draw_tiles(num_tiles, game.letter_bag) + player.hand
        possible_moves = valid_moves(game.board)
        move_choices = []
        best_move_choices = []
        print(hand_letters)
        tile_placements = {}
        temp_indexes = []
        temp_pos = []
        best_score = 0
        which_move = 0
        move_index = 0
        for curr_move in possible_moves:
            temp_letters = []
            letter_pos = []
            direction = "vertical"
            length = curr_move[1][0] - curr_move[0][0]
            if length == 0:
                direction = "horizontal"
                length = curr_move[1][1] - curr_move[0][1]
            #temp_dict = game.word_dict.trim_by_length(0, length)
            #temp_dict = temp_dict.trim_by_letters(hand_letters)
            #print(temp_dict.words)
            temp_pos = list(curr_move[0])
            for i in range(length):
                if game.board.tile_at(tuple(temp_pos)) is not None:
                    temp_letters.append(game.board.tile_at(tuple(temp_pos)))
                    letter_pos.append(tuple(temp_pos))
                if direction == "horizontal":
                    temp_pos[1] = temp_pos[1] + 1
                else:
                    temp_pos[0] = temp_pos[0] + 1
            temp_dict = game.word_dict.trim_by_length(0, length)
            print(temp_dict.words, "temP_dict.words")
            #temp_dict = temp_dict.trim_by_letters(hand_letters+temp_letters)
            temp_pos = list(curr_move[0])
            temp_hand_letters = [str(tile) for tile in hand_letters]
            print(temp_hand_letters+temp_letters, "letter set")
            temp_dict = temp_dict.trim_by_hand(temp_hand_letters+temp_letters)
            print(temp_dict.words, "temp_dict.words")
            temp_dict2 = []
            if len(letter_pos) == 1:
                print('one letter')
                """add in here somewhere in these if statements, ryans new function for trim by hand before the next dict"""
                if direction == "horizontal":
                    temp_dict2 = temp_dict.find_one_letter(temp_letters[0], letter_pos[0][1])
                else:
                    temp_dict2 = temp_dict.find_one_letter(temp_letters[0], letter_pos[0][0])
            if len(letter_pos) > 1:
                print('two letter')
                if direction == "horizontal":
                    temp_dict2 = temp_dict.find_many_letters(temp_letters, [letter[1]-curr_move[0][1] for letter in letter_pos])
                else:
                    temp_dict2 = temp_dict.find_many_letters(temp_letters, [letter[0]-curr_move[0][0] for letter in letter_pos])
            valid_words = []
            #temp_hand_letters = [str(tile) for tile in hand_letters]
            print(temp_hand_letters)
            #print(temp_dict2)
            """this code will need to change syntax to match the new data type ryan is making"""
            #print(temp_dict2)
            for word in temp_dict2:
                valid_words.append(word)
            print(valid_words)
            if len(valid_words) > 0:
                for word in valid_words:
                    temp_hand_tiles = hand_letters
                    temp_tile_placements = tile_placements
                    curr_offset = word.start_offsets.pop()
                    while True and word.start_offsets:
                        if curr_offset < 0:
                            curr_offset = word.start_offsets.pop()
                        else:
                            break
                    for i, letter in enumerate(word.word_str):
                        #temp_index = temp_hand_letters.index(word.word_str[i])
                        #print(temp_hand_tiles[temp_index])
                        if direction == "horizontal":
                            key = (curr_move[0][0], curr_offset+i)
                        else:
                            key = (curr_offset+i, curr_move[0][1])
                        if game.board.tile_at(key) is None and letter in temp_hand_letters:
                            temp_index = temp_hand_letters.index(letter)
                            value = temp_hand_tiles[temp_index]
                            pair = (key, value)
                            temp_tile_placements.update([pair])
                    """this is nonsense doing nothing never being changed"""
                    for i in range(len(letter_pos)):
                        if tuple(letter_pos[i]) in temp_tile_placements.keys():
                            temp_tile_placements.pop(tuple(letter_pos[i]))
                        #hand_letters.remove(word(i)
                    move_choices.append(Move(temp_hand_tiles, game.board.get_words(temp_tile_placements), temp_tile_placements))
                best_score = 0
                which_move = 0
                move_index = 0
                for move in move_choices:
                    which_move = which_move+1
                    if move.score(game.board, game.computer_science_terms) > best_score:
                        best_score = move.score(game.board, game.computer_science_terms)
                        move_index = which_move - 1
                best_move_choices.append(move_choices[move_index])
        #print(best_move_choices)
        which_move = 0
        move_index = 0
        for move in best_move_choices:
            which_move = which_move+1
            if move.score(game.board, game.computer_science_terms) > best_score:
                best_score = move.score(game.board, game.computer_science_terms)
                move_index = which_move - 1
        print(move_index, "move index")
        if len(best_move_choices) > 0:
            print(len(best_move_choices), "length of best moves")
            best_move = best_move_choices[move_index]
            return best_move
        else:
            return Move(hand_letters, [], {})


def does_extend_word(board: Board, position: Position) -> bool:
    """
    assume position is an empty tile
    supposed to check whether a singular tile is invalid due to the position of other words
    return true for every spot except one next to a word in the direction its written
    """
    for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        new_tile = (position[0] + direction[0], position[1] + direction[1])
        new_tile2 = (position[0] + direction[0] * 2, position[1] + direction[1] * 2)
        if board.tile_at(new_tile) is not None:
            if board.tile_at(new_tile2) is not None:
                return True
    return False


def is_corner(board: Board, position: Position) -> bool:
    """
    assume position is an empty tile: checks for corners including if it goes parallel to a word further away
    """
    tiles = 0
    temp_position = (position[0], position[1])
    for direction in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        if board.tile_at((temp_position[0] + direction[0], temp_position[1] + direction[1])) is not None:
            tiles = tiles + 1
        if tiles >= 2:
            return True
        temp2 = temp_position
        new_direction = (direction[1], direction[0])
        while 15 > temp2[0] >= 0 and 15 > temp2[1] >= 0:
            temp2 = (temp2[0] + new_direction[0], temp2[1] + new_direction[1])
            if board.tile_at(temp2) is not None:
                return True
    return False


def valid_moves(board: Board) -> List[Tuple[Position, Position]]:
    """
    takes the board state and returns the start and end positions
    in a list of valid ranges for moves
    """
    mylist = []
    for row in range(15):
        for col in range(15):
            tile = board.tile_at((row, col))
            if tile is not None:
                for direction in [(1, 0), (0, 1)]:
                    start_pos = (row, col)
                    end_pos = (row, col)
                    while True:
                        new_end_pos = (end_pos[0] + direction[0], end_pos[1] + direction[1])
                        if new_end_pos[0] >= 14 or new_end_pos[1] >= 14 or new_end_pos[0] < 0 or new_end_pos[1] < 0:
                            break
                        if does_extend_word(board, new_end_pos):
                            break
                        end_pos = new_end_pos
                    while True:
                        new_start_pos = (start_pos[0] + direction[0] * -1, start_pos[1] + direction[1] * -1)
                        if new_start_pos[0] >= 14 or new_start_pos[1] >= 14 or new_start_pos[0] < 0 or new_start_pos[1] < 0:
                            break
                        if does_extend_word(board, new_start_pos):
                            break
                        start_pos = new_start_pos
                    mylist.append((start_pos, end_pos))
    return mylist


# has to intersect a current word
# Note: if we decide that each Controller should have a name,
#   then creating a single instance for an AI Controller may not make sense if we want to have "AI 1" and "AI 2" for multiple AIs
#AI_CONTROLLER = AIController()
"""The instance of an AI Controller."""
