# Introduction

The **Battle of the Algorithms** is an exhilarating week-long coding tournament that tests and celebrates developers' skills. Eight talented participants will compete head-to-head, striving to craft the most efficient and effective algorithms. Each developer will receive a standardized User Interface (UI) and Application Programming Interface (API) to integrate their solutions. The competition follows an elimination-style format, with contestants facing off in pairs until one emerges as the ultimate champion.

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

#### Snake Collisions
- Developers must implement collision avoidance strategies to prevent the snake from hitting walls, obstacles, or rival snakes.

## Game Ending Rules

### Survival-Based
- The game ends when only one snake remains alive on the grid. This snake is declared the winner of the round.
- If multiple snakes are alive after **5 minutes**, the snake with the most food collected wins.

### Collision-Based
- If a snake collides with an obstacle, wall, or another snake, it loses - regardless of the food count.
- If two snakes collide head-on, the snake with the most food wins.

### Time-Based
- Each round will terminate after **5 minutes**.
- If the time expires before a collision occurs, the snake with the highest food count at the time of expiration wins.

### Sudden Death
- If a round reaches the time limit and there is no clear winner (**snakes have the same food count**), Sudden Death will be activated.
- One piece of food is placed on the grid for the snakes to compete for.
- The snake that collects the food first or survives the longest without collision will be declared the winner.

### Technical Failure
- If a participant’s algorithm crashes or behaves in a manner inconsistent with the rules, their snake is disqualified unless it is proven to be a technical fault unrelated to their code.

## Algorithm Submission

To participate in the **Battle of the Algorithms**, each developer will need to submit their AI algorithm as a Python script that can be executed by the backend during match execution. Here are the key steps for submitting and integrating your algorithm into the tournament:

### File Format
- Participants must submit their AI algorithm in **Python script format** (e.g., `player_name_algorithm.py`).
- The algorithm must be implemented as a **Python function or class** that interacts with the provided game state and returns a valid move for the snake (`up`, `down`, `left`, `right`).

### Submission Method
- Players will send their algorithm file to the organizer via **GitHub repository, email, or other file-sharing platforms**.
- The file should be named clearly to identify the developer (e.g., `player_name_algorithm.py`).

### API Integration
- The algorithm must adhere to the standardized **API** provided by the competition. Specifically, it should include:
  - A function to receive the **current game state** (e.g., snake positions, food, obstacles) and process this information.
  - A function to return the **next move** for the snake based on the game state.
- The **backend** will dynamically load and execute the algorithm files. It will pass the current game state to the algorithm and retrieve the next move (`up`, `down`, `left`, `right`) from the AI algorithm.

### Algorithm Behavior
- The algorithm should implement **survival and food collection strategies**, prioritizing staying alive while collecting food efficiently.
- It should avoid hitting **walls, obstacles, and rival snakes**, while navigating the grid and making strategic decisions.
- The algorithm **will not have access to the game visuals** but will only interact with the game state passed via the backend API.

### Testing and Debugging
- Before the tournament, it’s recommended to **test your algorithm** using the game setup provided. The algorithm should be able to run without errors and handle different game scenarios (**e.g., food collection, collision detection**).
- If there are errors in the algorithm, the player will be notified, and a chance to **fix the issue** may be provided before the match begins.

### Algorithm Safety
- If an algorithm **crashes or behaves incorrectly** (e.g., infinite loops or inconsistent rules), the snake will be **disqualified** from the round unless proven to be a technical fault unrelated to the code.

### File Naming Convention
- To avoid confusion, all algorithm files must follow a specific **naming convention**:
  - **Format**: `player_name_algorithm.py` (e.g., `alice_algorithm.py`).
  - This ensures easy identification and organization of submitted algorithms.

### Submission Deadline
- All algorithm submissions **must be received before the final tournament starts**.
- **Late submissions will not be accepted**, and players will be disqualified.

### File Uploading
- Once the organizer has received the algorithm files, they will manually reference the file paths and **initiate the matches via the backend system**.
- The backend will **"plug and play"** these files by loading them into the system and executing them against the game environment during matches.

