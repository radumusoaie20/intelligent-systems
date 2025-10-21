class LifeStrategy:

    def next_state(self, cell, env):
        pass


class ConwayStrategy(LifeStrategy):
    def next_state(self, cell, env):
        neighbors = cell.perceive(env)
        alive_neighbors = sum(n.state for n in neighbors)

        if cell.state == 1 and alive_neighbors in (2, 3):
            return 1
        elif cell.state == 0 and alive_neighbors == 3:
            return 1
        else:
            return 0