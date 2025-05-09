import pygame
from config import config

class SnakeSegment:
    def __init__(self, position, color, border_color):
        self.size = config.GRID_SIZE
        self.position = position
        self.color = color
        self.border_color = border_color

    def draw(self, board):
        """
        Draws the snake segment on the given board surface.
        """
        segment = pygame.Rect(self.position["x"], self.position["y"], self.size, self.size)
        pygame.draw.rect(board, self.color, segment)
        pygame.draw.rect(board, self.border_color, segment, 2)

class Snake:
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
        
    def move(self, delta_time):   
        """
        Moves the snake in the current direction based on the elapsed time since the last frame.
        """
        steps = 0

        self.movement_accumulator += ((delta_time / 1000) * config.GRID_SIZE * config.PLAYER_SPEED)

        if self.movement_accumulator >= config.GRID_SIZE:
            steps = self.movement_accumulator // config.GRID_SIZE
            self.movement_accumulator %= config.GRID_SIZE  # Preserve leftover movement

            previous_head_position = self.head_position.copy()

            match self.direction:
                case "left":
                    self.head_position["x"] -= config.GRID_SIZE * steps
                case "right":
                    self.head_position["x"] += config.GRID_SIZE * steps
                case "up":
                    self.head_position["y"] -= config.GRID_SIZE * steps
                case "down":
                    self.head_position["y"] += config.GRID_SIZE * steps

            self.head_position["x"] = round(self.head_position["x"])
            self.head_position["y"] = round(self.head_position["y"])
            self.body[0].position = self.head_position.copy()

            previous_segment_position = previous_head_position.copy()
            for i in range(1, len(self.body)):
                current_segment_position = self.body[i].position.copy()
                self.body[i].position = previous_segment_position
                previous_segment_position = current_segment_position

            if self.body:
                self.last_position = previous_segment_position.copy() 
                self.tail_position = self.body[-1].position.copy()
