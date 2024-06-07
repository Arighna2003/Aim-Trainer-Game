# Aim Trainer Game

## Overview

The Aim Trainer Game is a simple yet engaging game designed to help players improve their aiming skills. This project utilizes the Pygame library to create an interactive environment where players must click on growing targets within a limited time and lives. The game consists of three levels, each increasing in difficulty and featuring different target growth rates and backgrounds. Additionally, sound effects enhance the user experience by providing audio feedback when targets are successfully hit.

## Features

- **Three Levels of Increasing Difficulty**: Each level introduces new backgrounds and target growth rates to challenge players progressively.
- **Interactive UI**: The game displays real-time statistics such as time elapsed, speed (targets per second), hits, and remaining lives.
- **Audio Feedback**: Players receive immediate auditory feedback upon hitting a target, enhancing the immersive experience.
- **Non-Overlapping Targets**: Targets are generated in positions ensuring they do not overlap, providing a fair challenge.
- **Responsive Design**: The game is designed to run smoothly at 60 frames per second, ensuring a seamless user experience.
- **End Screen Statistics**: Detailed statistics including accuracy and score are presented at the end of each level, motivating players to improve.

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/aim-trainer-game.git
   cd aim-trainer-game
2. **Install Dependencies**
   ```sh
    pip install pygame
3. **Run the Game**
   ```sh
   python aim_trainer.py

## How to Play
Level One: Targets appear and grow at a moderate rate. Click on them before they shrink back and disappear.

Level Two: Targets grow faster, requiring quicker reactions.

Level Three: Targets grow even faster, presenting the ultimate challenge.


For each level:
Click on the targets as they appear.
Avoid missing targets as it reduces your lives.
Check your performance in terms of time, speed, hits, and accuracy on the top bar.
Proceed to the next level by clicking the "Next Level" button on the end screen.

## Contributing
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add some feature').
5. Push to the branch (git push origin feature-branch).
6. Open a Pull Request.

## License
This project is licensed under the [LICENSE]{MIT License}

## Acknowledgements
Pygame - The library used to create this game.
Sound effects sourced from freesound.org.
