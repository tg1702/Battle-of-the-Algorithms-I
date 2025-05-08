import pygame
import board, player
import colors

pygame.init()

# Screen Setup 
screen_width = 1280
screen_height = 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SnakeAI")
clock = pygame.time.Clock()

running = True

# Font Setup
title_font = pygame.font.SysFont(None, 40)

# Title Text
title_surface = title_font.render("Battle of the Algorithms", True, "white")

# Game Board Setup
board = board.Board(screen_width - 300, screen_height - 200)

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

    # Draw Player and Score Info
    screen.blit(title_surface, (screen_width/2 - 170, 50))
    
    player1.draw_score(screen, {"x": 150, "y": 100})
    player2.draw_score(screen, {"x": screen_width - 270, "y": 100})
    
    # Draw Player Snakes
    player1.snake.draw(board.board)
    player2.snake.draw(board.board)

    # Render Display
    pygame.display.flip()
    
    # Set Frame Rate
    clock.tick(60)
    
pygame.quit()