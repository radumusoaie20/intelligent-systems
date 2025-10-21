from  lab.lab2.conway.simulator import Simulator
from lab.lab2.conway.strategy import ConwayStrategy

simulator = Simulator(50, 50, life_strategy=ConwayStrategy())

simulator.run(iterations=200, frame_interval=100, filename="out/50_50.gif")
