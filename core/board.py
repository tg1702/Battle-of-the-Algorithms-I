import pygame
import config.colors as colors
from config import config

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = pygame.Surface((self.width, self.height))
        self.border = pygame.Surface((self.width + 10, self.height + 10))
        self.rows = height // config.GRID_SIZE
        self.cols = width // config.GRID_SIZE
    
    def draw(self, screen):
        """
        Draws the board and its border on the given screen surface, loading and scaling the background image.

        :param screen: The surface on which the board and border will be drawn
        :type screen: pygame.Surface
        """
        board_background = pygame.image.load("assets/board.png")
        board_background = pygame.transform.scale(board_background, (self.width, self.height))

        self.border.fill(colors.border_color)
        
        screen.blit(self.border, (145, 165))
        screen.blit(self.board, (150, 170))
        self.board.blit(board_background, (0, 0))

    