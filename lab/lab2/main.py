import matplotlib.pyplot as plt


from conway import ConwayGame
from lab.lab2.conway import OriginalRulesApplier, SimpleValueFinder

value_finder = SimpleValueFinder()

ruleApplier = OriginalRulesApplier(value_finder)

game = ConwayGame(15,15, ruleApplier, "config1", iterations=60)

game.run()