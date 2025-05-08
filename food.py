import random
import pygame
import colors

class Food:
    def __init__(self, board):
        self.size = 15
        self.x = random.randint(0, (board.width // self.size) - 1) * self.size
        self.y = random.randint(0, (board.height // self.size) - 1) * self.size
        self.hit = False
        
    def draw(self, board):
        """
        Draws the food on the given board surface.

        :param board: The surface on which the food will be drawn
        :type board: pygame.Surface
        """
        food = pygame.Rect(self.x, self.y, self.size, self.size)
        leaf = pygame.Rect(self.x  + self.size/2 - 2, self.y - 4, 4.5, 4)
        pygame.draw.rect(board.board, colors.food_color, food)
        pygame.draw.rect(board.board, colors.food_leaf_color, leaf)