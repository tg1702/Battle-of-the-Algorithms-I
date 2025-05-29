# --- Python Standard and Third-Party Libraries ---
import pygame
import threading
import traceback
import queue
from itertools import chain

# --- Project Modules ---
from config import config
import core.board as board_module
import core.scorebar as scorebar_module
import core.player as player
import core.game_state as game_state
import config.colors as colors
import core.game_over_screen as game_over_screen

# --- Pygame Initialization ---
pygame.init()

# --- Screen Setup ---
screen_width = config.SCREEN_WIDTH
screen_height = config.SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(config.TITLE)

# --- Timing Setup ---
clock = pygame.time.Clock()
game_start_time = pygame.time.get_ticks()
max_game_duration = config.GAME_DURATION
timer_font = pygame.font.SysFont(None, 36)

# --- Title Display Setup ---
title_font = pygame.font.SysFont(None, 40)
title_surface = title_font.render(config.TITLE, True, "white")

# --- Game Board and Scorebar ---
game_board = board_module.Board(config.BOARD_WIDTH, config.BOARD_HEIGHT)
game_scorebar = scorebar_module.ScoreBar(config.SCOREBAR_POS_X, config.SCOREBAR_POS_Y, screen)

# --- Controller Modules ---
player1_controller_module = "controllers.player1_controller"
player2_controller_module = "controllers.player2_controller"

# --- Players Initialization ---
player1 = player.Player(1, game_board, player1_controller_module)
player2 = player.Player(2, game_board, player2_controller_module)

# --- Game State ---
state = game_state.GameState(game_board, player1, player2)

# --- Game Over Screen ---
game_over_screen = game_over_screen.GameOverScreen()

# --- AI Timing Setup ---
last_ai_update_time = pygame.time.get_ticks()

# --- AI Thread Communication Queues ---
p1_result_queue = queue.Queue()
p2_result_queue = queue.Queue()


def ai_worker(player_obj, board_state_data, player_state_data, opponent_state_data, result_queue):
    """
    Thread worker for executing a player's AI move logic.
    Puts result (direction) into result_queue.
    """
    try:
        direction = player_obj.controller.get_next_move(board_state_data, player_state_data, opponent_state_data)
        if direction in ["left", "right", "up", "down"]:
            result_queue.put(direction)
        else:
            result_queue.put(None)
    except Exception as e:
        print(f"Error in {player_obj.name}'s controller: {e}")
        traceback.print_exc()
        result_queue.put(None)


def get_player_state(player_obj):
    """
    Returns a dictionary snapshot of the given player's state.
    """
    return {
        "id": player_obj.id,
        "head_position": player_obj.snake.head_position.copy(),
        "body": [{"row": seg.position["row"], "col": seg.position["col"]} for seg in player_obj.snake.body],
        "direction": player_obj.snake.direction,
        "score": player_obj.score,
        "length": len(player_obj.snake.body)
    }


def restart_game():
    """
    Resets the game by reinitializing players, game state, and timers.
    """
    global player1, player2, state, game_start_time, last_ai_update_time
    player1 = player.Player(1, game_board, player1_controller_module)
    player2 = player.Player(2, game_board, player2_controller_module)
    state = game_state.GameState(game_board, player1, player2)
    game_start_time = pygame.time.get_ticks()
    last_ai_update_time = pygame.time.get_ticks()


