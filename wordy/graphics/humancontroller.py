from typing import Optional

from wordy.base.controller import Controller
from wordy.base.game import Game, Player, Move


class HumanController(Controller):
    def __init__(self):
        super().__init__()

    def make_move(self, game: Game, player: Player) -> Optional[Move]:
        pass
