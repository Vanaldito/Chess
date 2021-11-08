import pygame
from pygame.sprite import Sprite

class Piece(Sprite):
    """ A class parent for pieces """

    def __init__(self, ai_game, square, image):
        """ Create a new piece """
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.square = square

        self.image = pygame.image.load(f"Assets/{image}.png")
        self.image = pygame.transform.scale(self.image, (self.settings.square_size,
                                                         self.settings.square_size))
        self.rect = self.image.get_rect()
        self.movement(self.square)

        self.already_moved = False
        self.active = False

    def movement(self, destination_square):
        """ Move the piece """
        self.rect.topleft = (destination_square[0] * self.settings.square_size,
                             destination_square[1] * self.settings.square_size) 
        self.square = destination_square

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the piece """
        pass

    def possible_movements(self, white_pieces, black_pieces, king):
        """ Return the possible movements of the piece """
        real_square = self.square
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        possible_movements = []
        for movement in self.theoretical_movements(white_pieces, black_pieces):
            self.movement(movement)

            # If there are a capture delete the piece temporarily
            capture = pygame.sprite.spritecollideany(self, enemy_pieces)
            if capture:
                enemy_pieces.remove(capture)

            if not king.check(white_pieces, black_pieces):
                possible_movements.append(movement)

            if capture:
                enemy_pieces.add(capture)
            self.movement(real_square)
        return possible_movements


class Pawn(Piece):
    """ A class to representing a pawn """

    def __init__(self, ai_game, square, color):
        """ Create a new pawn """
        super().__init__(ai_game, square, f"{color}p")
        self.color = color
        self.direction = 1 if self.color == "b" else -1
        self.en_passant = False

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the pawn """
        movements = []
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        if self._two_squares(white_pieces, black_pieces):
            movements.append((self.square[0], self.square[1]+self.direction))
            movements.append((self.square[0], self.square[1]+2*self.direction))
        elif self._one_square(white_pieces, black_pieces):
            movements.append((self.square[0], self.square[1]+self.direction))
        movements.extend(self._captures(enemy_pieces))
        movements.extend(self.move_en_passant(enemy_pieces))
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

    def _captures(self, enemy_pieces):
        """ Return the possible captures """
        moves = []
        for piece in enemy_pieces.sprites():
            if piece.square == (self.square[0]+1, self.square[1]+self.direction):
                moves.append(piece.square)
            if piece.square == (self.square[0]-1, self.square[1]+self.direction):
                moves.append(piece.square)
        return moves

    def promotion(self, pieces):
        """ Promotion the pawn """
        if self.square[1] == int(3.5 + self.direction * 3.5):
            pieces.add(Queen(self.ai_game, self.square, self.color))
            pieces.remove(self)

    def move_en_passant(self, enemy_pieces):
        movements = []
        for piece in enemy_pieces:
            if (type(piece) is Pawn and abs(piece.square[0] - self.square[0]) == 1 
                    and piece.square[1] == self.square[1]) and piece.en_passant:
                movements.append((piece.square[0], piece.square[1]+self.direction))
        return movements


