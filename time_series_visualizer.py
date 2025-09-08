import calendar
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATASET_FILENAME = "fcc-forum-pageviews.csv"
DATASET_PATH = Path(__file__).resolve().parent / DATASET_FILENAME
DATASET_URLS = [
    "https://raw.githubusercontent.com/freeCodeCamp/boilerplate-page-view-time-series-visualizer/main/fcc-forum-pageviews.csv",
    "https://raw.githubusercontent.com/freeCodeCamp/boilerplate-page-view-time-series-visualizer/master/fcc-forum-pageviews.csv",
]


def _ensure_dataset() -> None:
    if DATASET_PATH.exists():
        return
    for url in DATASET_URLS:
        try:
            urlretrieve(url, str(DATASET_PATH))
            return
        except Exception:
            continue


def _load_and_clean() -> pd.DataFrame:
    _ensure_dataset()
    df_local = pd.read_csv(DATASET_PATH, parse_dates=["date"], index_col="date")
    lower = df_local["value"].quantile(0.025)
    upper = df_local["value"].quantile(0.975)
    df_local = df_local[(df_local["value"] >= lower) & (df_local["value"] <= upper)]
    return df_local


# DataFrame global como no boilerplate do freeCodeCamp
try:
    df = _load_and_clean()
except Exception:
    # Mantém compatibilidade mesmo se sem internet/dataset
    df = pd.DataFrame(columns=["value"])  # type: ignore[assignment]


def draw_line_plot() -> plt.Figure:
    """Desenha o gráfico de linha das visualizações diárias."""
    df_plot = df.copy()

    fig, ax = plt.subplots(figsize=(12, 6))
    if not df_plot.empty:
        ax.plot(df_plot.index, df_plot["value"], color="red", linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.tight_layout()
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot() -> plt.Figure:
    """Desenha o gráfico de barras com média diária por mês agrupada por ano."""
    df_bar = df.copy()
    if df_bar.empty:
        df_bar = pd.DataFrame({"value": []})
        df_bar.index = pd.to_datetime(pd.Index([]), errors="coerce")

    df_bar["year"] = df_bar.index.year
    df_bar["month_num"] = df_bar.index.month

    monthly_means = df_bar.groupby(["year", "month_num"])['value'].mean().unstack(fill_value=0)

    month_numbers = list(range(1, 13))
    month_names = [calendar.month_name[m] for m in month_numbers]
    monthly_means = monthly_means.reindex(columns=month_numbers, fill_value=0)
    monthly_means.columns = month_names

    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_means.plot(kind="bar", ax=ax)

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months")

    fig.tight_layout()
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot() -> plt.Figure:
    """Desenha dois box plots: anual (tendência) e mensal (sazonalidade)."""
    df_box = df.copy()
    if df_box.empty:
        df_box = pd.DataFrame({"date": pd.to_datetime([]), "value": []})
    else:
        df_box = df_box.reset_index()

    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(x="month", y="value", data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.tight_layout()
    fig.savefig("box_plot.png")
    return fig


if __name__ == "__main__":
    draw_line_plot()
    draw_bar_plot()
    draw_box_plot()
