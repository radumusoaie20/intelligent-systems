import gymnasium as gym

from q_learn.q_learning.decay import exponential_decay
from q_learn.q_learning.policy import Policy, EpsilonGreedyPolicy
from q_learn.q_learning.q_learning import QLearning

env = gym.make("FrozenLake-v1", render_mode="rgb_array", is_slippery=False)

trigger = lambda x: x % 100 == 0

action_policy: Policy = EpsilonGreedyPolicy(epsilon=0.7)

q_learning = QLearning(env, action_policy, 0.8, 0.95, True,
                       trigger)

rewards, steps, q_table = q_learning.run(2000)

print(rewards)
print('\n----------\n')
print(steps)
print('\n----------\n')
print(q_table)
