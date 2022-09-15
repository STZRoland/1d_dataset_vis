import numpy as np
import pandas as pd
import streamlit as st

from dataset_vis_1d.load import array_to_df
from dataset_vis_1d.plots import alt_line_chart_multidim


def sample_choice_module(data: np.ndarray, dimensions: list[str], label_df: pd.DataFrame = None,
                         container: st.container = None) -> int:

    if container is None:
        container = st.container()
    container.subheader('Sample Visualization')
    idx = container.slider('Select a sample id', min_value=0, max_value=len(data)-1, value=0, step=1)

    plot_data = data[idx, st.session_state['start_idx']: st.session_state['end_idx']]

    sample_df = array_to_df(plot_data, column_names=dimensions)

    if label_df is not None:
        label = label_df.iloc[idx].to_list()
        title_list = []
        columns = label_df.columns.to_list()

        # remove = ['index', 'Unnamed: 0']
        # for r in remove:
        #     if r in columns:
        #         columns.remove(r)

        if columns[0] == 'Unnamed: 0':
            columns[0] = 'index'

        for la, co in zip(label, columns):
            title_list.append(co + ': ' + str(la))
        title = '   '.join(title_list)
    else:
        title = f'Index {idx}'

    chart = alt_line_chart_multidim(sample_df, title=title)
    container.altair_chart(chart, use_container_width=True)

    return idx
