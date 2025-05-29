import pygame
from config import config
from core.player import Player
from core.food import Food
from core.obstacle import Obstacle

class GameState:
    """
    Represents the current state of the game, including the board, players, food, and obstacles.
    Handles collision detection and core game logic.
    """
    def __init__(self, board, player1, player2):
        # Board Attributes
        self.board = board
        self.rows = board.rows
        self.cols = board.cols
        
        # Occupied Spaces
        self.food_locations = []
        self.obstacle_locations = []
        
        # Players
        self.player1 = player1 
        self.player2 = player2 
        self.winner = None
        
        # Game State Flags
        self.game_over = False
        self.time_up = False 
        
        # Sudden Death Attributes
        self.pre_sudden_death_active = False
        self.sudden_death_active = False
        self.sudden_death_food = None 
        self.sudden_death_start_time = None
        
        # Spawn Initial Food
        for _ in range(config.NUM_FOOD):
            self._spawn_food()
            
        # Spawn Initial Obstacles
        for _ in range(config.NUM_OBSTACLES):
            while True:
                new_obstacle = Obstacle()
                obstacle_positions = new_obstacle.get_occupied_positions()

                # Avoid placing on occupied positions
                occupied_positions = self._get_all_occupied_grid_positions(include_future_heads=False)
                if not any(pos in occupied_positions for pos in obstacle_positions):
                    self.obstacle_locations.append(new_obstacle)
                    break
                
    def _get_all_occupied_grid_positions(self, include_future_heads=True):
        """
        Returns all occupied grid positions as a set of (row, col) tuples.
        If include_future_heads is True, current snake heads are included.
        """
        occupied_positions = set()
        
        # Helper to convert pixel to (row, col) grid coordinates
        def pixel_to_grid(pixel_x, pixel_y):
            return (pixel_y // config.GRID_SIZE, pixel_x // config.GRID_SIZE)

        # Include future snake heads
        if include_future_heads:
            occupied_positions.add(pixel_to_grid(self.player1.snake.head_position["x"], self.player1.snake.head_position["y"]))
            occupied_positions.add(pixel_to_grid(self.player2.snake.head_position["x"], self.player2.snake.head_position["y"]))
        
        # Snake bodies
        for segment in self.player1.snake.body:
            occupied_positions.add(pixel_to_grid(segment.position["x"], segment.position["y"]))
        for segment in self.player2.snake.body:
            occupied_positions.add(pixel_to_grid(segment.position["x"], segment.position["y"]))
        
        # Food locations
        for food in self.food_locations:
            occupied_positions.add((food.grid_row, food.grid_col))
        
        # Obstacles
        for obs in self.obstacle_locations:
            occupied_positions.update(obs.get_occupied_positions())
            
        return occupied_positions
                            
    def _spawn_food(self, is_sudden_death_food=False):
        """
        Spawns a single food item in a valid, unoccupied location.
        If is_sudden_death_food is True, replaces all existing food with one sudden death item.
        """
        if is_sudden_death_food:
            self.food_locations.clear()
            self.sudden_death_food = None
            
        spawned = False
        attempts = 0
        max_attempts = self.rows * self.cols * 2

        while not spawned and attempts < max_attempts:
            new_food = Food()
            food_position_grid = (new_food.grid_row, new_food.grid_col)
            occupied_positions = self._get_all_occupied_grid_positions(include_future_heads=True)
            
            if food_position_grid in occupied_positions:
                attempts += 1
                continue
            
            if is_sudden_death_food:
                self.sudden_death_food = new_food
                self.food_locations.append(new_food)
            else:
                self.food_locations.append(new_food)
            spawned = True
        
        if not spawned:
            print("Warning: Could not spawn food. Board might be full.")
            self.winner = None
            self.game_over = True

    def resolve_collisions(self):
        """
        Resolves all collisions in the game simultaneously and updates the game state accordingly.
        All grid positions are handled as (row, col).
        """
        # Helper to convert pixel to (row, col) grid coordinates
        def pixel_to_grid(pixel_x, pixel_y):
            return (pixel_y // config.GRID_SIZE, pixel_x // config.GRID_SIZE)

        p1_head_grid = pixel_to_grid(self.player1.snake.head_position["x"], self.player1.snake.head_position["y"])
        p2_head_grid = pixel_to_grid(self.player2.snake.head_position["x"], self.player2.snake.head_position["y"])
        
        p1_collided = False
        p2_collided = False
        
        # Wall collisions
        if not (0 <= p1_head_grid[0] < self.rows and 0 <= p1_head_grid[1] < self.cols):
            p1_collided = True
            print(self.player1.name, "collided with a wall!")
            
        if not (0 <= p2_head_grid[0] < self.rows and 0 <= p2_head_grid[1] < self.cols):
            p2_collided = True
            print(self.player2.name, "collided with a wall!")
            

        # Self-collisions
        for i in range(1, len(self.player1.snake.body)):
            segment = self.player1.snake.body[i]
            
            if p1_head_grid == pixel_to_grid(segment.position["x"], segment.position["y"]):
                p1_collided = True
                print(self.player1.name, "self-collided!")
                break
            
        for i in range(1, len(self.player2.snake.body)):
            segment = self.player2.snake.body[i]
            
            if p2_head_grid == pixel_to_grid(segment.position["x"], segment.position["y"]):
                p2_collided = True
                print(self.player2.name, "self-collided!")
                break

        # Player-to-player collisions
        for segment in self.player2.snake.body:
            if p1_head_grid == pixel_to_grid(segment.position["x"], segment.position["y"]):
                p1_collided = True
                print(self.player1.name, "hit", self.player2.name + "!")
                break
        for segment in self.player1.snake.body:
            if p2_head_grid == pixel_to_grid(segment.position["x"], segment.position["y"]):
                p2_collided = True
                print(self.player2.name, "hit", self.player1.name + "!")
                break

        # Head on collision
        if p1_head_grid == p2_head_grid:
            p1_collided = True
            p2_collided = True
            print("Head-on collision!")
            
        # Obstacle collisions
        for obstacle in self.obstacle_locations:
            if p1_head_grid in obstacle.get_occupied_positions():
                p1_collided = True
                print(self.player1.name, "collided with an obstacle!")

            if p2_head_grid in obstacle.get_occupied_positions():
                p2_collided = True
                print(self.player2.name, "collided with an obstacle!")

        # Food collisions
        for food_item in list(self.food_locations): 
            food_pos_grid = (food_item.grid_row, food_item.grid_col)
            
            p1_eats = food_pos_grid == p1_head_grid and not p1_collided
            p2_eats = food_pos_grid == p2_head_grid and not p2_collided
            
            if p1_eats or p2_eats:
                if self.sudden_death_active and food_item == self.sudden_death_food:
                    if p1_eats and p2_eats:
                        if food_item in self.food_locations:
                            self.food_locations.remove(food_item)
                        self._spawn_food(is_sudden_death_food=True)
                    elif p1_eats:
                        self.winner = self.player1
                        self.player1.snake.grow()
                        self.player1.score += 1
                        self.game_over = True
                    elif p2_eats:
                        self.winner = self.player2
                        self.player2.snake.grow()
                        self.player2.score += 1
                        self.game_over = True
                else:
                    if p1_eats:
                        self.player1.snake.grow()
                        self.player1.score += 1
                    if p2_eats:
                        self.player2.snake.grow()
                        self.player2.score += 1
                    if food_item in self.food_locations:
                        self.food_locations.remove(food_item)
                    if not self.sudden_death_active:
                        self._spawn_food()

        # Update player status
        self.player1.collided = p1_collided
        self.player2.collided = p2_collided

        # Determine winner if not already set by sudden death
        if not self.game_over: 
            if p1_collided and p2_collided:
                if self.player1.score > self.player2.score:
                    self.winner = self.player1
                elif self.player2.score > self.player1.score:
                    self.winner = self.player2
                else:
                    self.winner = None
                self.game_over = True
            elif p1_collided:
                self.winner = self.player2
                self.game_over = True
            elif p2_collided:
                self.winner = self.player1
                self.game_over = True

    def start_pre_sudden_death(self):
        """
        Activates the pre-sudden death phase if not already active.
        """
        if self.pre_sudden_death_active or self.sudden_death_active:
            return

        self.pre_sudden_death_active = True
        self.pre_sudden_death_start_time = pygame.time.get_ticks()
            
    def start_sudden_death(self):
        """
        Starts sudden death mode and spawns a special food item.
        """
        if self.sudden_death_active:
            return

        self.sudden_death_active = True
        self.pre_sudden_death_active = False
        self.sudden_death_start_time = pygame.time.get_ticks()
        self.food_locations.clear()
        self._spawn_food(is_sudden_death_food=True)
                            
    def calculate_winner(self, player1, player2):
        """
        Finalizes the game and determines the winner based on collisions and scores.
        - If both players collided, the player with the higher score wins (or tie if scores match).
        - If only one player collided, the other wins.
        - If neither collided, the player with the higher score wins (or tie if scores match).
        """
        # Exit early if the game is already marked as over (e.g., from sudden death resolution)
        if self.game_over:
            return

        # Mark the game as over
        self.game_over = True

        # Case 1: Both players collided
        if player1.collided and player2.collided:
            if player1.score == player2.score:
                self.winner = None  # Tie
            elif player1.score > player2.score:
                self.winner = player1
            else:
                self.winner = player2

        # Case 2: Only player1 collided
        elif player1.collided:
            self.winner = player2

        # Case 3: Only player2 collided
        elif player2.collided:
            self.winner = player1

        # Case 4: Neither collided — determine winner by score
        else:
            if player1.score == player2.score:
                self.winner = None  # Tie
            elif player1.score > player2.score:
                self.winner = player1
            else:
                self.winner = player2