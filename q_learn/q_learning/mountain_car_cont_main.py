import math
import numpy as np
import  gymnasium as gym

from q_learn.q_learning.discretizer import UniformStateDiscretizer, UniformActionDecoder
from q_learn.q_learning.policy import EpsilonGreedyPolicy
from q_learn.q_learning.q_learning import QLearning

from matplotlib import pyplot as plt

# Defining the environment
train_env = gym.make('MountainCarContinuous-v0', render_mode=None)

# Mountain Car observation space is a 2D-vector, being suitable for tabular Q-learning (not many dimensions -> not many entries in the table)

low = [-1.2, -0.07]
high = [0.6, 0.07]
bins = [15, 15]

number_of_states = int(np.prod(bins))

state_encoder = UniformStateDiscretizer(low=low, high=high, bins=bins)

# The action space is continuous

low = [-1]
high = [1]
bins = [10]

number_of_actions = int(np.prod(bins))

action_decoder = UniformActionDecoder(lows=low, highs=high, bins=bins, strategy='center')

# Setup

episodes = 700

epsilon_start = 1.0
decay_rate = 0.8

epsilon_decay_function = lambda ep, eps: epsilon_start * math.exp((-2*ep * decay_rate) / episodes)

policy = EpsilonGreedyPolicy(epsilon=epsilon_start, epsilon_decay_function=epsilon_decay_function, epsilon_min=0)

agent = QLearning(env=train_env,
                  explorer=policy,
                  state_encoder=state_encoder,
                  action_decoder=action_decoder,
                  learning_rate=0.05,
                  discount_factor=0.99,
                  number_of_actions=number_of_actions,
                  number_of_states=number_of_states
                  )

averaging_step = 100

def reward_func(reward: float, env: gym.Env, state: gym.core.ObsType, next_state: gym.core.ObsType, action: gym.core.ActType) -> float:

    position, velocity = next_state

    # we want to encourage moving right
    reward += (position + 1.2) * 0.1 # (+ 1.2 to go from [-1.2, 0.6] to [0, 1.8])

    # encourage high velocity as well (since high velocity will help in reaching the goal without needing constant acceleration)
    reward += abs(velocity) * 0.5

    return reward

average_rewards, q_table = agent.run(number_of_episodes=episodes, averaging_step=averaging_step, reward_hook_func=reward_func)


# Plotting average rewards
plt.plot((averaging_step * np.arange(len(average_rewards)) + 1), average_rewards)
plt.title('Q-Learning Mountain Car Average Rewards')
plt.xlabel('Episode')
plt.ylabel('Average Reward')
plt.show()

train_env.close()

np.save('table.npy', q_table)

# Testing

arr = np.load('table.npy')

test_env = gym.make('MountainCarContinuous-v0', render_mode='rgb_array')

greedy_policy = EpsilonGreedyPolicy(epsilon=0.05)

eval_agent = QLearning(env=test_env,
                       explorer=greedy_policy,
                       state_encoder=state_encoder,
                       action_decoder=action_decoder,
                       number_of_actions=number_of_actions,
                       number_of_states=number_of_states,
                       shall_record=True,
                       episode_record_policy=lambda _: True)

eval_agent.q_table = arr

rwds, _= eval_agent.run(number_of_episodes=5)

print(rwds)

test_env.close()






