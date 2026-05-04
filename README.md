# Maze Race Simulator

## Overview
This project is a Python-based maze racing simulator that generates random mazes and compares the performance of two different pathfinding algorithms: Right-Wall Following and Flood-Fill. The system provides a real-time visualisation of both algorithms navigating the same maze environment, allowing direct comparison of their behaviour, efficiency, and decision-making strategies.

The project demonstrates key concepts in algorithm design, software development, and validation, particularly highlighting the contrast between rule-based and data-driven approaches to solving problems.

---

## Objectives
The main objectives of this project are:
- To generate complex, random mazes programmatically  
- To implement and compare two maze-solving algorithms  
- To visualise algorithm behaviour in real time  
- To evaluate differences in efficiency and path selection  
- To demonstrate structured software design and version control practices  

---

## Features
- **Random Maze Generation:**  
  Uses a recursive backtracking algorithm to create unique maze layouts for each run.

- **Dual Solver Comparison:**  
  Two independent algorithms solve the maze simultaneously:
  - **Right-Wall Following:** A simple rule-based navigation strategy  
  - **Flood-Fill:** A distance-based algorithm that finds an optimal path  

- **Real-Time Visualisation:**  
  Built with matplotlib to display:
  - Maze structure  
  - Solver paths  
  - Live movement of each solver  

- **Performance Measurement:**  
  Execution time is recorded for each solver, allowing direct comparison of efficiency.

---

## Algorithms Explained

### Right-Wall Following
This algorithm follows a local decision-making process:
1. Attempt to turn right  
2. Move forward if possible  
3. Turn left if needed  
4. Otherwise perform a U-turn  

- Simple and easy to implement  
- Does not guarantee optimal paths  
- Can result in loops or inefficient exploration  

---

### Flood-Fill Algorithm
This algorithm calculates a distance field from the goal:
- Each open cell is assigned a value representing distance to the goal  
- The solver moves to neighbouring cells with decreasing values  

- Always produces an optimal path  
- More computationally intensive  
- Demonstrates global path planning  

---

## Technologies Used
- **Python** – main programming language  
- **NumPy** – efficient numerical operations for maze representation  
- **Matplotlib** – real-time visualisation and simulation interface  

---

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
