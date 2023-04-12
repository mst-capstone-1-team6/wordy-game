import abc
import random
from dataclasses import dataclass
from typing import List, Tuple, Dict, Set
from typing import Optional

from wordy.base.board import Board, Position, Tile, WordPlacement, over_positions
from wordy.base.worddict import WordDict

LETTER_SCORING: Dict[int, Set[Tile]] = {
    1: set("EAIONRTLSU"),
    2: set("DG"),
    3: set("BCMP"),
    4: set("FHVWY"),
    5: set("K"),
    8: set("JX"),
    10: set("QZ"),
}


class Player:
    def __init__(self):
        self.score: int = 0
        self.hand: List[Tile] = []
        self.passed_last_turn = False




@dataclass
class Move:
    """
    Represents a move that a player can make.
    Note that you must validate that this is a valid move before creating this.
    Once a Move instance is created, it is expected that none of its values will be mutated.

    A move is designed to describe how a game's state should be altered.
    """

    new_hand: List[Tile]
    """The new hand of the player."""
    word_placement: List[WordPlacement]
    tile_placements: Dict[Position, Tile]

    def score(self, board: Board, computer_science_terms: Set[str]) -> int:
        intersection_count = 0
        score = 0
        is_horizontal_placement = True
        if len(self.tile_placements) >= 2:
            placements = list(self.tile_placements.keys())
            is_horizontal_placement = placements[0][0] == placements[1][0]

        ordered_tile_placement_positions = sorted(self.tile_placements.keys())
        for i, position in enumerate(ordered_tile_placement_positions):
            next_position = ordered_tile_placement_positions[i + 1] if i + 1 < len(ordered_tile_placement_positions) else None
            any_between = len(list(over_positions(position, next_position))) > 2 if next_position is not None else False
            if any_between:
                intersection_count += 1
                # print(f"({i}) between")

            horizontal_behind = board.tile_at((position[0], position[1] - 1)) is not None
            horizontal_front = board.tile_at((position[0], position[1] + 1)) is not None
            vertical_behind = board.tile_at((position[0] - 1, position[1])) is not None
            vertical_front = board.tile_at((position[0] + 1, position[1])) is not None

            if i == 0 and next_position is None:  # special case for a single tile being placed
                intersection_count += min(2, [horizontal_front, horizontal_behind, vertical_front, vertical_behind].count(True))
            else:
                if i == 0:
                    # for the first position, check to see if there's tiles "behind" us
                    if (is_horizontal_placement and horizontal_behind) or (not is_horizontal_placement and vertical_behind):
                        intersection_count += 1
                        # print(f"({i}) before")
                elif next_position is None:
                    # for the last position, check to see if there's tiles "in front" of us
                    if (is_horizontal_placement and horizontal_front) or (not is_horizontal_placement and vertical_front):
                        intersection_count += 1
                        # print(f"({i}) after")
                if (
                    ((horizontal_behind or horizontal_front) and not is_horizontal_placement)
                    or ((vertical_behind or vertical_front) and is_horizontal_placement)
                ):
                    intersection_count += 1

                    # print(f"({i}) above or below")

        computer_science_term_count = 0
        for placement in self.word_placement:
            for letter in placement.word:
                letter_score = next(value for value, letters in LETTER_SCORING.items() if letter in letters)
                score += letter_score

            if placement.word in computer_science_terms:
                computer_science_term_count += 1
        # print(f"Intersections: {intersection_count}")
        return score * (2 ** max(0, intersection_count - 1)) * (2 ** computer_science_term_count)


class Controller(abc.ABC):
    """
    Represents an object that can make moves.
    Effectively represents a player, but does not contain state.

    Since a Controller should not contain state, it should be possible for the same instance of (for instance) an AIController
    to be used to play against the same instance of an AIController.
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def make_move(self, game: 'Game', player: Player) -> Optional[Move]:  # TODO define return type
        pass

    @abc.abstractmethod
    def copy(self) -> 'Controller':
        pass


class LetterBag:

    def __init__(self):
        self.letters = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
                   'E', 'E', 'E', 'F', 'F', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'M',
                   'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'P', 'P', 'Q', 'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S',
                   'S', 'S', 'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U', 'V', 'V', 'W', 'W', 'X', 'Y', 'Y', 'Z']

    def get_tile(self):
        if len(self.letters) > 0:
            return self.letters.pop(random.randrange(len(self.letters)))
        else:
            return None

    def return_tile(self, tile: Tile):
        self.letters.append(tile)


class Game:
    def __init__(self, controllers: List[Controller], word_dict: WordDict, computer_science_terms: Set[str]):
        self.board = Board(15, {})
        self.players: List[Tuple[Player, Controller]] = [(Player(), controller) for controller in controllers]
        """A list where each entry contains a Player object and a Controller object. The player object may be mutated to update score and a player's hand"""
        self.word_dict = word_dict
        self.computer_science_terms = computer_science_terms
        self.turn_index = 0
        self.letter_bag = LetterBag()
        print(len(self.letter_bag.letters))
        self.end_condition = False

    @property
    def current_player(self) -> Tuple[Player, Controller]:
        return self.players[self.turn_index]

    def update(self):
        (current_player, current_controller) = self.current_player

        if not self.end_condition:
            move = current_controller.make_move(self, current_player)
            if move is not None:
                if move.new_hand == current_player.hand and not move.word_placement:  # check if the player is passing their turn
                    all_others_have_passed = all(player.passed_last_turn for player, _ in self.players[:self.turn_index] + self.players[self.turn_index + 1:])
                    if all_others_have_passed:
                        self.end_condition = True
                    current_player.passed_last_turn = True
                else:
                    current_player.passed_last_turn = False

                current_player.score += move.score(self.board, self.computer_science_terms)
                current_player.hand = move.new_hand
                self.board = self.board.place_tiles(move.tile_placements)
                self.turn_index = (self.turn_index + 1) % len(self.players)