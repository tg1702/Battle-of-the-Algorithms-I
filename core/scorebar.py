import pygame

class ScoreBar:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.height = 35
        self.width = screen.get_width() * 0.45
    
    
    def draw(self, screen, player1, player2):
        """
        Draws the score bar on the screen, which is a visual representation of the players' scores.
        
        The score bar is a rectangle divided into two parts, each representing one player's score.
        The length of each part is proportional to the player's score relative to the total score.
        The color of each part is the same as the player's color.
        """
        
        total_score = player1.score + player2.score
        player1_percentage = 0.5
        player2_percentage = 0.5
        
        if player1.score > 0:
            player1_percentage = player1.score/total_score or 0.50
        
        if player2.score > 0:
            player2_percentage = player2.score/total_score or 0.50
            
        player1_bar = pygame.Rect(self.x, self.y, self.width * player1_percentage + 1, self.height)
        player1_bar_border = pygame.Rect(self.x, self.y, self.width * player1_percentage + 1, self.height)
        
        player2_bar = pygame.Rect(self.x + self.width - (self.width * player2_percentage), self.y, self.width * player2_percentage + 1, self.height)
        player2_bar_border = pygame.Rect(self.x + self.width - (self.width * player2_percentage), self.y, self.width * player2_percentage + 1, self.height)
        
        pygame.draw.rect(screen, player1.color, player1_bar)
        pygame.draw.rect(screen, player2.color, player2_bar)
        
        pygame.draw.rect(screen, "white", player1_bar_border, 2)
        pygame.draw.rect(screen, "white", player2_bar_border, 2)