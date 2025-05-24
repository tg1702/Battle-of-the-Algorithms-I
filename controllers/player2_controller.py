import config.config as config
import heapq

def get_next_move(board_state, player_state, opponent_state):
    """AI strategy using A* pathfinding and risk/opponent awareness."""

    head = (player_state["head_position"]["x"], player_state["head_position"]["y"])
    direction = player_state["direction"]
    player_body = {(segment["x"], segment["y"]) for segment in player_state["body"]}
    opponent_body = {(segment["x"], segment["y"]) for segment in opponent_state["body"]}
    opponent_head = (opponent_state["head_position"]["x"], opponent_state["head_position"]["y"])

    board_width, board_height = board_state["width"], board_state["height"]
    food_locations = {tuple(f) for f in board_state["food_locations"]}
    all_occupied = player_body | opponent_body

    def is_safe(pos):
        x, y = pos
        return 0 <= x < board_width and 0 <= y < board_height and pos not in all_occupied

    def neighbors(pos):
        x, y = pos
        dirs = [("right", (x + config.GRID_SIZE, y)),
                ("left", (x - config.GRID_SIZE, y)),
                ("down", (x, y + config.GRID_SIZE)),
                ("up", (x, y - config.GRID_SIZE))]
        return [(name, nxt) for name, nxt in dirs if is_safe(nxt)]

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(start, goal):
        if not is_safe(goal):
            return None

        open_set = [(heuristic(start, goal), 0, start, [])]
        visited = {start}

        while open_set:
            _, g, current, path = heapq.heappop(open_set)
            if current == goal:
                return path + [current]

            for _, neighbor in neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    heapq.heappush(open_set, (g + 1 + heuristic(neighbor, goal), g + 1, neighbor, path + [current]))
        return None

    def future_risk(pos):
        return sum(1 for _, neighbor in neighbors(pos))

    def predict_opponent_moves():
        return {nxt for _, nxt in neighbors(opponent_head)}

    def evaluate(pos):
        if not is_safe(pos):
            return -float('inf')

        score = 0

        if food_locations:
            closest_food = min(
                food_locations,
                key=lambda f: heuristic(pos, f) - 0.7 * heuristic(opponent_head, f),
                default=None
            )
            if closest_food:
                score += 1 / (heuristic(pos, closest_food) + 1)

        score += 0.1 * future_risk(pos)

        if pos in predict_opponent_moves() and len(opponent_body) >= len(player_body):
            score -= 5

        return score

    # Try path to best food first
    if food_locations:
        target = min(
            food_locations,
            key=lambda f: heuristic(head, f) - 0.5 * heuristic(opponent_head, f),
        )
        path = a_star(head, target)
        if path and len(path) > 1:
            next_pos = path[1]
            dx, dy = next_pos[0] - head[0], next_pos[1] - head[1]
            if dx > 0: return "right"
            if dx < 0: return "left"
            if dy > 0: return "down"
            if dy < 0: return "up"

    # Fallback: safest move
    possible_moves = neighbors(head)
    if not possible_moves:
        return direction

    move_scores = {move: evaluate(pos) for move, pos in possible_moves}
    return max(move_scores, key=move_scores.get)

def set_player_name():
    return "Pink"
