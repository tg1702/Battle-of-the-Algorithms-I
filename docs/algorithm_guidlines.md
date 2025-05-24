# Algorithm Guidelines

## General Notes
- The algorithm should implement **survival and food collection strategies**, prioritizing staying alive while collecting food efficiently.
- It should avoid hitting **walls, obstacles, and rival snakes**, while navigating the grid and making strategic decisions.
- The algorithm **will not have access to the game visuals** but will only interact with the game state passed to the controller.

## Time Limit
  Your algorithm must return the next move within **50 milliseconds**. If your algorithm does not respond within this limit, the snake will automatically continue moving in its previous direction. Optimize your code to run efficiently within this constraint.  
  *Note: All documentation, code, and configuration files use a 50ms timeout. Please disregard any older references to a 1-second limit.*

## Grid Alignment 
  The game is played on a fixed-size grid. The size of each grid cell is defined by the `GRID_SIZE` constant in `config/config.py`.  
  **All movement, positions, and calculations must use multiples of `GRID_SIZE`.**  
  - All snake positions, food, and obstacles are always aligned to this grid.
  - When moving or checking for collisions, always increment or compare positions using `GRID_SIZE` (not a hardcoded value).

## Move Format
  Your algorithm should return one of the following strings for each move: `"up"`, `"down"`, `"left"`, or `"right"`.  
  - Moves must correspond to valid grid directions (i.e., a single step along the grid).

## Initial Direction
  The snake starts moving in an initial direction. If no move is returned on the first turn, it will continue moving in that initial direction.

## Valid Moves 
  The snake cannot directly reverse direction (e.g., from `"left"` to `"right"` immediately). Such moves should be avoided, as they may be ignored or cause the snake to collide with itself.

## Determinism
  The game environment is fully deterministic, with no random factors influencing snake movement during a turn. All snake movements are controlled by your algorithm, except for the initial starting direction.

---

**Important:**  
- All coordinates provided to your controller (e.g., `head_position`, food, obstacles) are in pixel units, but are always aligned to the grid (i.e., multiples of `GRID_SIZE`).
- To stay compatible with different grid settings, never hardcode movement values—always use `GRID_SIZE` for movement calculations.