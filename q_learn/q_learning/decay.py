def constant_decay(episode: int, epsilon: float, min_epsilon: float = 0.05, decay:float = 0.995):
    return max(min_epsilon, decay * epsilon)