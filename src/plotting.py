import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from cycler import cycler
from helpers import truncate_label


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
    y_max: int | None = None
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
    plt.show()


# Bar chart function

def plot_relative_growth_bar_chart(
    measures_df: pd.DataFrame,
    metric_name: str,
    growth_column: str = "Relative Change (%)",
    top_n: int = 15
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
    plt.show()


# Individual language line chart function

def plot_single_language_trend(
    trends_df: pd.DataFrame,
    language: str,
    metric_name: str,
    min_range: float = 10
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
    ax.yaxis.set_major_locator(MultipleLocator(10))
    ax.yaxis.set_minor_locator(MultipleLocator(5))

    ax.grid(True, which="major", linewidth=0.8)
    ax.grid(True, which="minor", linewidth=0.4, alpha=0.4)

    # Net change annotation
    net_change = values[-1] - values[0]
    sign = "+" if net_change >= 0 else ""
    color = "#0d49fb" if net_change >= 0 else "#e6091c"

    ax.text(
        0.02,
        0.95,
        f"Net change: {sign}{net_change:.1f} pp",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=12,
        color=color
    )

    plt.tight_layout()
    plt.show()



set_plot_style()
