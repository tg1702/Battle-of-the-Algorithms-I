import pygame
import board, scorebar, player, food
import colors

pygame.init()

# Screen Setup 
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakeAI")
clock = pygame.time.Clock()

running = True

# Board Setup
title_font = pygame.font.SysFont(None, 40)
title_surface = title_font.render("Battle of the Algorithms", True, "white")
board = board.Board(975, 510)
scorebar = scorebar.ScoreBar(350, 100, screen)
food_list = [food.Food(board) for _ in range(3)]

# Initialize Players
player1 = player.Player(1, "John", board)
player2 = player.Player(2, "Jenny", board)

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Fill Screen and Draw Game Board
    screen.fill(colors.background_color)
    board.draw(screen)

    # Render Text
    screen.blit(title_surface, (screen_width/2 - 165, 50))
    
    player1.draw_score(screen, {"x": 150, "y": 100})
    player2.draw_score(screen, {"x": screen_width - 270, "y": 100})
    
    # Draw Player Snakes
    player1.snake.draw(board.board)
    player2.snake.draw(board.board)
    
    for apple in food_list:
        if (board.occupied[apple.x // apple.size][apple.y // apple.size] == False):
            apple.draw(board)
        else:
            apple.x = 0
            apple.y = 0
            apple.draw(board)
    
    # Draw Score Bar
    scorebar.draw(screen, player1, player2)
    
    # Render Display
    pygame.display.flip()
    
    # Set Frame Rate
    clock.tick(60)
    
pygame.quit()