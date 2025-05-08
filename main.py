import pygame
import player
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
board_width = screen_width - 300
board_height = screen_height - 200
board = pygame.Surface((board_width, board_height))
border = pygame.Surface((board_width + 10, board_height + 10))
board_background = pygame.image.load("assets/board.png")
board_background = pygame.transform.scale(board_background, (board_width, board_height))

# Initialize Players
player1 = player.Player(1, "John", board)
player2 = player.Player(2, "Jenny", board)

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Set Screen and Border Color
    screen.fill(colors.background_color)
    border.fill(colors.border_color)
    
    # Draw Board
    screen.blit(border, (145, 165))
    screen.blit(board, (150, 170))
    board.blit(board_background, (0, 0))

    # Draw Player and Score Info
    screen.blit(title_surface, (screen_width/2 - 170, 50))
    
    player1.draw_score(screen, {"x": 150, "y": 100})
    player2.draw_score(screen, {"x": screen_width - 270, "y": 100})
    
    # Draw Player Snakes
    player1.snake.draw(board)
    player2.snake.draw(board)

    # Render Display
    pygame.display.flip()
    
    # Set Frame Rate
    clock.tick(60)
    
pygame.quit()