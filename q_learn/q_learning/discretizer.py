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


class Uniform1DActionDecoder:
    def __init__(self, low, high, bins):
        self.low = np.array(low)
        self.high = np.array(high)
        self.bins = np.array(bins)
        self.widths = (high - low) / bins


    def __call__(self, action_index):
        return self.low + self.widths * (action_index + 0.5)