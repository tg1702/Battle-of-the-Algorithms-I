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
            
            
    def check_player_collision(self, player, opponent):
        """
        Checks if the snake has collided with itself or the walls of the board.
        
        :param player: The player whose snake is being checked for collisions
        :type player: Player
        """
        head_x = player.snake.head_position["x"]
        head_y = player.snake.head_position["y"]
        
        # Check for wall collisions
        if (head_x < 0 or head_x >= self.board.width or head_y < 0 or head_y >= self.board.height):
            player.collided = True
            self.calculate_winner(self.player1, self.player2)
            return
            
        # Check for self-collisions
        next_head_x = head_x
        next_head_y = head_y
        direction = player.snake.direction
        
        if direction == "left":
            next_head_x -= config.GRID_SIZE
        elif direction == "right":
            next_head_x += config.GRID_SIZE
        elif direction == "up":
            next_head_y -= config.GRID_SIZE
        elif direction == "down":
            next_head_y += config.GRID_SIZE
            
        for i in range(len(player.snake.body)):
            segment = player.snake.body[i]
            if (segment.position["x"] == next_head_x and segment.position["y"] == next_head_y):
                player.collided = True
                self.calculate_winner(self.player1, self.player2)
                return
            
        # Check opponent collisions
        opponent_head_x = opponent.snake.head_position["x"]
        opponent_head_y = opponent.snake.head_position["y"]
        opponent_direction = opponent.snake.direction
        next_opponent_head_x = opponent_head_x
        next_opponent_head_y = opponent_head_y

        if opponent_direction == "left":
            next_opponent_head_x -= config.GRID_SIZE
        elif opponent_direction == "right":
            next_opponent_head_x += config.GRID_SIZE
        elif opponent_direction == "up":
            next_opponent_head_y -= config.GRID_SIZE
        elif opponent_direction == "down":
            next_opponent_head_y += config.GRID_SIZE

        # Head on collision
        if (next_head_x == next_opponent_head_x and next_head_y == next_opponent_head_y):
            self.player1.collided = True
            self.player2.collided = True
            self.calculate_winner(self.player1, self.player2)
            return
        
        # Body collision
        for i in range(len(opponent.snake.body)):
            segment = opponent.snake.body[i]
            if (segment.position["x"] == next_head_x and segment.position["y"] == next_head_y):
                player.collided = True
                self.calculate_winner(self.player1, self.player2)
                return

    
    def check_food_collision(self, player):
        """
        Checks if the snake has collided with any food items.
        
        :param player: The player whose snake is being checked for food collisions
        :type player: Player
        """
        for food in self.food_list:
            if (food.x // config.GRID_SIZE == player.snake.head_position["x"] // config.GRID_SIZE and 
                food.y // config.GRID_SIZE == player.snake.head_position["y"] // config.GRID_SIZE):
                    self.food_list.remove(food)
                    self.occupied[food.x // config.GRID_SIZE][food.y // config.GRID_SIZE] = {}
                    
                    self.food_list.append(Food())
                    self.occupied[self.food_list[-1].x // config.GRID_SIZE][self.food_list[-1].y // config.GRID_SIZE] = self.food_list[-1]
                    
                    player.snake.grow()
                    player.score += 1
                    
                    
    def calculate_winner(self, player1, player2):
        self.game_over = True
        
        if player1.collided and player2.collided:
            if player1.score == player2.score:
                self.winner = None
            elif player1.score > player2.score:
                self.winner = player1
            else:
                self.winner = player2
        elif (player1.collided):
            self.winner = player2
        else: 
            self.winner = player1
            
        return
            