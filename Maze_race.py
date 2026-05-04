
# Filename:       maze_race.py
# Description:    A Python application that generates a random maze and simulates
#                 two maze‑solving algorithms (Right‑Wall Following and Flood‑Fill)
# Date:           30/03/2026
# Author:         Sam Smith (ss5250)


from builtins import print
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.patches as patches
import numpy as np
import random
import time
print ('USERNAME SS5250')

# MAZE GENERATION 

def generate_maze(size):
    """
    Generates a random maze using a recursive backtracking algorithm
    
    """

    maze = np.ones((size, size), dtype=int)

    def carve(x, y):
        """    
        carves paths in the maze by moving to nearby cells in a random order.
        Every time it moves, it removes the wall between the current cell and the
        next one. This creates a random maze.
       
        """
        maze[y][x] = 0
        dirs = [(2,0),(-2,0),(0,2),(0,-2)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and maze[ny][nx] == 1:
                maze[y + dy//2][x + dx//2] = 0
                carve(nx, ny)

    carve(0, 0)
    maze[size-1][size-1] = 0
    return maze


# DIRECTIONS 

DIRS = [(1,0), (0,1), (-1,0), (0,-1)]

def open_cell(maze, x, y):
    """
    Checks whether a given cell is inside the maze boundaries and not a wall.
    
    Args:
        maze (np.ndarray): The maze grid.

    Returns:
        bool: True if the cell is open and accessible.
    """
    size = maze.shape[0]
    return 0 <= x < size and 0 <= y < size and maze[y][x] == 0



# RIGHT-WALL SOLVER 

def right_wall_step(maze, pos, direction):
    """
    Performs a single step of the right wall following algorithm.

    The solver attempts to (in order):
        1. Turn right if possible,
        2. Move straight if possible,
        3. Turn left if possible,
        4. Otherwise perform a U turn.

    Args:
        maze (np.ndarray): Maze grid.
        pos (tuple[int, int]): Current position (x, y).
        direction (int): Index into DIRS indicating current heading.

    Returns:
        tuple: (new_position, new_direction)
    """

    x, y = pos

    # Right turn
    right_dir = (direction - 1) % 4
    dx, dy = DIRS[right_dir]
    if open_cell(maze, x + dx, y + dy):
        return (x + dx, y + dy), right_dir

    # Straight
    dx, dy = DIRS[direction]
    if open_cell(maze, x + dx, y + dy):
        return (x + dx, y + dy), direction

    # Left
    left_dir = (direction + 1) % 4
    dx, dy = DIRS[left_dir]
    if open_cell(maze, x + dx, y + dy):
        return (x + dx, y + dy), left_dir

    # U-turn
    return (x, y), (direction + 2) % 4



# FLOOD FILL 

def compute_flood_fill(maze):
    """
    Computes a distance field

    Each open cell is assigned a number representing its shortest path distance
    to the goal.

    Args:
        maze (np.ndarray): Maze grid.

    Returns:
        dict: Mapping (x, y) -> distance-to-goal
    """

    size = maze.shape[0]
    goal = (size - 1, size - 1)

    flood = { (x, y): 9999 for y in range(size) for x in range(size) if maze[y][x] == 0 }
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
    """
    Takes a single step along the steepest descent of the previously computed
    flood fill distance field.

    Args:
        maze (np.ndarray): Maze grid.
        pos (tuple[int, int]): Current position.
        flood (dict): Mapping of cells to distance values.

    Returns:
        tuple[int, int]: New position after moving to the best neighbour.
    """

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
    """
    Controls the maze race simulation. Displays the maze, draws two solver
    paths, and runs both algorithms simultaneously until they reach the goal.
        
    """

    def __init__(self, maze):
        """
        Initialises solver state, computes flood fill map.

        Args:
            maze (np.ndarray): The maze grid to race through.
        """

        self.maze = maze
        self.size = maze.shape[0]
        self.goal = (self.size - 1, self.size - 1)

        # Solver states
        self.rw_pos = (0, 0)
        self.rw_dir = 0
        self.ff_pos = (0, 0)
        self.flood = compute_flood_fill(maze)

        self.rw_x, self.rw_y = [0], [0]
        self.ff_x, self.ff_y = [0], [0]

        self.running = False

        self.setup_plot()

    def setup_plot(self):
        """
        Sets up the matplotlib window, including the maze image, solver paths,
        actors, start/stop buttons, and titles.
        """

        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        plt.subplots_adjust(bottom=0.2)

        self.ax.imshow(self.maze, cmap='binary')

        # Start & end boxes
        self.ax.add_patch(patches.Rectangle((-0.5, -0.5), 1, 1, edgecolor='lime', facecolor='none', linewidth=2))
        self.ax.add_patch(patches.Rectangle((self.size-1.5, self.size-1.5), 1, 1, edgecolor='lime', facecolor='none', linewidth=2))

        self.ax.set_title("Maze Race: Right‑Wall (Red) vs Flood‑Fill (Green)")

        # Solver lines
        self.rw_line, = self.ax.plot(self.rw_x, self.rw_y, 'r-', linewidth=3)
        self.rw_dot, = self.ax.plot([0], [0], 'ro', markersize=6)

        self.ff_line, = self.ax.plot(self.ff_x, self.ff_y, 'g-', linewidth=3)
        self.ff_dot, = self.ax.plot([0], [0], 'go', markersize=6)

        # Buttons
        ax_start = plt.axes([0.1, 0.05, 0.35, 0.1])
        ax_stop = plt.axes([0.55, 0.05, 0.35, 0.1])

        self.btn_start = Button(ax_start, 'START')
        self.btn_stop = Button(ax_stop, 'STOP')

        self.btn_start.on_clicked(self.start)
        self.btn_stop.on_clicked(self.stop)

    def start(self, event):
        """
        Starts the race and sets timers for both solvers.
        """
        if not self.running:
            self.rw_start = time.time()
            self.ff_start = time.time()
            self.running = True
            self.run_race()

    def stop(self, event):
        """
        Stops the race mid simulation.
        """
        self.running = False

    def run_race(self):
        """
        Executes the simulation loop for both solvers until both finish or the
        stop button is pressed. Updates plot elements frame by frame.
        """

        rw_finished = False
        ff_finished = False

        while self.running and not (rw_finished and ff_finished):

            # Right‑wall solver
            if not rw_finished:
                self.rw_pos, self.rw_dir = right_wall_step(self.maze, self.rw_pos, self.rw_dir)
                self.rw_x.append(self.rw_pos[0])
                self.rw_y.append(self.rw_pos[1])
                self.rw_line.set_data(self.rw_x, self.rw_y)
                self.rw_dot.set_data([self.rw_pos[0]], [self.rw_pos[1]])

                if self.rw_pos == self.goal:
                    rw_finished = True
                    print(f"Right‑wall solver finished in {time.time() - self.rw_start:.4f} seconds")

            # Flood‑fill solver
            if not ff_finished:
                self.ff_pos = flood_fill_step(self.maze, self.ff_pos, self.flood)
                self.ff_x.append(self.ff_pos[0])
                self.ff_y.append(self.ff_pos[1])
                self.ff_line.set_data(self.ff_x, self.ff_y)
                self.ff_dot.set_data([self.ff_pos[0]], [self.ff_pos[1]])

                if self.ff_pos == self.goal:
                    ff_finished = True
                    print(f"Flood fill solver finished in {time.time() - self.ff_start:.4f} seconds")

            plt.pause(0.03)

        self.running = False



# RUN 

size = 21
maze = generate_maze(size)
race = MazeRace(maze)
plt.show()