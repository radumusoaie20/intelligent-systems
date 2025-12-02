from abc import ABC, abstractmethod
from typing import Callable

import numpy as np
import gymnasium as gym


class Policy(ABC):
    """Base class for Q-Learning policy"""

    @abstractmethod
    def select_action(self, state, q_table, env: gym.Env, episode: int = 0):
        """
        Returns an action given the current `state`, using the tabular Q-Learning table `q_table`,
        using an environment `env` supplied by `Gymnasium`
        :param state: The current state
        :param q_table: The Q-Learning table
        :param env: The environment that comes from Gymnasium
        :param episode: The episode at which the action is taken
        :return: An action that can be taken in the environment
        """
        pass


class RandomPolicy(Policy):
    def select_action(self, state, q_table, env, episode: int = 0):
        return env.action_space.sample()


class GreedyPolicy(Policy):
    def select_action(self, state, q_table, env, episode: int = 0):
        return np.argmax(q_table[state])


class EpsilonGreedyPolicy(Policy):

    def __init__(self, epsilon=0.2, epsilon_decay_function: Callable[[int, float], float]=None, epsilon_min: float=0.01):
        self.epsilon = epsilon
        self.decay_function = epsilon_decay_function if epsilon_decay_function else lambda ep, eps: epsilon
        self.epsilon_min = epsilon_min

    def select_action(self, state, q_table, env, episode: int = 0):

        self.epsilon = max(self.epsilon_min, self.decay_function(episode, self.epsilon))

        if np.random.uniform() < self.epsilon:
            action = env.action_space.sample() # :exploring
        else:
            action = np.argmax(q_table[state])

        return action


