import streamlit as st


def graph_range_module(sample_shape: tuple[int, int], container: st.container = None) -> (int, int):
    if container is None:
        container = st.container()

    default_size = sample_shape[0] if sample_shape[0] < 300 else 300

    size = container.number_input('Number of values', min_value=1,
                                  max_value=5000 if sample_shape[0] > 5000 else sample_shape[0],
                                  value=default_size)

    if not (size == sample_shape[0]):
        start = container.slider('Select start index', min_value=0, max_value=sample_shape[0] - size)
    else:
        start = 0

    end = start + size

    return start, end
