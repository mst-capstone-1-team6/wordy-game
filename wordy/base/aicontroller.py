from typing import Optional

from wordy.base.controller import Controller
from wordy.base.game import Game, Player, Move


class AIController(Controller):
    def __init__(self):
        super().__init__()

    def make_move(self, game: Game, player: Player) -> Optional[Move]:
        pass


# Note: if we decide that each Controller should have a name,
#   then creating a single instance for an AI Controller may not make sense if we want to have "AI 1" and "AI 2" for multiple AIs
AI_CONTROLLER = AIController()
"""The instance of an AI Controller."""