# --- Main Game Loop ---
running = True
while running:

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Restart game on mouse click over button or 'R' key press
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            width = game_over_screen.restart_button.width
            height = game_over_screen.restart_button.height

            if state.game_over:
                if config.RESTART_BUTTON_X <= mouse_pos[0] <= config.RESTART_BUTTON_Y + width and config.RESTART_BUTTON_Y <= mouse_pos[1] <= config.RESTART_BUTTON_Y + height:
                    restart_game()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and state.game_over:
                restart_game()

    # --- Game Logic ---
    if not state.game_over:
        current_loop_time = pygame.time.get_ticks()
        elapsed_game_time = current_loop_time - game_start_time

        # Activate pre-sudden-death if time limit reached
        if not state.sudden_death_active and not state.pre_sudden_death_active and elapsed_game_time >= max_game_duration:
            if player1.score == player2.score:
                state.start_pre_sudden_death()
            else:
                state.calculate_winner(player1, player2)

        # Transition to sudden death after pre-message delay
        if state.pre_sudden_death_active:
            if current_loop_time - state.pre_sudden_death_start_time >= config.PRE_SUDDEN_DEATH_MESSAGE_DURATION:
                state.start_sudden_death()
        else:
            # AI Update Interval
            if current_loop_time - last_ai_update_time >= config.AI_UPDATE_INTERVAL_MS:
                last_ai_update_time = current_loop_time

                # Build board state snapshot for controllers
                board_snapshot = {
                    "width": game_board.width,
                    "height": game_board.height,
                    "rows": game_board.rows,
                    "cols": game_board.cols,
                    "food_locations": [(food.grid_row, food.grid_col) for food in state.food_locations],
                    "obstacle_locations": list(chain.from_iterable(obs.get_occupied_positions() for obs in state.obstacle_locations))
                }

                # Capture current player states
                p1_state = get_player_state(player1)
                p2_state = get_player_state(player2)

                # Clear any leftover AI results
                while not p1_result_queue.empty():
                    p1_result_queue.get_nowait()
                while not p2_result_queue.empty():
                    p2_result_queue.get_nowait()

                # Start AI threads
                p1_thread = threading.Thread(target=ai_worker, args=(player1, board_snapshot, p1_state, p2_state, p1_result_queue), daemon=True)
                p2_thread = threading.Thread(target=ai_worker, args=(player2, board_snapshot, p2_state, p1_state, p2_result_queue), daemon=True)
                p1_thread.start()
                p2_thread.start()

                # Retrieve AI move decisions with timeout
                p1_thread.join(timeout=config.CONTROLLER_TIMEOUT_SECONDS)
                p2_thread.join(timeout=config.CONTROLLER_TIMEOUT_SECONDS)
                
                try:
                    p1_direction = p1_result_queue.get_nowait()
                    
                    if p1_direction is None:
                        print("Player 1 controller failed to return a valid result. Using current direction.")
                        p1_direction = player1.snake.direction
                        
                except queue.Empty:
                    print("Player 1 controller timed out. Using current direction.")
                    p1_direction = player1.snake.direction

                try:
                    p2_direction = p2_result_queue.get_nowait()
                    
                    if p2_direction is None:
                        print("Player 2 controller failed to return a valid result. Using current direction.")
                        p2_direction = player2.snake.direction
                        
                except queue.Empty:
                    print("Player 2 controller timed out. Using current direction.")
                    p2_direction = player2.snake.direction
                    
                # Apply directions and move snakes
                player1.snake.direction = p1_direction
                player2.snake.direction = p2_direction
                player1.snake.move()
                player2.snake.move()

                # Handle collisions, food, growth, deaths, etc.
                state.resolve_collisions()

        # Skip rendering updates after game ends
        if state.game_over:
            continue

    # --- Rendering ---
    screen.fill(colors.background_color)

    # Sudden Death Message Screen
    if state.pre_sudden_death_active:
        message_font = pygame.font.SysFont(None, 80, bold=True)
        message_surface = message_font.render("SUDDEN DEATH", True, "Red")
        message_rect = message_surface.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(message_surface, message_rect)

        remaining_message_time_ms = max(0, config.PRE_SUDDEN_DEATH_MESSAGE_DURATION - (pygame.time.get_ticks() - state.pre_sudden_death_start_time))
        seconds_left = (remaining_message_time_ms // 1000) + 1
        countdown_font = pygame.font.SysFont(None, 60)
        countdown_surface = countdown_font.render(str(seconds_left), True, "White")
        countdown_rect = countdown_surface.get_rect(center=(screen_width / 2, screen_height / 2 + 80))
        screen.blit(countdown_surface, countdown_rect)

    else:
        # Render Board
        game_board.draw(screen)

        # Update game timer
        if not state.game_over:
            if state.sudden_death_active:
                elapsed_sd_time_ms = pygame.time.get_ticks() - state.sudden_death_start_time
                elapsed_sd_seconds = elapsed_sd_time_ms // 1000
                minutes = elapsed_sd_seconds // 60
                seconds = elapsed_sd_seconds % 60
                timer_text = f"Sudden Death - {minutes:02}:{seconds:02}"
                timer_color = "White"
            else:
                elapsed_game_time_display = pygame.time.get_ticks() - game_start_time
                minutes = elapsed_game_time_display // 60000
                seconds = (elapsed_game_time_display % 60000) // 1000
                timer_text = f"{minutes:02}:{seconds:02}"
                timer_color = "Red" if elapsed_game_time_display > config.GAME_DURATION - 10000 else "White"
    
    # Render Title & Timer
    screen.blit(title_surface, (config.TITLE_POS_X, config.TITLE_POS_Y))
    timer_surface = timer_font.render(timer_text, True, timer_color)
    screen.blit(timer_surface, (config.TIMER_POS_X, config.TIMER_POS_Y))

    # Render Scores
    player1.draw_score(screen, {"x": config.PLAYER1_SCORE_POS_X, "y": config.PLAYER1_SCORE_POS_Y})
    player2.draw_score(screen, {"x": config.PLAYER2_SCORE_POS_X, "y": config.PLAYER2_SCORE_POS_Y})

    # Render Apples
    for apple in state.food_locations:
        apple.draw(game_board)

    # Render Obstacles
    for obstacle in state.obstacle_locations:
        obstacle.draw(game_board)

    # Render Snakes
    player1.snake.draw(game_board.board)
    player2.snake.draw(game_board.board)

    # Render Scorebar
    game_scorebar.draw(screen, player1, player2)

    # Game Over Overlay
    if state.game_over:
        game_over_screen.draw(screen, state.winner)

    # --- Display Update ---
    pygame.display.flip()
    clock.tick(config.FPS)

# --- Clean Exit ---
pygame.quit()