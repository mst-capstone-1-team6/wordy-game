import pygame

from wordy.base.aicontroller import AIController
from wordy.graphics.humancontroller import HumanController
from wordy.base.game import Game, Player, Controller
from wordy.graphics.common import common_handle_event
from wordy.graphics.screen import Screen
from wordy.graphics.tile import Tile
from wordy.graphics.cursor import Cursor
from wordy.graphics.button import Button
from wordy.graphics.boarddisplay import BoardDisplay


class GameScreen(Screen):

    def __init__(self, game: Game):
        super().__init__()
        self.game = game
        self.piece_size = 50

        self.ref_board = {}

        for p, c in self.game.players:
            if isinstance(c, HumanController):
                c.draw_tiles(self.game.letter_bag)

        self.ET_button = Button((self.piece_size * 15.5), (self.piece_size * 13.5), 200, 80, "END TURN")
        self.NH_button = Button((self.piece_size * 15.5), (self.piece_size * 11.5), 200, 80, "NEW HAND")
        self.UIdisplay = pygame.sprite.Group()
        self.UIdisplay.add(BoardDisplay(0, 0, 15, self.piece_size))
        self.UIdisplay.add(self.ET_button)
        self.UIdisplay.add(self.NH_button)

        self.board_tiles = pygame.sprite.LayeredUpdates()  # Holds all the tile sprite
        self.cursor = Cursor()  # Just a sprite to represent the cursor

    def __event_handler(self):
        (player, controller) = self.game.current_player

        for event in pygame.event.get():
            common_handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                assert isinstance(controller, HumanController)

                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]
                # Gets all the tiles that collide with the cursor
                sprite_collides = pygame.sprite.spritecollide(self.cursor, controller.hand_tiles, False)

                if event.button == 1 and sprite_collides:
                    s = sprite_collides[len(sprite_collides) - 1]  # Only selects the top most tile
                    controller.hand_tiles.move_to_front(s)
                    s.dragging = True
                    s.grid_lock = False
                    s.off_x = s.rect.x - self.cursor.rect.x
                    s.off_y = s.rect.y - self.cursor.rect.y
                    s.forming_word = True
                elif event.button == 1 and self.ET_button.rect.colliderect(self.cursor.rect):
                    # If the submit word button pressed, check if the move is valid
                    hand_letters = []
                    for tile in controller.hand_tiles:
                        hand_letters.append(tile.l)
                    player.hand = hand_letters
                    controller.end_turn(self.game.board, self.game.letter_bag)

                elif event.button == 1 and self.NH_button.rect.colliderect(self.cursor.rect):
                    # If the new hand button pressed, give the player a new hand
                    hand_letters = []
                    for tile in controller.hand_tiles:
                        hand_letters.append(tile.l)
                    player.hand = hand_letters
                    controller.new_hand(self.game.letter_bag)
                    controller.end_turn(self.game.board, self.game.letter_bag)

            elif event.type == pygame.MOUSEBUTTONUP:
                self.cursor.rect.x = event.pos[0]
                self.cursor.rect.y = event.pos[1]
                for s in controller.hand_tiles:  # Loop over all tiles to find the one being dragged
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
                for s in controller.hand_tiles:  # Update the position of a dragged tile
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
                        self.board_tiles.add(Tile((i, j), self.game.board.tile_at((i, j)), True))

        game_display.fill((255, 255, 255))

        # Draw the UI elements
        self.UIdisplay.draw(game_display)

        # Draw the tiles on the board
        self.board_tiles.draw(game_display)

        (player, controller) = self.game.current_player

        pygame.font.init()
        font = pygame.font.SysFont('Comic Sans MS', 40)

        if isinstance(controller, HumanController):

            controller.hand_tiles.draw(game_display)
            controller.hand_tiles.update(game_display)

            # Display current player's name
            text_surface = font.render(controller.name, True, (0, 0, 0))
            game_display.blit(text_surface, (self.piece_size * 16.5, self.piece_size * 2))

            # Display how many tiles left in the bag
            text_surface = font.render(str(len(self.game.letter_bag.letters)) + " letters left", True, (0, 0, 0))
            game_display.blit(text_surface, (self.piece_size * 16, self.piece_size * 0))

        p: Player
        c: Controller
        for i in range(len(self.game.players)):
            (p, c) = self.game.players[i]
            if isinstance(c, AIController):
                text_surface = font.render("Computer: " + str(p.score), True, (0, 0, 0))
            else:
                text_surface = font.render(c.name + ": " + str(p.score), True, (0, 0, 0))
            game_display.blit(text_surface, (self.piece_size * (1+(4*i)), self.piece_size * 15.3))

        # there is a player whose turn it is
        # there is a controller corresponding to that player
        # if that controller is a HumanPlayer, then we should display their hand on the screen and handle drag/drops as a move

        # TODO check if the game has ended. If it has, then display a pop up showing results (winner or tie) of the game

    def next_screen(self) -> 'Screen':
        # TODO return something other than self when the game has ended. (Likely will return an instance of a TitleScreen)
        return self

