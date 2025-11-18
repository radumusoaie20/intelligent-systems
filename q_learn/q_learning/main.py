import gymnasium as gym

from q_learn.q_learning.policy import Policy, EpsilonGreedyPolicy
from q_learn.q_learning.q_learning import QLearning

env = gym.make("FrozenLake-v1", render_mode="rgb_array", is_slippery=False)

trigger = lambda x: x % 100 == 0

action_policy: Policy = EpsilonGreedyPolicy(epsilon=0.2)

q_learning = QLearning(env, action_policy, 0.1, 0.95, True,
                       trigger)

q_learning.run(1000, verbose=True)

