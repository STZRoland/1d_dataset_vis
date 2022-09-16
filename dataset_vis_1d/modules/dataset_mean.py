import numpy as np
import pandas as pd
import streamlit as st

from dataset_vis_1d.load import array_to_df
from dataset_vis_1d.utils import select_range
from dataset_vis_1d.plots import alt_line_chart_multidim, alt_fill_between_chart_multidim


def dataset_mean_module(data: np.ndarray, dimensions: list[str], plot_range: tuple[int, int] = None,
                        container: st.container = None):
    if container is None:
        container = st.container()
    container.subheader('Mean and Standard Deviation of the Dimensions')
    selected_dims = container.multiselect('Dimensions to plot', dimensions, default=dimensions)

    plot_data, indices = select_range(data, plot_range)

    mean_df, std_df_1, std_df_2 = mean_std_array(plot_data, dimensions, indices=indices)

    if selected_dims:
        mean_chart = alt_line_chart_multidim(mean_df[selected_dims])
        std_chart = alt_fill_between_chart_multidim(std_df_1[selected_dims], std_df_2[selected_dims], opacity=0.3,
                                                    color_domain=dimensions)
        chart = mean_chart + std_chart
        container.altair_chart(chart, use_container_width=True)


@st.cache
def mean_std_array(data: np.ndarray, dimensions: list[str], indices: np.ndarray = None) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)

    mean_df = array_to_df(mean, column_names=dimensions, indices=indices)
    std_df_1 = array_to_df((mean + std), column_names=dimensions, indices=indices)
    std_df_2 = array_to_df((mean - std), column_names=dimensions, indices=indices)

    return mean_df, std_df_1, std_df_2
