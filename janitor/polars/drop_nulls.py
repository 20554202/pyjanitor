"""drop_nulls implementation for polars."""

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
def drop_nulls(df: pl.DataFrame, full_null_cols: int = 1) -> pl.DataFrame:
    """
    Drop rows based on null values in a Polars DataFrame.

    Parameters
    ----------
    df : pl.DataFrame
        The input Polars DataFrame to process.
    full_null_cols : int, optional
        Determines which rows to drop:
        - `1`: Drop rows with all columns null (default).
        - `0`: Drop rows with any null values in any column.

    Returns
    -------
    pl.DataFrame
        A Polars DataFrame with the appropriate rows dropped.

    Raises
    ------
    ValueError
        If `full_null_cols` is not 0 or 1.
    """
    if full_null_cols == 1:
        df = df.filter(~pl.all_horizontal(pl.all().is_null()))
    elif full_null_cols == 0:
        df = df.filter(~pl.any_horizontal(pl.all().is_null()))
    else:
        raise ValueError("full_null_cols must be 0 or 1")
    return df
