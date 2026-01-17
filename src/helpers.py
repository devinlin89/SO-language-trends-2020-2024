import pandas as pd

def generate_metric_trends(metric_by_year: dict) -> pd.DataFrame:
    """
    Assembles yearly metric Series into a single trends DataFrame.

    Parameters
    ----------
    metric_by_year : dict
        Dictionary mapping year (int) to a pandas Series containing
        metric values indexed by option (e.g. programming language).

    Returns
    -------
    pandas.DataFrame
        DataFrame indexed by option with columns representing years.
    """

    # Ensure consistent year ordering
    ordered_years = sorted(metric_by_year.keys())

    # Creates metric trends DataFrame
    trends_df = pd.DataFrame({
        year: metric_by_year[year]
        for year in ordered_years
    })

    # Move index to column
    trends_df = trends_df.reset_index()

    # Rename the index column to "Language"
    trends_df = trends_df.rename(
        columns={trends_df.columns[0]: "Language"}
    )

    return trends_df


def generate_measures_df(metric_name: str,
    metric_trends_df: pd.DataFrame,
    language_column: str = "Language") -> pd.DataFrame:

    """
    Assembles metric trends DataFrame into DatFrame with these measures:
    - Mean of metric
    - Absolute change
    - Average yearly change
    - Relative change

    Parameters
    ----------
    metric_name: str
        Name of the metric

    metric_trends_df : pandas.DataFrame
        DataFrame containing metric data of all languages in every year

    Returns
    -------
    pandas.DataFrame
        DataFrame indexed by option with columns representing years.
    """

    # Creates measures dataframe
    metric_measures_df = pd.DataFrame(
        index=metric_trends_df[language_column]
    )

    # Identify year columns
    year_columns = sorted(
        metric_trends_df.columns.drop(language_column)
    )

    # Mean across all years
    metric_measures_df[f"Mean {metric_name}"] = (
        metric_trends_df[year_columns]
        .mean(axis="columns")
        .values
    )

    # Absolute change from first to last year
    metric_measures_df["4-year Change"] = (
        metric_trends_df[year_columns[-1]] - metric_trends_df[year_columns[0]]
    ).values

    # Average yearly change
    metric_measures_df["Annual Change"] = (
        metric_measures_df["4-year Change"] / (len(year_columns) - 1)
    )

    # Relative Change
    metric_measures_df["Relative Change (%)"] = (
        metric_measures_df["4-year Change"] / metric_trends_df[year_columns[0]].values
    ).replace([float("inf"), -float("inf")], pd.NA) * 100

    return metric_measures_df


def truncate_label(label: str, max_len: int = 16) -> str:
    """
    Truncates a text label to a specified maximum length.

    If the label exceeds the maximum length, it is shortened and appended
    with an ellipsis to preserve readability in plots.

    Parameters
    ----------
    label : str
        The label text to be evaluated.
    max_len : int
        The maximum allowed length of the label in characters.

    Returns
    -------
    str
        The original label if its length is within the limit;
        otherwise, a truncated version ending with an ellipsis.
    """

    return label if len(label) <= max_len else label[:max_len - 6] + "…"