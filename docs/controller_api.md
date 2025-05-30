# Player Controller API Documentation

## Table of Contents
- [Introduction](#introduction)
- [How the Controller Works](#how-the-controller-works)
- [Controller File Structure](#controller-file-structure)
- [Required Functions](#required-functions)
- [Data Structures](#data-structures)
- [Return Values](#return-values)
- [Example Controller](#example-controller)
- [Tips and Best Practices](#tips-and-best-practices)
- [Additional Resources](#additional-resources)

---

## Introduction

This document describes how to create a Python AI controller for the Battle of the Algorithms I - Snake AI competition. Each controller determines the snake's direction of movement and provides a player name.

---

## How the Controller Works

- Player controller files are Python files that contain the logic for how a snake in the game will behave. These files are placed in the `controllers/` directory.

- The game engine will import your controller and call specific functions (`get_next_move`, `set_player_name`) as needed.
- The engine passes game state data to your controller every frame and expects a move in response.

---

## Controller File Structure

There are 3 player controller files in the `controllers/` directory:
- player1_controller.py
- player2_controller.py 
- example_controller.py

The `example_controller.py` file is provided as a template for you to create your own controller. You can use this as a starting point for your own logic. It contains example functions and comments to help you understand how to implement your AI.

The `player1_controller.py` and `player2_controller.py` files are the ones that will be used in the game. You can implement your logic in the `player1_controller.py` and use the `player2_controller.py` file for testing purposes. Your test opponent can be any logic you want, including a random move generator or a more complex AI.

---

## Required Functions

### `get_next_move`

```python
def get_next_move(board_state, player_state, opponent_state):
    # Your logic here
    return "direction"  # Must be "left", "right", "up", or "down"
```
This function is called every frame to determine your next move.

#### Parameters:
- **`board_state`**: a dictionary describing the board and environment.
- **`player_state`**: a dictionary with your snake’s data.
- **`opponent_state`**: a dictionary with your opponent’s data.

---

### `set_player_name`

```python
def set_player_name():
    return "YourName" # Please keep it short and sweet :)
```
Called once at game start to set your snake’s display name.

---

## Data Structures
> **Note:**  
> All coordinates (such as positions for snakes, food, and obstacles) passed to the controller are now in **grid cell units** (row, col).
> You should perform all movement and position calculations using these grid cell indices to ensure your logic is compatible with the game’s rules.

### `board_state`
A dictionary containing info about the game world.

```python
{
    "width": int,              # Board width in pixels
    "height": int,             # Board height in pixels
    "rows": int,               # Board rows 
    "cols": int,               # Board columns 
    "food_locations": [        # List of (row, col) tuples for each food item (grid-based)
        (row1, col1), (row2, col2), ...
    ],
    "obstacle_locations": [    # List of (row, col) tuples for each occupied cell by obstacles (grid-based)
        (row1, col1), (row2, col2), ...
    ]
}
```

> **Note:**  
> **Food locations and obstacle locations are both provided as grid cell (row, col) tuples.**  
> You do **not** need to convert these values further.  
> 
> For example, if you receive a food location `(6, 5)`, it refers to the grid cell at row 6, column 5.

### `player_state` / `opponent_state`

A dictionary representing either your snake or your opponent. Structure is identical for both:

```python
{
    "id": int,                               # Player number (1 or 2)
    "head_position": {"row": int, "col": int},       # Current head position in grid cells
    "body": [                                       # List of segment positions, head first, in grid cells
        {"row": int, "col": int},
        ...
    ],
    "direction": "left"|"right"|"up"|"down",        # Current direction
    "score": int,                                   # Current score
    "length": int                                   # Number of body segments
}
```

---

## Return Values

`set_player_name` must return a string representing the name of your snake. `(e.g "Jane")`
- This value will be displayed on the scoreboard and match results.
- If any other data type is returned, the engine will ignore it and log an error.

`get_next_move` must return one of the following strings:
  - `"left"`
  - `"right"`
  - `"up"`
  - `"down"`
- Any other value will be ignored by the engine and logged as an error.

---

## Example Controller

```python
def set_player_name():
    return "SnakeBot"

def get_next_move(board_state, player_state, opponent_state):
    head = player_state["head_position"]
    if board_state["food_locations"]:
        target_row, target_col = board_state["food_locations"][0]
        if target_col < head["col"]:
            return "left"
        elif target_col > head["col"]:
            return "right"
        elif target_row < head["row"]:
            return "up"
        elif target_row > head["row"]:
            return "down"
    # Default: keep moving in the current direction
    return player_state["direction"]
```

---

## Tips and Best Practices

- **Handle Edge Cases:** Avoid walls and obstacles by checking `obstacle_locations` and board boundaries.
- **Be Efficient:** Your AI must return within the configured timeout (see `CONTROLLER_TIMEOUT_SECONDS` in config). Taking too long to return a move will result in a timeout and skipped turn.
- **Default Safely:** If you can't decide, continue in your current direction.

---

## Additional Resources

- Example Controller: [`controllers/example_controller.py`](../controllers/example_controller.py)
- Algorithm Guidelines:  [`algorithm_guidelines.md`](algorithm_guidelines.md)
- Python Docs: [python.org](https://docs.python.org/3/)

---