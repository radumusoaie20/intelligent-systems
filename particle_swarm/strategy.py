from perlin_noise import PerlinNoise

class MapStrategy:
    def initialize_map(self, width: int, height:  int):
        pass


class PerlinNoiseMapStrategy(MapStrategy):

    def __init__(self, octaves, seed):
        self.noise = PerlinNoise(octaves=octaves, seed=seed)


    def initialize_map(self, width: int, height: int):
        return [[self.noise([x, y]) for x in range(width)] for y in range(height) ]


