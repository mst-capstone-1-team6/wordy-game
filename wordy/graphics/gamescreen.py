import pygame
import random

from typing import List
from wordy.base.aicontroller import AI_CONTROLLER
from wordy.graphics.humancontroller import HumanController
from wordy.base.game import Game, Player, Move
from wordy.graphics.common import common_handle_event
from wordy.graphics.screen import Screen
from wordy.graphics.tile import Tile
from wordy.graphics.cursor import Cursor
from wordy.base.board import Board
from wordy.graphics.button import Button
from wordy.graphics.boarddisplay import BoardDisplay


class GameScreen(Screen):
    current_control: HumanController = HumanController()
    def __init__(self):
        super().__init__()
        self.piece_size = 50

        self.ref_board = {}
        # TODO Instantiate HumanControllers here or pass parameters through constructor so that the TitleScreen controls the type of Controllers present

        self.game = Game([HumanController()])

        self.ET_button = Button((self.piece_size * 15.5), (self.piece_size * 13.5), 200, 80, "END TURN")
        self.NH_button = Button((self.piece_size * 15.5), (self.piece_size * 11.5), 200, 80, "NEW HAND")
        self.UIdisplay = pygame.sprite.Group()
        self.UIdisplay.add(BoardDisplay(0, 0, 15, self.piece_size))
        self.UIdisplay.add(self.ET_button)
        self.UIdisplay.add(self.NH_button)

        self.board_tiles = pygame.sprite.LayeredUpdates()  # Holds all the tile sprite
        self.cursor = Cursor()  # Just a sprite to represent the cursor

        """
        for p in self.all_players:
            tempgroup = pygame.sprite.LayeredUpdates()
            for i in range(7):
                play_tile = Tile(self.piece_size * 17, self.piece_size * (3 + i), self.letter_bag.pop(random.randrange(len(self.letter_bag))), i)
                tempgroup.add(play_tile)
            p.hand = tempgroup

        self.current_player: Player = self.all_players[0]

        # Places a bunch of random tiles off to the side
        for i in range(4*13):
            temp_tile = Tile(((posx % 4) * self.piece_size) + (self.piece_size*16), (int(posx / 4) * self.piece_size) + (self.piece_size*0), chr(random.randrange(ord('a'), ord('z') + 1)).upper())
            self.all_sprites.add(temp_tile)
        """

    def __event_handler(self):
        for event in pygame.event.get():
            common_handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:

                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]
                # Gets all the tiles that collide with the cursor
                sprite_collides = pygame.sprite.spritecollide(self.cursor, self.current_control.hand_tiles, False)

                if event.button == 1 and sprite_collides:
                    s = sprite_collides[len(sprite_collides) - 1]  # Only selects the top most tile
                    self.current_control.hand_tiles.move_to_front(s)
                    s.dragging = True
                    s.grid_lock = False
                    s.off_x = s.rect.x - self.cursor.rect.x
                    s.off_y = s.rect.y - self.cursor.rect.y
                    s.forming_word = True
                elif event.button == 1 and self.ET_button.rect.colliderect(self.cursor.rect):
                    # If the submit word button pressed, check if the move is valid
                    self.current_control.end_turn(self.game.board)
                elif event.button == 1 and self.NH_button.rect.colliderect(self.cursor.rect):
                    # If the new hand button pressed, give the player a new hand
                    self.current_control.new_hand(self.game.letter_bag)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]
                for s in self.current_control.hand_tiles:  # Loop over all tiles to find the one being dragged
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
                        s.grid_spot = ((s.rect.x / s.piece_size[0]), (s.rect.y / s.piece_size[1]))

                        # Check to see if the tile is in the board, if so make it a forming word
                        if 14 >= s.grid_spot[0] >= 0 and 14 >= s.grid_spot[1] >= 0:
                            s.forming_word = True
                        else:
                            s.rect.x = ((s.prev_spot[0]) * s.piece_size[0])
                            s.rect.y = ((s.prev_spot[1]) * s.piece_size[1])
                            s.forming_word = False
                            s.grid_spot = s.prev_spot

            elif event.type == pygame.MOUSEMOTION:
                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]
                for s in self.current_control.hand_tiles:  # Update the position of a dragged tile
                    if s.dragging:
                        s.rect.x = self.cursor.rect.x + s.off_x
                        s.rect.y = self.cursor.rect.y + s.off_y

    def update(self, game_display):
        self.__event_handler()

        # self.game.update() This will call make move of what ever controller is acted upon
        # Will need to handle human controller to set up what ever move is currently happening
        # game.update will update the board
        # Will need to iterate over the board to get where to place tiles at spots in the dict
        # self.game.current_player will return tuple of the controller and player
        # game.move contains the new hand, controllers will draw tiles after their turn

        self.game.update()

        if len(self.board_tiles.sprites()) != self.game.board.num_tiles():
            self.board_tiles = pygame.sprite.LayeredUpdates()
            for i in range(self.game.board.size):
                for j in range(self.game.board.size):
                    if self.game.board.tile_at((i, j)):
                        self.board_tiles.add(Tile((i, j), self.game.board.tile_at((i, j))))

        game_display.fill((255, 255, 255))

        # Draw the UI elements
        self.UIdisplay.draw(game_display)

        # Draw the tiles on the board
        self.board_tiles.draw(game_display)

        (player, controller) = self.game.current_player

        if isinstance(controller, HumanController):
            self.current_control = controller

            controller.draw_tiles(self.game.letter_bag)
            controller.hand_tiles.draw(game_display)
            controller.hand_tiles.update(game_display)

            pygame.font.init()
            font = pygame.font.SysFont('Comic Sans MS', 40)

            # Display current player's name
            text_surface = font.render(self.current_control.name, True, (0, 0, 0))
            game_display.blit(text_surface, (self.piece_size * 16.5, self.piece_size * 2))

            # Display how many tiles left in the bag
            text_surface = font.render(str(len(self.game.letter_bag.letters)) + " letters left", True, (0, 0, 0))
            game_display.blit(text_surface, (self.piece_size * 16, self.piece_size * 0))

        # there is a player whose turn it is
        # there is a controller corresponding to that player
        # if that controller is a HumanPlayer, then we should display their hand on the screen and handle drag/drops as a move

        # TODO loop through self.game.players and display scores on screen

        # TODO check if the game has ended. If it has, then display a pop up showing results (winner or tie) of the game

    def next_screen(self) -> 'Screen':
        # TODO return something other than self when the game has ended. (Likely will return an instance of a TitleScreen)
        return self

