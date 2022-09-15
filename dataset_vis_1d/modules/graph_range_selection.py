import streamlit as st


def graph_range_module(sample_shape: tuple[int, int], container: st.container = None) -> (int, int):
    if container is None:
        container = st.container()

    default_size = sample_shape[0] if sample_shape[0] < 300 else 300

    size = container.number_input('Number of values', min_value=1, max_value=1000, value=default_size)
    start = container.slider('Select start index', min_value=0, max_value=sample_shape[0] - size + 1)
    end = start + size

    return start, end
