class Particle:
    def __init__(self, x: int, y: int, value: float, velocity: [int, int]):
        self.position = [x , y]
        self.value = value

        self.local = self.position.copy()
        self.velocity = velocity

    def __str__(self):
        x, y = self.position
        return f'({x}, {y}), v={self.value}'
