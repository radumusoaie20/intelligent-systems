import swarm.particle_swarm.particle_swarm_simulator as ps
import swarm.particle_swarm.simulation_terminator as st
from swarm.particle_swarm.strategy import PerlinNoiseMapStrategy
from swarm.particle_swarm.initialization import UniformParticleInitialization

swarm = ps.ParticleSwarm(200, 200,
                         number_of_particles=70,
                         current_velocity_weight=0.4,
                         best_local_weight=0.2,
                         best_global_weight=1.8,
                         search_minimum=False,
                         initialization_strategy=UniformParticleInitialization(),
                         simulation_terminator=st.IterationTerminator(200),
                         map_strategy=PerlinNoiseMapStrategy(14, 5),
                         random_local=1,
                         random_global=1,
                         velocity_max_magnitude = 5.0)


animation, result = swarm.run(frame_interval=200, save_path='out/file.gif',  verbose=False)

