from typing import Protocol
import gymnasium as gym

class RewardHook(Protocol):
    def __call__(self,
                 reward: float,
                 env: gym.Env,
                 state: gym.core.ObsType,
                 next_state: gym.core.ObsType,
                 action: gym.core.ActType) -> float:
        pass


