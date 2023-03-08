from typing import Optional, List, Tuple

from wordy.base.board import Board, Position
from wordy.base.game import Game, Player, Move, Controller


class AIController(Controller):
    def __init__(self):
        super().__init__()

    def make_move(self, game: Game, player: Player) -> Optional[Move]:
        possible_moves = valid_moves(game.board)
        tile_range = possible_moves[0]
        pass


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
                        if new_end_pos[0] >= 15 or new_end_pos[1] >= 15 or new_end_pos[0] < 0 or new_end_pos[1] < 0:
                            break
                        if does_extend_word(board, new_end_pos):
                            break
                        end_pos = new_end_pos
                    while True:
                        new_start_pos = (start_pos[0] + direction[0] * -1, start_pos[1] + direction[1] * -1)
                        if new_start_pos[0] >= 15 or new_start_pos[1] >= 15 or new_start_pos[0] < 0 or new_start_pos[1] < 0:
                            break
                        if does_extend_word(board, new_start_pos):
                            break
                        start_pos = new_start_pos
                    mylist.append((start_pos, end_pos))
    return mylist


# cant change any current word, has to intersect a current word
# Note: if we decide that each Controller should have a name,
#   then creating a single instance for an AI Controller may not make sense if we want to have "AI 1" and "AI 2" for multiple AIs
AI_CONTROLLER = AIController()
"""The instance of an AI Controller."""
