"""clean_excel_dates implementation for polars."""

from datetime import datetime, timedelta

from dateutil import parser

from janitor.utils import import_message

from .polars_flavor import register_expr_method

try:
    import polars as pl
except ImportError:
    import_message(
        submodule="polars",
        package="polars",
        conda_channel="conda-forge",
        pip_install=True,
    )


# Register `clean_dates` as an expression method
@register_expr_method
def clean_excel_dates(
    expr: pl.Expr,
    excel: bool = False,
    format: str = None,
    **kwargs,
) -> pl.Expr:
    """
    Clean date expressions in a Polars column.

    Args:
        expr: Polars expression to clean.
        excel: If True, interpret values as Excel numeric dates.
        format: Optional, format cleaned dates as strings.
        kwargs: Additional arguments for `dateutil.parser.parse`.

    Returns:
        Polars expression with cleaned dates.
    """
    if excel:
        expr = _parse_excel_dates_expr(expr)
    else:
        expr = _parse_generic_dates_expr(expr, **kwargs)

    if format:
        expr = _format_dates_expr(expr, format)

    return expr


# Private Helper: Parse Excel Dates
def _parse_excel_dates_expr(expr: pl.Expr) -> pl.Expr:
    """
    Parse Excel numeric dates into Python dates.

    Args:
        expr: Polars expression to parse.

    Returns:
        Polars expression with parsed dates.
    """
    excel_epoch = datetime(1899, 12, 30)

    return expr.map_elements(
        lambda x: (
            (excel_epoch + timedelta(days=int(float(x)))).date()
            if x is not None
            else None
        ),
        return_dtype=pl.Date,
    )


# Private Helper: Parse Generic Date Strings
def _parse_generic_dates_expr(expr: pl.Expr, **kwargs) -> pl.Expr:
    """
    Parse generic date strings into Python dates.

    Args:
        expr: Polars expression to parse.
        kwargs: Additional arguments for `dateutil.parser.parse`.

    Returns:
        Polars expression with parsed dates.
    """
    return expr.map_elements(
        lambda x: parser.parse(x, **kwargs).date() if x else None,
        return_dtype=pl.Date,
    )


# Private Helper: Format Dates
def _format_dates_expr(expr: pl.Expr, format: str) -> pl.Expr:
    """
    Format dates into specified string format.

    Args:
        expr: Polars expression with parsed dates.
        format: String format for the dates.

    Returns:
        Polars expression with formatted date strings.
    """
    return expr.map_elements(
        lambda d: d.strftime(format) if d else None, return_dtype=pl.Utf8
    )
