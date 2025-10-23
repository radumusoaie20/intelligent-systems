class NeighbourFinder:
    def find_neighbours(self, x, y, env):
        """
        Returns the neighbour for a given position in an environment
        :param x: The horizontal position
        :param y: The vertical position
        :param env: The environment variable (of type Environment)
        :return: A list of neighbours
        """
        raise NotImplementedError


class StandardNeighbourFinder(NeighbourFinder):
    def find_neighbours(self, x, y, env):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < env.width and 0 <= ny < env.height:
                neighbors.append(env.grid[nx][ny])

        return neighbors


class ToroidNeighbourFinder(NeighbourFinder):
    """
    Provides the ability to find neighbours while in edges (by extending the existing map around the other side)
    """
    def find_neighbours(self, x, y, env):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = []

        for dx, dy in directions:
            nx, ny = (x + dx) % env.width, (y + dy) % env.height

            neighbors.append(env.grid[nx][ny])

        return neighbors