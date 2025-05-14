from config import config
import pygame
import config.colors as colors

class GameOverScreen:
    """
    A class responsible for displaying the game over screen when the game ends. 
    It shows the winner's name and a "GAME OVER" message.
    """
    def __init__(self):
        board_width = config.BOARD_WIDTH
        board_height = config.BOARD_HEIGHT
        self.width = board_width - 300
        self.height = board_height - 100
        self.restart_button = pygame.Rect(self.width/3, 300, self.width/3, 40)
        self.surface = pygame.Surface((self.width, self.height))
        self.border = pygame.Surface((self.width + 20, self.height + 20))
       
    def draw(self, screen, winner):
        # Select Border Color
        if winner == None:
            winner_name = "Draw"
            game_over_color = "red"
        else:
            winner_name = winner.name
            game_over_color = winner.snake.border_color
        
        # Define Text
        title_font = pygame.font.SysFont(None, 40)
        game_over_title_surface = title_font.render("GAME OVER", True, "white")
        
        winner_font = pygame.font.SysFont(None, 32)
        game_over_winner_surface = winner_font.render(f"Winner: {winner_name}", True, game_over_color)
        
        restart_font = pygame.font.SysFont(None, 28)
        restart_surface = restart_font.render("Restart", True, (53, 53, 53))
    
        # Select Colors
        self.surface.fill(colors.border_color)
        self.border.fill(game_over_color)
        
        # Draw Crown
        crown = pygame.image.load("assets/crown.png")
        crown = pygame.transform.scale(crown, (200, 200))
        self.surface.blit(crown, (self.width/2 - 100, 60))
        
        # Restart Button        
        pygame.draw.rect(self.surface, game_over_color, self.restart_button)
        
        # Render Game Over Text
        self.surface.blit(game_over_title_surface, (self.width/2 - 80, 50))
        self.surface.blit(game_over_winner_surface, (self.width/2 - 70, 250))
       
        # Draw Game Over Screen
        screen.blit(self.border, (290, 210))
        screen.blit(self.surface, (300, 220))
        screen.blit(restart_surface, (config.SCREEN_WIDTH/2 - 30, 530))
        
        