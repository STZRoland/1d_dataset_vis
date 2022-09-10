import numpy as np
import pandas as pd
import streamlit as st

from dataset_vis_1d.load import array_to_df
from dataset_vis_1d.plots import alt_line_chart_multidim


def sample_choice(data: np.ndarray, dimensions: list[str], label_df: pd.DataFrame = None) -> (st.container, int):

    container = st.container()
    container.subheader('Sample Visualization')
    idx = container.slider('Select a sample id', min_value=0, max_value=len(data)-1, value=0, step=1)

    sample_df = array_to_df(data[idx], column_names=dimensions)

    if label_df is not None:
        label = label_df.iloc[idx].to_list()
        title_list = []
        columns = label_df.columns.to_list()
        if columns[0] == 'Unnamed: 0':
            columns[0] = 'Index'

        for la, co in zip(label, columns):
            title_list.append(co + ': ' + str(la))
        title = '   '.join(title_list)
    else:
        title = f'Index {idx}'

    chart = alt_line_chart_multidim(sample_df, title=title)
    container.altair_chart(chart, use_container_width=True)

    return container, idx
