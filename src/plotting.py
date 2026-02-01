import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from cycler import cycler
from helpers import truncate_label

from pathlib import Path
FIG_DIR = Path("../figures")

# Saving Function

def save_figure(
    filename: str,
    folder: str,
    dpi: int = 300,
    bbox_inches: str = "tight"
):
    """
    Saves the current Matplotlib figure to the figures directory.
    """

    folder_path = FIG_DIR / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    path = folder_path / filename
    plt.savefig(path, dpi=dpi, bbox_inches=bbox_inches)


# High-visibility color set

HIGH_VIS_15 = [
    "#0d49fb",  # vivid blue
    "#e6091c",  # red
    "#26eb47",  # green
    "#8936df",  # purple
    "#fec32d",  # yellow
    "#25d7fd",  # cyan
    "#ff7f0e",  # orange
    "#2ca02c",  # dark green
    "#d62728",  # dark red
    "#9467bd",  # muted purple
    "#8c564b",  # brown
    "#17becf",  # teal
    "#bcbd22",  # olive
    "#7f7f7f",  # grey
    "#e377c2",  # pink
]


# Global plotting style

def set_plot_style():
    """
    Sets global Matplotlib style for figures.
    """

    plt.rcParams["axes.prop_cycle"] = cycler(color=HIGH_VIS_15)

    plt.rcParams.update({
        # Fonts
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 12,

        # Figure resolution
        "figure.dpi": 120,
        "savefig.dpi": 300,

        # Axes
        "axes.titlesize": 16,
        "axes.labelsize": 16,

        # Grid
        "axes.grid": True,
        "grid.alpha": 0.5,
        "grid.linestyle": "-",

        # Lines
        "lines.linewidth": 2,
        "lines.markersize": 5,

        # Legend
        "legend.fontsize": 10,
        "legend.labelspacing": 1.15,
        "legend.frameon": False,  # no border

        # Ticks
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
    })


# Line chart function

