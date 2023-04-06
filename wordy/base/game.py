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

    def score(self, computer_science_terms: Set[str]) -> int:
        score = 0
        for tile in self.tile_placements.values():
            letter_score = next(value for value, letters in LETTER_SCORING.items() if tile in letters)
            score += letter_score

        intersection_multiplier = 1
        computer_science_term_count = 0
        for placement in self.word_placement:
            segment_count = 0
            was_last_tile_on_board: Optional[bool] = None
            for position in over_positions(placement.word_start, placement.word_end):
                tile_on_board = position not in self.tile_placements
                if tile_on_board != was_last_tile_on_board:
                    segment_count += 1
                was_last_tile_on_board = tile_on_board
            intersection_count = segment_count // 2  # divide by 2 and floor result
            # 1 intersection is to be expected, so start gaining double points at 2 intersections
            intersection_multiplier *= 2 ** max(0, intersection_count - 1)
            if placement.word in computer_science_terms:
                computer_science_term_count += 1
        print(f"Multiplier: {intersection_multiplier}")
        return score * intersection_multiplier * (2 ** computer_science_term_count)


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


class LetterBag:
    letters = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'B', 'C', 'C', 'D', 'D', 'D', 'D', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
               'E', 'E', 'E', 'F', 'F', 'G', 'G', 'G', 'H', 'H', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'J', 'K', 'L', 'L', 'L', 'L', 'M',
               'M', 'N', 'N', 'N', 'N', 'N', 'N', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'P', 'P', 'Q', 'R', 'R', 'R', 'R', 'R', 'R', 'S', 'S',
               'S', 'S', 'T', 'T', 'T', 'T', 'T', 'T', 'U', 'U', 'U', 'U', 'V', 'V', 'W', 'W', 'X', 'Y', 'Y', 'Z']

    def get_tile(self) -> Tile:
        return self.letters.pop(random.randrange(len(self.letters)))

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

    @property
    def current_player(self) -> Tuple[Player, Controller]:
        return self.players[self.turn_index]

    def update(self):
        (current_player, current_controller) = self.current_player
        move = current_controller.make_move(self, current_player)
        if move is not None:
            if move.new_hand == current_player.hand and not move.word_placement:  # check if the player is passing their turn
                if current_player.passed_last_turn:
                    print("Hey! TODO end the game here! This is the second occurrence of this player passing their turn.")
                current_player.passed_last_turn = True
            else:
                current_player.passed_last_turn = False

            self.board = self.board.place_tiles(move.tile_placements)
            current_player.score += move.score(self.computer_science_terms)
            self.turn_index = (self.turn_index + 1) % len(self.players)
