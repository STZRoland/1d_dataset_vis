import altair as alt
import pandas as pd
import streamlit as st

from dataset_vis_1d.utils import melt_df


def alt_line_chart_multidim(df: pd.DataFrame, title: str = ''):
    melted = melt_df(df)

    chart = alt.Chart(melted).mark_line().encode(
        x='index',
        y='value',
        color='dim'
    ).properties(
        title=title
    )

    return chart


def alt_fill_between_chart_multidim(df_low: pd.DataFrame, df_high: pd.DataFrame, opacity: float = 0.5,
                                    color_domain: list[str] = None):
    if not 0.0 <= opacity <= 1.0:
        raise ValueError(f'opacity {opacity} is not in [0.0, 1.0].')

    melted_low = melt_df(df_low)
    melted_high = melt_df(df_high)

    if color_domain is None:
        color_scale = alt.Scale()
    else:
        color_scale = alt.Scale(domain=color_domain)

    combined = melted_low
    combined['value_high'] = melted_high['value']

    chart = alt.Chart(combined).mark_area().encode(
        x='index',
        y=alt.Y('value', title='value'),
        y2='value_high',
        # color=alt.Color('dim', scale=alt.Scale(domain=['dim_1', 'dim_2', 'dim_3'])),
        color=alt.Color('dim', scale=color_scale),
        opacity=alt.value(opacity)
    )

    return chart


def alt_multibar_chart_custom(df: pd.DataFrame, columns: st.columns, column_names: list[str]):
    if not (len(columns) == len(column_names)):
        raise AttributeError('Columns of the inputs do not match!')

    for i, col in enumerate(columns):

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('dimensions'),
            y=alt.Y(column_names[i], title='',
                    # scale=alt.Scale(domain=(- df[column_names[i]].abs().max(), df[column_names[i]].abs().max()))
                    ),
            color=alt.Color('dimensions', legend=None),
            opacity=alt.value(0.7)
        ).properties(
            title=column_names[i]
        )
        col.altair_chart(chart, use_container_width=True)
