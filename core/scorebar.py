import pygame

class ScoreBar:
    """
    Represents the score bar in the game, which visually represents the players' scores.
    The score bar is a rectangle divided into two parts, each representing one player's score.
    """
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.height = 35
        self.width = screen.get_width() * 0.45
    
    
    def draw(self, screen, player1, player2):
        """
        Draws the score bar on the given screen surface, representing the scores of two players.
        The score bar is divided into two parts, each representing one player's score, drawn in their respective colors.
        """
        
        total_score = player1.score + player2.score
        player1_percentage = 0.5
        player2_percentage = 0.5
        
        if total_score > 0:
            player1_percentage = player1.score/total_score
            player2_percentage = player2.score/total_score
            
        player1_bar = pygame.Rect(self.x, self.y, self.width * player1_percentage + 1, self.height)
        player1_bar_border = pygame.Rect(self.x, self.y, self.width * player1_percentage + 1, self.height)
        
        player2_bar = pygame.Rect(self.x + self.width - (self.width * player2_percentage), self.y, self.width * player2_percentage + 1, self.height)
        player2_bar_border = pygame.Rect(self.x + self.width - (self.width * player2_percentage), self.y, self.width * player2_percentage + 1, self.height)
        
        if player1.score > player2.score:
            pygame.draw.rect(screen, player1.color, player1_bar)
            pygame.draw.rect(screen, "white", player1_bar_border, 2)
        
            pygame.draw.rect(screen, player2.color, player2_bar)
            pygame.draw.rect(screen, "white", player2_bar_border, 2)
        else:
            pygame.draw.rect(screen, player2.color, player2_bar)
            pygame.draw.rect(screen, "white", player2_bar_border, 2)
        
            pygame.draw.rect(screen, player1.color, player1_bar)
            pygame.draw.rect(screen, "white", player1_bar_border, 2)