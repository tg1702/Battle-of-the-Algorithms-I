# This is the Player 2 AI controller file.
# You can implement your snake AI logic here to test playing against an opponent.
# This is useful for developing and debugging your Player 1 AI.
#
# Similar to Player 1, you will need to implement:
# 1. `get_next_move(board_state_data, player_state_data, opponent_state_data)`
# 2. `set_player_name()`
#
# Refer to `docs/controller_api.md` for more details.
# Good Luck!
import random
import config

def set_player_name():
    return "SnakeBot"

def get_next_move(board_state, player_state, opponent_state):
    head = player_state["head_position"]
    #if board_state["obstacle_locations"]:
    direction = player_state["direction"]

    if head["x"] + 10 >= board_state["width"] and direction == "right":
        direction = "down" 
    if head["y"] + 60 >= board_state["height"] and direction == "down":
        direction = "left"
    if head["y"] - 10 <= 0 and direction == "up":
        direction = "right"
    if head["x"] - 10 <= 0 and direction == "left":
        direction = "down"

            
    if board_state["food_locations"]:
        obs = board_state["food_locations"]
        obs.sort(key=lambda x: abs(x[0] - head["x"]) + abs(x[1] - head["y"]))
        target_x, target_y = obs[0]
        if target_x < head["x"]:
            return "left"
        elif target_x > head["x"]:
            return "right"
        elif target_y < head["y"]:
            return "up"
        elif target_y > head["y"]:
            return "down"

    return direction


"""


        obs = board_state["obstacle_locations"]
        obs.sort(key=lambda x: x[0], reverse=True)
        #print("obs = ", obs)

        food = board_state["food_locations"]
        food.sort(key=lambda x: x[0], reverse=True)
        #print("food = " , food)

        if player_state["direction"] == "left":
            for o in obs:
                if head["x"] - 30 < o[0] * 15:
                    return "down"
        
        if player_state["direction"] == "right":
            for o in obs:
                if head["x"] + 30 < o[0] * 15:
                    return "down"

        if player_state["direction"] == "up":
            for o in obs:
                if head["y"] - 30 < o[0] * 15:
                    return "right"
        
        if player_state["direction"] == "down":
            for o in obs:
                if head["y"] + 30 < o[0] * 15:
                    return "right"
"""