# Filename:       maze_race.py
# Description:    A Python application that generates a random maze and simulates
#                 two maze‑solving algorithms (Right‑Wall Following and Flood‑Fill)
# Version:        v3 (User input + Reset button)
# Date:           30/03/2026
# Author:         Sam Smith (ss5250)

from builtins import print
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches
import numpy as np
import random
import time

print('USERNAME SS5250')


# MAZE GENERATION
def generate_maze(size):
    maze = np.ones((size, size), dtype=int)

    def carve(x, y):
        maze[y][x] = 0
        dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)

    carve(0, 0)
    maze[size - 1][size - 1] = 0
    return maze


# DIRECTIONS
DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def open_cell(maze, x, y):
    size = maze.shape[0]
    return 0 <= x < size and 0 <= y < size and maze[y][x] == 0


# RIGHT-WALL SOLVER
def right_wall_step(maze, pos, direction):
    x, y = pos

    right_dir = (direction - 1) % 4
    dx, dy = DIRS[right_dir]
    if open_cell(maze, x + dx, y + dy):
        return (x + dx, y + dy), right_dir

    dx, dy = DIRS[direction]
    if open_cell(maze, x + dx, y + dy):
        return (x + dx, y + dy), direction

    left_dir = (direction + 1) % 4
    dx, dy = DIRS[left_dir]
    if open_cell(maze, x + dx, y + dy):
        return (x + dx, y + dy), left_dir

    return (x, y), (direction + 2) % 4


# FLOOD FILL (UNCHANGED)
def compute_flood_fill(maze):
    size = maze.shape[0]
    goal = (size - 1, size - 1)

    flood = {(x, y): 9999 for y in range(size) for x in range(size) if maze[y][x] == 0}
    flood[goal] = 0

    changed = True
    while changed:
        changed = False
        for (x, y), val in list(flood.items()):
            for dx, dy in DIRS:
                nx, ny = x + dx, y + dy
                if open_cell(maze, nx, ny):
                    if flood[(nx, ny)] + 1 < val:
                        flood[(x, y)] = flood[(nx, ny)] + 1
                        changed = True
    return flood


def flood_fill_step(maze, pos, flood):
    x, y = pos
    best = pos
    best_val = flood[pos]

    for dx, dy in DIRS:
        nx, ny = x + dx, y + dy
        if open_cell(maze, nx, ny) and flood[(nx, ny)] < best_val:
            best = (nx, ny)
            best_val = flood[(nx, ny)]
    return best


# RACE ENGINE
class MazeRace:

    def __init__(self, maze):
        self.maze = maze
        self.size = maze.shape[0]
        self.goal = (self.size - 1, self.size - 1)

        self.rw_pos = (0, 0)
        self.rw_dir = 0
        self.ff_pos = (0, 0)
        self.flood = compute_flood_fill(maze)

        self.rw_x, self.rw_y = [0], [0]
        self.ff_x, self.ff_y = [0], [0]

        self.running = False
        self.setup_plot()

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        plt.subplots_adjust(bottom=0.2)

        self.ax.imshow(self.maze, cmap='binary')

        self.ax.set_title("Maze Race: Right‑Wall (Red) vs Flood‑Fill (Green)")

        # Solver visuals
        self.rw_line, = self.ax.plot(self.rw_x, self.rw_y, 'r-', linewidth=3)
        self.ff_line, = self.ax.plot(self.ff_x, self.ff_y, 'g-', linewidth=3)

        # Buttons
        ax_start = plt.axes([0.05, 0.05, 0.25, 0.1])
        ax_stop = plt.axes([0.375, 0.05, 0.25, 0.1])
        ax_reset = plt.axes([0.7, 0.05, 0.25, 0.1])

        self.btn_start = Button(ax_start, 'START')
        self.btn_stop = Button(ax_stop, 'STOP')
        self.btn_reset = Button(ax_reset, 'RESET')

        self.btn_start.on_clicked(self.start)
        self.btn_stop.on_clicked(self.stop)
        self.btn_reset.on_clicked(self.reset)

    def start(self, event):
        if not self.running:
            print("Simulation started")
            self.rw_start = time.time()
            self.ff_start = time.time()
            self.running = True
            self.run_race()

    def stop(self, event):
        self.running = False

    def reset(self, event):
        """
        Generates a new maze and resets solver positions
        """
        print("Generating new maze...")

        self.maze = generate_maze(self.size)
        self.flood = compute_flood_fill(self.maze)

        self.rw_pos = (0, 0)
        self.ff_pos = (0, 0)

        self.rw_x, self.rw_y = [0], [0]
        self.ff_x, self.ff_y = [0], [0]

        self.ax.clear()
        self.ax.imshow(self.maze, cmap='binary')
        self.ax.set_title("Maze Race: Right‑Wall (Red) vs Flood‑Fill (Green)")

        self.rw_line, = self.ax.plot(self.rw_x, self.rw_y, 'r-', linewidth=3)
        self.ff_line, = self.ax.plot(self.ff_x, self.ff_y, 'g-', linewidth=3)

        plt.draw()

    def run_race(self):
        rw_finished = False
        ff_finished = False

        while self.running and not (rw_finished and ff_finished):

            if not rw_finished:
                self.rw_pos, self.rw_dir = right_wall_step(self.maze, self.rw_pos, self.rw_dir)
                self.rw_x.append(self.rw_pos[0])
                self.rw_y.append(self.rw_pos[1])
                self.rw_line.set_data(self.rw_x, self.rw_y)

                if self.rw_pos == self.goal:
                    rw_finished = True
                    print(f"Right‑wall finished in {time.time() - self.rw_start:.4f}s")

            if not ff_finished:
                self.ff_pos = flood_fill_step(self.maze, self.ff_pos, self.flood)
                self.ff_x.append(self.ff_pos[0])
                self.ff_y.append(self.ff_pos[1])
                self.ff_line.set_data(self.ff_x, self.ff_y)

                if self.ff_pos == self.goal:
                    ff_finished = True
                    print(f"Flood-fill finished in {time.time() - self.ff_start:.4f}s")

            plt.pause(0.03)

        self.running = False


# USER INPUT 
def get_maze_size():
    while True:
        try:
            size = int(input("Enter maze size (odd number > 5): "))
            if size > 5 and size % 2 == 1:
                print(f"Generating maze of size {size}...")
                return size
            else:
                print("Invalid input. Must be odd and >5.")
        except ValueError:
            print("Enter a valid number.")


# RUN
size = get_maze_size()
maze = generate_maze(size)
race = MazeRace(maze)
plt.show()
