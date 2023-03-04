import pygame

from wordy.base.aicontroller import AI_CONTROLLER
from wordy.base.game import Game
from wordy.graphics.common import common_handle_event
from wordy.graphics.screen import Screen


class GameScreen(Screen):

    def __init__(self):
        super().__init__()
        # TODO Instantiate HumanControllers here or pass parameters through constructor so that the TitleScreen controls the type of Controllers present
        self.game = Game([AI_CONTROLLER, AI_CONTROLLER])

    def __event_handler(self):
        for event in pygame.event.get():
            common_handle_event(event)

    def update(self):
        self.__event_handler()
        # there is a player whose turn it is
        # there is a controller corresponding to that player
        # if that controller is a HumanPlayer, then we should display their hand on the screen and handle drag/drops as a move
        (player, controller) = self.game.current_player
        # TODO check if controller is a HumanController
        #   If it is, then display the player's hand

        # TODO loop through self.game.players and display scores on screen

        # TODO check if the game has ended. If it has, then display a pop up showing results (winner or tie) of the game

    def next_screen(self) -> 'Screen':
        # TODO return something other than self when the game has ended. (Likely will return an instance of a TitleScreen)
        return self

