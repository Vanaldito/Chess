import pygame
from pygame.sprite import Sprite

class Piece(Sprite):
    """ A class parent for pieces """

    def __init__(self, ai_game, square, image):
        """ Create a new piece """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.square = square

        self.image = pygame.image.load(f"Assets/{image}.png")
        self.image = pygame.transform.scale(self.image, (self.settings.square_size,
                                                         self.settings.square_size))
        self.rect = self.image.get_rect()
        self.movement(self.square)

        self.already_moved = False

    def movement(self, destination_square):
        """ Move the piece """
        self.rect.topleft = (destination_square[0] * self.settings.square_size,
                             destination_square[1] * self.settings.square_size) 
        self.square = destination_square
        self.already_moved = True

    def possible_movements(self):
        """ Return the movements of the piece """
        pass


class Pawn(Piece):
    """ A class to representing a pawn """

    def __init__(self, ai_game, square, color):
        """ Create a new pawn """
        super().__init__(ai_game, square, f"{color}p")
        self.color = color
        self.direction = 1 if self.color == "b" else -1
        self.en_passant = False

    def possible_movements(self, white_pieces, black_pieces):
        """ Return the movements of the pawn """
        movements = []
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        if self._two_squares(white_pieces, black_pieces):
            movements.append((self.square[0], self.square[1]+self.direction))
            movements.append((self.square[0], self.square[1]+2*self.direction))
        elif self._one_square(self, white_pieces, black_pieces):
            movements.append((self.square[0], self.square[1]+self.direction))
        return movements

    def _one_square(self, white_pieces, black_pieces):
        """ Check if the pawn can move one square """
        for piece in white_pieces.sprites():
            if piece.square == (self.square[0], self.square[1]+self.direction):
                return False
        for piece in black_pieces.sprites():
            if piece.square == (self.square[0], self.square[1]+self.direction):
                return False
        return True

    def _two_squares(self, white_pieces, black_pieces):
        """ Check if the pawn can move two squares """
        if self.already_moved or not self._one_square(white_pieces, black_pieces):
            return False
        for piece in white_pieces.sprites():
            if piece.square == (self.square[0], self.square[1]+2*self.direction):
                return False
        for piece in black_pieces.sprites():
            if piece.square == (self.square[0], self.square[1]+2*self.direction):
                return False
        return True

    def capture(self, enemy_pieces):
        """ Return the possible captures """


class Rook(Piece):
    """ A class to representing a rook """

    def __init__(self, ai_game, square, color):
        """ Create a new rook """
        super().__init__(ai_game, square, f"{color}R")


class Knight(Piece):
    """ A class to representing a knight """

    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}N")


class Bishop(Piece):
    """ A class to representing a bishop """

    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}B")


class Queen(Piece):
    """ A class to representing a queen """

    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}Q")


class King(Piece):
    """ A class to representing a king """
    
    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}K")
