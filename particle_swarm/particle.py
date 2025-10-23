class Particle:
    def __init__(self, x: int, y: int, value: float):
        self.x = x
        self.y = y
        self.value = value

        self.best = value
