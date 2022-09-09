from pathlib import Path

import numpy as np
import pandas as pd


def check_paths(*paths: Path):
    for path in paths:
        if not path.is_file() or path.is_dir():
            raise ValueError(f'Path {path} is neither a file, nor a dir!')


def dimensions_to_indices(dimensions: list[str]) -> tuple[int, ...]:
    indices = []
    for dim in dimensions:
        indices.append(int(dim[-1]))
    return tuple(indices)


def convert_channel_last(data: np.ndarray) -> np.ndarray:
    shape = data.shape
    if shape[1] < shape[2]:
        data = np.swapaxes(data, 1, 2)
    return data


def melt_df(df: pd.DataFrame) -> pd.DataFrame:
    return df.reset_index().melt('index', var_name='dim', value_name='value')