class Rook(Piece):
    """ A class to representing a rook """

    def __init__(self, ai_game, square, color):
        """ Create a new rook """
        super().__init__(ai_game, square, f"{color}R")
        self.color = color

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the rook """
        dirs = [(1,0),(0,-1),(-1,0),(0,1)]
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        friendly_pieces = black_pieces if self.color == "b" else white_pieces
        movements = []
        for direction in dirs:
            temporary_square = self.square 
            flag = True # If the flag is true we continue moving the piece along the column, row or diagonal
            while flag:
                temporary_square = (temporary_square[0]+direction[0], 
                                    temporary_square[1]+direction[1])
                for piece in enemy_pieces:
                    if piece.square == temporary_square:
                        movements.append(temporary_square)
                        flag = False
                for piece in friendly_pieces:
                    if piece.square == temporary_square:
                        flag = False
                if (temporary_square[0] < 0 or temporary_square[0] > 7 or
                        temporary_square[1] < 0 or temporary_square[1] > 7):
                    flag = False
                if flag:
                    movements.append(temporary_square)
        return movements


class Knight(Piece):
    """ A class to representing a knight """

    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}N")
        self.color = color

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the knight """
        dirs = [(2,1),(2,-1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2)]
        friendly_pieces = white_pieces if self.color == "w" else black_pieces
        movements = []
        for direction in dirs:
            flag = True # If flag is true, the square is available
            temporary_square = (self.square[0]+direction[0],
                                self.square[1]+direction[1])
            for piece in friendly_pieces:
                if piece.square == temporary_square:
                    flag = False
            if (temporary_square[0] < 0 or temporary_square[0] > 7 or
                    temporary_square[1] < 0 or temporary_square[1] > 7):
                flag = False
            if flag:
                movements.append(temporary_square)
        return movements


class Bishop(Piece):
    """ A class to representing a bishop """

    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}B")
        self.color = color

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the bishop """
        dirs = [(1,1),(1,-1),(-1,-1),(-1,1)]
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        friendly_pieces = black_pieces if self.color == "b" else white_pieces
        movements = []
        for direction in dirs:
            temporary_square = self.square 
            flag = True
            while flag:
                temporary_square = (temporary_square[0]+direction[0], 
                                    temporary_square[1]+direction[1])
                for piece in enemy_pieces:
                    if piece.square == temporary_square:
                        movements.append(temporary_square)
                        flag = False
                for piece in friendly_pieces:
                    if piece.square == temporary_square:
                        flag = False
                if (temporary_square[0] < 0 or temporary_square[0] > 7 or
                        temporary_square[1] < 0 or temporary_square[1] > 7):
                    flag = False
                if flag:
                    movements.append(temporary_square)
        return movements


class Queen(Piece):
    """ A class to representing a queen """

    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}Q")
        self.color = color

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the queen """
        dirs = [(1,0),(1,1),(0,1),(-1,0),(0,-1),(1,-1),(-1,-1),(-1,1)]
        enemy_pieces = white_pieces if self.color == "b" else black_pieces
        friendly_pieces = black_pieces if self.color == "b" else white_pieces
        movements = []
        for direction in dirs:
            temporary_square = self.square 
            flag = True
            while flag:
                temporary_square = (temporary_square[0]+direction[0], 
                                    temporary_square[1]+direction[1])
                for piece in enemy_pieces:
                    if piece.square == temporary_square:
                        movements.append(temporary_square)
                        flag = False
                        break
                for piece in friendly_pieces:
                    if piece.square == temporary_square:
                        flag = False
                        break
                if (temporary_square[0] < 0 or temporary_square[0] > 7 or
                        temporary_square[1] < 0 or temporary_square[1] > 7):
                    flag = False
                if flag:
                    movements.append(temporary_square)
        return movements


class King(Piece):
    """ A class to representing a king """
    
    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}K")
        self.color = color

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the king """
        dirs = [(1,0),(1,1),(0,1),(-1,0),(0,-1),(1,-1),(-1,-1),(-1,1)]
        friendly_pieces = white_pieces if self.color == "w" else black_pieces
        movements = []
        for direction in dirs:
            flag = True # If flag is true, the square is available
            temporary_square = (self.square[0]+direction[0],
                                self.square[1]+direction[1])
            for piece in friendly_pieces:
                if piece.square == temporary_square:
                    flag = False
            if (temporary_square[0] < 0 or temporary_square[0] > 7 or
                temporary_square[1] < 0 or temporary_square[1] > 7):
                flag = False
            if flag:
                movements.append(temporary_square)
        return movements

    def check(self, white_pieces, black_pieces):
        """ Check if the king is in check """
        enemy_pieces = white_pieces if self.color == "b" else black_pieces 
        for piece in enemy_pieces:
            if self.square in piece.theoretical_movements(white_pieces, black_pieces):
                return True
        return False
