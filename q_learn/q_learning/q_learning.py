import base64
import glob
import io
import os
from collections.abc import Callable

import cv2
import gymnasium as gym
from gymnasium.core import RenderFrame
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
                 episode_record_policy: Callable[[int], bool] = lambda ep: False,
                 video_folder: str = "videos",
                 name_prefix: str = "test",
                 fps: int = 25,
                 successful_episode_record_policy: Callable[[list[list], list[float]], bool] = lambda frames, rewards: False,):
        """
        Construct a Q-Learning object meant to run the tabular Q-learning algorithm.
        :param env: The environment to run the Q-learning on, provided by Gymnasium
        :param explorer: The policy to use for exploration
        :param learning_rate: The learning rate
        :param discount_factor: The discount factor (Gamma)
        :param shall_record: If set to `True`, it enables episode recording, otherwise it disables it
        :param episode_record_policy: Policy to use for episode recording based on the index of the episode
        :param video_folder: The folder where to save videos to
        :param name_prefix: The prefix a video saved has
        :param fps: The frames per second
        :param successful_episode_record_policy: Function that upon returning `True` permits saving the episode
        based on its rewards or frames. *This policy differs based on the environment reward system*.
        """
        self.env = env
        self.policy = explorer
        self.learning_rate = clamp(learning_rate, 0, 1)
        self.discount_factor = clamp(discount_factor, 0, 1)
        self.fps = fps

        self.shall_record = shall_record

        self.successful_trigger = successful_episode_record_policy

        n_states = env.observation_space.n
        n_actions = env.action_space.n

        self.number_of_states = n_states
        self.number_of_actions = n_actions

        self.q_table = np.zeros((n_states, n_actions))

        self.video_folder = video_folder
        self.name_prefix = name_prefix

        self.episode_trigger = episode_record_policy

        if shall_record:
            self.env = RecordVideo(self.env, video_folder=video_folder, name_prefix=name_prefix, episode_trigger=episode_record_policy,
                                   fps=fps)

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

            episode_frames = []
            episode_rewards = []

            # initial frame
            frame = self.env.render()
            episode_frames.append(frame)

            episode_over = False
            while not episode_over:

                action = self.policy.select_action(state, self.q_table, self.env, episode_num)

                next_state, reward, terminated, truncated, info = self.env.step(action)

                # frame after step
                frame_after = self.env.render()
                episode_frames.append(frame_after)

                episode_rewards.append(reward)

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


            if self.shall_record:
                if self.successful_trigger(episode_frames, episode_rewards):
                    self.save_episode_video(episode_frames, episode_num)


            rewards[episode_num] = total_rewards
            steps[episode_num] = step

        return rewards, steps, self.q_table

    def save_episode_video(self, frames: list[list], episode_num: int):
        os.makedirs(self.video_folder, exist_ok=True)
        height, width, _ = frames[0].shape
        filename = os.path.join(self.video_folder, f"{self.name_prefix}-episode-{episode_num}.mp4")
        out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (width, height))
        for f in frames:
            f_bgr = cv2.cvtColor(f, cv2.COLOR_RGB2BGR)
            out.write(f_bgr)
        out.release()

