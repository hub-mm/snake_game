# Game of Snake in Python
A classic Snake Game implemented in Python using Tkinter for the GUI.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Screenshots](#screenshots)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Game Controls](#game-controls)
- [How to Play](#how-to-play)
- [High Score](#high-score-tracking)
- [Known Issues](#known-issues)
- [Future Improvements](#future-improvements)
- [Contact Information](#contact-information)

## Introduction
This Snake game is a modern take on the classic arcade game.
Navigate the snake to eat food, grow longer, and try to achieve the highest score possible.

## Features
- Simple and intuitive controls.
- Increasing difficulty as the snake grows.
- High score tracking saved between sessions.

## Screenshots
- **Game Play Screenshot**
![Game Play Image One](./img/game_play_1.png)
![Game Play Image Two](./img/game_play_2.png)


- **Game Over Screenshot**
![Game Over](./img/game_over.png)

## Requirements
- **Python 3.6 or later**
- **Tkinter** (usually included with Python on Windows and macOS)

## Installation
### Windows and macOS
1. Download and install Python from the [official website](https://www.python.org/downloads/).
2. Verify Python installation:
    ```bash
    python3 --version
    ```
### Linux
1. Install Python 3 and Tkinter
   - Debian/Ubuntu:
       ```bash
       sudo apt-get install python3 python3-tk
       ```
   - Fedora:
       ```bash
       sudo dnf install python3 python3-tkinter
       ```
   - Arch Linux:
       ```bash
       sudo pacman -S python tk
       ```
2. Verify installation:
    ```bash
    python3 --version
    python3 -m tkinter
    ```

3. Clone or download this repository to your local machine:
   ```bash
   git clone
   ```

## Running the Game
Navigate to the directory containing main.py file and run:
```bash
    python3 main.py
```

## Game Controls
- **Movement**
    - Arrow Keys: *Up, Down, Left, Right*
    - WASD Keys: *W (up), A (Left), S (Down), D (right)*

## How to Play
- **Objective:** Eat as much food as possible to grow longer and increase your score.
- **Gameplay:**
  - Use the keyboard controls to navigate the snake.
  - Avoid colliding with the walls or the snake's own body.
  - Each time the snake eats food, it grows longer and moves slightly faster.
- **Scoring:**
  - Earn points for each piece of food consumed.
  - Try to beat the high score!

## High Score Tracking
- The game saves the highest scored achieved in a file named highscore.txt.
- The high score is displayed on the game over screen and next to the score.
- **Reset High Score:** To reset the high score, delete the *highscore.txt* file.

## Known Issues
- **Tkinter Not Installed Error:**
  - If you receive an error about Tkinter not being installed, 
    follow the installation steps in the [Requirements](#Requirements) section.
- **Game Window Not Focusing:**
  - On some systems, the game window may not come to the front automatically.
    Click on the window to activate it.

## Future Improvements
- Add sound effects and background music.
- Implement different difficulty levels.
- Introduce obstacles and power-ups.
- Implement restart ability.

## Contact Information
- **GitHub:** [GitHub Profile: hub-mm](https://github.com/hub-mm) 