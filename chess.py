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

        self.clock = pygame.time.Clock()

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

            self.clock.tick(self.settings.FPS)

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
                self._move(friendly_pieces, enemy_pieces, checked_square)
            else:
                active_piece = None
                for piece in friendly_pieces:
                    if piece.square == checked_square:
                        # Desactive the piece if press it two times
                        if piece == self.active_piece:
                            active_piece = None
                        # If press other piece, change the active piece
                        else:
                            active_piece = piece
                        break
                self.active_piece = active_piece
        else:
            for piece in friendly_pieces:
                if piece.square == checked_square:
                    self.active_piece = piece
                    break

    def _move(self, friendly_pieces, enemy_pieces, square):
        """ Move the active piece, realize the captures and change of turn """
        # The next lines is for the en passant capture 

        # Capture the piece en passant
        if type(self.active_piece) is Pawn and square in self.active_piece.move_en_passant(enemy_pieces):
            self.active_piece.movement((square[0], self.active_piece.square[1]))
            pygame.sprite.groupcollide(friendly_pieces, enemy_pieces, False, True)

        # The en passant capture only be made on the movement inmediately after of the enemy pawn 
        # makes the double-step move
        for piece in enemy_pieces:
            if type(piece) is Pawn:
                piece.en_passant = False

        if type(self.active_piece) is Pawn:
            if square[1] == self.active_piece.square[1] + 2*self.active_piece.direction:
                self.active_piece.en_passant = True

        self.active_piece.movement(square)
        self.active_piece.already_moved = True

        # Check the captures
        pygame.sprite.groupcollide(friendly_pieces, enemy_pieces, False, True)

        if type(self.active_piece) is Pawn:
            # The pawn is turned into a queen
            self.active_piece.promotion(friendly_pieces)

        self.turn = "b" if self.turn == "w" else "w"

        self.active_piece = None

        king = self.white_king if self.turn == "w" else self.black_king
        self._check_checkmate(self.turn, enemy_pieces, king)

    def _check_checkmate(self, color, pieces, king):
        """ Check if the king is in checkmate """
        for piece in pieces:
            if piece.possible_movements(self.white_pieces, self.black_pieces, king):
                return None

        if king.check(self.white_pieces, self.black_pieces):
            print(f"{color} lose")
            pygame.quit()
            sys.exit()

    def _draw_possible_movements(self):
        """ Draw circles in the possible movements if there are a active piece """
        king = self.white_king if self.turn == "w" else self.black_king

        # Draw a rectangle in the active piece square
        pygame.draw.rect(self.screen, self.settings.active_color, (self.active_piece.square[0]*self.settings.square_size,
                         self.active_piece.square[1]*self.settings.square_size, self.settings.square_size, 
                         self.settings.square_size), 5, 1)       

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
