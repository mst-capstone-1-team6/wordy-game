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

    def __init__(self, game: Game, return_screen: Screen):
        super().__init__()
        self.game = game
        self.return_screen = return_screen
        self.piece_size = 50
        self.menu = False
        self.rematch = False
        self.player_num = 0

        for p, c in self.game.players:
            if isinstance(c, HumanController):
                c.draw_tiles(self.game.letter_bag)

        self.ET_button = Button((self.piece_size * 15.65), (self.piece_size * 13.45), 190, 76, "END TURN")
        self.NH_button = Button((self.piece_size * 15.65), (self.piece_size * 11.85), 190, 76, "NEW HAND")
        self.AR_button = Button((self.piece_size * 17), (self.piece_size * 10.4), 50, 50, "Arrow")
        self.CT_button = Button((self.piece_size * 15.65), (self.piece_size * 8), 190, 76, "Continue")
        self.RM_button = Button((self.piece_size * 15.65), (self.piece_size * 13.45), 190, 76, "Rematch")
        self.ME_button = Button((self.piece_size * 15.65), (self.piece_size * 11.85), 190, 76, "Menu")
        self.GameUI = pygame.sprite.Group()
        self.BoardUI = pygame.sprite.Group()
        self.EndUI = pygame.sprite.Group()
        self.TurnUI = pygame.sprite.Group()
        self.BoardUI.add(BoardDisplay(0, 0, 15, self.piece_size))
        self.GameUI.add(self.ET_button)
        self.GameUI.add(self.NH_button)
        self.GameUI.add(self.AR_button)
        self.TurnUI.add(self.CT_button)
        self.EndUI.add(self.RM_button)
        self.EndUI.add(self.ME_button)

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

                if event.button == 1 and self.CT_button.rect.colliderect(self.cursor.rect) and not self.player_num == self.game.turn_index:
                    self.player_num = self.game.turn_index
                elif event.button == 1 and self.ME_button.rect.colliderect(self.cursor.rect) and self.game.end_condition:
                    self.menu = True
                elif event.button == 1 and self.RM_button.rect.colliderect(self.cursor.rect) and self.game.end_condition:
                    self.rematch = True

                elif event.button == 1 and sprite_collides and self.player_num == self.game.turn_index:
                    s = sprite_collides[len(sprite_collides) - 1]  # Only selects the top most tile
                    controller.hand_tiles.move_to_front(s)
                    s.dragging = True
                    s.grid_lock = False
                    s.off_x = s.rect.x - self.cursor.rect.x
                    s.off_y = s.rect.y - self.cursor.rect.y
                    s.forming_word = True

                elif event.button == 1 and self.ET_button.rect.colliderect(self.cursor.rect) and self.player_num == self.game.turn_index:
                    # If the submit word button pressed, check if the move is valid
                    hand_letters = []
                    for tile in controller.hand_tiles:
                        hand_letters.append(tile.l)
                    player.hand = hand_letters
                    controller.end_turn(self.game.board, self.game.letter_bag)

                elif event.button == 1 and self.NH_button.rect.colliderect(self.cursor.rect) and self.player_num == self.game.turn_index:
                    # If the new hand button pressed, give the player a new hand
                    hand_letters = []
                    for tile in controller.hand_tiles:
                        hand_letters.append(tile.l)
                    player.hand = hand_letters
                    controller.new_hand(self.game.letter_bag)
                    controller.end_turn(self.game.board, self.game.letter_bag)

                elif event.button == 1 and self.AR_button.rect.colliderect(self.cursor.rect) and self.player_num == self.game.turn_index:
                    controller.return_tiles()

            elif event.type == pygame.MOUSEBUTTONUP and isinstance(controller, HumanController):
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
                if isinstance(controller, HumanController):
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
            self.between_turns = True
            self.board_tiles = pygame.sprite.LayeredUpdates()
            for i in range(self.game.board.size):
                for j in range(self.game.board.size):
                    if self.game.board.tile_at((i, j)):
                        self.board_tiles.add(Tile((i, j), self.game.board.tile_at((i, j)), True))

        game_display.fill((255, 255, 255))

        # Draw the UI elements
        self.BoardUI.draw(game_display)


        # Draw the tiles on the board
        self.board_tiles.draw(game_display)

        (player, controller) = self.game.current_player

        pygame.font.init()
        font = pygame.font.Font('assets/ARIALBD.TTF', 28)

        if self.game.end_condition:
            font = pygame.font.Font('assets/ARIALBD.TTF', 50)
            text_surface = font.render("GAME", True, (0, 0, 0))
            game_display.blit(text_surface, (750 + (125 - (text_surface.get_rect().size[0] / 2)), self.piece_size * 2))
            text_surface = font.render("OVER", True, (0, 0, 0))
            game_display.blit(text_surface, (750 + (125 - (text_surface.get_rect().size[0] / 2)), self.piece_size * 3))
            font = pygame.font.Font('assets/ARIALBD.TTF', 35)
            text_surface = font.render("Final Scores:", True, (0, 0, 0))
            game_display.blit(text_surface, (750 + (125 - (text_surface.get_rect().size[0] / 2)), self.piece_size * 5))
            p: Player
            c: Controller
            for i in range(len(self.game.players)):
                (p, c) = self.game.players[i]
                if isinstance(c, AIController):
                    text_surface = font.render("AI: " + str(p.score), True, (0, 0, 0))
                else:
                    text_surface = font.render(c.name + ": " + str(p.score), True, (0, 0, 0))
                game_display.blit(text_surface, (750 + (125-(text_surface.get_rect().size[0]/2)), self.piece_size * (7+(1*i))))
            self.EndUI.draw(game_display)


        elif isinstance(controller, HumanController):

            # Display how many tiles left in the bag
            text_surface = font.render(str(len(self.game.letter_bag.letters)) + " letters left", True, (0, 0, 0))
            game_display.blit(text_surface, (self.piece_size * 15.7, self.piece_size * 0.2))

            p: Player
            c: Controller
            for i in range(len(self.game.players)):
                (p, c) = self.game.players[i]
                if isinstance(c, AIController):
                    text_surface = font.render("AI: " + str(p.score), True, (0, 0, 0))
                else:
                    text_surface = font.render(c.name + ": " + str(p.score), True, (0, 0, 0))
                game_display.blit(text_surface, (self.piece_size * (0.3 + (5 * i)), self.piece_size * 15.2))

            if not self.player_num == self.game.turn_index:
                self.TurnUI.draw(game_display)
                text_surface = font.render("It is now", True, (0, 0, 0))
                game_display.blit(text_surface, (750 + (125-(text_surface.get_rect().size[0]/2)), self.piece_size * 5.8))
                text_surface = font.render(controller.name + "'s", True, (0, 0, 0))
                game_display.blit(text_surface, (750 + (125-(text_surface.get_rect().size[0]/2)), self.piece_size * 6.4))
                text_surface = font.render("turn", True, (0, 0, 0))
                game_display.blit(text_surface, (750 + (125 - (text_surface.get_rect().size[0] / 2)), self.piece_size * 7))

            else:
                self.GameUI.draw(game_display)

                # Display current player's name
                text_surface = font.render(controller.name, True, (0, 0, 0))
                game_display.blit(text_surface, (750 + (125-(text_surface.get_rect().size[0]/2)), self.piece_size * 2))

                controller.hand_tiles.draw(game_display)
                controller.hand_tiles.update(game_display)

        self.game.update()
        # there is a player whose turn it is
        # there is a controller corresponding to that player
        # if that controller is a HumanPlayer, then we should display their hand on the screen and handle drag/drops as a move

        # TODO check if the game has ended. If it has, then display a pop up showing results (winner or tie) of the game

    def next_screen(self) -> 'Screen':
        if self.game.end_condition and self.menu:
            return self.return_screen
        if self.game.end_condition and self.rematch:
            new_game = Game([controller.copy() for _, controller in self.game.players], self.game.word_dict, self.game.computer_science_terms)
            return GameScreen(new_game, self.return_screen)
        return self

