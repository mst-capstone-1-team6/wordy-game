from typing import Tuple, Dict, Optional, Literal, List, Generator
from dataclasses import dataclass

Position = Tuple[int, int]
# Tile = str
Tile = Literal['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

ALPHABET = set(chr(code) for code in range(65, 65 + 26))


def over_positions(start: Position, end: Position, inclusive: bool = True) -> Generator[Position, None, None]:
    current_position = start
    while True:
        at_goal = current_position == end
        if at_goal and not inclusive:
            return None
        yield current_position
        if at_goal:
            return None
        if current_position[0] == end[0]:
            row_change = 0
        elif current_position[0] < end[0]:
            row_change = 1
        else:
            row_change = -1
        if current_position[1] == end[1]:
            col_change = 0
        elif current_position[1] < end[1]:
            col_change = 1
        else:
            col_change = -1
        current_position = (current_position[0] + row_change, current_position[1] + col_change)


@dataclass
class WordPlacement:
    word_start: Position
    word_end: Position
    word: str


class Board:
    """
    A board is a square of tiles where (0, 0) is the upper left corner.
    Each instance of a board should be immutable.
    You should not be altering a board's state directly, but rather
    """

    def __init__(self, size: int, tile_dict: Dict[Position, Tile]):
        self.size = size
        self.__tile_dict = tile_dict

    def tile_at(self, position: Position) -> Optional[Tile]:
        """
        :param position: The position
        :return: The tile or None if not present at position
        """
        return self.__tile_dict.get(position)

    def num_tiles(self):
        return len(self.__tile_dict)

    def get_words(self, tiles: Dict[Position, Tile]) -> List[WordPlacement]:
        new_board = self.place_tiles(tiles)
        spelled_words = []

        last_x = -1
        last_y = -1
        for position, tile in tiles.items():

            # First if statement will handle finding words vertical to the current tile
            i = position[1]
            j = position[1]
            vert_word = tile

            if not (new_board.tile_at((position[0], position[1] + 1)) or new_board.tile_at((position[0], position[1] - 1))
                    or new_board.tile_at((position[0] + 1, position[1])) or new_board.tile_at((position[0] - 1, position[1]))):
                spelled_words.append(WordPlacement(position, position, vert_word))
            # The last_x/last_y will take into account that we aren't repeating the same word multiple times
            if last_x != position[0] and (new_board.tile_at((position[0], i + 1)) or new_board.tile_at((position[0], j - 1))):
                # While loop will move 1 tile up and down at a time until it can no longer
                while (new_board.tile_at((position[0], i + 1))) or (new_board.tile_at((position[0], j - 1))):
                    if new_board.tile_at((position[0], i + 1)):
                        # If there is a tile below, add it to the end of the word
                        vert_word = vert_word + new_board.tile_at((position[0], i + 1))
                        i += 1
                    if new_board.tile_at((position[0], j - 1)):
                        # If there is a tile above, add it to the start of the word
                        vert_word = new_board.tile_at((position[0], j - 1)) + vert_word
                        j -= 1
                # Add whatever word we got to the list of spelled words
                start = (position[0], j)
                end = (position[0], i)
                spelled_words.append(WordPlacement(start, end, vert_word))
                last_x = position[0]

            # Second if statement will handle finding words horizontal to the current tile
            i = position[0]
            j = position[0]
            hori_word = tile
            # This will work much the same to the vertical one, just flipped the x and y
            if last_y != position[1] and (new_board.tile_at((i + 1, position[1])) or new_board.tile_at((j - 1, position[1]))):
                while (new_board.tile_at((i + 1, position[1]))) or (new_board.tile_at((j - 1, position[1]))):
                    if new_board.tile_at((i + 1, position[1])):
                        hori_word = hori_word + new_board.tile_at((i + 1, position[1]))
                        i += 1
                    if new_board.tile_at((j - 1, position[1])):
                        hori_word = new_board.tile_at((j - 1, position[1])) + hori_word
                        j -= 1
                start = (j, position[1])
                end = (i, position[1])
                spelled_words.append(WordPlacement(start, end, hori_word))
                last_y = position[1]

        return spelled_words

    def place_tiles(self, tiles: Dict[Position, Tile]) -> 'Board':
        new_dict = dict(self.__tile_dict)
        for position, tile in tiles.items():
            if position in new_dict:
                raise ValueError(f"Position: {position} is already in this dictionary! old dict: {self.__tile_dict} tiles: {tiles}")
            new_dict[position] = tile
        return Board(self.size, new_dict)

    def __str__(self):
        return "\n".join("".join(self.tile_at((row, col)) or " " for col in range(self.size)) for row in range(self.size))
