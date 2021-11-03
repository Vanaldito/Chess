import pygame, sys
import time

from pygame.locals import *

from game.new_game import create_white_pieces, create_black_pieces
from settings import Settings
from game.board import Board
from game.piece import *

class ChessGame:
    """ A class to manage the game """

    def __init__(self):
        """ Create a new game instance """
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(self.settings.screen_size)

        self.board = Board(self)

        self.white_king, self.white_pieces = create_white_pieces(self)
        self.black_king, self.black_pieces = create_black_pieces(self)

        self.turn = "w"
        self.active_piece = None

    def run_game(self):
        """ Init the game loop """
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """ Check the game events """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                self._check_mousebuttondown_events(event)

    def _check_mousebuttondown_events(self, event):
        """ Respond to mousebuttondown events """
        checked_square = (event.pos[0] // self.settings.square_size,
                          event.pos[1] // self.settings.square_size)
        possible_pieces = self.white_pieces if self.turn == "w" else self.black_pieces 
        enemy_pieces = self.white_pieces if self.turn == "b" else self.black_pieces
        if self.active_piece: 
            if checked_square in self.active_piece.possible_movements(self.white_pieces, self.black_pieces):
                self.active_piece.movement(checked_square)
                pygame.sprite.groupcollide(possible_pieces, enemy_pieces, False, True)
                self.turn = "b" if self.turn == "w" else "w"
            self.active_piece = None
        else:
            for piece in possible_pieces:
                if piece.square == checked_square:
                    self.active_piece = piece
                    break

    def _draw_possible_movements(self):
        """ Draw the possible movements if there are a active piece """
        for movement in self.active_piece.possible_movements(self.white_pieces, self.black_pieces):
            pygame.draw.circle(self.screen, self.settings.movement_color, ((movement[0]+0.5)*self.settings.square_size, 
                              (movement[1]+0.5)*self.settings.square_size), self.settings.square_size//3)

    def _update_screen(self):
        """ Show the screen """
        self.screen.fill((0,0,0))

        self.board.update()
        self.white_pieces.draw(self.screen)
        self.black_pieces.draw(self.screen)
        if self.active_piece:
            self._draw_possible_movements()
        
        pygame.display.update()


if __name__ == "__main__":
    ai_game = ChessGame()
    ai_game.run_game()
