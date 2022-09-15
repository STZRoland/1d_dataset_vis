from pathlib import Path

import numpy as np
import pandas as pd


def check_paths(*paths: Path):
    for path in paths:
        if not path.is_file() and not path.is_dir():
            raise ValueError(f'Path {path} is neither a file, nor a dir!')


def dimensions_to_indices(dimensions: list[str]) -> tuple[int, ...]:
    indices = []
    for dim in dimensions:
        indices.append(int(dim[-1]))
    return tuple(indices)


def convert_channel_last(data: np.ndarray) -> np.ndarray:
    shape = data.shape
    if shape[-2] < shape[-1]:
        data = np.swapaxes(data, -1, -2)
    return data


def melt_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.reset_index().melt('index', var_name='dim', value_name='value')


def pad_array_list(array_list: list[np.ndarray]) -> np.ndarray:
    """Pads all elements in a list of np.ndarray to the same size and returns them as a np.ndarray"""

    channels = convert_channel_last(array_list[0]).shape[-1]
    max_length = 0

    for i in range(len(array_list)):
        array_list[i] = convert_channel_last(array_list[i])

        if array_list[i].shape[-1] != channels:
            raise ValueError('All np arrays in the folder must have the same number of channels.')

        if len(array_list[i]) > max_length:
            max_length = len(array_list[i])

    padded_array = np.zeros((len(array_list), max_length, channels))
    for num, array in enumerate(array_list):
        if len(array) < max_length:
            padded_array[num, 0: len(array), :] = array

    return padded_array

