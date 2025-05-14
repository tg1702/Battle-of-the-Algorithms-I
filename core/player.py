import pygame
import colors
import core.snake as snake
import importlib.util
import sys

class Player: 
    def __init__(self, id, name, board, controller_path):
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
            
        self.controller = self._load_controller(controller_path)
        
    def _load_controller(self, controller_module_name):
        """Loads the player's controller file."""
        try:
            module = importlib.import_module(controller_module_name)
            if not hasattr(module, 'get_next_move') or not callable(module.get_next_move):
                raise AttributeError(f"Controller module {controller_module_name} must contain a function named 'get_next_move'.")
            return module
        except ModuleNotFoundError:
            raise FileNotFoundError(f"Could not find controller module: {controller_module_name}. Ensure '{controller_module_name}.py' exists in a directory accessible by Python's module search path (e.g., the 'controllers' directory).")
        except AttributeError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Error loading controller module {controller_module_name}: {e}")
    
    def get_next_direction(self, game_state):
        """Gets the next move direction from the player's controller."""
        if self.controller:
            board_info = {
                "width": self.board.width,
                "height": self.board.height,
                "food_locations": [(food.x, food.y) for food in game_state.food_list],
                "player1_body": [{"x": seg.position["x"], "y": seg.position["y"]} for seg in game_state.player1.snake.body],
                "player2_body": [{"x": seg.position["x"], "y": seg.position["y"]} for seg in game_state.player2.snake.body]
            }
            player_info = {
                "head_position": self.snake.head_position.copy(),
                "body": [{"x": seg.position["x"], "y": seg.position["y"]} for seg in self.snake.body],
                "direction": self.snake.direction,
                "score": self.score
            }
            opponent_player = game_state.player2 if self.id == 1 else game_state.player1
            opponent_info = {
                "head_position": opponent_player.snake.head_position.copy(),
                "body": [{"x": seg.position["x"], "y": seg.position["y"]} for seg in opponent_player.snake.body],
                "direction": opponent_player.snake.direction,
                "score": opponent_player.score
            }
            return self.controller.get_next_move(board_info, player_info, opponent_info)
        return None 

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