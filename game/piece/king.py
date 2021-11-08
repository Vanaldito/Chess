from .piece import Piece

from .rook import Rook

class King(Piece):
    """ A class to representing a king """
    
    def __init__(self, ai_game, square, color):
        super().__init__(ai_game, square, f"{color}K")
        self.color = color

    def theoretical_movements(self, white_pieces, black_pieces):
        """ Return the theoretical movements of the king """
        dirs = [(1,0),(1,1),(0,1),(-1,0),(0,-1),(1,-1),(-1,-1),(-1,1)]

        friendly_pieces = white_pieces if self.color == "w" else black_pieces
        enemy_pieces = white_pieces if self.color == "b" else black_pieces

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
        #movements.extend(self._castle(white_pieces, black_pieces))
        return movements

#    def _castle(self, white_pieces, black_pieces):
#        movements = []
#        if not self.already_moved:
#            movements.append(self.short_castle(white_pieces, black_pieces))
#            movements.append(self.large_castle(white_pieces, black_pieces))
#        return movements
#
#    def short_castle(self, white_pieces, black_pieces):
#        friendly_pieces = white_pieces if self.color == "w" else black_pieces
#        enemy_pieces = white_pieces if self.color == "b" else black_pieces
#
#        movements = []
#        if not self.check(white_pieces, black_pieces):
#            for piece in friendly_pieces:
#                if (type(piece) is Rook and not piece.already_moved and 
#                        piece.square[0] - self.square[0] == 2):
#                    real_square = self.square
#                    self.movements
#
    def check(self, white_pieces, black_pieces):
        """ Check if the king is in check """
        enemy_pieces = white_pieces if self.color == "b" else black_pieces 
        for piece in enemy_pieces:
            if self.square in piece.theoretical_movements(white_pieces, black_pieces):
                return True
        return False
