import numpy as np
import pandas as pd
import streamlit as st


def outlier_removal_module(data: np.ndarray, labels_df: pd.DataFrame = None, container: st.container = None) \
        -> (np.ndarray, pd.DataFrame):
    if container is None:
        container = st.container()
    container.header('Outlier Removal')

    indices_str = container.text_input('Input the indexes of outliers to be removed with spaces in between.')

    if not indices_str == '':
        indices = [int(x) for x in indices_str.split(' ') if x != '']
        data = np.delete(data, indices, axis=0)
        labels_df = labels_df.drop(index=indices)

    return data, labels_df
