# Ultimate Tic-Tac-Toe (Pygame)

An advanced, strategic version of Tic-Tac-Toe built with **Python** and **Pygame**. This project implements "Ultimate Tic-Tac-Toe," where each square of a 3 x 3 board contains a smaller Tic-Tac-Toe board.



## 📋 Features
* **Nested Logic**: The move you make in a local board dictates which board your opponent must play in next.
* **Interactive GUI**: Built using Pygame with real-time mouse event handling.
* **Visual Feedback**: Highlighting system to show valid move areas and board states.
* **Win Detection**: Complex algorithms to track wins across 9 local boards and 1 global board.

## 🛠️ Tech Stack
* **Language**: Python 3.x
* **Library**: Pygame
* **Version Control**: Git/GitHub

## 🚀 Getting Started

### Prerequisites
Ensure you have Python installed. You will also need the `pygame` library:
```bash
pip install pygame
```

## Installation
Clone the repository using SSH:
```bash
git clone git@github.com:anupam-sec/Ultimate-Tic-Tac-Toe-Game.git
```
Navigate to the project folder:
```bash
cd Ultimate-Tic-Tac-Toe-Game
```
Run the application:
```bash
python Ultimate_Tic_Tac_Toe.py
```

## 🎮 Game Rules
1. Win three local boards in a row to win the game.
2. Your opponent is sent to the local board corresponding to the square you just marked.
3. If you are sent to a board that is already full or won, you can play anywhere (Open Move).
