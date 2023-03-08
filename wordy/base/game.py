import abc
from dataclasses import dataclass
from typing import List, Tuple, Dict
from typing import Optional

import pygame.sprite

from wordy.base.board import Board, Position, Tile


class Player:
    def __init__(self, player_name):
        self.score: int = 0
        self.hand: pygame.sprite.LayeredUpdates = pygame.sprite.LayeredUpdates()
        self.passed_last_turn = False
        self.missing_ties: List[int] = []
        self.name = player_name


@dataclass
class WordPlacement:
    tile_placements: Dict[Position, Tile]
    word_start: Position
    word_end: Position
    word: str


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
    word_placement: Optional[WordPlacement]


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


class Game:
    def __init__(self, controllers: List[Controller]):
        self.board = Board(15, {})
        self.players: List[Tuple[Player, Controller]] = [(Player("player"), controller) for controller in controllers]
        """A list where each entry contains a Player object and a Controller object. The player object may be mutated to update score and a player's hand"""
        self.turn_index = 0

    @property
    def current_player(self) -> Tuple[Player, Controller]:
        return self.players[self.turn_index]

    def update(self):
        (current_player, current_controller) = self.current_player
        move = current_controller.make_move(self, current_player)
        if move is not None:
            if move.new_hand == current_player.hand and move.word_placement is None:  # check if the player is passing their turn
                if current_player.passed_last_turn:
                    print("Hey! TODO end the game here! This is the second occurrence of this player passing their turn.")
                current_player.passed_last_turn = True
            else:
                current_player.passed_last_turn = False
                word_placement = move.word_placement
                if word_placement is not None:
                    self.board = self.board.place_tiles(word_placement.tile_placements)
            # do something and update board
            self.turn_index = (self.turn_index + 1) % len(self.players)