def plot_line_chart_top_languages_trends(
    trends_df: pd.DataFrame,
    metric_name: str,
    top_n: int = 15,
    y_min: int | None = None,
    y_max: int | None = None,
    save: bool = False,
    filename: str | None = None
):
    """
    Plots line chart trends for the top N programming languages
    based on the most recent year's metric value.

    Parameters
    ----------
    trends_df : pd.DataFrame
        DataFrame containing a 'Language' column and year columns.
    metric_name : str
        Name of the metric (e.g. Usage, Desired, Loved/Admired).
    top_n : int
        Number of top languages to plot.
    y_min : int or None
        Optional lower bound for y-axis.
    y_max : int or None
        Optional upper bound for y-axis.
    """

    # Extract year columns dynamically
    year_columns = (
        trends_df
        .columns
        .drop("Language")
        .astype(int)
        .sort_values()
        .tolist()
    )

    latest_year = year_columns[-1]

    # Select top N languages by most recent year
    top_languages = (
        trends_df
        .sort_values(by=latest_year, ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # Create A4 portrait figure
    plt.figure(figsize=(8.27, 11.69))

    # Plot each language
    for rank, row in top_languages.iterrows():
        plt.plot(
            year_columns,
            row[year_columns],
            marker="o",
            label=f"{rank + 1}. {row['Language']}"
        )

    # Axis labels
    plt.xlabel("Year")
    plt.ylabel(f"{metric_name} Percentage (%)")

    # Centered figure-level title (accounts for legend)
    plt.suptitle(
        f"{metric_name} Trends of Top {top_n} Programming Languages "
        f"({year_columns[0]}-{year_columns[-1]})",
        fontsize=18,
        y=0.99
    )

    # X-axis formatting
    plt.xticks(year_columns)

    # Y-axis limits
    ax = plt.gca()
    if y_min is not None or y_max is not None:
        ax.set_ylim(
            bottom=y_min if y_min is not None else ax.get_ylim()[0],
            top=y_max if y_max is not None else ax.get_ylim()[1]
        )

    # Force ticks every 5 units
    ax.yaxis.set_major_locator(MultipleLocator(5))

    # Legend outside plot
    plt.legend(
        title="Languages",
        title_fontsize=14,
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )

    plt.tight_layout()

    if save:
        if filename is None:
            filename = f"{metric_name.lower().replace("/", "_")}_trends_line_chart.png"
        save_figure(filename, folder="Top_Languages_Trends_Line_Charts")

    plt.show()


# Bar chart function

def plot_relative_growth_bar_chart(
    measures_df: pd.DataFrame,
    metric_name: str,
    growth_column: str = "Relative Change (%)",
    top_n: int = 15,
    save: bool = False,
    filename: str | None = None
):
    """
    Plots a horizontal bar chart showing relative growth and decline
    for a given metric.

    Parameters
    ----------
    measures_df : pd.DataFrame
        DataFrame indexed by programming language.
    metric_name : str
        Name of the metric (Usage, Desired, Loved/Admired).
    growth_column : str
        Column containing relative growth values (percentage).
    top_n : int
        Number of top growing and declining languages to display.
    """

    # Drop missing or infinite values
    growth_series = (
        measures_df[growth_column]
        .replace([float("inf"), -float("inf")], pd.NA)
        .dropna()
    )

    # Select top growth and decline
    top_growth = growth_series.nlargest(top_n)
    top_decline = growth_series.nsmallest(top_n)

    plot_series = (
        pd.concat([top_growth, top_decline])
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8.27, 5))

    colors = [
        "#0d49fb" if value >= 0 else "#e6091c"
        for value in plot_series.values
    ]

    plt.bar(
        plot_series.index,
        plot_series.values,
        color=colors
    )

    plt.xlabel("Programming Language")
    plt.ylabel("Relative Change (%)")

    plt.xticks(rotation=45, ha="right")

    labels = [truncate_label(l) for l in plot_series.index]
    positions = range(len(labels))

    ax = plt.gca()
    ax.set_xticks(positions)
    ax.set_xticklabels(labels)

    ax.grid(axis="x", which="major")

    plt.title(
        f"Relative Change in {metric_name} "
        f"(Top {top_n} Growth and Decline)",
        pad=20
    )

    plt.tight_layout(pad=1.5)

    if save:
        if filename is None:
            filename = f"{metric_name.lower().replace("/", "_")}_relative_growth_bar_chart.png"
        save_figure(filename, folder="Relative_Change_Bar_Charts")

    plt.show()


# Individual language line chart function

def plot_single_language_trend(
    trends_df: pd.DataFrame,
    language: str,
    metric_name: str,
    min_range: float = 10,
    save: bool = False,
    filename: str | None = None
):
    """
    Plots the trend of a single programming language over time.
    Ensures a minimum y-axis range and annotates net change.
    """

    # Extract year columns
    year_columns = (
        trends_df
        .columns
        .drop("Language")
        .astype(int)
        .sort_values()
        .tolist()
    )

    series = (
        trends_df
        .loc[trends_df["Language"] == language, year_columns]
        .squeeze()
        .dropna()
    )

    if len(series) < 2:
        print(f"Not enough data to plot {language}.")
        return

    years = series.index.tolist()
    values = series.values

    plt.figure(figsize=(6, 4))

    plt.plot(
        years,
        values,
        marker="o",
        linewidth=2
    )

    plt.title(
        f"{language} {metric_name} Trend ({years[0]}-{years[-1]})",
        pad=15
    )
    plt.xlabel("Year")
    plt.ylabel(f"{metric_name} Percentage (%)")
    plt.xticks(years)

    # Y-axis scaling logic
    y_min_data = values.min()
    y_max_data = values.max()
    data_range = y_max_data - y_min_data

    # Ensure minimum vertical span
    if data_range < min_range:
        mid = (y_min_data + y_max_data) / 2
        y_min = mid - min_range / 2
        y_max = mid + min_range / 2
    else:
        y_min = y_min_data - 0.1 * data_range
        y_max = y_max_data + 0.1 * data_range

    # Snap to multiples of 10
    y_min = 10 * np.floor(y_min / 10)
    y_max = 10 * np.ceil(y_max / 10)

    # Clip to valid percentage range
    y_min = max(0, y_min)
    y_max = min(100, y_max)

    ax = plt.gca()
    ax.set_ylim(y_min, y_max)

    # Major and minor ticks
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_minor_locator(MultipleLocator(1))

    ax.grid(True, which="major", linewidth=0.8)

    # Net change annotation
    net_change = values[-1] - values[0]
    sign = "+" if net_change >= 0 else ""
    color = "#0d49fb" if net_change >= 0 else "#e6091c"

    ax.text(
        0.02,
        0.95,
        f"Net change: {sign}{net_change:.2f} pp",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        color=color
    )

    plt.tight_layout()

    if save:
        if filename is None:
            filename = f"{language.lower().replace("/", "_")}_{metric_name.lower().replace("/", "_")}_trend_line_chart.png"
        save_figure(filename, folder=f"Individual_Language_Line_Charts/{metric_name.replace("/", "_")}")

    plt.show()


# Gap bar chart function

def plot_gap_bar_chart(
    gap_series: pd.Series,
    metric_label: str,
    top_n: int = 5,
    figsize: tuple = (8, 6)
):
    """
    Plots a horizontal bar chart showing the gap between two metrics
    (e.g. Admired-Desired or Usage-Desired).

    Parameters
    ----------
    gap_series : pd.Series
        Series indexed by Language containing gap values (can be positive or negative).
    metric_label : str
        Label describing the gap (e.g. "Admired-Desired", "Usage-Desired").
    top_n : int
        Number of top positive and top negative gaps to display.
    figsize : tuple
        Figure size.
    """

    # Select top positive and negative gaps
    top_positive = gap_series.sort_values(ascending=False).head(top_n)
    top_negative = gap_series.sort_values(ascending=True).head(top_n)

    plot_data = pd.concat([top_positive, top_negative[::-1]])

    # Colors: blue for positive, red for negative
    colors = plot_data.apply(lambda x: "#0d49fb" if x >= 0 else "#e6091c")

    fig, ax = plt.subplots(figsize=figsize)

    ax.barh(
        plot_data.index,
        plot_data.values,
        color=colors
    )

    ax.set_xlabel("Distance Percentage Points (%)")
    ax.set_title(
        f"{metric_label} \n(Top {top_n} Lowest and Highest)",
        pad=15
    )

    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.xaxis.set_minor_locator(MultipleLocator(1))

    ax.grid(axis="x", linestyle="-", alpha=0.4)
    ax.grid(axis="y", visible=False)

    plt.tight_layout()
    plt.show()


# Scatter plot function

def plot_language_scatter(
    df,
    x_col: str,
    y_col: str,
    title: str,
    x_label: str,
    y_label: str,
    annotate: bool = False
):
    """
    Plots a scatterplot comparing two language metrics (e.g. Usage vs Desired).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame indexed by language.
    x_col : str
        Column name for x-axis values.
    y_col : str
        Column name for y-axis values.
    title : str
        Plot title.
    x_label : str
        X-axis label.
    y_label : str
        Y-axis label.
    annotate : bool, optional
        Whether to annotate points with language names.
    """

    x = df[x_col]
    y = df[y_col]

    # Axis limits snapped to multiples of 10
    min_val = int(np.floor(min(x.min(), y.min()) / 10) * 10)
    max_val = int(np.ceil(max(x.max(), y.max()) / 10) * 10)

    fig, ax = plt.subplots(figsize=(7, 7))

    ax.scatter(x, y, s=30, marker="x")

    # 45-degree reference line
    ax.plot(
        [min_val, max_val],
        [min_val, max_val],
        linestyle="--",
        linewidth=1,
        alpha=0.7
    )

    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)

    ax.set_aspect("equal", adjustable="box")

    ax.set_title(title, pad=20)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.set_xticks(range(min_val, max_val + 1, 10))
    ax.set_yticks(range(min_val, max_val + 1, 10))

    ax.grid(True)

    if annotate:
        for lang, xv, yv in zip(df.index, x, y):
            ax.annotate(
                lang,
                (xv, yv),
                textcoords="offset points",
                xytext=(5, 5),
                fontsize=8
            )

    plt.tight_layout()
    plt.show()


set_plot_style()
