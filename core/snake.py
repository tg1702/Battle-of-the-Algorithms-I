import pygame
from config import config

class Snake:
    def __init__(self, position, direction, color, border_color):
        self.size = config.GRID_SIZE
        self.length = 1
        self.direction = direction
        self.color = color
        self.border_color = border_color
        self.position = position
        self.movement_accumulator = 0
    
    def draw(self, board):
        """
        Draws the snake on the given board surface.

        :param board: The surface on which the snake will be drawn
        :type board: pygame.Surface
        """
        snake = pygame.Rect(self.position["x"], self.position["y"], self.size, self.size)
        pygame.draw.rect(board, self.color, snake)
        pygame.draw.rect(board, self.border_color, snake, 2)
        
    def move(self, delta_time):    
        steps = 0
        
        self.movement_accumulator += ((delta_time / 1000) * config.GRID_SIZE * config.PLAYER_SPEED)

        if self.movement_accumulator >= config.GRID_SIZE:
            steps = self.movement_accumulator // config.GRID_SIZE
            self.movement_accumulator %= config.GRID_SIZE  # Preserve leftover movement
            
        match self.direction:
            case "left":
                self.position["x"] -= config.GRID_SIZE * steps
            case "right":
                self.position["x"] += config.GRID_SIZE * steps
            case "up":
                self.position["y"] -= config.GRID_SIZE * steps
            case "down":
                self.position["y"] += config.GRID_SIZE * steps
                
        self.position["x"] = round(self.position["x"])
        self.position["y"] = round(self.position["y"])

        