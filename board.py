import pygame
import colors

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = pygame.Surface((self.width, self.height))
        self.border = pygame.Surface((self.width + 10, self.height + 10))
    
    def draw(self, screen):
        board_background = pygame.image.load("assets/board.png")
        board_background = pygame.transform.scale(board_background, (self.width, self.height))

        self.border.fill(colors.border_color)
        
        screen.blit(self.border, (145, 165))
        screen.blit(self.board, (150, 170))
        self.board.blit(board_background, (0, 0))
        