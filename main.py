from pathlib import Path

import streamlit as st
from omegaconf import OmegaConf

from dataset_vis_1d.calculations import get_mean_std
from dataset_vis_1d.load import load_data, load_labels, array_to_df
from dataset_vis_1d.utils import check_paths
from dataset_vis_1d.plots import alt_line_chart_multidim, alt_fill_between_chart_multidim

cfg = OmegaConf.load('config.yaml')
data_path = Path(cfg.paths.data)
label_path = Path(cfg.paths.labels)

check_paths(data_path, label_path)


data = load_data(data_path)
labels = load_labels(label_path)

dimensions = [f'dim_{i}' for i in range(data.shape[-1])]

##################################
st.header("Dataset Visualization")

mean, var = get_mean_std(data)

mean_df = array_to_df(mean, column_names=dimensions)
std_df_1 = array_to_df((mean + var), column_names=dimensions)
std_df_2 = array_to_df((mean - var), column_names=dimensions)

st.subheader('Mean and Standard Deviation of the Dimensions')
selected_dims = st.multiselect('Dimensions to plot', dimensions, default=dimensions)

if selected_dims:
    mean_chart = alt_line_chart_multidim(mean_df[selected_dims])
    std_chart = alt_fill_between_chart_multidim(std_df_1[selected_dims], std_df_2[selected_dims], opacity=0.2)

    chart = mean_chart + std_chart
    st.altair_chart(chart, use_container_width=True)


