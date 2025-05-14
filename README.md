# Battle of the Algorithms 🏆🐍

A week-long AI coding tournament where developers compete by programming intelligent snakes for survival in a strategic grid-based game. Participants submit Python-based AI algorithms that navigate, collect food, and avoid obstacles while competing against rival snakes. The competition follows an elimination-style format, leading to a final showdown to determine the ultimate champion!  

## Key Features  

- ⚔️ **Elimination Tournament** – Compete head-to-head until only one remains  
- 🧠 **AI-Driven Snake Game** – Program your snake using decision-making & pathfinding  
- 🎯 **Survival & Strategy** – Avoid obstacles, collect food, and outlast opponents  
- 🔗 **Standardized API** – Integrate your AI seamlessly into the game environment  

## Getting Started
### Documentation Review
Before diving into the code, it's crucial to familiarize yourself with the tournament's rules and game design. The [Competition Brief](docs/competition_brief.md) outlines the objectives, rules, and guidelines for participation. When you're ready to implement your AI, refer to the [Controller API documentation](docs/controller_api.md) for details on how to create your snake's controller.

### Installation
1. Clone the Repository
```git clone https://github.com/TaigaTi/Battle-of-the-Algorithms-I.git```

2. Setup Virtual Environment
```python -m venv venv```

3. Start Virtual Environment
```.\venv\Scripts\Activate```

4. Install Requirements
```pip install -r requirements.txt```

5. Run SnakeAI
```python -m main```

## Documentation
- [Competition Brief](docs/competition_brief.md) – Overview of the tournament rules and game design
- [Controller API](docs/controller_api.md) – Understand how to implement your AI logic

## File Structure
```plaintext
snakeai/
├── config/
│   ├── config.py
│   └── colors.py
├── core/
│   ├── board.py
│   ├── food.py
│   ├── game_over_screen.py
│   ├── game_state.py
│   ├── player.py
│   ├── scorebar.py
│   └── snake.py
├── controllers/
│   ├── player1_controller.py
│   ├── player2_controller.py
│   └── example.py
├── docs/
│   ├── controller_api.md
│   └── competition_brief.md
├── main.py
├── README.md
└── requirements.txt
```
