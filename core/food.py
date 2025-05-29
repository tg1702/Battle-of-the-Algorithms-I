import random
import pygame
import config.colors as colors
from config import config

class Food:
    """
    Represents the food in the game.
    """
    def __init__(self):
        self.size = config.GRID_SIZE
        self.grid_row = random.randint(0, (config.BOARD_HEIGHT // self.size) - 1)
        self.grid_col = random.randint(0, (config.BOARD_WIDTH // self.size) - 1)
        self.x = self.grid_col * self.size  
        self.y = self.grid_row * self.size  
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