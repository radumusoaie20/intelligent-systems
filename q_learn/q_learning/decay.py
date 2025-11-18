def exponential_decay(episode: int, epsilon_start=1.0, epsilon_min=0.01, decay_rate=0.995):
    return max(epsilon_min, epsilon_start * (decay_rate ** episode))

def linear_decay(episode: int, epsilon_start=1.0, epsilon_min=0.01, max_episodes=1000):
    epsilon = epsilon_start - (episode / max_episodes) * (epsilon_start - epsilon_min)
    return max(epsilon_min, epsilon)

def inverse_decay(episode: int, epsilon_start=1.0, k=0.001):
    return epsilon_start / (1 + k * episode)