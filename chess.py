import pygame, sys
import time

from pygame.locals import *

from new_game import create_white_pieces, create_black_pieces
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

        self.white_pieces = create_white_pieces(self)
        self.black_pieces = create_black_pieces(self)

    def run_game(self):
        """ Init the game loop """
        while True:
            self._check_events()
            self._update_screen()
            init = time.time()
            for piece in self.white_pieces:
                piece.possible_movements(self.white_pieces, self.black_pieces)
            end = time.time()
            print(end-init)

    def _check_events(self):
        """ Check the game events """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def _update_screen(self):
        """ Show the screen """
        self.screen.fill((0,0,0))

        self.board.update()
        self.white_pieces.draw(self.screen)
        self.black_pieces.draw(self.screen)
        
        pygame.display.update()


if __name__ == "__main__":
    ai_game = ChessGame()
    ai_game.run_game()
