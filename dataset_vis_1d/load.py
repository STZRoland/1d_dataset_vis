from pathlib import Path

import numpy as np
import pandas as pd

from dataset_vis_1d.utils import convert_channel_last, pad_array_list


def load_data(path: Path) -> np.ndarray:
    if path.is_file():
        data = np.load(str(path))

        if data.ndim == 2:
            data = data[..., np.newaxis]

        data = convert_channel_last(data)
        return data

    if path.is_dir():
        files = sorted(path.glob('*.npy'))

        array_list = []
        for f in files:
            array_list.append(np.load(str(f)))

        return pad_array_list(array_list)


def load_labels(path: Path) -> pd.DataFrame:
    if path.is_file():
        labels = pd.read_csv(path)
        return labels

    if path.is_dir():
        raise ValueError('Labels must be provided all in one file.')


def array_to_df(data: np.ndarray, column_names: list = None) -> pd.DataFrame:
    if column_names is None:
        column_names = [f'dim_{i+1}' for i in range(data.shape[-1])]

    data_df = pd.DataFrame(
        data,
        columns=column_names
    )

    return data_df
