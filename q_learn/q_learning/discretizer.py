import numpy as np
import gymnasium as gym


class UniformStateDiscretizer:
    def __init__(self, low, high, bins):
        self.low = np.array(low)
        self.high = np.array(high)
        self.bins = np.array(bins)

    def __call__(self, obs: gym.core.ObsType):
        obs = np.clip(obs, self.low, self.high) # clipping extreme values

        ratios = (obs - self.low) / (self.high - self.low) # from uniform quantization to get the bin (bucket) index

        indices = np.floor(ratios * self.bins).astype(int) # modified formula to truncate
        indices = np.clip(indices, 0, self.bins - 1) # floor the ratios to get integers, then clamp values outside (0, bin_number)

        # we have 8 indices now, we need one unique value from it
        # if we have something like:
        # bins = [4, 3, 2]
        # indices = [2, 1, 0]

        # then, bins[0] tells us that the first feature has 4 possible values, bins[1] tells us 3 and so on
        # this would mean, in total, a number of values equal to 4*3*2 = 24 total possibilities

        # these will be actions/states to be encoded, so we need to get a unique index
        # the easiest way is to generate something like a 1-D array from the bins, then return the index of the indices element, which is unique

        # this is where ravel_multi_index does the heavy lifting, by doing exactly that
        # it flattens a multidimensional grid, then returns the index for the element in that grid

        # for performance reason, it uses a mathematical formula directly to generate the index
        return np.ravel_multi_index(indices, self.bins)


class UniformActionDecoder:
    """
    Decodes discrete indices to continuous actions for N-dimensional action spaces.
    """

    def __init__(self, lows, highs, bins, strategy="center"):
        self.lows = np.array(lows, dtype=float)
        self.highs = np.array(highs, dtype=float)
        self.bins = np.array(bins, dtype=int)
        self.strategy = strategy

        self.widths = (self.highs - self.lows) / self.bins
        self.dim = len(self.lows)

        if len(self.highs) != self.dim or len(self.bins) != self.dim:
            raise ValueError("lows, highs, bins must all have the same length")

    def __call__(self, indices):
        """
        :param indices: An array of discrete indices. (have to be integers)
        Returns: np.array of decoded continuous action values
        """
        indices = np.array(indices, dtype=int)
        if len(indices) != self.dim:
            raise ValueError(f"indices length {len(indices)} != number of dimensions {self.dim}")

        actions = np.zeros(self.dim)


        for i in range(self.dim):
            idx = np.clip(indices[i], 0, self.bins[i] - 1)
            if self.strategy == "left":
                actions[i] = self.lows[i] + idx * self.widths[i]
            elif self.strategy == "right":
                actions[i] = self.lows[i] + (idx + 1) * self.widths[i]
            elif self.strategy == "center":
                actions[i] = self.lows[i] + (idx + 0.5) * self.widths[i]
            else:
                raise ValueError(f"Unknown strategy {self.strategy}")

        return actions




