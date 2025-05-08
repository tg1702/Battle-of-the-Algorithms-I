from config import config
from core.player import Player
from core.food import Food

class GameState:
    def __init__(self, board, player1, player2):
        self.board = board
        self.rows = self.board.rows
        self.cols = self.board.cols
        self.occupied = [[{} for _ in range(self.rows)] for _ in range(self.cols)]
        self.food_list = []
        self.game_over = False
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        
        for i in range(0, 3):
            self.food_list.append(Food())
            self.occupied[self.food_list[i].x // config.GRID_SIZE][self.food_list[i].y // config.GRID_SIZE] = self.food_list[i]
            
    def check_player_collision(self, player):
        """
        Checks if the snake has collided with itself or the walls of the board.
        
        :param player: The player whose snake is being checked for collisions
        :type player: Player
        """
        # Check for wall collisions
        if (player.snake.position["x"] < 0 or 
            player.snake.position["x"] >= self.board.width or 
            player.snake.position["y"] < 0 or 
            player.snake.position["y"] >= self.board.height):
            self.game_over = True
            self.winner = self.player1 if player == self.player2 else self.player2
            
        # Check for self-collisions
        
    
    def check_food_collision(self, player):
        """
        Checks if the snake has collided with any food items.
        
        :param player: The player whose snake is being checked for food collisions
        :type player: Player
        """
        for food in self.food_list:
            if (food.x // config.GRID_SIZE == player.snake.position["x"] // config.GRID_SIZE and 
                food.y // config.GRID_SIZE == player.snake.position["y"] // config.GRID_SIZE):
                    self.food_list.remove(food)
                    self.occupied[food.x // config.GRID_SIZE][food.y // config.GRID_SIZE] = {}
                    
                    self.food_list.append(Food())
                    self.occupied[self.food_list[-1].x // config.GRID_SIZE][self.food_list[-1].y // config.GRID_SIZE] = self.food_list[-1]
                    
                    player.snake.length += 1
                    player.score += 1
                