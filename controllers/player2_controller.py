# This is the Player 1 AI controller file.
# Contestants should implement their snake AI logic within this file.
# Your code will determine Player 1's next move based on the provided game state.
#
# You will need to implement two functions:
# 1. `get_next_move(board_state_data, player_state_data, opponent_state_data)`:
#    This function should return the next direction for the snake ("up", "down", "left", or "right").
# 2. `set_player_name()`:
#    This function should return a string representing the name of your AI player.
#
# For more detailed information on the expected input and output formats,
# please refer to the documentation at `docs/controller_api.md`.
# Happy Coding!

from . import a_star
from config import config

def set_player_name():
    return "SnakeBot"


def print_grid(grid, start=None, goal=None):
    for r, row in enumerate(grid):
        line = ""
        for c, val in enumerate(row):
            if start and (r, c) == start:
                line += "S "
            elif goal and (r, c) == goal:
                line += "G "
            elif val == 1:
                line += ". "
            else:
                line += "# "
        print(line)
    print()

def get_next_move(board_state, player_state, opponent_state):
    head = player_state["head_position"]

    #if board_state["obstacle_locations"]:
    direction = player_state["direction"]

    obstacles = board_state["obstacle_locations"]
    fruits = board_state["food_locations"]

    rows = board_state["rows"]
    cols = board_state["cols"]

    body = player_state["body"]
    opponent_body = opponent_state["body"]

    grid = [[1 for c in range(cols)] for r in range(rows)]

    
    
    for ob in obstacles:
        grid[ob[0]][ob[1]] = 0

    
    for b in body:
        grid[b["row"]][b["col"]] = 0

    for o in opponent_body:
        grid[o["row"]][o["col"]] = 0      

    
    
    start = (head["row"], head["col"])

    fruits.sort(key=lambda x: (x[0] - head["row"])**2 + (x[1] - head["col"])**2)
    goal = (fruits[0][0], fruits[0][1])

   
    
    path = a_star.a_star(start, goal, grid)
    if path and len(path) > 1: 
        ans = path[1]
    elif path and len(path) == 1:
        ans = path[0]
    else:
        return direction

    

    if (start[0] + -1, start[1] + 0) == ans:
        if direction != "down": # accounting for snake bumping into itself
            direction = "up"
        else:
            direction = "right"
    elif (start[0] + 1, start[1] + 0) == ans:
        if direction != "up": # accounting for snake bumping into itself
            direction = "down"
        else:
            direction = "left"
    elif (start[0] + 0, start[1] + -1) == ans:
        if direction != "right": # accounting for snake bumping into itself
            direction = "left"
        else:
            direction = "down"
    elif (start[0] + 0, start[1] + 1) == ans:
        if direction != "left": # accounting for snake bumping into itself
            direction = "right"
        else:
            direction = "up"
    else:
        pass
        #print(start, ans)

            

    return direction
    # Default: keep moving in the current direction
    return player_state["direction"]