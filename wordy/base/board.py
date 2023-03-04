from typing import Tuple, Dict, Optional, Literal

Position = Tuple[int, int]
# Tile = str
Tile = Literal['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

ALPHABET = set(chr(code) for code in range(65, 65 + 26))


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

    def place_tiles(self, tiles: Dict[Position, Tile]) -> 'Board':
        new_dict = dict(self.__tile_dict)
        for position, tile in tiles.items():
            if position in new_dict:
                raise ValueError(f"Position: {position} is already in this dictionary! old dict: {self.__tile_dict} tiles: {tiles}")
            new_dict[position] = tile
        return Board(self.size, new_dict)

    def __str__(self):
        return "\n".join("".join(self.tile_at((row, col)) or " " for col in range(self.size)) for row in range(self.size))
