import numpy as np
import pandas as pd
import streamlit as st


def subset_selection_module(data: np.ndarray, label_df: pd.DataFrame) -> (st.container, np.ndarray):
    container = st.container()
    container.subheader('Select a subset of the data')

    selected_data, selected_labels = select_subset(data, label_df, container)
    st.write(f'Shape of the selected data: {selected_data.shape}')

    return container, selected_data, selected_labels


def select_subset(data: np.ndarray, label_df: pd.DataFrame, container: st.container) -> (np.ndarray, pd.DataFrame):
    """Creates multiselect widgets for each label and returns a subset of the data according to the selection."""
    columns = label_df.columns.to_list()

    # Remove non-label values
    remove = ['index', 'Unnamed: 0']
    for r in remove:
        if r in columns:
            columns.remove(r)

    selections = {}
    for c in columns:
        options = label_df[c].unique()
        selections[c] = container.multiselect(c, options=options, default=options[1])

    # indices = np.zeros(len(data))
    all_empty = True
    for key, value in selections.items():
        if not value:
            # Nothing selected
            continue
        else:
            all_empty = False
            # new_indices = label_df.iloc[indices][key].isin(value).to_numpy()
            # indices = np.logical_or(indices, new_indices)
            indices = label_df[label_df[key].isin(value)].index.values
            label_df = label_df.iloc[indices].reset_index()
            data = data[indices]

    # if all_empty:
    #     indices = np.logical_not(indices)
    #
    # return data[indices], label_df.iloc[indices]

    return data, label_df
