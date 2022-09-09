from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd

from dataset_vis_1d.utils import convert_channel_last


def load_data(path: Path) -> Union[np.ndarray, list[np.ndarray]]:
    if path.is_file():
        data = np.load(str(path))

        if data.ndim == 2:
            data = data[..., np.newaxis]

        data = convert_channel_last(data)
        return data


def load_labels(path: Path) -> Union[pd.DataFrame, list[pd.DataFrame]]:
    if path.is_file():
        labels = pd.read_csv(path)
        return labels


def array_to_df(data: np.ndarray, column_names: list = None) -> pd.DataFrame:
    if column_names is None:
        column_names = [f'dim_{i+1}' for i in range(data.shape[-1])]

    data_df = pd.DataFrame(
        data,
        columns=column_names
    )

    return data_df
