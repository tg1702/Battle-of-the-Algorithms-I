import pygame
from config import config

class SnakeSegment:
    """
    Represents a single segment of the snake.
    Each segment is a square on the grid.
    """
    def __init__(self, position, color, border_color):
        self.size = config.GRID_SIZE
        self.position = position
        self.color = color
        self.border_color = border_color

    def draw(self, board):
        """
        Draws the snake segment on the given board surface.
        """
        x = self.position["col"] * self.size
        y = self.position["row"] * self.size
        segment = pygame.Rect(x, y, self.size, self.size)
        pygame.draw.rect(board, self.color, segment)
        pygame.draw.rect(board, self.border_color, segment, 2)

class Snake:
    """
    Represents the snake in the game, including its body segments, direction, and movement.
    """
    def __init__(self, position, direction, color, border_color):
        self.size = config.GRID_SIZE
        self.length = 1
        self.direction = direction
        self.color = color
        self.border_color = border_color
        self.last_position = position.copy()
        self.head_position = position.copy()
        self.tail_position = position.copy()
        self.movement_accumulator = 0
        self.body = [SnakeSegment(position, color, border_color)]
    
    def draw(self, board):
        """
        Draws the snake on the given board surface.
        """
        for segment in self.body:
            segment.draw(board)
            
    def grow(self):
        """
        Increases the length of the snake by adding a new segment at the end of the body.
        """      
        new_segment = SnakeSegment(self.last_position.copy(), self.color, self.border_color)
        self.body.append(new_segment)
        self.length += 1
        
    def move(self):
        """
        Moves the snake one grid unit in its current direction.
        This method is now called discretely based on the AI update interval.
        """
        # Update head position based on current direction
        if self.direction == "left":
            self.head_position["col"] -= 1
        elif self.direction == "right":
            self.head_position["col"] += 1
        elif self.direction == "up":
            self.head_position["row"] -= 1
        elif self.direction == "down":
            self.head_position["row"] += 1
            
        # Update body segments
        # Move all segments to the position of the segment in front of them, starting from the tail
        if self.body:
            # The last segment's current position becomes the new `last_position` for growth
            self.last_position = self.body[-1].position.copy()

            for i in range(len(self.body) - 1, 0, -1):
                self.body[i].position = self.body[i-1].position.copy() # Move segment to previous segment's pos

            # The first body segment (which was previously the head) gets the old head position
            self.body[0].position = self.head_position.copy()

            # Update tail position
            self.tail_position = self.body[-1].position.copy()