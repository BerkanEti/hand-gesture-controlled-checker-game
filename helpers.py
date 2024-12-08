import pygame
from constants import *

class Dot:
    SIZE = 5

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.SIZE)


def button_hovered(dot):
    if UP_BUTTON[0] <= dot.x <= UP_BUTTON[0] + UP_BUTTON[2] and UP_BUTTON[1] <= dot.y <= UP_BUTTON[1] + UP_BUTTON[3]:
        return "UP"
    elif DOWN_BUTTON[0] <= dot.x <= DOWN_BUTTON[0] + DOWN_BUTTON[2] and DOWN_BUTTON[1] <= dot.y <= DOWN_BUTTON[1] + DOWN_BUTTON[3]:
        return "DOWN"
    elif LEFT_BUTTON[0] <= dot.x <= LEFT_BUTTON[0] + LEFT_BUTTON[2] and LEFT_BUTTON[1] <= dot.y <= LEFT_BUTTON[1] + LEFT_BUTTON[3]:
        return "LEFT"
    elif RIGHT_BUTTON[0] <= dot.x <= RIGHT_BUTTON[0] + RIGHT_BUTTON[2] and RIGHT_BUTTON[1] <= dot.y <= RIGHT_BUTTON[1] + RIGHT_BUTTON[3]:
        return "RIGHT"
    elif SELECT_BUTTON[0] <= dot.x <= SELECT_BUTTON[0] + SELECT_BUTTON[2] and SELECT_BUTTON[1] <= dot.y <= SELECT_BUTTON[1] + SELECT_BUTTON[3]:
        return "SELECT"
    return None


def colorize_button(screen, dot):
    hovered = button_hovered(dot)
    if hovered == "UP":
        pygame.draw.rect(screen, GREEN, UP_BUTTON)
    elif hovered == "DOWN":
        pygame.draw.rect(screen, GREEN, DOWN_BUTTON)
    elif hovered == "LEFT":
        pygame.draw.rect(screen, GREEN, LEFT_BUTTON)
    elif hovered == "RIGHT":
        pygame.draw.rect(screen, GREEN, RIGHT_BUTTON)


def take_average_dist(buffer):
    x_values = [x for x, y in buffer]
    y_values = [y for x, y in buffer]
    x_avg = sum(x_values) / len(x_values)
    y_avg = sum(y_values) / len(y_values)
    avg_dist = (x_avg**2 + y_avg**2) ** 0.5
    return x_avg, y_avg, avg_dist


def calculate_furthest_index(x_avg, y_avg, buffer):
    distances = [((x - x_avg)**2 + (y - y_avg)**2)**0.5 for x, y in buffer]
    return distances.index(max(distances))
