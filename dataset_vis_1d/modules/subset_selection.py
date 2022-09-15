import numpy as np
import pandas as pd
import streamlit as st


def subset_selection_module(data: np.ndarray, label_df: pd.DataFrame, container: st.container = None) \
        -> (np.ndarray, pd.DataFrame):
    if container is None:
        container = st.container()
    container.header('Select a subset of the data')

    selected_data, selected_labels = select_subset(data, label_df, container)
    container.write(f'Shape of the selected data: {selected_data.shape}')
    container.write('')

    return selected_data, selected_labels


# @st.cache
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
        selections[c] = container.multiselect(c, options=options)

    for key, value in selections.items():
        if not value:
            # Nothing selected
            continue
        else:
            indices = label_df[label_df[key].isin(value)].index.values
            label_df = label_df.iloc[indices].reset_index(drop=True)
            data = data[indices]

    return data, label_df
