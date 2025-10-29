import copy
from random import random

import numpy as np
from fontTools.designspaceLib.types import clamp
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from particle_swarm.initialization import ParticleInitialization, RandomParticleInitialization
from particle_swarm.simulation_terminator import SimulationTerminator, IterationTerminator
from strategy import MapStrategy, PerlinNoiseMapStrategy



# Input params


class ParticleSwarm:
    def __init__(self, grid_width,  grid_height,
                map_strategy: MapStrategy=PerlinNoiseMapStrategy(10, 5),
                current_velocity_weight: float = 0.6,
                best_local_weight: float = 0.4,
                best_global_weight: float = 0.5,
                number_of_particles: int = 10,
                initialization_strategy: ParticleInitialization = RandomParticleInitialization(),
                search_minimum = False,
                simulation_terminator: SimulationTerminator = IterationTerminator(100),
                particle_size: int = 5):
        """
        Initializes a number of particles for the given grid of the given size
        :param grid_width: The width of the grid
        :param grid_height: The height of the grid
        :param map_strategy: The strategy used to initialize the grid's values (if none passed, it wil default to PerlinNoise strategy)
        :param current_velocity_weight: How much influence a cell current velocity has for the next position
        :param best_local_weight: How much influence a cell's best local has on the next position computation
        :param number_of_particles: The number of particles used
        :param best_global_weight:  How much influence the global best has on the next position for a cell
        :param number_of_particles: The number of particles used
        :param initialization_strategy: The strategy to initialize the particles positions
        :param search_minimum: If true, the particles will tend towards the minimum value in the grid, otherwise towards the maximum value
        :param simulation_terminator: The simulation terminator
        :param particle_size: The size of the particles when rendered
        """

        self.anim = None
        self.width = grid_width
        self.height = grid_height
        self.strategy = map_strategy or PerlinNoiseMapStrategy(5, 10)

        self.grid = self.strategy.initialize_map(self.width, self.height)

        self.local_weight = best_local_weight
        self.global_weight = best_global_weight
        self.velocity_weight = current_velocity_weight
        self.number_of_particles = number_of_particles

        self.particles = initialization_strategy.initialize(self.grid, self.number_of_particles)

        # get the highest(or lowest best value from the particles

        if search_minimum:
            self.best = min(self.particles, key=lambda p: self.f(p.local), default=None).position
        else:
            self.best = max(self.particles, key=lambda p: self.f(p.local), default=None).position

        self.search_minimum = search_minimum

        self.terminator = simulation_terminator

        self.fig, self.ax = plt.subplots()
        self.mat = self.ax.matshow(self.grid)


        px = [p.position[0] for p in self.particles]
        py = [p.position[1] for p in self.particles]
        self.scatter = plt.scatter(px, py, c='red', s=particle_size)

        plt.colorbar(self.mat, ax=self.ax, label='Noise Value')

        self.text = self.ax.text(2, 0, "", bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 2})

    def f(self, pos):
        return self.grid[pos[0]][pos[1]]

    def step(self):
        w = self.velocity_weight
        phi_p = self.local_weight
        phi_g = self.global_weight
        for p in self.particles:
            for d in range(2):
                rp = random()
                rg = random()
                p.velocity[d] = int(w * p.velocity[d] + phi_p * rp * (p.local[d] - p.position[d]) + phi_g * rg * (self.best[d] - p.position[d]))

            p.position[0] = clamp(p.position[0] + p.velocity[0], 0, self.width - 1)
            p.position[1] = clamp(p.position[1] + p.velocity[1], 0, self.height - 1)

            if self.search_minimum:
                if self.f(p.position) < self.f(p.local):
                    p.local = p.position.copy()
                    if self.f(p.local) < self.f(self.best):
                        self.best = p.local.copy()
            else:
                if self.f(p.position) > self.f(p.local):
                    p.local = p.position.copy()
                    if self.f(p.local) > self.f(self.best):
                        self.best = p.local.copy()

    def record(self, verbose):

        frames = []
        px = [p.position[0] for p in self.particles]
        py = [p.position[1] for p in self.particles]
        frames.append((px, py))

        if verbose:
            print(f"-- Step 0 --")
            print(f"Best Position: {self.best}")
            print(f"Best Value: {self.f(self.best)}")
            print("-----------")


        step = 1
        while not self.terminator.shall_terminate(self):
            self.step()
            px = [p.position[0] for p in self.particles]
            py = [p.position[1] for p in self.particles]
            frames.append((px, py))
            step += 1

            if verbose:
                print(f"-- Step {step} --")
                print(f"Best Position: {self.best}")
                print(f"Best Value: {self.f(self.best)}")
                print("-----------")

        return frames


    def run(self, frame_interval=50, save_path=None, verbose=False):
        """
        Runs the simulation
        :param frame_interval: The interval between each frame
        :param save_path: Where to save the animation (if not set, the animation will just be played)
        :param verbose: Whether to show print statements regarding the simulation for each step
        :return: A tuple composed of the simulation final best particle position and its value
        """
        frames = self.record(verbose)

        def update(frame):
            px, py = frames[frame]
            offsets = np.stack([px, py]).T
            self.scatter.set_offsets(offsets)
            self.text.set_text(f"Step {frame}")

            return self.mat, self.scatter, self.text


        self.anim = FuncAnimation(
            self.fig, update, frames=len(frames), interval=frame_interval
        )

        if save_path:
            self.anim.save(save_path)
        else:
            plt.show()

        return self.best, self.f(self.best)




