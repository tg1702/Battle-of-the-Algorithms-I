import pygame
import config.colors as colors
import core.snake as snake
import importlib.util
import sys

class Player: 
    """
    Represents a player in the game, including their snake and score.
    """
    def __init__(self, id, board, controller_path):
        self.id = id
        self.name = ""
        self.color = getattr(colors, f"player{self.id}_color")
        self.border_color = getattr(colors, f"player{self.id}_border_color")
        self.score = 0
        self.board = board  
        self.collided = False     

        position = {"x": 0, "y": board.height//2}
        
        self.snake = snake.Snake(position, "right", self.color, self.border_color)
        
        if self.id == 2: 
            position = {"x": board.width - self.snake.size, "y": board.height//2}
            self.snake.head_position = position
            self.snake.direction = "left"
            
        self.controller = self._load_controller(controller_path)
        self.name = self.controller.set_player_name()
        
    def _load_controller(self, controller_module_name):
        """Loads the player's controller file."""
        try:
            module = importlib.import_module(controller_module_name)
            if not hasattr(module, 'get_next_move') or not callable(module.get_next_move):
                raise AttributeError(f"Controller module {controller_module_name} must contain a function named 'get_next_move'.")
            if not hasattr(module, 'set_player_name') or not callable(module.set_player_name):
                raise AttributeError(f"Controller module {controller_module_name} must contain a function named 'set_player_name'.")
            return module
        except ModuleNotFoundError:
            raise FileNotFoundError(f"Could not find controller module: {controller_module_name}. Ensure '{controller_module_name}.py' exists in a directory accessible by Python's module search path (e.g., the 'controllers' directory).")
        except AttributeError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Error loading controller module {controller_module_name}: {e}")

    def draw_score(self, surface, position):
        """
        Draws the player's name and score on the given surface at the specified position.
        """
        font = pygame.font.SysFont(None, 25)
        
        name_surface = font.render("Player " + str(self.id) + " - " + self.name, True, self.border_color)
        score_surface = font.render(f"Score: {self.score}", True, "white")
        
        surface.blit(name_surface, (position["x"], position["y"]))
        surface.blit(score_surface, (position["x"], position["y"] + 25))