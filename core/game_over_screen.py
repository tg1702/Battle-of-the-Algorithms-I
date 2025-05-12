from config import config
import pygame
import colors

class GameOverScreen:
    """
    A class responsible for displaying the game over screen when the game ends. 
    It shows the winner's name and a "GAME OVER" message.
    """
    def __init__(self):
        return
        
       
    def draw(self, screen, winner):
        board_width = config.BOARD_WIDTH
        board_height = config.BOARD_HEIGHT
        
        game_over_screen_width = board_width - 300
        game_over_screen_height = board_height - 100
        
        
        if winner == None:
            winner_name = "Draw"
            game_over_color = "red"
        else:
            winner_name = winner.name
            game_over_color = winner.color
        
        title_font = pygame.font.SysFont(None, 40)
        game_over_title_surface = title_font.render("GAME OVER", True, "white")
        winner_font = pygame.font.SysFont(None, 32)
        game_over_winner_surface = winner_font.render(f"Winner: {winner_name}", True, game_over_color)
        
        
        game_over_screen = pygame.Surface((game_over_screen_width, game_over_screen_height))
        border = pygame.Surface((game_over_screen_width + 20, game_over_screen_height + 20))
    
        
        
        game_over_screen.fill(colors.border_color)
        border.fill(game_over_color)
        
        # Draw Game Over Screen
        screen.blit(border, (290, 210))
        screen.blit(game_over_screen, (300, 220))
        
        # Render Game Over Text
        screen.blit(game_over_title_surface, (config.SCREEN_WIDTH/2 - 80, 250))
        screen.blit(game_over_winner_surface, (config.SCREEN_WIDTH/2 - 75, 300))