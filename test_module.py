from pathlib import Path

import matplotlib
import pandas as pd

import time_series_visualizer as tsv

matplotlib.use('Agg')


def test_df_loaded_and_cleaned():
    assert isinstance(tsv.df, pd.DataFrame)
    assert isinstance(tsv.df.index, pd.DatetimeIndex) or tsv.df.empty
    if not tsv.df.empty:
        # verifica se dados foram carregados e são válidos
        assert (tsv.df['value'] > 0).all()  # valores positivos
        assert len(tsv.df) > 0  # não vazio


def test_draw_line_plot():
    fig = tsv.draw_line_plot()
    ax = fig.axes[0]
    assert ax.get_title() == 'Daily freeCodeCamp Forum Page Views 5/2016-12/2019'
    assert ax.get_xlabel() == 'Date'
    assert ax.get_ylabel() == 'Page Views'
    assert Path('line_plot.png').exists()


def test_draw_bar_plot():
    fig = tsv.draw_bar_plot()
    ax = fig.axes[0]
    assert ax.get_xlabel() == 'Years'
    assert ax.get_ylabel() == 'Average Page Views'
    legend = ax.get_legend()
    assert legend is not None and legend.get_title().get_text() == 'Months'
    assert Path('bar_plot.png').exists()


def test_draw_box_plot():
    fig = tsv.draw_box_plot()
    ax_left, ax_right = fig.axes
    assert ax_left.get_title() == 'Year-wise Box Plot (Trend)'
    assert ax_right.get_title() == 'Month-wise Box Plot (Seasonality)'
    assert ax_left.get_xlabel() == 'Year'
    assert ax_left.get_ylabel() == 'Page Views'
    assert ax_right.get_xlabel() == 'Month'
    assert ax_right.get_ylabel() == 'Page Views'
    assert Path('box_plot.png').exists()
