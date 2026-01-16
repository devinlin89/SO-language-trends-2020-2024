import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from cycler import cycler

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

def set_plot_style():
    """
    Sets global Matplotlib style for all figures.
    Intended for academic / report-ready visualizations.
    """

    plt.rcParams["axes.prop_cycle"] = (cycler(color=HIGH_VIS_15))

    plt.rcParams.update({
        # Font
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 12,

        # Figure
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
        "legend.fontsize": 12,
        "legend.frameon": True,
        "legend.labelspacing": 1.15,

        # Ticks
        "xtick.labelsize": 12,
        "ytick.labelsize": 12,
    })


def plot_line_chart_top_languages_trends(
    trends_df: pd.DataFrame,
    metric_name: str,
    top_n: int = 15,
    y_min: int | None = None,
    y_max: int | None = None
):

    """
    Plots line chart for the top n programming languages
    based on the most recent year's metric value.

    Parameters
    ----------
    trends_df : pd.DataFrame
        DataFrame with a 'Language' column and year columns (e.g. 2020-2024)
    metric_name : str
        Name of the metric (e.g. 'Usage', 'Desired', 'Admired')
    top_n : int
        Number of top languages to plot
    y_min : int or None
        Lower bound for y-axis (optional)
    y_max : int or None
        Upper bound for y-axis (optional)
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

    # Select top n languages by most recent year
    latest_year = year_columns[-1]

    top_languages = (
        trends_df
        .sort_values(by=latest_year, ascending=False)
        .head(top_n)
    )

    # Create figure (A4 portrait)
    plt.figure(figsize=(8.27, 11.69))

    for _, row in top_languages.iterrows():
        plt.plot(
            year_columns,
            row[year_columns],
            marker="o",
            linewidth=2,
            label=row["Language"]
        )

    plt.xlabel("Year")
    plt.ylabel(f"{metric_name} Percentage (%)")

    plt.title(
        f"{metric_name} Trends of Top {top_n} Programming Languages "
        f"({year_columns[0]}-{year_columns[-1]})", pad=20
    )

    plt.xticks(year_columns)

    if y_min is not None or y_max is not None:
        plt.ylim(
            y_min if y_min is not None else plt.ylim()[0],
            y_max if y_max is not None else plt.ylim()[1]
        )

    ax = plt.gca()

    if y_min is not None or y_max is not None:
        ax.set_ylim(
            bottom=y_min if y_min is not None else None,
            top=y_max if y_max is not None else None
        )
        ax.yaxis.set_minor_locator(MultipleLocator(1))
        ax.grid(True, which="major", linewidth=0.8)

    ax.yaxis.set_major_locator(MultipleLocator(5))

    plt.legend(
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        title="Languages",
        title_fontsize=14,
        frameon=True
    )

    plt.grid(True)
    plt.tight_layout()
    plt.show()

set_plot_style()