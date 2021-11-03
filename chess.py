import pygame, sys

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
        pygame.display.set_caption("Chess Game")

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

        friendly_pieces = self.white_pieces if self.turn == "w" else self.black_pieces 
        enemy_pieces = self.white_pieces if self.turn == "b" else self.black_pieces
        king = self.white_king if self.turn == "w" else self.black_king

        if self.active_piece: 
            if checked_square in self.active_piece.possible_movements(self.white_pieces, self.black_pieces, king):
                self.active_piece.movement(checked_square)
                self.active_piece.already_moved = True

                # Check the captures
                pygame.sprite.groupcollide(friendly_pieces, enemy_pieces, False, True)

                self.turn = "b" if self.turn == "w" else "w"
                self.active_piece = None
            else:
                self.active_piece = None
                for piece in friendly_pieces:
                    if piece.square == checked_square:
                        self.active_piece = piece
                        break
        else:
            for piece in friendly_pieces:
                if piece.square == checked_square:
                    self.active_piece = piece
                    break

    def _draw_possible_movements(self):
        """ Draw circles in the possible movements if there are a active piece """
        king = self.white_king if self.turn == "w" else self.black_king

        pygame.draw.rect(self.screen, self.settings.active_color, (self.active_piece.square[0]*self.settings.square_size,
                         self.active_piece.square[1]*self.settings.square_size, self.settings.square_size, 
                         self.settings.square_size), 5)       

        for movement in self.active_piece.possible_movements(self.white_pieces, self.black_pieces, king):
            pygame.draw.circle(self.screen, self.settings.movement_color, ((movement[0]+0.5)*self.settings.square_size, 
                              (movement[1]+0.5)*self.settings.square_size), self.settings.square_size//3)
        
    def _update_screen(self):
        """ Show the screen """
        self.screen.fill((0,0,0))

        self.board.update()

        if self.active_piece:
            self._draw_possible_movements()

        self.white_pieces.draw(self.screen)
        self.black_pieces.draw(self.screen)

        pygame.display.update()


if __name__ == "__main__":
    ai_game = ChessGame()
    ai_game.run_game()
