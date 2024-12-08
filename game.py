import os
import pygame
from graphic import Graphic
from board import Board
from constants import BLUE, RED

class Game:
    def __init__(self):
        self.graphic = Graphic()
        self.board = Board()
        self.turn = BLUE
        self.selected_piece = None
        self.hop = False
        self.selected_valid_moves = []
        self.hovered_square = (1,5) # (x,y)
       

    def setup(self):
        self.graphic.setup_screen()
    
    def event_loop(self):
        if(self.selected_piece != None) :
            self.selected_valid_moves = self.board.valid_moves(self.selected_piece,self.hop)
        if(self.graphic.press_control) :
            self.graphic.press_control = False
            if(self.board.is_pressed_select(self.graphic.dots[-1])) :
                if self.hop == False:
                    if self.board.location(self.hovered_square).occupant != None and self.board.location(self.hovered_square).occupant.color == self.turn:
                        self.selected_piece = self.hovered_square
                    

                    elif self.selected_piece != None and self.hovered_square in self.board.valid_moves(self.selected_piece):

                        self.board.move_piece(self.selected_piece, self.hovered_square)
                    
                        if self.hovered_square not in self.board.adjacent_squares(self.selected_piece):
                            self.board.remove_piece(((self.selected_piece[0] + self.hovered_square[0]) >> 1, (self.selected_piece[1] + self.hovered_square[1]) >> 1))
                            self.hop = True
                            self.selected_piece = self.hovered_square

                        else:
                            self.other_turn()

                if self.hop == True:					
                    if self.selected_piece != None and self.hovered_square in self.board.valid_moves(self.selected_piece, self.hop):
                        self.board.move_piece(self.selected_piece, self.hovered_square)
                        self.board.remove_piece(((self.selected_piece[0] + self.hovered_square[0]) >> 1, (self.selected_piece[1] + self.hovered_square[1]) >> 1))

                    if self.board.valid_moves(self.hovered_square, self.hop) == []:
                            self.other_turn()

                    else:
                        self.selected_piece = self.hovered_square

                             
             
            else :
                self.hovered_square = self.board.set_hovered_square(self.graphic.dots[-1],self.hovered_square)
                
        
    
    def update(self):
        self.graphic.update_display(self.board,self.selected_valid_moves,self.selected_piece,self.hovered_square)
    
    def terminate(self):
        pygame.quit()
        os._exit(0)
    
    def main(self):
        self.setup()
        while True:
            self.event_loop()
            self.update()
            
    
    def other_turn(self):
        if self.turn == BLUE:
            self.graphic.dot_color = RED
            self.turn = RED
        else:
            self.graphic.dot_color = BLUE
            self.turn = BLUE
        self.selected_piece = None
        self.selected_valid_moves = []
        self.hop = False
        if(self.is_end_game()):
            if(self.turn == BLUE):
                self.graphic.draw_message("Red Wins!")
            else:
                self.graphic.draw_message("Blue Wins!")
        
    def is_end_game(self):
        for x in range(8):
            for y in range(8):
                if self.board.matrix[x][y].occupant != None and self.board.matrix[x][y].occupant.color == self.turn:
                    if self.board.valid_moves((x,y)) != []:
                        return False
        return True
