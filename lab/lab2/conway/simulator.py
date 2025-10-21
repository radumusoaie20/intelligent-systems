from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from lab.lab2.conway import strategy
from lab.lab2.conway.dir_util import make_file_dir_if_not_exist
from lab.lab2.conway.environment import Environment
from lab.lab2.conway.strategy import ConwayStrategy


class Simulator:
    def __init__(self, width, height, life_strategy=ConwayStrategy(), initial_state=None):
        self.width = width
        self.height = height
        self.strategy = life_strategy
        self.environment = Environment(width, height)
        self.initialize_cells(initial_state)

        # Animation

        self.fig, self.ax = plt.subplots()

        states = [[cell.state for cell in row] for row in self.environment.grid]

        self.mat = self.ax.matshow(states, vmin=0, vmax=1)
        self.text = self.ax.text(0.5, 0.5, "", bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 2})

    def initialize_cells(self, initial_state):

        if initial_state is not None:

            for x in range(self.width):
                for y in range(self.height):
                    state = int(initial_state[x][y])
                    self.environment.grid[x][y] = state
                    self.environment.grid[x][y].strategy = strategy

    def __update(self, data):
        self.environment.step()
        states = [[cell.state for cell in row] for row in self.environment.grid]

        self.mat.set_data(states)
        self.text.set_text(f'Iteration {data}')
        return [self.mat]

    def run(self, frame_interval:int=100, iterations:int=40, filename:str="out/animation.gif"):
        """Runs and saves the simulation for the given number of iterations, spacing the frames at the given time interval."""
        animation = FuncAnimation(self.fig, self.__update, interval=frame_interval, save_count=iterations)

        make_file_dir_if_not_exist(filename)
        animation.save(filename)
