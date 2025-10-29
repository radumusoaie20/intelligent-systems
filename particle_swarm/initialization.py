import random

from particle_swarm.particle import Particle


class ParticleInitialization:
    def initialize(self,
                   grid,
                   number_of_particles: int) -> set[Particle]:
        pass


class RandomParticleInitialization(ParticleInitialization):

    def initialize(self,
                   grid,
                   number_of_particles: int) -> set[Particle]:

        particles: set[Particle] = set()

        while len(particles) < number_of_particles:
            x_lo = 0
            y_lo = 0
            x_up = len(grid) - 1
            y_up = len(grid[0]) - 1


            px = random.randint(x_lo, x_up)
            py = random.randint(y_lo, y_up)

            vx = abs(x_up - x_lo)
            vy = abs(y_up - y_lo)


            velocity_x = random.randint(-vx, vx)
            velocity_y = random.randint(-vy, vy)
            velocity = [velocity_x, velocity_y]

            particle = Particle(px, py, grid[px][py], velocity)

            particles.add(particle)

        return particles








