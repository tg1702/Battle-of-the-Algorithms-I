import pygame
import colors
import core.snake as snake

class Player: 
    def __init__(self, id, name, board):
        self.id = id
        self.name = name
        self.color = getattr(colors, f"player{self.id}_color")
        self.border_color = getattr(colors, f"player{self.id}_border_color")
        self.score = 0
        self.board = board  
        self.collided = False     

        position = {"x": 0, "y": board.height/2}
        
        self.snake = snake.Snake(position, "right", self.color, self.border_color)
        
        if self.id == 2: 
            position = {"x": board.width - self.snake.size, "y": board.height/2}
            self.snake.head_position = position
            self.snake.direction = "left"

    def draw_score(self, surface, position):
        """
        Draws the player's name and score on the given surface at the specified position.
        
        :param surface: The surface on which the name and score will be drawn
        :type surface: pygame.Surface
        :param position: A dictionary containing the x and y coordinates of the top-left corner of the name and score
        :type position: dict
        """
        font = pygame.font.SysFont(None, 25)
        
        name_surface = font.render("Player " + str(self.id) + " - " + self.name, True, self.border_color)
        score_surface = font.render(f"Score: {self.score}", True, "white")
        
        surface.blit(name_surface, (position["x"], position["y"]))
        surface.blit(score_surface, (position["x"], position["y"] + 25))