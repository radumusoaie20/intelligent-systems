# Conway's Game of Life

from enum import Enum
import numpy as np

class GridValueFinder:
    def __init__(self, world: np.array):
        self.world = world

    def find_value(self, x: int, y: int):
        pass

class SimpleValueFinder(GridValueFinder):

    def find_value(self, x: int, y: int):
        rows = len(self.world)
        cols = len(self.world[0])

        if x > rows - 1 or x < 0:
            return None

        if y > cols - 1 or y < 0:
            return None

        return self.world[x][y]


class RulesApplier:
    def __init__(self, value_finder: GridValueFinder):
        self.finder = value_finder
    def apply(self, world: np.array, x: int, y: int) -> bool:
        pass

    def get_neighbours_indices(self, x: int, y: int) -> list[(int, int)]:
        """ Gets for the cell at (x, y) its neighbours indices using the `value_finder` """
        result = list([])

        # left neighbour
        if self.finder.find_value(x - 1, y) is not None:
            result.append((x - 1, y))

        # right neighbour
        if self.finder.find_value(x + 1, y) is not None:
            result.append((x + 1, y))

        # top neighbour
        if self.finder.find_value(x, y - 1) is not None:
            result.append((x, y - 1))

        # bottom neighbour
        if self.finder.find_value(x, y + 1) is not None:
            result.append((x, y + 1))

        # top-left neighbour
        if self.finder.find_value(x - 1, y - 1) is not None:
            result.append((x - 1, y - 1))

        # top-right neighbour
        if self.finder.find_value(x - 1, y + 1) is not None:
            result.append((x - 1, y + 1))

        # bottom-left neighbour
        if self.finder.find_value(x + 1, y - 1) is not None:
            result.append((x + 1, y - 1))

        # bottom-right neighbour
        if self.finder.find_value(x + 1, y + 1) is not None:
            result.append((x + 1, y + 1))

        return result




class OriginalRulesApplier:
    def apply(self, world: np.array, x, y) -> bool:
        pass




class ConwayGame:
    def __init__(self, x: int, y: int, rule: RulesApplier):
        self.alive = 1
        self.dead = 0

        self.rule = rule
        self.size_x = x
        self.size_y = y

        self.world: np.array = self.__init_grid()
    def __init_grid(self) -> np.array:
        return np.random.choice([self.alive, self.dead], size=(self.size_x, self.size_y))

    def apply_rules(self):
        new_world = self.world.copy()





