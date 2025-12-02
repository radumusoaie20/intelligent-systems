from collections.abc import Callable

import gymnasium as gym
from q_learn.q_learning.policy import Policy, EpsilonGreedyPolicy
from q_learn.q_learning.q_learning import QLearning

env = gym.make("FrozenLake-v1", render_mode="rgb_array", is_slippery=False)

trigger = lambda ep: ep % 50 == 0 # only record successful episodes

success_trigger: Callable[[list[list], list[float]], bool] = lambda frames, rwds: any(r > 0 for r in rwds)

action_policy: Policy = EpsilonGreedyPolicy(epsilon=0.7)


q_learning = QLearning(env=env,
                       number_of_actions=env.action_space.n,
                       number_of_states=env.observation_space.n,
                       explorer=action_policy,
                       learning_rate=0.8,
                       discount_factor=0.95,
                       shall_record=True,
                       episode_record_policy=trigger,
                       successful_episode_record_policy=success_trigger,
                       fps=5)

rewards, steps, q_table = q_learning.run(500)

print(rewards)
print('\n----------\n')
print(steps)
print('\n----------\n')
print(q_table)
