import numpy as np
import streamlit as st
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, PowerTransformer, Normalizer


def normalization_selection_module(subset_data: np.ndarray, whole_data: np.ndarray, container: st.container = None) \
        -> np.ndarray:
    if container is None:
        container = st.container()
    container.header('Normalization method')
    container.write('Applied for each channel of the data.')

    method = container.selectbox('Select the method for normalization.', options=_options, index=0)
    normalization_function = _normalization_function_dict[method]

    use_whole_data = container.checkbox('Use whole dataset for normalization?', value=True)
    if use_whole_data:
        normalized_data = normalization_function(subset_data, whole_data)
    else:
        normalized_data = normalization_function(subset_data, subset_data)

    return normalized_data


def transform_sklearn(func):
    """Wrapper function for transforming the input into 2d shape as for sklearn required."""
    def wrap(transform_data: np.ndarray, fit_data: np.ndarray):
        data_shape = transform_data.shape

        if len(data_shape) != 2:
            transform_data = transform_data.reshape((-1, transform_data.shape[-1]))
            fit_data = fit_data.reshape((-1, fit_data.shape[-1]))

        transform_data = func(transform_data, fit_data)

        if len(data_shape) != 2:
            transform_data = transform_data.reshape(data_shape)

        return transform_data
    return wrap



@st.cache
def no_normalization(transform_data: np.ndarray, fit_data: np.ndarray) -> np.ndarray:
    return transform_data


@st.cache
@transform_sklearn
def normalize_mean_var(transform_data: np.ndarray, fit_data: np.ndarray) -> np.ndarray:
    scaler = StandardScaler()
    scaler.fit(fit_data)
    return scaler.transform(transform_data)


@st.cache
@transform_sklearn
def normalize_zero_one(transform_data: np.ndarray, fit_data: np.ndarray) -> np.ndarray:
    scaler = MinMaxScaler()
    scaler.fit(fit_data)
    return scaler.transform(transform_data)


@st.cache
@transform_sklearn
def normalize_robust(transform_data: np.ndarray, fit_data: np.ndarray) -> np.ndarray:
    scaler = RobustScaler()
    scaler.fit(fit_data)
    return scaler.transform(transform_data)


@st.cache
@transform_sklearn
def normalize_power_transform(transform_data: np.ndarray, fit_data: np.ndarray) -> np.ndarray:
    scaler = PowerTransformer()
    scaler.fit(fit_data)
    return scaler.transform(transform_data)


@st.cache
@transform_sklearn
def normalize_normalizer_l2(transform_data: np.ndarray, fit_data: np.ndarray) -> np.ndarray:
    scaler = Normalizer(norm='l2')
    scaler.fit(fit_data)
    return scaler.transform(transform_data)


_normalization_function_dict = {
    'None': no_normalization,
    '[0, 1]': normalize_zero_one,
    '0 mean and 1 variance': normalize_mean_var,
    'Robust': normalize_robust,
    'Power Transform': normalize_power_transform,
    'Normalizer L2': normalize_normalizer_l2
}
_options = list(_normalization_function_dict.keys())
