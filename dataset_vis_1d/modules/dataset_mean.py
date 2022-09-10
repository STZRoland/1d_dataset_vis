import numpy as np
import pandas as pd
import streamlit as st

from dataset_vis_1d.calculations import get_mean_std
from dataset_vis_1d.load import array_to_df
from dataset_vis_1d.modules.subset_selection import select_subset
from dataset_vis_1d.plots import alt_line_chart_multidim, alt_fill_between_chart_multidim


def dataset_mean_module(data: np.ndarray, dimensions: list[str], label_df: pd.DataFrame = None) -> st.container:
    container = st.container()
    container.subheader('Mean and Standard Deviation of the Dimensions')

    mean, var = get_mean_std(data)

    mean_df = array_to_df(mean, column_names=dimensions)
    std_df_1 = array_to_df((mean + var), column_names=dimensions)
    std_df_2 = array_to_df((mean - var), column_names=dimensions)

    selected_dims = container.multiselect('Dimensions to plot', dimensions, default=dimensions[0])

    if selected_dims:
        mean_chart = alt_line_chart_multidim(mean_df[selected_dims])
        std_chart = alt_fill_between_chart_multidim(std_df_1[selected_dims], std_df_2[selected_dims], opacity=0.3,
                                                    color_domain=dimensions)

        chart = mean_chart + std_chart
        container.altair_chart(chart, use_container_width=True)

    return container
