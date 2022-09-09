import numpy as np


def get_mean_std(data: np.ndarray):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    return mean, std
