# Python Libraries
import pygame
import threading
import traceback
import queue
from itertools import chain

# User-Defined Imports
from config import config
import core.board as board_module
import core.scorebar as scorebar_module
import core.player as player
import core.game_state as game_state
import config.colors as colors
import core.game_over_screen as game_over_screen

pygame.init()

# Screen Setup
screen_width = config.SCREEN_WIDTH
screen_height = config.SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(config.TITLE)

# Timing Setup
clock = pygame.time.Clock()
game_start_time = pygame.time.get_ticks()
max_game_duration = 5 * 60 * 1000  # 5 minutes in milliseconds
timer_font = pygame.font.SysFont(None, 36)

# Title Setup
title_font = pygame.font.SysFont(None, 40)
title_surface = title_font.render("Battle of the Algorithms I", True, "white")

# Board and Scorebar Setup
game_board = board_module.Board(config.BOARD_WIDTH, config.BOARD_HEIGHT)
game_scorebar = scorebar_module.ScoreBar(350, 100, screen)

# Player Controller Modules
player1_controller_module = "controllers.player1_controller"
player2_controller_module = "controllers.player2_controller"

# Players
player1 = player.Player(1, game_board, player1_controller_module)
player2 = player.Player(2, game_board, player2_controller_module)

# Game State
state = game_state.GameState(game_board, player1, player2)
apples = state.food_locations
obstacles = state.obstacle_locations

# Game Over Screen
game_over_screen = game_over_screen.GameOverScreen()

# AI Timing
last_ai_update_time = pygame.time.get_ticks()

# AI Thread Result Queues
p1_result_queue = queue.Queue()
p2_result_queue = queue.Queue()


def ai_worker(player_obj, board_state_data, player_state_data, opponent_state_data, result_queue):
    """
    Worker function for AI controller to run in a separate thread.
    """
    try:
        direction = player_obj.controller.get_next_move(board_state_data, player_state_data, opponent_state_data)
        result_queue.put(direction)
    except Exception as e:
        print(f"Error in {player_obj.name}'s controller: {e}")
        traceback.print_exc()
        result_queue.put(None)
    finally:
        if result_queue.empty():
            result_queue.put("none")


def get_player_state(player_obj):
    """
    Returns a dictionary representation of the player's state.
    """
    return {
        "id": player_obj.id,
        "head_position": player_obj.snake.head_position.copy(),
        "body": [{"x": seg.position["x"], "y": seg.position["y"]} for seg in player_obj.snake.body],
        "direction": player_obj.snake.direction,
        "score": player_obj.score,
        "length": len(player_obj.snake.body)
    }


def restart_game():
    """
    Restarts the game by reinitializing the game state and players.
    """
    global player1, player2, state, apples, obstacles, game_start_time, last_ai_update_time
    player1 = player.Player(1, game_board, player1_controller_module)
    player2 = player.Player(2, game_board, player2_controller_module)
    state = game_state.GameState(game_board, player1, player2)
    apples = state.food_locations
    obstacles = state.obstacle_locations
    game_start_time = pygame.time.get_ticks()
    last_ai_update_time = pygame.time.get_ticks()


running = True

while running:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Restart Game If Restart Button Clicked or 'R' Key Pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            restart_x = config.SCREEN_WIDTH / 2 - 110
            restart_y = 520
            width = game_over_screen.restart_button.width
            height = game_over_screen.restart_button.height

            if state.game_over:
                if (restart_x <= mouse_pos[0] <= restart_x + width and
                        restart_y <= mouse_pos[1] <= restart_y + height):
                    restart_game()
                    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and state.game_over:
                restart_game()

    # Main Game Logic
    if not state.game_over:
        current_loop_time = pygame.time.get_ticks()
        elapsed_game_time = current_loop_time - game_start_time

        # Check Elapsed Game Time Against Max Game Duration
        if elapsed_game_time >= max_game_duration:
            state.game_over = True
            state.time_up = True
            state.calculate_winner(player1, player2)
            continue

        # AI Update Logic
        if current_loop_time - last_ai_update_time >= config.AI_UPDATE_INTERVAL_MS:
            last_ai_update_time = current_loop_time

            board_snapshot = {
                "width": game_board.width,
                "height": game_board.height,
                "rows": game_board.rows,
                "cols": game_board.cols,
                "food_locations": [(food.x, food.y) for food in state.food_locations],
                "obstacle_locations": list(chain.from_iterable(obs.get_occupied_positions() for obs in state.obstacle_locations))
            }

            # Get Player States
            p1_state = get_player_state(player1)
            p2_state = get_player_state(player2)

            # Clear Result Queues
            while not p1_result_queue.empty():
                p1_result_queue.get_nowait()
            while not p2_result_queue.empty():
                p2_result_queue.get_nowait()

            # Start Threads for AI Controllers
            p1_thread = threading.Thread(target=ai_worker, args=(player1, board_snapshot, p1_state, p2_state, p1_result_queue), daemon=True)
            p2_thread = threading.Thread(target=ai_worker, args=(player2, board_snapshot, p2_state, p1_state, p2_result_queue), daemon=True)
            p1_thread.start()
            p2_thread.start()

            # Get Player 1 Direction
            try:
                direction = p1_result_queue.get(timeout=config.CONTROLLER_TIMEOUT_SECONDS)
                if direction in ["left", "right", "up", "down"]:
                    player1.snake.direction = direction
                else:
                    print(f"Invalid move returned by Player {player1.id}: {direction}")
            except queue.Empty:
                print("Player 1 controller timed out.")

            # Get Player 2 Direction
            try:
                direction = p2_result_queue.get(timeout=config.CONTROLLER_TIMEOUT_SECONDS)
                if direction in ["left", "right", "up", "down"]:
                    player2.snake.direction = direction
                else:
                    print(f"Invalid move returned by Player {player2.id}: {direction}")
            except queue.Empty:
                print("Player 2 controller timed out.")

            # Move Snakes
            player1.snake.move()
            player2.snake.move()
            
            # Check Food Collisions
            state.check_food_collision(player1)
            state.check_food_collision(player2)
            
            # Check Player Collisions
            state.check_player_collision(player1, player2)
            state.check_player_collision(player2, player1)
            if state.game_over:
                continue
            
    # Render Screen
    screen.fill(colors.background_color)
    game_board.draw(screen)
    screen.blit(title_surface, (screen_width / 2 - 165, 50))

    # Render Timer
    if not state.game_over:
        elapsed_game_time = pygame.time.get_ticks() - game_start_time
        minutes = elapsed_game_time // 60000
        seconds = (elapsed_game_time % 60000) // 1000
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = timer_font.render(timer_text, True, "white")
        screen.blit(timer_surface, (20, 20))

    # Render Scores
    player1.draw_score(screen, {"x": 150, "y": 100})
    player2.draw_score(screen, {"x": screen_width - 270, "y": 100})

    # Draw Apples
    for apple in apples:
        apple.draw(game_board)
        
    # Draw Obstacles
    for obstacle in obstacles:
        obstacle.draw(game_board)

    # Draw Snakes
    player1.snake.draw(game_board.board)
    player2.snake.draw(game_board.board)

    # Draw Scorebar
    game_scorebar.draw(screen, player1, player2)

    # Draw Game Over Screen
    if state.game_over:
        game_over_screen.draw(screen, state.winner)

    # Update Display
    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()