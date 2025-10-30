import matplotlib.pyplot as plt
from IPython.core.display import HTML

import particle_swarm_simulator as ps
import simulation_terminator as st
from particle_swarm.strategy import PerlinNoiseMapStrategy

swarm = ps.ParticleSwarm(100, 100,
                         number_of_particles=50,
                         current_velocity_weight=0.9,
                         best_local_weight=2.0,
                         best_global_weight=2.0,
                         search_minimum=True,
                         simulation_terminator=st.IterationTerminator(150),
                         map_strategy=PerlinNoiseMapStrategy(20, 10))


animation, result = swarm.run(frame_interval=200,  verbose=False)

