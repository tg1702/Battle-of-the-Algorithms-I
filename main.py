import pygame
from config import config
import core.board as board, core.scorebar as scorebar, core.player as player
import core.game_state as game_state
import config.colors as colors
import core.game_over_screen as game_over_screen

# Import Controllers
import controllers.player1_controller as player1_controller_path
import controllers.player2_controller as player2_controller_path

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

# Timer Setup
game_start_time = pygame.time.get_ticks()
max_game_duration = 5 * 60 * 1000  # 5 minutes in milliseconds
timer_font = pygame.font.SysFont(None, 36)

# Board Setup
title_font = pygame.font.SysFont(None, 40)
title_surface = title_font.render("Battle of the Algorithms I", True, "white")
board = board.Board(board_width, board_height)
scorebar = scorebar.ScoreBar(350, 100, screen)

# Initialize Players
player1_controller_module = "controllers.player1_controller"
player2_controller_module = "controllers.player2_controller"

player1 = player.Player(1, board, player1_controller_module)
player2 = player.Player(2, board, player2_controller_module)

# Game State
state = game_state.GameState(board, player1, player2)
apples = state.food_list

# Game Over Screen
game_over_screen = game_over_screen.GameOverScreen()

while running:
    # Handle Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            width = game_over_screen.restart_button.width
            height = game_over_screen.restart_button.height
            restart_x = config.SCREEN_WIDTH/2 - 110
            restart_y = 520
            
            if state.game_over == True:
                if mouse_pos[0] >= restart_x and mouse_pos[0] <= restart_x + width and mouse_pos[1] >= restart_y and mouse_pos[1] <= restart_y + height:    
                    # Clear Screen
                    screen.fill("black")
                    
                    # Reset State
                    player1 = player.Player(1, board, player1_controller_module)
                    player2 = player.Player(2, board, player2_controller_module)

                    state.game_over = False
                    state = game_state.GameState(board, player1, player2)
                    apples = state.food_list  
                    
                    # Reset time variables
                    previous_time = pygame.time.get_ticks()
                    game_start_time = pygame.time.get_ticks()
                
    if state.game_over == False:      
        #  Check Elapsed Time
        elapsed_time = pygame.time.get_ticks() - game_start_time
        if elapsed_time >= max_game_duration:
            state.game_over = True
            state.time_up = True
            state.calculate_winner(player1, player2)
            continue

        # Get player 1's move
        p1_direction = player1.get_next_direction(state)
        if p1_direction in ["left", "right", "up", "down"]:
            player1.snake.direction = p1_direction

        # Get player 2's move
        p2_direction = player2.get_next_direction(state)
        if p2_direction in ["left", "right", "up", "down"]:
            player2.snake.direction = p2_direction
        
        # Calculate Time
        current_time = pygame.time.get_ticks()
        delta_time = current_time - previous_time
        previous_time = current_time
                
        # Fill Screen and Draw Game Board
        screen.fill(colors.background_color)
        board.draw(screen)

        # Render Text
        screen.blit(title_surface, (screen_width/2 - 165, 50))
        
        # Draw Timer
        minutes = elapsed_time // 60000
        seconds = (elapsed_time % 60000) // 1000
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = timer_font.render(timer_text, True, "white")
        screen.blit(timer_surface, (20, 20))
        
        player1.draw_score(screen, {"x": 150, "y": 100})
        player2.draw_score(screen, {"x": screen_width - 270, "y": 100})
            
        # Draw Food
        for apple in apples:
            apple.draw(board)
            
        # Check Food Collisions
        state.check_food_collision(player1)
        state.check_food_collision(player2)
        
        # Check collisions for player 1
        state.check_player_collision(player1, player2)
        
        # Check collisions for player 2
        state.check_player_collision(player2, player1)
        
        # Draw Score Bar
        scorebar.draw(screen, player1, player2)
        
        # Draw Player Snakes
        player1.snake.move(delta_time)
        player2.snake.move(delta_time)
        player1.snake.draw(board.board)
        player2.snake.draw(board.board)
    
    else: 
        # Render Game Over Screen
        game_over_screen.draw(screen, state.winner)
        
    # Render Display
    pygame.display.flip()
    
    # Set Frame Rate
    clock.tick(config.FPS)
        
pygame.quit()