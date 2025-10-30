from perlin_noise import PerlinNoise

class MapStrategy:
    def initialize_map(self, width: int, height:  int):
        raise NotImplementedError


class PerlinNoiseMapStrategy(MapStrategy):

    def __init__(self, octaves, seed):
        self.noise = PerlinNoise(octaves=octaves, seed=seed)


    def initialize_map(self, width: int, height: int):
        return [[self.noise([x/width, y/height]) for y in range(width)] for x in range(height)]


