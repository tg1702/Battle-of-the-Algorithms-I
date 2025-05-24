import config.config as config
import heapq
import itertools

def get_next_move(board_state, player_state, opponent_state):
    """Improves AI strategy with pathfinding, risk assessment, and opponent growth anticipation."""

    head_x, head_y = player_state["head_position"]["x"], player_state["head_position"]["y"]
    direction = player_state["direction"]
    player_body = set((segment["x"], segment["y"]) for segment in player_state["body"])
    player_length = len(player_state["body"])
    food_locations = set((f[0], f[1]) for f in board_state["food_locations"])
    board_width = board_state["width"]
    board_height = board_state["height"]

    opponent_body = set((segment["x"], segment["y"]) for segment in opponent_state["body"])
    opponent_head_x, opponent_head_y = opponent_state["head_position"]["x"], opponent_state["head_position"]["y"]
    opponent_length = len(opponent_state["body"])

    def is_safe(x, y, occupied):
        """Checks if a cell (x, y) is within bounds and not occupied."""
        return 0 <= x < board_width and 0 <= y < board_height and (x, y) not in occupied

    def get_neighbors(x, y):
        """Returns valid neighboring cells."""
        neighbors = [(x + config.GRID_SIZE, y, "right"), (x - config.GRID_SIZE, y, "left"),
                     (x, y + config.GRID_SIZE, "down"), (x, y - config.GRID_SIZE, "up")]
        return [(nx, ny, move) for nx, ny, move in neighbors if is_safe(nx, ny, player_body | opponent_body)]

    def get_safe_neighbors(x, y, occupied):
        """Returns only safe neighboring cells."""
        neighbors = [(x + config.GRID_SIZE, y), (x - config.GRID_SIZE, y),
                     (x, y + config.GRID_SIZE), (x, y - config.GRID_SIZE)]
        return [(nx, ny) for nx, ny in neighbors if is_safe(nx, ny, occupied)]

    def heuristic(a, b):
        """Manhattan distance heuristic."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star_path(start, goal, occupied):
        """A* pathfinding algorithm."""
        if not is_safe(goal[0], goal[1], occupied):
            return None

        open_set = [(heuristic(start, goal), 0, start, [])]  # f_score, g_score, current, path
        visited = {start}

        while open_set:
            f, g, current, path = heapq.heappop(open_set)

            if current == goal:
                return path + [current]

            x, y = current
            for nx, ny, move in get_neighbors(x, y): # Using get_neighbors to ensure only safe moves are considered
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    new_g = g + config.GRID_SIZE
                    new_f = new_g + heuristic((nx, ny), goal)
                    heapq.heappush(open_set, (new_f, new_g, (nx, ny), path + [current]))
        return None

    def assess_future_risk(x, y, occupied):
        """Estimates future collision risk by checking nearby safe spaces."""
        safe_neighbors = get_safe_neighbors(x, y, occupied)
        return len(safe_neighbors)

    def predict_opponent_head_moves():
        """Predicts potential next head positions of the opponent."""
        possible_opponent_moves = []
        ox, oy = opponent_head_x, opponent_head_y
        for dx, dy in [(config.GRID_SIZE, 0), (-config.GRID_SIZE, 0), (0, config.GRID_SIZE), (0, -config.GRID_SIZE)]:
            nx, ny = ox + dx, oy + dy
            if is_safe(nx, ny, player_body | opponent_body):
                possible_opponent_moves.append((nx, ny))
        return possible_opponent_moves

    def evaluate_move(next_head):
        """Evaluates a potential move based on safety, food proximity, and future risk."""
        if not is_safe(next_head[0], next_head[1], player_body | opponent_body):
            return -float('inf')

        score = 0

        # Food pursuit with opponent consideration
        closest_food = min(food_locations, key=lambda f: heuristic(next_head, f) - 0.7 * heuristic((opponent_head_x, opponent_head_y), f), default=None)
        if closest_food:
            score += 1 / (heuristic(next_head, closest_food) + 1) # Closer food is better, avoid division by zero

        # Encourage moves towards open spaces
        score += 0.1 * assess_future_risk(next_head[0], next_head[1], player_body)

        # Discourage moving towards predicted opponent head positions (anticipatory collision avoidance)
        predicted_opponent_heads = predict_opponent_head_moves()
        if next_head in predicted_opponent_heads and opponent_length >= player_length:
            score -= 5  # Heavily penalize moving towards a potentially larger opponent's next move

        return score

    # Prioritize finding a path to the closest food
    if food_locations:
        closest_food = min(food_locations, key=lambda f: heuristic((head_x, head_y), f) - 0.5 * heuristic((opponent_head_x, opponent_head_y), f))
        path_to_food = a_star_path((head_x, head_y), closest_food, player_body | opponent_body)

        if path_to_food and len(path_to_food) > 1:
            next_x, next_y = path_to_food[1]
            if next_x > head_x:
                return "right"
            elif next_x < head_x:
                return "left"
            elif next_y > head_y:
                return "down"
            elif next_y < head_y:
                return "up"

    # If no clear path to food or no food, consider other safe moves
    possible_moves = get_neighbors(head_x, head_y)
    if not possible_moves:
        return direction  # No safe moves, continue current direction

    move_evaluations = {move: evaluate_move((nx, ny)) for nx, ny, move in possible_moves}
    best_move = max(move_evaluations, key=move_evaluations.get)
    return best_move

def set_player_name():
    """Sets the player's name."""
    return "Blue"