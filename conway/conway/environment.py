import random
from conway.conway.cell import Cell
from conway.conway.neighbour import StandardNeighbourFinder


class Environment:
    def __init__(self, width, height, neighbour_finder=None):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y, random.randint(0, 1)) for x in range(height)] for y in range(width)]
        self.finder = neighbour_finder or StandardNeighbourFinder()


    def get_neighbors(self, x, y):
        """Returns the neighbors of the cell at (x, y).
        :param x: x coordinate
        :param y: y coordinate"""
        return self.finder.find_neighbours(x, y, self)

    def step(self):
        """Updates the environment based on the current cell states."""
        next_states = [
            [cell.decide_next_state(self) for cell in row]
            for row in self.grid
        ]
        for x, row in enumerate(self.grid):
            for y, cell in enumerate(row):
                cell.state = next_states[x][y]
