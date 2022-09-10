from pathlib import Path

import streamlit as st
from omegaconf import OmegaConf

from dataset_vis_1d.load import load_data, load_labels, array_to_df
from dataset_vis_1d.modules.dataset_mean import dataset_mean_module
from dataset_vis_1d.modules.dataset_statistics import dataset_statistics_module
from dataset_vis_1d.modules.sample_choice import sample_choice_module
from dataset_vis_1d.modules.subset_selection import subset_selection_module
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
    else:
        labels = None

    if hasattr(cfg, 'dimensions'):
        dimensions = [str(dim) for dim in cfg.dimensions]
    else:
        dimensions = [f'dim_{i+1}' for i in range(data.shape[-1])]

    ##################################
    st.header("Dataset Visualization")

    with st.sidebar:
        subset_selection_container, selected_data, selected_labels = subset_selection_module(data, label_df=labels)
    dataset_mean_container = dataset_mean_module(selected_data, dimensions=dimensions, label_df=selected_labels)
    dataset_statistics_container = dataset_statistics_module(selected_data, dimensions=dimensions)
    sample_choice_container = sample_choice_module(selected_data, dimensions=dimensions, label_df=selected_labels)


if __name__ == '__main__':
    main()
