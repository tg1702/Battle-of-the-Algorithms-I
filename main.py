import pygame, time
from config import config
import core.board as board, core.scorebar as scorebar, core.player as player, core.food as food
import core.game_state as game_state
import colors

pygame.init()

running = True

# Screen Setup 
screen_width = config.SCREEN_WIDTH
screen_height = config.SCREEN_HEIGHT
board_width = config.BOARD_WIDTH
board_height = config.BOARD_HEIGHT

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(config.TITLE)

# Setup Time
clock = pygame.time.Clock()
previous_time = pygame.time.get_ticks()

# Board Setup
title_font = pygame.font.SysFont(None, 40)
title_surface = title_font.render("Battle of the Algorithms", True, "white")
board = board.Board(board_width, board_height)
scorebar = scorebar.ScoreBar(350, 100, screen)

# Initialize Players
player1 = player.Player(1, "John", board)
player2 = player.Player(2, "Jenny", board)

# Game State
state = game_state.GameState(board, player1, player2)
apples = state.food_list

while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player1.snake.direction = "left"
                
            if event.key == pygame.K_RIGHT:
                player1.snake.direction = "right"
                
            if event.key == pygame.K_DOWN:
                player1.snake.direction = "down"
                
            if event.key == pygame.K_UP:
                player1.snake.direction = "up"
                
    if state.game_over == False:
        # Calculate Time
        current_time = pygame.time.get_ticks()
        delta_time = current_time - previous_time
        previous_time = current_time
                
        # Fill Screen and Draw Game Board
        screen.fill(colors.background_color)
        board.draw(screen)

        # Render Text
        screen.blit(title_surface, (screen_width/2 - 165, 50))
        
        player1.draw_score(screen, {"x": 150, "y": 100})
        player2.draw_score(screen, {"x": screen_width - 270, "y": 100})
            
        # Draw Food
        for apple in apples:
            apple.draw(board)
            
         # Check Collisions
        state.check_food_collision(player1)
        state.check_food_collision(player2)
        state.check_player_collision(player1)
        # state.check_player_collision(player2)
        
        # Draw Score Bar
        scorebar.draw(screen, player1, player2)
        
        # Draw Player Snakes
        player1.snake.move(delta_time)
        player2.snake.move(delta_time)
        player1.snake.draw(board.board)
        player2.snake.draw(board.board)
        
        # Render Display
        pygame.display.flip()
        
        # Set Frame Rate
        clock.tick(config.FPS)
    
pygame.quit()