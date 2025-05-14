# controllers/player2_controller.py
import config.config as config

def get_next_move(board_state, player_state, opponent_state):
    """
    Determines the next move for Player 1's snake.  This version has some basic
    AI to avoid self-collisions and head towards food.

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
    food_locations = board_state["food_locations"]

    def is_safe_move(x, y):
        """Checks if a move to (x, y) is safe (not out of bounds or self-collision)."""
        if x < 0 or x >= board_state["width"] or y < 0 or y >= board_state["height"]:
            return False
        for segment in body:
            if segment["x"] == x and segment["y"] == y:
                return False
        return True

    def get_possible_moves():
        """Gets a list of safe possible moves."""
        moves = []
        if direction != "left" and is_safe_move(head_x + config.GRID_SIZE, head_y):
            moves.append("right")
        if direction != "right" and is_safe_move(head_x - config.GRID_SIZE, head_y):
            moves.append("left")
        if direction != "up" and is_safe_move(head_x, head_y + config.GRID_SIZE):
            moves.append("down")
        if direction != "down" and is_safe_move(head_x, head_y - config.GRID_SIZE):
            moves.append("up")
        return moves

    def get_closest_food():
        """Finds the closest food to the snake's head."""
        if not food_locations:
            return None
        closest_food = food_locations[0]
        min_distance = float('inf')
        for food_x, food_y in food_locations:
            distance = abs(food_x - head_x) + abs(food_y - head_y)
            if distance < min_distance:
                min_distance = distance
                closest_food = (food_x, food_y)
        return closest_food

    possible_moves = get_possible_moves()
    if not possible_moves:
        return direction  # Stay in the same direction if no safe moves

    closest_food = get_closest_food()
    if closest_food:
        food_x, food_y = closest_food
        dx = food_x - head_x
        dy = food_y - head_y

        if abs(dx) > abs(dy):
            if dx > 0 and "right" in possible_moves:
                return "right"
            elif dx < 0 and "left" in possible_moves:
                return "left"
        else:
            if dy > 0 and "down" in possible_moves:
                return "down"
            elif dy < 0 and "up" in possible_moves:
                return "up"

    return possible_moves[0]  # If no food-directed move, take the first safe move