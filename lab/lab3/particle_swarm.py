from fontTools.designspaceLib.types import clamp

from lab.lab3.strategy import MapStrategy, PerlinNoiseMapStrategy



# Input params

# width, height of grid
# number of particles to choose
# w - weight of current velocity
# l - weight of particle's best local position
# g - weight of particle's best position (globally)
class ParticleSwarm:
    def __int__(self, grid_width,  grid_height,
                map_strategy: MapStrategy=None,
                current_velocity_weight: float = 0.6,
                best_local_weight: float = 0.4,
                best_global_weight: float = 0.5,
                number_of_particles: int = 10):
        """
        Initializes a number of particles for the given grid of the given size
        :param grid_width: The width of the grid
        :param grid_height: The height of the grid
        :param map_strategy: The strategy used to initialize the grid's values (if none passed, it wil default to PerlinNoise strategy)
        :param current_velocity_weight: How much influence a cell current velocity has for the next position
        :param best_local_weight: How much influence a cell's best local has on the next position computation
        :param number_of_particles: The number of particles used
        :param best_global_weight:  How much influence the global best has on the next position for a cell
        """

        self.width = grid_width
        self.height = grid_height
        self.strategy = map_strategy or PerlinNoiseMapStrategy(5, 10)

        self.grid = self.strategy.initialize_map(self.width, self.height)

        self.local_weight = clamp(best_local_weight, 0, 1)
        self.global_weight = clamp(best_global_weight, 0, 1)
        self.velocity_weight = clamp(current_velocity_weight, 0, 1)






