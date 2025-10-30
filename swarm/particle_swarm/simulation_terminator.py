class SimulationTerminator:
    def shall_terminate(self, simulation):
        raise NotImplementedError


class IterationTerminator(SimulationTerminator):
    def __init__(self, max_iterations):
        self.iteration = 0
        self.max_iterations = max_iterations

    def shall_terminate(self, simulation):
        self.iteration += 1
        if self.iteration == self.max_iterations:
            return True
        return False