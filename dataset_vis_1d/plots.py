import altair as alt
import pandas as pd

from dataset_vis_1d.utils import melt_df


def alt_line_chart_multidim(df: pd.DataFrame):
    melted = melt_df(df)

    chart = alt.Chart(melted).mark_line().encode(
        x='index',
        y='value',
        color='dim'
    )

    return chart


def alt_fill_between_chart_multidim(df_low: pd.DataFrame, df_high: pd.DataFrame, opacity: float = 0.5):
    if not 0.0 <= opacity <= 1.0:
        raise ValueError(f'opacity {opacity} is not in [0.0, 1.0].')

    melted_low = melt_df(df_low)
    melted_high = melt_df(df_high)

    combined = melted_low
    combined['value_high'] = melted_high['value']

    chart = alt.Chart(combined).mark_area().encode(
        x='index',
        y='value',
        y2='value_high',
        color='dim',
        opacity=alt.value(opacity)
    )

    return chart
