# controllers/basic_controller.py

def get_next_move(board_state, player_state, opponent_state):
    """
    A very basic snake controller.  It always tries to move right, unless
    that's not a safe move, in which case it tries down, then up, then left.
    If none of those are safe, it returns the current direction.

    Args:
        board_state (dict): Information about the game board.
        player_state (dict): Information about the current player's snake.
        opponent_state (dict): Information about the opponent's snake.

    Returns:
        str: The next direction ("left", "right", "up", "down").
    """
    head_x = player_state["head_position"]["x"]
    head_y = player_state["head_position"]["y"]
    direction = player_state["direction"]
    body = player_state["body"]

    def is_safe_move(x, y):
        """Checks if a move to (x, y) is safe (not out of bounds or self-collision)."""
        if x < 0 or x >= board_state["width"] or y < 0 or y >= board_state["height"]:
            return False
        for segment in body:
            if segment["x"] == x and segment["y"] == y:
                return False
        return True

    if direction != "left" and is_safe_move(head_x + 20, head_y):
        return "right"
    elif direction != "up" and is_safe_move(head_x, head_y + 20):
        return "down"
    elif direction != "down" and is_safe_move(head_x, head_y - 20):
        return "up"
    elif direction != "right" and is_safe_move(head_x - 20, head_y):
        return "left"
    else:
        return direction  # Stay in the same direction if no safe moves
    
def set_player_name():
    return "Player Name"