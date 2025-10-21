import random
from lab.lab2.conway.cell import Cell

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y, random.randint(0, 1)) for y in range(height)] for x in range(width)]



    def get_neighbors(self, x, y):
        """Returns the neighbors of the cell at (x, y).
        :param x: x coordinate
        :param y: y coordinate"""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append(self.grid[nx][ny])

        return neighbors

    def step(self):
        """Updates the environment based on the current cell states."""
        next_states = [
            [cell.decide_next_state(self) for cell in row]
            for row in self.grid
        ]
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                cell.state = next_states[x][y]
