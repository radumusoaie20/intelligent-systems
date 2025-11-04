from random import random, uniform

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from swarm.particle_swarm.dir_util import make_file_dir_if_not_exist
from swarm.particle_swarm.initialization import ParticleInitialization, RandomParticleInitialization
from swarm.particle_swarm.simulation_terminator import SimulationTerminator, IterationTerminator
from swarm.particle_swarm.strategy import MapStrategy, PerlinNoiseMapStrategy

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
                particle_size: int = 5,
                velocity_max_magnitude=None,
                random_local: float = None,
                random_global: float = None):
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
        :param velocity_max_magnitude The maximum allowed magnitude for a particle velocity. If the particle's velocity magnitude exceeds this,
        then it will normalize the vector to be equal to it. By default, it is set to `None` and won't apply any normalization.
        :param random_local: If set to a float value, it will influence the result the particle's best known local position has on the velocity. If not set (`None`),
        then it will be chosen randomly for each velocity update.
        :param random_global: If set to a float value, it will influence the result the best known global position has on a particle's velocity. If not set (`None`),
        then it will be chosen randomly for each velocity update.
        """

        self.velocity_max_magnitude = velocity_max_magnitude
        self.anim = None
        self.width = grid_width
        self.height = grid_height
        self.strategy = map_strategy or PerlinNoiseMapStrategy(5, 10)

        self.rp = random_local
        self.rg = random_global

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

            # d=0: x, d=1: y
            for d in range(2):

                if self.rp is not None:
                    rp = self.rp
                else:
                    rp = random()

                if self.rg is not None:
                    rg = self.rg
                else: rg = random()

                p.velocity[d] = w * p.velocity[d] + phi_p * rp * (p.local[d] - p.position[d]) + phi_g * rg * (self.best[d] - p.position[d])


            # Normalize the velocity vector if possible
            if self.velocity_max_magnitude is not None:

                # If we have a vector v = (a, b), then norm(v) = sqrt(a^2 + b^2)
                # If we want to have another vector w = s * v, where s is a scalar and norm(w) = t, then
                # we have norm(w) = norm(s * v) = s * norm(v) = t, from which we can say that
                # s = t/norm(v)
                # so the vector we are looking for is w = t / norm(v) * v, where t is our desired magnitude and v is our velocity vector

                vel = np.array(p.velocity, dtype = float)
                norm_vec = np.linalg.norm(vel)
                # this only happens if we exceed the maximum magnitude
                if norm_vec > self.velocity_max_magnitude:
                    vel = (vel * self.velocity_max_magnitude) / norm_vec # multiplication first to not truncate results from the division

                p.velocity[0] = float(vel[0])
                p.velocity[1] = float(vel[1])

            # Update positions but reflect the velocity in case a particle gets stuck in a corner (like a bounce effect, but with dampening factor)
            damping_factor = 0.7

            for d, max_val in zip(range(2), [self.width, self.height]):
                p.position[d] += int(p.velocity[d])

                # Handling edges (bounce back)
                if p.position[d] < 0:
                    p.position[d] = 0
                    p.velocity[d] = -damping_factor * p.velocity[d] + uniform(-0.2, 0.2) # add a bit of randomness to encourage exploration

                elif p.position[d] >= max_val:
                    p.position[d] = max_val - 1
                    p.velocity[d] = -damping_factor * p.velocity[d] + uniform(-0.2, 0.2)


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


    def run(self, frame_interval=50, save_path: str=None, verbose=False):
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
            self.fig, func=update, frames=len(frames), interval=frame_interval
        )

        if save_path:
            make_file_dir_if_not_exist(save_path)
            self.anim.save(save_path)
        else:
            plt.show()

        return self.anim, (self.best, self.f(self.best))




