from enum import Enum
from pathlib import Path
from typing import List, Tuple

import pygame
from pygame.rect import Rect
from pygame.sprite import Sprite, spritecollide, Group

from wordy.base.aicontroller import AIController
from wordy.base.game import Game
from wordy.base.worddict import file_to_set, WordDict
from wordy.graphics import DISPLAY_WIDTH
from wordy.graphics.common import common_handle_event
from wordy.graphics.gamescreen import GameScreen
from wordy.graphics.humancontroller import HumanController
from wordy.graphics.screen import Screen


class PlayerType(Enum):
    HUMAN = 1
    AI = 2


def _create_sprite(image_path: str, width: int, height: int):
    sprite = Sprite()
    image = pygame.transform.scale(pygame.image.load(image_path), (width, height))
    sprite.image = image
    sprite.rect = image.get_rect()
    return sprite


def _create_button_player():
    return _create_sprite("assets/title/Player.png", 200, 80)


def _create_button_ai():
    return _create_sprite("assets/title/AI.png", 200, 80)


def _create_button_start_game():
    # 230 is an estimate to keep the same ratio
    return _create_sprite("assets/title/StartGame.png", 230, 80)


def _create_button_remove():
    # 230 is an estimate to keep the same ratio
    return _create_sprite("assets/title/Remove.png", 230, 80)


def _create_button_add_ai():
    return _create_sprite("assets/title/AddAI.png", 230, 80)


def _create_button_add_player():
    return _create_sprite("assets/title/AddPlayer.png", 230, 80)


def _rect_center_to(rect: Rect, x: int, y: int):
    rect.centerx = x
    rect.centery = y


def _create_cursor():
    cursor = Sprite()
    cursor.rect = Rect(1, 1, 1, 1)
    return cursor


class TitleScreen(Screen):

    def __init__(self):
        super().__init__()
        self.__next_screen: 'Screen' = self
        self.word_dict = WordDict.from_file("assets/dicts/full_dict.txt")
        self.computer_science_terms = file_to_set(Path("assets/dicts/cs_dict.txt"), self.word_dict)
        self.players: List[PlayerType] = []

        self.cursor = _create_cursor()

        self.ui_display = Group()
        self.player_slots: List[Tuple[Group, Tuple[int, int], Group, Tuple[int, int]]] = [
            (Group(), (DISPLAY_WIDTH / 2 - 150, 100 + i * 100), Group(), (DISPLAY_WIDTH / 2 + 150, 100 + i * 100)) for i in range(4)
        ]
        """A list of (player group, player position, remove group, remove position)"""
        for (_, _, group, remove_position) in self.player_slots:
            button = _create_button_remove()
            group.add(button)
            _rect_center_to(button.rect, remove_position[0], remove_position[1])
        self.button_start_game = _create_button_start_game()
        _rect_center_to(self.button_start_game.rect, DISPLAY_WIDTH / 2, 600)
        self.button_add_human = _create_button_add_player()
        self.button_add_ai = _create_button_add_ai()
        _rect_center_to(self.button_add_human.rect, DISPLAY_WIDTH / 2 - 150, 510)
        _rect_center_to(self.button_add_ai.rect, DISPLAY_WIDTH / 2 + 150, 510)

        self.ui_display.add(self.button_start_game)
        self.ui_display.add(self.button_add_human)
        self.ui_display.add(self.button_add_ai)
        self.sprite_pool_player = [_create_button_player() for _ in range(4)]
        self.sprite_pool_ai = [_create_button_ai() for _ in range(4)]

        self.update_players([PlayerType.HUMAN, PlayerType.AI])

    def __start_game(self):
        controllers = []
        player_count = 1
        for player_type in self.players:
            if player_type == PlayerType.HUMAN:
                controllers.append(HumanController(f"Player {player_count}", self.word_dict))
                player_count += 1
            else:
                controllers.append(AIController("AI"))
        # controllers = [HumanController("Player1", self.word_dict), HumanController("Player2", self.word_dict),
        #                HumanController("Player3", self.word_dict), HumanController("Player4", self.word_dict)],
        game = Game(controllers, self.word_dict, self.computer_science_terms)
        self.__next_screen = GameScreen(game, self)

    def __event_handler(self):
        for event in pygame.event.get():
            common_handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]

                collision_sprites = spritecollide(self.cursor, self.ui_display, dokill=False)
                if self.button_start_game in collision_sprites:
                    self.__start_game()
                elif self.button_add_human in collision_sprites:
                    self.update_players(self.players + [PlayerType.HUMAN])
                elif self.button_add_ai in collision_sprites:
                    self.update_players(self.players + [PlayerType.AI])
                for i, (slot_group, _, remove_button_group, _) in enumerate(self.player_slots):
                    if spritecollide(self.cursor, slot_group, dokill=False):
                        new_players = list(self.players)
                        new_players.insert(0, new_players.pop(i))
                        self.update_players(new_players)
                    if spritecollide(self.cursor, remove_button_group, dokill=False):
                        self.update_players(self.players[:i] + self.players[i + 1:])

    def update_players(self, new_players: List[PlayerType]):
        if not (2 <= len(new_players) <= 4):
            return  # silently return when invalid number of players is given
        old_players = self.players
        self.players = new_players
        for i in range(4):
            (slot_group, position, _, _) = self.player_slots[i]
            old_player_type = old_players[i] if i < len(old_players) else None
            new_player_type = new_players[i] if i < len(new_players) else None
            if old_player_type != new_player_type:
                old_sprites = []
                if old_player_type is not None:
                    sprite = slot_group.sprites()[0]
                    slot_group.remove(sprite)
                    old_sprites.append(sprite)
                    # print("removed old")
                if new_player_type is not None:
                    if new_player_type == PlayerType.HUMAN:
                        sprite = self.sprite_pool_player.pop()
                    elif new_player_type == PlayerType.AI:
                        sprite = self.sprite_pool_ai.pop()
                    else:
                        raise AssertionError()
                    _rect_center_to(sprite.rect, position[0], position[1])
                    slot_group.add(sprite)
                    # print(f"({i}) added new {new_player_type}")

                if old_player_type == PlayerType.HUMAN:
                    for sprite in old_sprites:
                        self.sprite_pool_player.append(sprite)
                elif old_player_type == PlayerType.AI:
                    for sprite in old_sprites:
                        self.sprite_pool_ai.append(sprite)

    def update(self, game_display):
        self.__event_handler()
        game_display.fill((255, 255, 255))
        self.ui_display.draw(game_display)
        for slot_group, _, _, _ in self.player_slots:
            slot_group.draw(game_display)
        for i, _ in enumerate(self.players):
            (_, _, remove_button_group, _) = self.player_slots[i]
            remove_button_group.draw(game_display)

    def next_screen(self) -> 'Screen':
        return self.__next_screen
