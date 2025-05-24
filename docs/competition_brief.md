# Introduction

The **Battle of the Algorithms** is an exhilarating week-long coding tournament that tests and celebrates developers' skills. Eight talented participants will compete head-to-head, striving to craft the most efficient and effective algorithms. Each developer will receive a standardized User Interface (UI) and Application Programming Interface (API) to integrate their solutions. The competition follows an elimination-style format, with contestants facing off in pairs until one emerges as the ultimate champion!

## Rules

### Elimination Style Tournament
- Two developers will compete head-to-head in each match. The winner advances, and the loser is eliminated.
- Matches will continue until the final showdown between the last two developers.

### Duration
- The competition spans a week, ensuring ample time for participants to develop and refine their algorithms.

### Final Competition
- At the end of the week, all algorithms will face off in a tournament mode to determine the ultimate champion.
- Each algorithm must operate autonomously during matches.

## Game Design

Participants will program an AI version of the classic **Snake game**, where the snake navigates a grid to survive and gather food while avoiding obstacles and rival snakes. Developers must focus on strategic decision-making, efficient pathfinding, and adaptability to succeed.

### Gameplay Mechanics

#### Objective
- The AI snake that survives the longest while collecting food wins.
- Algorithms should prioritize survival strategies while optimizing food collection.

#### Grid & Obstacles
- The game is played on a standardized grid with randomly placed obstacles to challenge navigation.

#### Food Placement
- Food ("apples") will spawn in varying quantities and locations on the grid.
- Multiple apples can spawn at a time.
- There will always be a minimum 3 apples on the grid.
- When an apple is collected, a new one will spawn in a random location.

#### Snake Collisions
- Developers must implement collision avoidance strategies to prevent the snake from hitting walls, obstacles, or rival snakes, while prioritizing food collection.

## Game Ending Rules

### Survival-Based
- The game ends when only one snake remains alive on the grid. This snake is declared the winner of the round.
- If multiple snakes are alive after **5 minutes**, the snake with the most food collected wins.

### Collision-Based
- If a snake collides with an obstacle, wall, or another snake, it loses - regardless of the food count.

### Time-Based
- Each round will terminate after **5 minutes**.
- If the time expires before a collision occurs, the snake with the highest food count at the time of expiration wins.

### AI Decision Time Limit
- Each AI has a **1-second time limit** to choose a new direction for the snake's movement.
- If a direction is not chosen within this time, the snake will continue moving in the previous direction.

### Sudden Death
- If a round reaches the time limit and there is no clear winner (**snakes have the same food count**), Sudden Death will be activated.
- One piece of food is placed on the grid for the snakes to compete for.
- The snake that collects the food first or survives the longest without collision will be declared the winner.

### Technical Failure
- If a participant’s algorithm crashes or behaves in a manner inconsistent with the rules, their snake will be disqualified unless it is proven to be a technical fault unrelated to their code.

## Algorithm Submission

To participate in the **Battle of the Algorithms**, each developer will need to submit their AI algorithm as a Python script that can be executed by the backend during match execution. Here are the key steps for submitting and integrating your algorithm into the tournament:

### File Format
- Participants must submit their AI algorithm in **Python script format**.
- The algorithm must utilize the provided **API** in the [Controller API Documentation](docs/controller_api.md) to interact with the game environment and make decisions based on the game state.

### File Naming Convention
- To avoid confusion, all algorithm files must follow a specific **naming convention**:
  - **Format**: `name_algorithm.py` (e.g., `alice_algorithm.py`).
  - This ensures easy identification and organization of submitted algorithms.


### Submission Method
- Players will send their algorithm file to the organizer via the following submission form: [File Submission](https://forms.gle/xHtAgJYsiFmvfpkc7).
- The file should be named clearly to identify the developer, following the naming convention mentioned above.
- No submissions will be accepted after the final deadline.

### API Integration
- The algorithm must adhere to the standardized **API** provided by the competition in the [Controller API Documentation](docs/controller_api.md). Specifically, it should include:
  - A function to return the **next move** for the snake based on the game state.
  - A function to return the **name** of the player.

### Algorithm Behavior
- The algorithm should implement **survival and food collection strategies**, prioritizing staying alive while collecting food efficiently.
- It should avoid hitting **walls, obstacles, and rival snakes**, while navigating the grid and making strategic decisions.
- The algorithm **will not have access to the game visuals** but will only interact with the game state passed to the controller.

### Testing and Debugging
- Before the tournament, it’s recommended to **test your algorithm** using the game setup provided.
- If there are errors in the final submission, the player will be notified, and a chance to **fix the issue** may be provided before the match begins - up to one day after the deadline.

### Algorithm Safety
- If an algorithm **crashes or behaves incorrectly** (e.g., infinite loops or inconsistent rules), the snake will be **disqualified** from the round unless proven to be a technical fault unrelated to the submitted algorithm.

### Submission Deadline
- All algorithm submissions **must be received before the final tournament starts**.
- **Late submissions will not be accepted**, and players will be disqualified.
