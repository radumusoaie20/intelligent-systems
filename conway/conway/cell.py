import conway.conway.strategy as s


class Cell:
    def __init__(self, x, y, state = 0, strategy = None):
        self.x = x
        self.y = y
        self.state = state
        self.strategy = strategy or s.ConwayStrategy()

    def perceive(self, env):
        """Gathers information from the environment for the cell (the cell neighbours)
        :param env: Environment object (The grid)
        """
        return env.get_neighbors(self.x, self.y)


    def decide_next_state(self, env):
        """Computes the next state of the cell based on the cell life strategy
        :param env: Environment object (The grid)
        """
        return self.strategy.next_state(self, env)

    def __str__(self):
        return str(self.state)

