import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from conway.conway.cell import Cell
from conway.conway.dir_util import make_file_dir_if_not_exist
from conway.conway.environment import Environment
from conway.conway.strategy import ConwayStrategy
from conway.conway.neighbour import StandardNeighbourFinder


class ConwaySimulator:
    def __init__(self, width, height, life_strategy=ConwayStrategy(), initial_state=None,
                 neighbour_finder=StandardNeighbourFinder()):
        self.width = width
        self.height = height
        self.strategy = life_strategy
        self.environment = Environment(width, height, neighbour_finder)
        self.initialize_cells(initial_state)

        # Animation

        self.fig, self.ax = plt.subplots()

        states = self.__get_cells_states()

        self.mat = self.ax.matshow(states, vmin=0, vmax=1, origin='upper')
        self.text = self.ax.text(0.5, 0.5, "", bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 2})

    def initialize_cells(self, initial_state):

        if initial_state is not None:

            for x in range(self.height):
                for y in range(self.width):
                    state = int(initial_state[x][y])
                    self.environment.grid[x][y] = Cell(x, y, state)
                    self.environment.grid[x][y].strategy = self.strategy

    def __update(self, data):

        if data != 0:
            self.environment.step()
        states = self.__get_cells_states()

        self.mat.set_data(states)
        self.text.set_text(f'Iteration {data}')
        return [self.mat]

    def __get_cells_states(self):
        states = np.array([[cell.state for cell in row] for row in self.environment.grid])
        return states

    def run(self, frame_interval:int=100, iterations:int=40, filename:str=None) -> FuncAnimation:
        """Runs and returns the simulation for the given number of iterations, spacing the frames at the given time interval. If the filename parameter is not null, it will be saved to that file.
        :param frame_interval The interval between frames
        :param iterations The number of iterations to run the simulation for
        :param filename The name of the file where to save the simulation video (can include directories)"""
        animation = FuncAnimation(self.fig, self.__update, interval=frame_interval, save_count=iterations)

        if filename is not None:
            make_file_dir_if_not_exist(filename)
            animation.save(filename)

        return animation
