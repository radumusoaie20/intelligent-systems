class Particle:
    def __init__(self, x: int, y: int, value: float, velocity: [int, int]):
        self.position = [x , y]
        self.value = value

        self.local = self.position.copy()
        self.velocity = velocity
