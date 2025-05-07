import pygame
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
score_font = pygame.font.SysFont(None, 25)
title_font = pygame.font.SysFont(None, 40)

# Title Text
title_surface = title_font.render("Battle of the Algorithms", True, "white")

# Player 1 Text 
player1_name_surface = score_font.render("Player 1 - Name", True, colors.player1_border_color)
player1_score_surface = score_font.render("Score: 0", True, "white")

# Player 2 Text
player2_name_surface = score_font.render("Player 2 - Name", True, colors.player2_border_color)
player2_score_surface = score_font.render("Score: 0", True, "white")
 
# Game Board Setup
board_width = screen_width - 300
board_height = screen_height - 200
board = pygame.Surface((board_width, board_height))
border = pygame.Surface((board_width + 10, board_height + 10))
board_background = pygame.image.load("assets/board.png")
board_background = pygame.transform.scale(board_background, (board_width, board_height))

# Snake Position
snake_x = 0
snake_y = 0

while running:
    # Poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Set Screen and Border Color
    screen.fill(colors.background_color)
    border.fill(colors.border_color)
    
    # Draw Player and Score Info
    screen.blit(title_surface, (screen_width/2 - 170, 50))
    
    screen.blit(player1_name_surface, (150, 100))
    screen.blit(player1_score_surface, (150, 125))
    
    screen.blit(player2_name_surface, (screen_width - 270, 100))
    screen.blit(player2_score_surface, (screen_width - 270, 125))
    
    # Render Player 1
    snake = pygame.Rect(snake_x, snake_y, 15, 15)
    pygame.draw.rect(board, colors.player1_color, snake)
    pygame.draw.rect(board, colors.player1_border_color, snake, 2)
    
    # Render Player 2
    snake = pygame.Rect(board_width - 15, board_height - 15, 15, 15) # FIX THIS PLEEK
    pygame.draw.rect(board, colors.player2_color, snake)
    pygame.draw.rect(board, colors.player2_border_color, snake, 2)
    
    # Draw Board
    screen.blit(border, (145, 165))
    screen.blit(board, (150, 170))
    board.blit(board_background, (0, 0))

    # Render Display
    pygame.display.flip()
    
    # Set Frame Rate
    clock.tick(60)
    
pygame.quit()