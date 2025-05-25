import pygame
from config import config
from core.player import Player
from core.food import Food
from core.obstacle import Obstacle

class GameState:
    """
    Represents the state of the game, including the board, players, and food.
    Handles collision detection and game logic.
    """
    def __init__(self, board, player1, player2):
        # Board Attributes
        self.board = board
        self.rows = self.board.rows
        self.cols = self.board.cols
        
        # Occupied Spaces
        self.occupied = [[{} for _ in range(self.rows)] for _ in range(self.cols)]
        self.food_locations = []
        self.obstacle_locations = []
        
        # Players
        self.player1 = player1 
        self.player2 = player2 
        self.winner = None
        
        # Game State
        self.game_over = False
        self.time_up = False
        
        # Sudden Death Attributes
        self.pre_sudden_death_active = False
        self.sudden_death_active = False
        self.sudden_death_food = None 
        self.sudden_death_start_time = None
        
        # Initialize food on the board
        for _ in range(config.NUM_FOOD):
            self._spawn_food()
            
        # Initialize obstacles on the board
        for _ in range(config.NUM_OBSTACLES):
            while True:
                new_obstacle = Obstacle()
                obstacle_positions = new_obstacle.get_occupied_positions()  # must return grid positions

                # Gather all occupied positions
                occupied_positions = set()
                
                for segment in self.player1.snake.body:
                    gx, gy = segment.position["x"] // config.GRID_SIZE, segment.position["y"] // config.GRID_SIZE
                    occupied_positions.add((gx, gy))
                for segment in self.player2.snake.body:
                    gx, gy = segment.position["x"] // config.GRID_SIZE, segment.position["y"] // config.GRID_SIZE
                    occupied_positions.add((gx, gy))
                for food in self.food_locations:
                    gx, gy = food.x // config.GRID_SIZE, food.y // config.GRID_SIZE
                    occupied_positions.add((gx, gy))
                for obs in self.obstacle_locations:
                    occupied_positions.update(obs.get_occupied_positions())

                if not any(pos in occupied_positions for pos in obstacle_positions):
                    self.obstacle_locations.append(new_obstacle)
                    for (x, y) in obstacle_positions:
                        self.occupied[x][y] = new_obstacle
                    break
                
    def _spawn_food(self, is_sudden_death_food=False):
        """
        Helper method to spawn a single food item in a random, unoccupied spot.
        Can be used for initial food, new food during regular gameplay, or the sudden death apple.
        """
        while True:
            new_food = Food()
            food_position_grid = (new_food.x // config.GRID_SIZE, new_food.y // config.GRID_SIZE)

            # Gather all occupied positions by snakes, existing food, and obstacles
            occupied_positions = set()
            
            for seg in self.player1.snake.body:
                occupied_positions.add((seg.position["x"] // config.GRID_SIZE, seg.position["y"] // config.GRID_SIZE))
                
            for seg in self.player2.snake.body:
                occupied_positions.add((seg.position["x"] // config.GRID_SIZE, seg.position["y"] // config.GRID_SIZE))
                
            for existing_food in self.food_locations:
                # Ensure we don't consider the food we're about to replace as occupied
                if existing_food != new_food: 
                    occupied_positions.add((existing_food.x // config.GRID_SIZE, existing_food.y // config.GRID_SIZE))
                    
            for obs in self.obstacle_locations:
                occupied_positions.update(obs.get_occupied_positions())
                
            # If a sudden death food exists and it's not the one we're trying to place, consider its position occupied to avoid overlap.
            if self.sudden_death_food and self.sudden_death_food != new_food:
                occupied_positions.add((self.sudden_death_food.x // config.GRID_SIZE, self.sudden_death_food.y // config.GRID_SIZE))

            if food_position_grid not in occupied_positions:
                if is_sudden_death_food:
                    self.sudden_death_food = new_food
                self.food_locations.append(new_food)
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
            if (segment.position["x"] // config.GRID_SIZE == head_x // config.GRID_SIZE and
                segment.position["y"] // config.GRID_SIZE == head_y // config.GRID_SIZE):
                player.collided = True
                self.calculate_winner(self.player1, self.player2)
                return
            
        # Collision with opponent's body
        for segment in opponent.snake.body:
            if (segment.position["x"] // config.GRID_SIZE == head_x // config.GRID_SIZE and
                segment.position["y"] // config.GRID_SIZE == head_y // config.GRID_SIZE):
                player.collided = True
                self.calculate_winner(self.player1, self.player2)
                return

        # Head-on collision with opponent
        opponent_head_x = opponent.snake.head_position["x"]
        opponent_head_y = opponent.snake.head_position["y"]

        if (head_x // config.GRID_SIZE == opponent_head_x // config.GRID_SIZE and
            head_y // config.GRID_SIZE == opponent_head_y // config.GRID_SIZE):
            self.player1.collided = True
            self.player2.collided = True
            self.calculate_winner(self.player1, self.player2)
            return
        
        # Obstacle collision
        head_x = player.snake.head_position["x"]
        head_y = player.snake.head_position["y"]
        head_grid = (head_x // config.GRID_SIZE, head_y // config.GRID_SIZE)

        for obstacle in self.obstacle_locations:
            if head_grid in obstacle.get_occupied_positions():  # must be grid-based
                player.collided = True
                self.calculate_winner(self.player1, self.player2)
                return

        
    def check_food_collision(self, player):
        """
        Checks if the player's snake head is on any food.
        If so, remove that food and spawn a new one in an unoccupied spot.
        The player's snake grows and score increases by 1.
        
        Returns True if the sudden death food was eaten by this player, False otherwise.
        """
        eats_sudden_death_food = False
        for food in list(self.food_locations): # Iterate over a copy to allow removal
            if (food.x // config.GRID_SIZE == player.snake.head_position["x"] // config.GRID_SIZE and 
                food.y // config.GRID_SIZE == player.snake.head_position["y"] // config.GRID_SIZE):
                
                self.food_locations.remove(food)
                self.occupied[food.x // config.GRID_SIZE][food.y // config.GRID_SIZE] = {} 

                if self.sudden_death_active and food == self.sudden_death_food:
                    eats_sudden_death_food = True
                    # Do NOT set game_over or winner here. Let main loop decide for fairness.
                    return eats_sudden_death_food # Exit early if sudden death food is eaten

                # Spawn new food avoiding snakes and existing food
                while True:
                    new_food = Food()
                    new_food_position_grid = (new_food.x // config.GRID_SIZE, new_food.y // config.GRID_SIZE)

                    occupied_positions = set()
                    for seg in self.player1.snake.body:
                        occupied_positions.add((seg.position["x"] // config.GRID_SIZE, seg.position["y"] // config.GRID_SIZE))
                    for seg in self.player2.snake.body:
                        occupied_positions.add((seg.position["x"] // config.GRID_SIZE, seg.position["y"] // config.GRID_SIZE))
                    for existing_food in self.food_locations:
                        occupied_positions.add((existing_food.x // config.GRID_SIZE, existing_food.y // config.GRID_SIZE))
                    for obs in self.obstacle_locations: # Added obstacle positions for food spawning
                        occupied_positions.update(obs.get_occupied_positions())
                    if self.sudden_death_food and self.sudden_death_food != new_food: # Don't place regular food on sudden death food
                        occupied_positions.add((self.sudden_death_food.x // config.GRID_SIZE, self.sudden_death_food.y // config.GRID_SIZE))

                    if new_food_position_grid not in occupied_positions:
                        break

                self.food_locations.append(new_food)
                self.occupied[new_food.x // config.GRID_SIZE][new_food.y // config.GRID_SIZE] = new_food
                
                player.snake.grow()
                player.score += 1
                return eats_sudden_death_food # Return False for regular food
            
        return eats_sudden_death_food # Return False if no food was eaten
    
    def start_pre_sudden_death(self):
        """
        Initiates the pre-sudden death phase (displaying message).
        """
        if self.pre_sudden_death_active or self.sudden_death_active:
            return # Already in pre-sudden death or actual sudden death

        self.pre_sudden_death_active = True
        self.pre_sudden_death_start_time = pygame.time.get_ticks()
            
    def start_sudden_death(self):
        """
        Initiates sudden death mode. Clears all existing food and spawns one special sudden death food.
        """
        if self.sudden_death_active:
            return # Already in sudden death

        self.sudden_death_active = True
        self.pre_sudden_death_active = False
        self.sudden_death_start_time = pygame.time.get_ticks() # Record start time in milliseconds
        
       # Update the occupied grid with the new snake positions
        for segment in self.player1.snake.body:
            gx, gy = segment.position["x"], segment.position["y"]
            if 0 <= gx < self.cols and 0 <= gy < self.rows:
                self.occupied[gx][gy]  = self.player1.snake
        for segment in self.player2.snake.body:
            gx, gy = segment.position["x"] , segment.position["y"]
             
            if 0 <= gx < self.cols and 0 <= gy < self.rows:
                self.occupied[gx][gy] = self.player2.snake 
                
        # Clear all existing food
        for food in self.food_locations:
            self.occupied[food.x // config.GRID_SIZE][food.y // config.GRID_SIZE] = {}
        self.food_locations.clear()

        # Spawn one sudden death food
        self._spawn_food(is_sudden_death_food=True)
                        
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
