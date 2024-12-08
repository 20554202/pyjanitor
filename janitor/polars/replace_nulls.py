"""replace_nulls implementation for polars."""

from janitor.utils import import_message

from .polars_flavor import register_dataframe_method

try:
    import polars as pl
except ImportError:
    import_message(
        submodule="polars",
        package="polars",
        conda_channel="conda-forge",
        pip_install=True,
    )


@register_dataframe_method
def replace_nulls(df: pl.DataFrame, extra_nulls: list = None) -> pl.DataFrame:
    """
    Replace specified null-like values with `None` in a Polars DataFrame.

    Parameters
    ----------
    df : pl.DataFrame
        The input Polars DataFrame to process.
    extra_nulls : list, optional
        Additional null-like values to replace, by default None.

    Returns
    -------
    pl.DataFrame
        A Polars DataFrame with specified null-like values replaced by `None`.
    """
    default_nulls = [
        "N/A",
        "NA",
        "n/a",
        "na",
        "NULL",
        "null",
        "None",
        "none",
        "NaN",
        "nan",
        "missing",
        "MISSING",
        "unknown",
        "UNKNOWN",
        "",
        " ",
        "?",
        "#N/A",
        "Removed",
        "#DIV/0",
    ]

    if extra_nulls:
        null_values = default_nulls + extra_nulls
    else:
        null_values = default_nulls

    df = df.with_columns(pl.all().replace(null_values, None))
    return df
