from config import config
from core.player import Player
from core.food import Food

class GameState:
    def __init__(self, board, player1, player2):
        self.board = board
        self.rows = self.board.rows
        self.cols = self.board.cols
        self.occupied = [[{} for _ in range(self.rows)] for _ in range(self.cols)]
        self.food_list = []
        self.game_over = False
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        
        for i in range(0, 3):
            self.food_list.append(Food())
            self.occupied[self.food_list[i].x // config.GRID_SIZE][self.food_list[i].y // config.GRID_SIZE] = self.food_list[i]