import pygame
import random

from wordy.base.aicontroller import AI_CONTROLLER
from wordy.base.game import Game
from wordy.graphics.common import common_handle_event
from wordy.graphics.screen import Screen
from wordy.graphics.tile import Tile
from wordy.graphics.cursor import Cursor
from wordy.base.board import Board
from wordy.graphics.button import Button


class GameScreen(Screen):

    def __init__(self):
        super().__init__()
        # TODO Instantiate HumanControllers here or pass parameters through constructor so that the TitleScreen controls the type of Controllers present
        self.game = Game([AI_CONTROLLER, AI_CONTROLLER])
        self.game_board = Board(15, {})
        self.submit_word_but = Button()  # Button to submit a word/turn
        self.all_sprites = pygame.sprite.LayeredUpdates()  # Holds all the tile sprite
        self.cursor = Cursor()  # Just a sprite to represent the cursor

        # Places a bunch of random tiles off to the side
        for posx in range(35):
            temp_tile = Tile(((posx % 7) * 30) + 540, (int(posx / 7) * 30) + 90, chr(random.randrange(ord('a'), ord('z') + 1)).upper())
            self.all_sprites.add(temp_tile)

    def __event_handler(self):
        for event in pygame.event.get():
            common_handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:

                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]
                # Gets all the tiles that collide with the cursor
                sprite_collides = pygame.sprite.spritecollide(self.cursor, self.all_sprites, False)

                if event.button == 1 and sprite_collides:
                    s = sprite_collides[len(sprite_collides) - 1]  # Only selects the top most tile
                    if not s.locked:  # if the tile is not locked, then start dragging it
                        self.all_sprites.move_to_front(s)
                        s.dragging = True
                        s.grid_lock = False
                        s.off_x = s.rect.x - self.cursor.rect.x
                        s.off_y = s.rect.y - self.cursor.rect.y
                elif event.button == 1 and self.submit_word_but.rect.colliderect(self.cursor.rect):
                    # If the submit word button pressed, check if the move is valid
                    self.check_word()

            elif event.type == pygame.MOUSEBUTTONUP:
                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]
                for s in self.all_sprites:  # Loop over all tiles to find the one being dragged
                    if event.button == 1 and s.dragging:  # If the tile is being dragged, release it
                        s.dragging = False
                        s.rect.x = self.cursor.rect.x + s.off_x
                        s.rect.y = self.cursor.rect.y + s.off_y
                        s.off_x = 0
                        s.off_y = 0
                        s.grid_lock = True

                        # Puts the tile in a grid spot
                        s.rect.y = (s.piece_size[1] * (int(s.rect.centery / s.piece_size[1])))
                        s.rect.x = (s.piece_size[0] * (int(s.rect.centerx / s.piece_size[0])))
                        s.grid_spot = ((s.rect.x / s.piece_size[0]) - 1, (s.rect.y / s.piece_size[1]) - 1)

                        # Check to see if the tile is in the board, if so make it a forming word
                        if 14 >= s.grid_spot[0] >= 0 and 14 >= s.grid_spot[1] >= 0:
                            s.forming_word = True
                        else:
                            s.forming_word = False
                            s.prev_spot = s.grid_spot

            elif event.type == pygame.MOUSEMOTION:
                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]
                for s in self.all_sprites:  # Update the position of a dragged tile
                    if s.dragging:
                        s.rect.x = self.cursor.rect.x + s.off_x
                        s.rect.y = self.cursor.rect.y + s.off_y

    def update(self, game_display):
        self.__event_handler()
        game_display.fill((255, 255, 255))
        self.draw_grid(game_display, 15, 15, 30, 30, 30)
        self.all_sprites.draw(game_display)
        self.all_sprites.update(game_display)
        self.submit_word_but.update(game_display)
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

    def check_word(self):
        temp_dict = {}

        # Will try to put all the new tiles into the dict
        # If it doesn't work, returns all new tiles to their original spots
        try:
            # Putting the new tiles into a temp dict
            for s in self.all_sprites:
                if s.forming_word:
                    if not (s.grid_spot in temp_dict):
                        temp_dict[s.grid_spot] = s.l
                    else:
                        raise ValueError()
            self.game_board = self.game_board.place_tiles(temp_dict)  # Passing the temp dict to the game board

            # Locking all the new word tiles
            for s in self.all_sprites:
                if s.forming_word:
                    s.forming_word = False
                    s.locked = True
                    s.prev_spot = s.grid_spot
        except ValueError:
            # Resetting all the new word tiles to the original position
            for s in self.all_sprites:
                if s.forming_word:
                    s.rect.x = ((s.prev_spot[0] + 1) * s.piece_size[0])
                    s.rect.y = ((s.prev_spot[1] + 1) * s.piece_size[1])
                    s.grid_spot = s.prev_spot
                    s.forming_word = False
                    s.locked = False

    def draw_grid(self, game_display, height, width, sqr_size, x, y):
        background = pygame.rect.Rect(x, y, (height * sqr_size) + 1, (width * sqr_size) + 1)
        pygame.draw.rect(game_display, (0, 0, 0), background)

        for i in range(height):
            for j in range(width):
                square = pygame.rect.Rect(x + (j * sqr_size) + 1, y + (i * sqr_size) + 1, sqr_size - 1, sqr_size - 1)
                pygame.draw.rect(game_display, (255, 255, 255), square)
