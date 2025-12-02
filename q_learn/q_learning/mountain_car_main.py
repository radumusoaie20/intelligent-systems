import math

import numpy as np
import  gymnasium as gym

from q_learn.q_learning.discretizer import UniformStateDiscretizer, Uniform1DActionDecoder
from q_learn.q_learning.policy import EpsilonGreedyPolicy, GreedyPolicy
from q_learn.q_learning.q_learning import QLearning

# Defining the environment

train_env = gym.make('MountainCarContinuous-v0', render_mode=None)

# Mountain Car observation space is a 2D-vector, being suitable for tabular Q-learning (not many dimensions -> not many entries in the table)

low = [-1.2, -0.07]
high = [0.6, 0.07]
bins = [8, 8] # total = 8 * 8 = 64

number_of_states = int(np.prod(bins))

state_encoder = UniformStateDiscretizer(low=low, high=high, bins=bins)

# Mountain Car action space is a one dimensional vector, being the directional force of the care
action_low = [-1.0]
action_high = [1.0]
actions_bins = 4 # not that many speeds, in order to explore fast



action_decoder = Uniform1DActionDecoder(low=train_env.action_space.low,
                                      high=train_env.action_space.high,
                                      bins=actions_bins)

number_of_actions = int(np.prod(actions_bins))

# Setup

episodes = 1000
epsilon_decay_fn = lambda eps, ep: 0.9*math.exp(-ep/episodes)

policy = EpsilonGreedyPolicy(epsilon=0.9, epsilon_min=0.05, epsilon_decay_function=epsilon_decay_fn)

agent = QLearning(env=train_env,
                  explorer=policy,
                  state_encoder=state_encoder,
                  action_decoder=action_decoder,
                  learning_rate=0.1,
                  discount_factor=0.99,
                  number_of_actions=number_of_actions,
                  number_of_states=number_of_states
                  )
rewards, steps, q_table = agent.run(number_of_episodes=episodes)


print(q_table)

# Testing

test_env = gym.make('MountainCarContinuous-v0', render_mode='rgb_array')

greedy_policy = GreedyPolicy()

eval_agent = QLearning(env=test_env,
                       explorer=greedy_policy,
                       state_encoder=state_encoder,
                       action_decoder=action_decoder,
                       number_of_actions=number_of_actions,
                       number_of_states=number_of_states,
                       shall_record=True,
                       episode_record_policy=lambda _: True)

eval_agent.q_table = q_table

rwds, _, _ = eval_agent.run(number_of_episodes=5)

print(rwds)

test_env.close()
train_env.close()






