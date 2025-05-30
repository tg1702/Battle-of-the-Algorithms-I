# Battle of the Algorithms 🏆🐍

A 2 week AI coding tournament where developers compete by programming intelligent snakes for survival in a strategic grid-based game. Participants submit Python-based AI algorithms that navigate, collect food, and avoid obstacles while competing against rival snakes. The competition follows an elimination-style format, leading to a final showdown to determine the ultimate champion!  

## Competition Timeline
- 👩🏾‍💻 Coding Begins: May 25th @ 3pm
- 🗃 Coding Ends: June 7th @ 3pm
- 👾 Live Tournament: June 14th @ 6pm on Discord
- 👑 Winner Announced: June 14th (End of Live Tournament)
- 📹 Video Submissions: June  14th @ 11pm

## Key Features  

- ⚔️ **Elimination Tournament** – Compete head-to-head until only one remains  
- 🧠 **AI-Driven Snake Game** – Program your snake using decision-making & pathfinding  
- 🎯 **Survival & Strategy** – Avoid obstacles, collect food, and outlast opponents  
- 🔗 **Standardized API** – Integrate your AI seamlessly into the game environment  

## Getting Started
### Documentation Review
Before diving into the code, it's crucial to familiarize yourself with the tournament's rules and game design. The [Competition Brief](docs/competition_brief.md) outlines the objectives, rules, and guidelines for participation. When you're ready to implement your AI, refer to the [Controller API Documentation](docs/controller_api.md) and [Algorithm Guidelines](docs\algorithm_guidelines.md) for details on how to create your snake's controller and general algorithm guidelines.

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
- [Algorithm Guidelines](docs/algorithm_guidelines.md) – Guidelines for the creation of algorithms
- [Competition Brief](docs/competition_brief.md) – Overview of the tournament rules and game design
- [Controller API](docs/controller_api.md) – Understand how to implement your AI logic
- [Video Submission Guidelines](docs/video_submission_guidelines.md) – Overview of video submission guidelines

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
│   ├── obstacle.py
│   ├── player.py
│   ├── scorebar.py
│   └── snake.py
├── controllers/
│   ├── player1_controller.py
│   ├── player2_controller.py
│   └── example_controller.py
├── docs/
│   ├── algorithm_guidelines.md
│   ├── controller_api.md
│   ├── competition_brief.md
│   └── video_submission_guidelines.md
├── main.py
├── README.md
└── requirements.txt
```
