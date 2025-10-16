import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

alive = 1
dead = 0

class GridValueFinder:

    def find_value(self, world: np.array, x: int, y: int):
        pass

class SimpleValueFinder(GridValueFinder):

    def find_value(self, world: np.array, x: int, y: int):
        rows = len(world)
        cols = len(world[0])

        if x > rows - 1 or x < 0:
            return None

        if y > cols - 1 or y < 0:
            return None

        return world[x,y]


class RulesApplier:
    def __init__(self, value_finder: GridValueFinder):
        self.finder = value_finder
    def shall_live(self, world: np.array, x: int, y: int) -> bool:
        """ Returns `True` if the cell at [x, y] shall live, `False` otherwise. """
        pass

    def get_neighbours_indices(self, world: np.array, x: int, y: int) -> list[(int, int)]:
        """ Gets for the cell at (x, y) its neighbours indices using the `value_finder` """
        result = list([])

        # left neighbour
        if self.finder.find_value(world, x - 1, y) is not None:
            result.append((x - 1, y))

        # right neighbour
        if self.finder.find_value(world, x + 1, y) is not None:
            result.append((x + 1, y))

        # top neighbour
        if self.finder.find_value(world, x, y - 1) is not None:
            result.append((x, y - 1))

        # bottom neighbour
        if self.finder.find_value(world, x, y + 1) is not None:
            result.append((x, y + 1))

        # top-left neighbour
        if self.finder.find_value(world, x - 1, y - 1) is not None:
            result.append((x - 1, y - 1))

        # top-right neighbour
        if self.finder.find_value(world, x - 1, y + 1) is not None:
            result.append((x - 1, y + 1))

        # bottom-left neighbour
        if self.finder.find_value(world, x + 1, y - 1) is not None:
            result.append((x + 1, y - 1))

        # bottom-right neighbour
        if self.finder.find_value(world, x + 1, y + 1) is not None:
            result.append((x + 1, y + 1))

        return result



class OriginalRulesApplier(RulesApplier):
    def shall_live(self, world: np.array, x, y) -> bool:
        indices = self.get_neighbours_indices(world, x, y)

        alive_neighbours = 0
        is_cell_alive = world[x, y]
        for index in indices:
            n_x, ny = index
            value = world[n_x, ny]
            if value == alive:
                alive_neighbours += 1

        if alive_neighbours < 2 and is_cell_alive:
            return False

        if (alive_neighbours == 2 or alive_neighbours == 3) and is_cell_alive:
            return True

        if alive_neighbours > 3 and is_cell_alive:
            return False

        if alive_neighbours == 3 and not is_cell_alive:
            return True

        # Assuming that a dead cell won't be able to become a live cell if the neighbours are less than 3
        return False



class ConwayGame:
    def __init__(self, x: int, y: int, rule: RulesApplier, filename: str = "test", iterations: int = 40):

        self.rule = rule
        self.size_x = x
        self.size_y = y

        self.world: np.array = self.__init_grid()
        self.filename: str = filename
        self.iterations: int = iterations

        # For animation

        self.fig, self.ax = plt.subplots()
        self.mat = self.ax.matshow(self.world, vmin=0, vmax=1)
        self.text = self.ax.text(0, 0, "", bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 2})

    def __init_grid(self) -> np.array:
        return np.random.choice([alive, dead], size=(self.size_x, self.size_y))

    def step(self):
        new_world = self.world.copy()
        for i in range(self.size_x):
            for j in range(self.size_y):
                will_live = self.rule.shall_live(self.world, i, j)
                if will_live:
                    new_world[i, j] = alive
                else:
                    new_world[i, j] = dead

        return new_world

    def update(self, data):
        self.world = self.step()
        self.mat.set_data(self.world)
        self.text.set_text(f'Iteration {data}')
        return[self.mat]


    def run(self):
        animation = FuncAnimation(self.fig, self.update, interval=1000, save_count=self.iterations)
        animation.save(f"{self.filename}.gif")









