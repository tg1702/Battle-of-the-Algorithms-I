## Player Controller API Documentation

The player controller API defines how your snake's AI communicates with the game engine. Your controller must be implemented as a Python file (e.g., `player1_controller.py`) located in the `controllers/` directory.

## Making A Player Controller
Player controller files are Python files that contain the logic for how a snake in the game will behave.  These files are placed in the `controllers/` directory.

For example, a controller for player 1 would typically be named `player1_controller.py`, and a controller for player 2 would be named `player2_controller.py`.

# Controller File Structure
The controller files are structured to allow you to implement your own logic for the snake's behavior. The game engine will call the functions defined in these files to determine the snake's next move based on the current game state.

There are 3 player controller files in the `controllers/` directory:
- player1_controller.py
- player2_contoller.py 
- example.py

The `example.py` file is provided as a template for you to create your own controller. You can use this as a starting point for your own logic. It contains example functions and comments to help you understand how to implement your AI.

The `player1_controller.py` and `player2_controller.py` files are the ones that will be used in the game. You can implement your logic in the `player1_controller.py` and use the `player2_controller.py` file for testing purposes. Your test opponent can be any logic you want, including a random move generator or a more complex AI.

### `get_next_move` Function

Each controller file must define a function named `get_next_move` with the following signature:

```python
def get_next_move(board_state, player_state, opponent_state):
    # Your logic here
    return "direction"  # Must be "left", "right", "up", or "down"
```

This function is called by the game engine each frame to determine the snake's next move.

### Input Parameters

The `get_next_move` function receives the following input parameters:

* `board_state` (dict): Information about the game board.

* `player_state` (dict): Information about the current player's snake.

* `opponent_state` (dict): Information about the opponent's snake.

### Data Structures

Below is a detailed description of the data provided in the input dictionaries:

#### `board_state` (dict)

* `"width"` (int): The width of the game board in pixels.

* `"height"` (int): The height of the game board in pixels.

* `"food_locations"` (list of tuples): A list of tuples, where each tuple `(food_x, food_y)` represents the x and y coordinates (in pixels) of a food item on the board.

* `"player1_body"` (list of dicts): A list representing the segments of player 1's snake's body. Each element in the list is a dictionary with the following structure:

  * `"x"` (int): The x-coordinate (in pixels) of the snake segment.

  * `"y"` (int): The y-coordinate (in pixels) of the snake segment.

* `"player2_body"` (list of dicts): A list representing the segments of player 2's snake's body. Each element in the list is a dictionary with the following structure:
  * `"x"` (int): The x-coordinate (in pixels) of the snake segment.

  * `"y"` (int): The y-coordinate (in pixels) of the snake segment.

#### `player_state` (dict)

* `"head_position"` (dict):

  * `"x"` (int): The x-coordinate (in pixels) of the player's snake's head.

  * `"y"` (int): The y-coordinate (in pixels) of the player's snake's head.

* `"direction"` (str): The current direction the player's snake is moving. Possible values are: `"left"`, `"right"`, `"up"`, or `"down"`.

* `"body"` (list of dicts): A list representing the segments of the player's snake's body. Each element in the list is a dictionary with the following structure:

  * `"x"` (int): The x-coordinate (in pixels) of the snake segment.

  * `"y"` (int): The y-coordinate (in pixels) of the snake segment.

* `"score"` (int): The current score of the player.

#### `opponent_state` (dict)

* `"head_position"` (dict):

  * `"x"` (int): The x-coordinate (in pixels) of the opponent's snake's head.

  * `"y"` (int): The y-coordinate (in pixels) of the opponent's snake's head.

* `"direction"` (str): The current direction the opponent's snake is moving. Possible values are: `"left"`, `"right"`, `"up"`, or `"down"`.

* `"body"` (list of dicts): A list representing the segments of the opponent's snake's body. Each element in the list is a dictionary with the following structure:

  * `"x"` (int): The x-coordinate (in pixels) of the snake segment.

  * `"y"` (int): The y-coordinate (in pixels) of the snake segment.

* `"score"` (int): The current score of the opponent.

#### Return Value

The `get_next_move` function must return a string representing the direction the snake should move. The string must be one of the following:

* `"left"`

* `"right"`

* `"up"`

* `"down"`


### `set_player_name` Function

Each controller file must define a function named `set_player_name` with the following signature:

```python
def set_player_name():
    return "Your Name"
```
This function is called by the game engine to set the name of the snake. 

#### Return Value
The `set_player_name` function must return a string representing the name of the player. The string can be any valid Python string, but it should not contain any special characters or spaces.