import pygame

from wordy.graphics.common import common_handle_event
from wordy.graphics.screen import Screen
from wordy.graphics.gamescreen import GameScreen
from wordy.base.game import Player


class TitleScreen(Screen):

    def __init__(self):
        super().__init__()
        self.__next_screen: 'Screen' = self

    def __event_handler(self):
        for event in pygame.event.get():
            common_handle_event(event)
            # TODO check if some button is pressed. If it is, set self.__next_screen = GameScreen()

    def update(self, game_display):
        self.__event_handler()

    def next_screen(self) -> 'Screen':
        return GameScreen([Player("Player1"), Player("Player2")])
