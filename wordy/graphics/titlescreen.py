from pathlib import Path

import pygame

from wordy.base.game import Game
from wordy.base.worddict import file_to_set, WordDict
from wordy.graphics.common import common_handle_event
from wordy.graphics.humancontroller import HumanController
from wordy.graphics.screen import Screen
from wordy.graphics.gamescreen import GameScreen


class TitleScreen(Screen):

    def __init__(self):
        super().__init__()
        self.__next_screen: 'Screen' = self
        self.word_dict = WordDict.from_file("assets/dicts/full_dict.txt")
        self.computer_science_terms = file_to_set(Path("assets/dicts/cs_dict.txt"), self.word_dict)

    def __event_handler(self):
        for event in pygame.event.get():
            common_handle_event(event)
            # TODO check if some button is pressed. If it is, set self.__next_screen = GameScreen()

    def update(self, game_display):
        self.__event_handler()

    def next_screen(self) -> 'Screen':
        game = Game(
            [HumanController("Player1", self.word_dict), HumanController("Player2", self.word_dict), HumanController("Player3", self.word_dict), HumanController("Player4", self.word_dict)],
            self.word_dict, self.computer_science_terms
        )
        return GameScreen(game)
