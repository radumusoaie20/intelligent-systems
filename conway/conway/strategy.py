class LifeStrategy:

    def next_state(self, cell, env):
        raise NotImplementedError


"""
1. Any live cell with two or three live neighbours lives on to the next generation.
2. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""
class ConwayStrategy(LifeStrategy):
    def next_state(self, cell, env):
        neighbors = cell.perceive(env)
        alive_neighbors = sum(n.state for n in neighbors)

        if cell.state == 1 and alive_neighbors in (2, 3):
            return 1
        elif cell.state == 1 and (alive_neighbors > 3 or alive_neighbors < 2):
            return 0
        elif cell.state == 0 and alive_neighbors == 3:
            return 1
        else:
            return 0


class HighLifeStrategy(LifeStrategy):
    def next_state(self, cell, env):
        neighbors = cell.perceive(env)
        alive_neighbors = sum(n.state for n in neighbors)

        if cell.state == 1 and alive_neighbors in (2, 3):
            return 1
        elif cell.state == 1 and (alive_neighbors > 3 or alive_neighbors < 2):
            return 0
        elif cell.state == 0 and alive_neighbors in (3, 6):
            return 1
        else:
            return 0