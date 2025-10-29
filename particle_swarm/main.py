import particle_swarm_simulator as ps
import simulation_terminator as st

swarm = ps.ParticleSwarm(50, 50,
                         number_of_particles=30,
                         current_velocity_weight=0.9,
                         best_local_weight=2.0,
                         best_global_weight=2.0,
                         search_minimum=True,
                         simulation_terminator=st.IterationTerminator(150))


result = swarm.run(frame_interval=50, save_path='test.gif', verbose=True)

