import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

from dataset_vis_1d.plots import alt_multibar_chart_custom


def dataset_statistics(data: np.ndarray, dimensions: list[str]) -> st.container:
    mean = np.mean(data, axis=(0, 1))
    var = np.var(data, axis=(0, 1))
    min_v = np.min(data, axis=(0, 1))
    max_v = np.max(data, axis=(0, 1))

    statistics = ['mean', 'var', 'min', 'max']
    df = pd.DataFrame({
        'dimensions': dimensions,
        'mean': mean,
        'var': var,
        'min': min_v,
        'max': max_v
    })

    container = st.container()
    container.subheader('Dataset Statistics')

    container.table(df)

    cols = container.columns(4)

    alt_multibar_chart_custom(df, cols, statistics)

    return container
