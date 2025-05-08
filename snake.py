import pygame

class Snake:
    def __init__(self, position, color, border_color):
        self.color = color
        self.border_color = border_color
        self.position = position
        self.size = 15
        self.length = 1
    
    def draw(self, board):
        """
        Draws the snake on the given board surface.

        :param board: The surface on which the snake will be drawn
        :type board: pygame.Surface
        """
        
        snake = pygame.Rect(self.position["x"], self.position["y"], self.size, self.size)
        pygame.draw.rect(board, self.color, snake)
        pygame.draw.rect(board, self.border_color, snake, 2)
        