"""
    def new_hand(self):
        # Put all the tiles back in the bag
        for s in self.current_player.hand.sprites():
            self.letter_bag.append(s.l)

        # Get new tiles for the player
        tempgroup = pygame.sprite.LayeredUpdates()
        for i in range(7):
            play_tile = Tile(self.piece_size * 17, self.piece_size * (3 + i), self.letter_bag.pop(random.randrange(len(self.letter_bag))), i)
            tempgroup.add(play_tile)
        self.current_player.hand = tempgroup

        self.current_player = self.all_players[(self.all_players.index(self.current_player) + 1) % len(self.all_players)]

    def check_word(self):
        temp_dict = {}

        # Will try to put all the new tiles into the dict
        # If it doesn't work, returns all new tiles to their original spots
        try:
            # Putting the new tiles into a temp dict
            flag = False
            for s in self.current_player.hand.sprites():
                if s.forming_word:
                    if not (s.grid_spot in temp_dict):
                        if s.grid_spot == (7, 7):  # Check if the tile is going through the middle
                            flag = True
                        temp_dict[s.grid_spot] = s.l
                    else:
                        raise ValueError()
            if self.first_word and not flag and temp_dict:  # If it is the first word, and it does not intersect middle, reject it
                raise ValueError()
            self.game_board = self.game_board.place_tiles(temp_dict)  # Passing the temp dict to the game board
            self.first_word = False
            # Locking all the new word tiles
            for s in self.current_player.hand:
                if s.forming_word:
                    s.forming_word = False
                    s.locked = True
                    s.prev_spot = s.grid_spot
                    self.board_tiles.add(s)
                    self.current_player.missing_ties.append(s.hand_pos)
                    self.current_player.hand.remove(s)

            # Refill the tiles used in the hand
            for i in self.current_player.missing_ties:
                play_tile = Tile(self.piece_size * 17, self.piece_size * (3 + i), self.letter_bag.pop(random.randrange(len(self.letter_bag))), i)
                self.current_player.hand.add(play_tile)
            self.current_player.missing_ties = []

            # Cycle to the next player
            self.current_player = self.all_players[(self.all_players.index(self.current_player) + 1) % len(self.all_players)]

        except ValueError:
            # Resetting all the new word tiles to the original position
            for s in self.current_player.hand:
                if s.forming_word:
                    s.rect.x = ((s.prev_spot[0]) * s.piece_size[0])
                    s.rect.y = ((s.prev_spot[1]) * s.piece_size[1])
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
    """
