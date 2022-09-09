import streamlit as st


class SampleSlider:
    def __init__(self, n_samples):
        self.container = st.container()
        self._idx = self.container.slider('Select the sample to use', 0, n_samples-1, 0,  step=1)

    def get_sample_idx(self):
        return self._idx
