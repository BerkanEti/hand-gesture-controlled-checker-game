from constants import WHITE, BLACK, RED, BLUE, NORTHWEST, NORTHEAST, SOUTHWEST, SOUTHEAST
from piece import Square, Piece
from helpers import button_hovered

class Board:
    def __init__(self):
          self.matrix = self.new_board()
		  
    def new_board(self):
        matrix = [[None] * 8 for i in range(8)]
        
        for x in range(8) :
             for y in range(8) :
                    if (x % 2 != 0) and (y % 2 == 0) :
                        matrix[y][x] = Square(WHITE)
                    elif (x % 2 != 0) and (y % 2 != 0):
                        matrix[y][x] = Square(BLACK)
                    elif (x % 2 == 0) and (y % 2 != 0):
                        matrix[y][x] = Square(WHITE)
                    elif (x % 2 == 0) and (y % 2 == 0): 
                        matrix[y][x] = Square(BLACK)

        for x in range(8):
            for y in range(3):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(RED)
            for y in range(5, 8):
                if matrix[x][y].color == BLACK:
                    matrix[x][y].occupant = Piece(BLUE)
        # matrix[1][5].occupant = Piece(BLUE)
        # matrix[2][4].occupant = Piece(RED)
        # matrix[4][2].occupant = Piece(RED)


        return matrix
            
        
    def board_str(self,board) :
         board_str = [None * 8] * 8
         for x in range(8) :
             for y in range(8) :
                    if board[x][y].color == "WHITE" :
                        board_str[x][y] = "WHITE"
                    else :
                        board_str[x][y] = "BLACK"
    
    def relative_coords(self, direction,coord):
        x = coord[0]
        y = coord[1]
        if direction == NORTHWEST:
            return (x - 1, y - 1)
        elif direction == NORTHEAST:
            return (x + 1, y - 1)
        elif direction == SOUTHWEST:
            return (x - 1, y + 1)
        elif direction == SOUTHEAST:
            return (x + 1, y + 1)
        else : 
            
            return 0

    def adjacent_squares(self,coord):
        x = coord[0]
        y = coord[1]
        return [self.relative_coords(NORTHWEST,coord), self.relative_coords(NORTHEAST,coord), self.relative_coords(SOUTHWEST,coord), self.relative_coords(SOUTHEAST,coord)
                ]

    def location(self,coord):
        x = coord[0]
        y = coord[1]
        return self.matrix[x][y]

    def blind_valid_moves(self,coord):
        x = coord[0]
        y = coord[1]
        
        
        if(self.matrix[x][y].occupant != None):
            
            if self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == BLUE:
                
                blind_valids = [self.relative_coords(NORTHWEST, (x,y)), self.relative_coords(NORTHEAST, (x,y))]
                
            elif self.matrix[x][y].occupant.king == False and self.matrix[x][y].occupant.color == RED:
                
                blind_valids = [self.relative_coords(SOUTHWEST, (x,y)), self.relative_coords(SOUTHEAST, (x,y))]

            else:
                
                blind_valids = [self.relative_coords(NORTHWEST, (x,y)), self.relative_coords(NORTHEAST, (x,y)), self.relative_coords(SOUTHWEST, (x,y)), self.relative_coords(SOUTHEAST, (x,y))]
        else :
             blind_valids = []
        
        return blind_valids
    
    def valid_moves(self, pixel, hop = False):
        x = pixel[0]
        y = pixel[1]
        blind_valid_moves = self.blind_valid_moves((x,y)) 
        valid_moves = []

        if hop == False:
            for move in blind_valid_moves:
                if hop == False:
                    
                    
                    if self.on_board(move):
                        if self.location(move).occupant == None:
                            valid_moves.append(move)

                        elif self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
                            valid_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        else: # hop == True
            for move in blind_valid_moves:
                if self.on_board(move) and self.location(move).occupant != None:
                    if self.location(move).occupant.color != self.location((x,y)).occupant.color and self.on_board((move[0] + (move[0] - x), move[1] + (move[1] - y))) and self.location((move[0] + (move[0] - x), move[1] + (move[1] - y))).occupant == None: # is this location filled by an enemy piece?
                        valid_moves.append((move[0] + (move[0] - x), move[1] + (move[1] - y)))

        return valid_moves

    def remove_piece(self, coord):
        self.matrix[coord[0]][coord[1]].occupant = None
    
    def move_piece(self, start, end):
        self.matrix[end[0]][end[1]].occupant = self.matrix[start[0]][start[1]].occupant
        self.matrix[start[0]][start[1]].occupant = None
        self.king(end)
    
    def is_end_square(self, coord):
        if coord[1] == 0 or coord[1] == 7:
            return True
        return False
    
    def on_board(self, coord):
        if coord[0] >= 0 and coord[0] <= 7 and coord[1] >= 0 and coord[1] <= 7:
            return True
        return False
    
    def king(self, coord):
        if(self.matrix[coord[0]][coord[1]].occupant != None):
            if(self.matrix[coord[0]][coord[1]].occupant.color == RED and coord[1] == 7):
                self.matrix[coord[0]][coord[1]].occupant.king = True
            elif(self.matrix[coord[0]][coord[1]].occupant.color == BLUE and coord[1] == 0):
                self.matrix[coord[0]][coord[1]].occupant.king = True

    def is_pressed_select(self,dot) :
        hovered = button_hovered(dot)
        if(hovered == "SELECT") :
            return True
        return False
    
    def set_hovered_square(self,dot,hovered_square) :
        hovered = button_hovered(dot)
        temp = hovered_square
        if(hovered == "UP") :
            hovered_square = (hovered_square[0], hovered_square[1] - 1)
        elif(hovered == "DOWN") :
            hovered_square = (hovered_square[0], hovered_square[1] + 1)
        elif(hovered == "LEFT") :
            hovered_square = (hovered_square[0] - 1, hovered_square[1])
        elif(hovered == "RIGHT") :
            hovered_square = (hovered_square[0] + 1, hovered_square[1])
    
        if(self.on_board(hovered_square) == False) :
            hovered_square = temp
        return hovered_square