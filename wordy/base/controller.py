import abc
from typing import Optional

from wordy.base.game import Game, Player, Move


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
    def make_move(self, game: Game, player: Player) -> Optional[Move]:  # TODO define return type
        pass


