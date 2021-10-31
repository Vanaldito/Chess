import pygame, sys

from pygame.locals import *

from settings import Settings
from game.board import Board
from game.piece import Piece

class ChessGame:
    """ A class to manage the game """

    def __init__(self):
        """ Create a new game instance """
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(self.settings.screen_size)

        self.board = Board(self)
        self.pieces = pygame.sprite.Group()

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

    def _update_screen(self):
        """ Show the screen """
        self.screen.fill((0,0,0))

        self.board.update()
        self.pieces.draw(self.screen)
        
        pygame.display.update()


if __name__ == "__main__":
    ai_game = ChessGame()
    ai_game.run_game()
