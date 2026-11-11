🪙 Race for Coins
Race for Coins is a small arcade game built with Python and Pygame.

The game was developed in the context of the MOOC Advanced Python Programming training as a practical exercise to apply Python programming concepts through game development.

You control a robot racing against a computer-controlled monster to collect coins scattered around the arena.

Teleportation doors can move you across the arena, while the monster continuously hunts for the closest coin and mysteriously blinks in and out of existence.

The first to collect 15 coins wins. 🤖 ⚔️ 👾

🎮 How to Play
Use the arrow keys to control the robot:

⬆️ Up Arrow — move up
⬇️ Down Arrow — move down
⬅️ Left Arrow — move left
➡️ Right Arrow — move right
Collect coins before the monster reaches them.

🚪 Teleportation Doors
Walking through a door transports your robot to its paired door on the other side of the arena.

Your movement direction is preserved when leaving the portal, so use the doors strategically to reach coins faster.

👾 The Monster
The monster automatically moves toward the closest available coin.

The monster also blinks. While invisible, it cannot collect coins, giving you a chance to get ahead.

🏆 Winning
The first player to collect 15 coins wins the match.

When the game ends, press Space to start a new match.

🚀 Installation
1. Clone the repository
git clone YOUR_REPOSITORY_URL

cd race-for-coins

2. Create a virtual environment
macOS / Linux:

python3 -m venv .venv

source .venv/bin/activate

Windows:

python -m venv .venv

.venv\Scripts\activate

3. Install the dependencies
pip install -r requirements.txt

4. Run the game
python game.py

📦 Requirements
The project uses Pygame.

The requirements.txt file contains:

pygame>=2.6,<3

📁 Project Structure
race-for-coins/

├── README.md

├── requirements.txt

├── .gitignore

├── game.py

└── assets/

    ├── robot.png

    ├── monster.png

    ├── coin.png

    └── door.png

✨ Features
🤖 Player-controlled robot
👾 Computer-controlled opponent
🪙 Dynamic coin spawning
🚪 Teleportation doors
✨ Blinking enemy mechanic
🏆 Score tracking
🔄 Quick match restart
🛠️ Built With
Python 3
Pygame
Have fun and grab the coins before the monster does! 🪙