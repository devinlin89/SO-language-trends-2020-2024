import pandas as pd

def calculate_multiselect_percentage(survey_df: pd.DataFrame,
    column: str, excluded_languages: set | None = None) -> pd.Series:

    """
    Calculates the percentage distribution for a multi-select survey column.

    Each response may contain multiple selections separated by semicolons.
    The function counts how often each option appears and divides it by
    the total number of respondents who answered the question.

    Parameters
    ----------
    survey_df : pandas.DataFrame
        DataFrame containing survey responses for one year.
    column : str
        Name of the multi-select column to analyze.

    Returns
    -------
    pandas.Series
        Series indexed by option, containing percentages sorted in
        descending order.
    """

    responses = survey_df[column].dropna()
    total_respondents = responses.shape[0]

    option_counts = (
        responses
        .str.split(";")
        .explode()
        .str.strip()
        .value_counts()
    )

    option_counts = option_counts[
        ~option_counts.index.isin(excluded_languages)
    ]

    percentages = (option_counts / total_respondents) * 100

    return percentages.sort_values(ascending=False)


def calculate_admired_percentage(survey_df: pd.DataFrame,
    have_column: str = "LanguageHaveWorkedWith",
    want_column: str = "LanguageWantToWorkWith",
    excluded_languages: set | None = None) -> pd.Series:

    """
    Calculates the Admired percentage for programming languages.

    Admired is defined as the percentage of respondents who used a language
    in the past year and want to continue using it next year.

    Parameters
    ----------
    survey_df : pandas.DataFrame
        DataFrame containing survey responses for one year.
    have_column : str
        Column listing languages respondents have worked with.
    want_column : str
        Column listing languages respondents want to work with next year.

    Returns
    -------
    pandas.Series
        Series indexed by programming language, containing Admired
        percentages sorted in descending order.
    """

    # Keep only respondents who answered BOTH questions
    valid_responses = survey_df[[have_column, want_column]].dropna()

    admired_counts = {}
    used_counts = {}

    for _, row in valid_responses.iterrows():
        used = {
            lang.strip()
            for lang in row[have_column].split(";")
            if lang.strip() not in excluded_languages
        }

        wanted = {
            lang.strip()
            for lang in row[want_column].split(";")
            if lang.strip() not in excluded_languages
        }

        for lang in used:
            used_counts[lang] = used_counts.get(lang, 0) + 1
            if lang in wanted:
                admired_counts[lang] = admired_counts.get(lang, 0) + 1

    admired_percentage = {
        lang: (admired_counts.get(lang, 0) / used_counts[lang]) * 100
        for lang in used_counts
    }

    return (
        pd.Series(admired_percentage)
        .sort_values(ascending=False)
    )
