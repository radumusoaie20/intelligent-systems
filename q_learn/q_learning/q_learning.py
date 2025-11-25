import base64
import glob
import io
from collections.abc import Callable

import gymnasium as gym
from gymnasium.wrappers import RecordVideo
from pygame.math import clamp

from q_learn.q_learning.policy import Policy
import numpy as np

from IPython.display import HTML
from IPython import display


class QLearning:

    def __init__(self, env: gym.Env, explorer: Policy,
                 learning_rate: float = 0.3,
                 discount_factor: float = 0.7,
                 shall_record: bool = False,
                 episode_record_policy: Callable[[int], bool] = lambda ep: True,
                 video_folder: str = "videos",
                 name_prefix: str = "test",
                 ):
        self.env = env
        self.policy = explorer
        self.learning_rate = clamp(learning_rate, 0, 1)
        self.discount_factor = clamp(discount_factor, 0, 1)

        self.shall_record = shall_record


        n_states = env.observation_space.n
        n_actions = env.action_space.n

        self.number_of_states = n_states
        self.number_of_actions = n_actions

        self.q_table = np.zeros((n_states, n_actions))

        self.video_folder = video_folder
        self.name_prefix = name_prefix

        self.episode_trigger = episode_record_policy

        if shall_record:
            self.env = RecordVideo(self.env, video_folder=video_folder, name_prefix=name_prefix, episode_trigger=episode_record_policy)

        pass

    def reset_table(self):
        self.q_table = np.zeros((self.number_of_states, self.number_of_actions))

    def run(self, number_of_episodes: int = 5, reset_seed=0):

        # reset Q-Table between runs
        self.reset_table()

        # Returned data
        rewards = np.zeros(number_of_episodes)
        steps = np.zeros(number_of_episodes)

        for episode_num in range(number_of_episodes):

            state, info = self.env.reset(seed=reset_seed)
            step = 0
            total_rewards = 0

            episode_over = False
            while not episode_over:

                action = self.policy.select_action(state, self.q_table, self.env, episode_num)

                next_state, reward, terminated, truncated, info = self.env.step(action)

                # Update Q-Learning table
                delta = (
                        reward
                        + self.discount_factor * np.max(self.q_table[next_state, :])
                        - self.q_table[state, action]
                )


                self.q_table[state, action] = self.q_table[state, action] + self.learning_rate * delta

                state = next_state

                step += 1
                total_rewards += reward

                episode_over = truncated or terminated

            rewards[episode_num] = total_rewards
            steps[episode_num] = step

        return rewards, steps, self.q_table

    def _show_video(self, episode: int):
        mp4list = glob.glob(f'{self.video_folder}/{self.name_prefix}-episode-{episode}.mp4')
        if len(mp4list) > 0:
            mp4 = mp4list[0]
            video = io.open(mp4, 'r+b').read()
            encoded = base64.b64encode(video)
            display.display(HTML(data='''<video alt="test" autoplay
                    loop controls style="height: 400px;">
                    <source src="data:video/mp4;base64,{0}" type="video/mp4" />
                 </video>'''.format(encoded.decode('ascii'))))
        else:
            print("Could not find video")

    def show_episode(self, episode):

        if self.shall_record:
            if self.episode_trigger(episode):
                self._show_video(episode)
            else:
                raise Exception('Episode was not recorded because of the episode trigger policy. Aborting.')

        else:
            raise Exception('Cannot show episodes since video recording was disabled')



