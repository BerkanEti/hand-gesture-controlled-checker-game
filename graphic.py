import pygame
import cv2
import mediapipe as mp
from constants import (
    WHITE, BLUE, BLACK, GOLD, HOVERED_COLOR, HIGH, UP_BUTTON, DOWN_BUTTON, LEFT_BUTTON, RIGHT_BUTTON, SELECT_BUTTON
)
from helpers import button_hovered, colorize_button, take_average_dist, calculate_furthest_index, Dot

class Graphic :
    def __init__(self) :
        self.caption = "HCI - MP Controlled Checkers"
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.window_size = 750
        self.board_size = 600
        self.screen = pygame.display.set_mode((self.window_size,self.window_size))
        self.background = pygame.image.load("/resources/board_2.png")
        self.square_size = self.board_size >> 3 # 750 / 8 = 93.75
        self.piece_size = self.square_size >> 1 # 93.75 / 2 = 46.875
        self.alert_message = False


        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.cap = cv2.VideoCapture(0)
        self.buffer = []
        self.dots = []
        self.dot_color = BLUE
        self.pressed = False
        self.press_control = False
        
    
    def setup_screen(self) :
        pygame.init() 
        pygame.display.set_caption(self.caption)
    
    def update_display(self,board,valid_moves,selected_piece,hovered_square) :
        self.screen.blit(self.background,(0,0))
        self.draw_board_pieces(board)
        self.highlight_squares(valid_moves,selected_piece,hovered_square)
        self.update_hover()
    
        if(self.alert_message) :
            self.screen.blit(self.text_surface_obj, self.text_rect_obj)
        pygame.display.update()
        self.clock.tick(self.fps)

    def update_hover(self) :
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_finger_landmark = hand_landmarks.landmark[8]
                x,y = int(index_finger_landmark.x * 750), int(index_finger_landmark.y * 750)
                
                if(len(self.buffer) < 3) :
                    self.buffer.append([x,y])
                    continue
                
                x_avg,y_avg,avg_dist = take_average_dist(self.buffer)
                furthest_index = calculate_furthest_index(x,y,self.buffer)
                self.buffer.pop(furthest_index)  
                self.buffer.append([x,y])

                self.dots.append(Dot(x_avg,y_avg,self.dot_color))

                if(len(self.dots) > 10) :
                    self.dots.pop(0)
         
                colorize_button(self.screen,self.dots[-1])  

                for dot in self.dots:
                    dot.draw(self.screen)

                thumb = hand_landmarks.landmark[4]
                x_thumb,y_thumb = int(thumb.x * 750), int(thumb.y * 750)
                forefinger = hand_landmarks.landmark[8]
                x_forefinger,y_forefinger = int(forefinger.x * 750), int(forefinger.y * 750)

                press_distance = ((x_forefinger - x_thumb)**2 + (y_forefinger - y_thumb)**2)**0.5
                press_threshold = 50
            
                if press_distance < press_threshold:
                    if self.pressed:
                        continue
                    self.pressed = True
                    self.press_control = True

                else:
                    self.pressed = False


    def draw_board_square(self,x,y,color) :
        pygame.draw.rect(self.screen,color,(x*self.square_size,y*self.square_size,self.square_size,self.square_size))

    def draw_board_pieces(self,board) :
        for x in range(8):
            for y in range(8) :
                if board.matrix[x][y].occupant != None:
                    pygame.draw.circle(self.screen,board.matrix[x][y].occupant.color,self.pixel_coords((x,y)),self.piece_size)
                    if board.matrix[x][y].occupant.king == True:
                        pygame.draw.circle(self.screen,GOLD,self.pixel_coords((x,y)),int (self.piece_size / 1.7), self.piece_size >> 2)
	
    def pixel_coords(self,board_coords) :
        return (board_coords[0] * self.square_size + self.piece_size, board_coords[1] * self.square_size + self.piece_size)
    
    def board_coords(self,coords) :
        return (coords[0] // self.square_size, coords[1] // self.square_size)
    
    def highlight_squares(self,squares,original,hovered_square) :
        pygame.draw.rect(self.screen,HOVERED_COLOR,(hovered_square[0] * self.square_size,hovered_square[1] * self.square_size,self.square_size,self.square_size))
        for square in squares :
            pygame.draw.rect(self.screen,HIGH,(square[0]*self.square_size,square[1]*self.square_size,self.square_size,self.square_size))
        if(original != None) :
            pygame.draw.rect(self.screen, HIGH, (original[0] * self.square_size, original[1] * self.square_size, self.square_size, self.square_size))

    def draw_message(self,message) :
        self.alert_message = True
        self.font_obj = pygame.font.Font('freesansbold.ttf', 32)
        self.text_surface_obj = self.font_obj.render(message, True, WHITE, BLACK)
        self.text_rect_obj = self.text_surface_obj.get_rect()
        self.text_rect_obj.center = (self.window_size // 2, self.window_size // 2)