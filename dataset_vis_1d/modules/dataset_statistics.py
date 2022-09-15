import numpy as np
import pandas as pd
import streamlit as st

from dataset_vis_1d.plots import alt_multibar_chart_custom


def dataset_statistics_module(data: np.ndarray, dimensions: list[str], container: st.container = None):

    statistics_df = get_statistics_df(data, dimensions)
    statistics = ['mean', 'var', 'min', 'max']

    if container is None:
        container = st.container()
    container.subheader('Subset Statistics')

    container.table(statistics_df)

    cols = container.columns(4)
    alt_multibar_chart_custom(statistics_df, cols, statistics)


@st.cache
def get_statistics_df(data: np.ndarray, dimensions: list[str]) -> pd.DataFrame:
    mean = np.mean(data, axis=(0, 1))
    median= np.median(data, axis=(0, 1))
    var = np.var(data, axis=(0, 1))
    min_v = np.min(data, axis=(0, 1))
    max_v = np.max(data, axis=(0, 1))

    if np.all(np.isclose(mean, 0.0)):
        mean = np.zeros_like(mean)

    min_indices = np.where(data == min_v)
    max_indices = np.where(data == max_v)
    order_min = np.argsort(min_indices[-1])
    order_max = np.argsort(max_indices[-1])

    min_indices = min_indices[0][order_min]
    max_indices = max_indices[0][order_max]

    df = pd.DataFrame({
        'dim': dimensions,
        'mean': mean,
        'median': median,
        'var': var,
        'min': min_v,
        'max': max_v,
        'min_idx': min_indices,
        'max_idx': max_indices
    })

    return df
