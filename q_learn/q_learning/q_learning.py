import os
from collections.abc import Callable

import cv2
import gymnasium as gym
from gymnasium.wrappers import RecordVideo
from pygame.math import clamp

from q_learn.q_learning.policy import Policy
import numpy as np

class QLearning:

    def __init__(self, env: gym.Env, explorer: Policy,
                 number_of_states: int,
                 number_of_actions: int,
                 learning_rate: float = 0.3,
                 discount_factor: float = 0.7,
                 shall_record: bool = False,
                 episode_record_policy: Callable[[int], bool] = lambda ep: False,
                 video_folder: str = "videos",
                 name_prefix: str = "test",
                 fps: int = 25,
                 successful_episode_record_policy: Callable[[list[list], list[float]], bool] = lambda frames, rewards: False,
                 state_encoder=None, # used for continuous observation spaces (coming from env)
                 action_decoder=None, # used for continuous action spaces (since q-table actions are indices, we need a decoder to get back in continuous space)
                 ):
        """
        Construct a Q-Learning object meant to run the tabular Q-learning algorithm.
        :param env: The environment to run the Q-learning on, provided by Gymnasium
        :param number_of_states: The number of states to use in the Q-learning table
        :param number_of_actions: The number of actions to use in the Q-learning table
        :param state_encoder: The state encoder to use in the Q-learning table (for continuous states coming from the environment)
        :param action_decoder: The action decoder to use in the Q-learning table (for an index to get the real action value)
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

        if number_of_states is None:
            raise ValueError("number_of_states cannot be None")

        if number_of_actions is None:
            raise ValueError("number_of_actions cannot be None")

        n_states = number_of_states
        n_actions = number_of_actions

        # encoder
        # since gym gives us the state, if it is continuous, then we need to encode it (to discrete values)
        self.state_encoder = state_encoder

        # decoder
        # since q-table gives us the action, we need to decode it from discrete to it's supposed continuous value
        self.action_decoder = action_decoder


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


    def encode_state(self, state):
        return self.state_encoder(state) if self.state_encoder else state

    def decode_action(self, action_idx):
        return self.action_decoder(action_idx) if self.action_decoder else action_idx



    def run(self, number_of_episodes: int = 5,
                  reset_seed=0):

        """
        Run Q-Learning episodes
        :param number_of_episodes: The number of episodes to run
        :param reset_seed: Seed for the environment reset
        :return: rewards, steps, Q-table
        """

        # reset Q-Table between runs
        self.reset_table()

        # Returned data
        rewards = np.zeros(number_of_episodes)
        steps = np.zeros(number_of_episodes)


        for episode_num in range(number_of_episodes):

            raw_state, info = self.env.reset(seed=reset_seed)

            state = self.encode_state(raw_state)


            step = 0
            total_rewards = 0

            episode_frames = []
            episode_rewards = []

            # initial frame

            if self.shall_record:
                frame = self.env.render()
                episode_frames.append(frame)

            success = None
            episode_over = False
            while not episode_over:

                action_idx = int(self.policy.select_action(state, self.q_table, self.env, episode_num))



                # decode action from q-table
                action = self.decode_action(action_idx)

                raw_next_state, reward, terminated, truncated, info = self.env.step(action)

                # encode for q-table storage
                next_state = self.encode_state(raw_next_state)


                # frame after step
                if self.shall_record:
                    frame_after = self.env.render()
                    episode_frames.append(frame_after)

                episode_rewards.append(reward)

                delta = (
                        reward
                        + self.discount_factor * np.max(self.q_table[next_state])
                        - self.q_table[state, action_idx]
                )

                self.q_table[state, action_idx] = self.q_table[state, action_idx] + self.learning_rate * delta

                state = next_state

                step += 1
                total_rewards += reward

                episode_over = truncated or terminated
                success = terminated


            if self.shall_record:
                if self.successful_trigger:
                    if self.successful_trigger(episode_frames, episode_rewards) or success is True:
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

