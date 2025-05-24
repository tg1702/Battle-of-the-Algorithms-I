from config import config
from core.player import Player
from core.food import Food

class GameState:
    """
    Represents the state of the game, including the board, players, and food.
    Handles collision detection and game logic.
    """
    def __init__(self, board, player1, player2):
        self.board = board
        self.rows = self.board.rows
        self.cols = self.board.cols
        self.occupied = [[{} for _ in range(self.rows)] for _ in range(self.cols)]
        self.food_list = []
        self.game_over = False
        self.time_up = False
        self.player1 = player1 
        self.player2 = player2 
        self.winner = None
        
        # Initialize food on the board 
        for _ in range(3):
            while True:
                new_food = Food()
                food_position_grid = (new_food.x // config.GRID_SIZE, new_food.y // config.GRID_SIZE)

                # Gather all occupied positions by snakes and food
                occupied_positions = set()
                for segment in self.player1.snake.body:
                    occupied_positions.add((segment.position["x"] // config.GRID_SIZE, segment.position["y"] // config.GRID_SIZE))
                for segment in self.player2.snake.body:
                    occupied_positions.add((segment.position["x"] // config.GRID_SIZE, segment.position["y"] // config.GRID_SIZE))
                for existing_food in self.food_list:
                    occupied_positions.add((existing_food.x // config.GRID_SIZE, existing_food.y // config.GRID_SIZE))

                if food_position_grid not in occupied_positions:
                    self.food_list.append(new_food)
                    self.occupied[new_food.x // config.GRID_SIZE][new_food.y // config.GRID_SIZE] = new_food
                    break

    def check_player_collision(self, player, opponent):
        """
        Checks if the player's snake collides with walls, itself, or the opponent.
        Assumes the snake has already moved.
        """
        head_x = player.snake.head_position["x"]
        head_y = player.snake.head_position["y"]
        
        # Wall collision
        if (head_x < 0 or head_x >= self.board.width or 
            head_y < 0 or head_y >= self.board.height):
            player.collided = True
            self.calculate_winner(self.player1, self.player2)
            return
            
        # Self collision
        for i in range(1, len(player.snake.body)):
            segment = player.snake.body[i]
            if (segment.position["x"] == head_x and segment.position["y"] == head_y):
                player.collided = True
                self.calculate_winner(self.player1, self.player2)
                return
            
        # Collision with opponent's body
        for segment in opponent.snake.body:
            if (segment.position["x"] == head_x and segment.position["y"] == head_y):
                player.collided = True
                self.calculate_winner(self.player1, self.player2)
                return

        # Head-on collision with opponent
        opponent_head_x = opponent.snake.head_position["x"]
        opponent_head_y = opponent.snake.head_position["y"]

        if (head_x == opponent_head_x and head_y == opponent_head_y):
            self.player1.collided = True
            self.player2.collided = True
            self.calculate_winner(self.player1, self.player2)
            return
        
    def check_food_collision(self, player):
        """
        Checks if the player's snake head is on any food.
        If so, remove that food and spawn a new one in an unoccupied spot.
        The player's snake grows and score increases by 1.
        """
        for food in list(self.food_list):  # Iterate over a copy to allow removal
            if (food.x // config.GRID_SIZE == player.snake.head_position["x"] // config.GRID_SIZE and 
                food.y // config.GRID_SIZE == player.snake.head_position["y"] // config.GRID_SIZE):
                self.food_list.remove(food)
                self.occupied[food.x // config.GRID_SIZE][food.y // config.GRID_SIZE] = {}

                # Spawn new food avoiding snakes and existing food
                while True:
                    new_food = Food()
                    new_food_position_grid = (new_food.x // config.GRID_SIZE, new_food.y // config.GRID_SIZE)

                    occupied_positions = set()
                    for seg in self.player1.snake.body:
                        occupied_positions.add((seg.position["x"] // config.GRID_SIZE, seg.position["y"] // config.GRID_SIZE))
                    for seg in self.player2.snake.body:
                        occupied_positions.add((seg.position["x"] // config.GRID_SIZE, seg.position["y"] // config.GRID_SIZE))
                    for existing_food in self.food_list:
                        occupied_positions.add((existing_food.x // config.GRID_SIZE, existing_food.y // config.GRID_SIZE))

                    if new_food_position_grid not in occupied_positions:
                        break

                self.food_list.append(new_food)
                self.occupied[new_food.x // config.GRID_SIZE][new_food.y // config.GRID_SIZE] = new_food
                
                player.snake.grow()
                player.score += 1
                return 
                        
    def calculate_winner(self, player1, player2):
        """
        Determines the winner based on the game state.
        If both players collide, the one with the higher score wins.
        If both collide with the wall or each other, it's a tie.
        """
        self.game_over = True
        
        if (player1.collided and player2.collided) or self.time_up:
            if player1.score == player2.score:
                self.winner = None  # Tie
            elif player1.score > player2.score:
                self.winner = player1
            else:
                self.winner = player2
        elif player1.collided:
            self.winner = player2
        elif player2.collided:
            self.winner = player1
        else:
            # No collisions, winner by higher score or tie
            if player1.score == player2.score:
                self.winner = None
            elif player1.score > player2.score:
                self.winner = player1
            else:
                self.winner = player2
                
        return
