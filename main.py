from pathlib import Path

import streamlit as st
from omegaconf import OmegaConf

from dataset_vis_1d.load import load_data, load_labels, array_to_df
from dataset_vis_1d.modules.dataset_mean import dataset_mean_module
from dataset_vis_1d.modules.dataset_statistics import dataset_statistics_module
from dataset_vis_1d.modules.sample_choice import sample_choice_module
from dataset_vis_1d.modules.subset_selection import subset_selection_module
from dataset_vis_1d.modules.normalization_selection import normalization_selection_module
from dataset_vis_1d.modules.outlier_removal import outlier_removal_module
from dataset_vis_1d.modules.graph_range_selection import graph_range_module
from dataset_vis_1d.utils import check_paths


def main():
    cfg = OmegaConf.load('config.yaml')

    # Load data
    data_path = Path(cfg.paths.data)
    check_paths(data_path)
    data = load_data(data_path)

    if cfg.paths.labels is not None:
        label_path = Path(cfg.paths.labels)
        check_paths(label_path)
        labels = load_labels(label_path)
        if len(labels) != len(data):
            raise ValueError(f'There are unequal amount of samples ({len(data)}) and labels({len(labels)})')
    else:
        labels = None

    if hasattr(cfg, 'dimensions'):
        dimensions = [str(dim) for dim in cfg.dimensions]
    else:
        dimensions = [f'dim_{i+1}' for i in range(data.shape[-1])]

    ##################################
    st.header("Dataset Visualization")

    with st.sidebar:
        graph_range_expander = st.expander('Graph range')
        start_idx, end_idx = graph_range_module(data[0].shape, container=graph_range_expander)
        st.session_state['start_idx'] = start_idx
        st.session_state['end_idx'] = end_idx

        outlier_removal_expander = st.expander('Outlier Removal')
        data, labels = \
            outlier_removal_module(data, labels, container=outlier_removal_expander)

        subset_selection_expander = st.expander('Subset Selection')
        selected_data, selected_labels = \
            subset_selection_module(data, label_df=labels, container=subset_selection_expander)

        normalization_method_expander = st.expander('Normalization Method')
        selected_data = normalization_selection_module(selected_data, data, container=normalization_method_expander)

    dataset_mean_module(selected_data, dimensions=dimensions)
    dataset_statistics_module(selected_data, dimensions=dimensions)
    sample_idx = sample_choice_module(selected_data, dimensions=dimensions, label_df=selected_labels)


if __name__ == '__main__':
    main()
