import random
import pygame
import os
from config import config

class Obstacle:
    """
    Represents an obstacle composed of repeating spike images.
    Orientation can be horizontal or vertical, and length varies from 3 to 5 grid units.
    """
    def __init__(self):
        self.size = config.GRID_SIZE
        self.orientation = random.choice(["horizontal", "vertical"])
        self.length = random.randint(4, 6)

        if self.orientation == "horizontal":
            self.width = self.size * self.length
            self.height = self.size
        else:
            self.width = self.size
            self.height = self.size * self.length

        max_x = (config.BOARD_WIDTH - self.width) // self.size
        max_y = (config.BOARD_HEIGHT - self.height) // self.size
        
        self.x = random.randint(0, max_x) * self.size
        self.y = random.randint(0, max_y) * self.size

        # Load and scale the tile image (1 grid size)
        image_path = os.path.join("assets", "spike.png")
        self.tile_image = pygame.image.load(image_path)
        self.tile_image = pygame.transform.scale(self.tile_image, (self.size, self.size))

    def draw(self, board):
        """
        Draws the obstacle as a row/column of repeated spike tiles.
        """
        for i in range(self.length):
            if self.orientation == "horizontal":
                tile_x = self.x + i * self.size
                tile_y = self.y
            else:
                tile_x = self.x
                tile_y = self.y + i * self.size
                
            board.board.blit(self.tile_image, (tile_x, tile_y))

    def get_occupied_positions(self):
        """
        Returns all grid positions occupied by this obstacle.
        """
        positions = []
        
        for i in range(self.length):
            if self.orientation == "horizontal":
                grid_x = self.x // self.size
                grid_y = (self.y + i * self.size) // self.size
            else:
                grid_x = (self.x + i * self.size) // self.size
                grid_y = self.y // self.size
            positions.append((grid_x, grid_y))
            
        return positions
