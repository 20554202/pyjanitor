from datetime import datetime

import polars as pl
from polars.testing import assert_frame_equal

from janitor import polars  # noqa: F401


def test_clean_dates_excel():
    """Test Excel numeric dates"""
    df = pl.DataFrame({"dates": [43831, 43832, None]})
    result = df.with_columns(pl.col("dates").clean_excel_dates(excel=True))

    expected = pl.DataFrame(
        {
            "dates": [
                datetime(2020, 1, 1).date(),
                datetime(2020, 1, 2).date(),
                None,
            ]
        }
    )
    assert_frame_equal(result, expected)


def test_clean_dates_generic_strings():
    """Test generic date strings"""
    df = pl.DataFrame({"dates": ["2023-10-11", "11/12/2023", None]})
    result = df.with_columns(pl.col("dates").clean_excel_dates())

    expected = pl.DataFrame(
        {
            "dates": [
                datetime(2023, 10, 11).date(),
                datetime(2023, 11, 12).date(),
                None,
            ]
        }
    )
    assert_frame_equal(result, expected)


def test_clean_dates_formatting():
    """Test date formatting"""
    df = pl.DataFrame({"dates": ["2023-10-11", "11/12/2023", None]})
    result = df.with_columns(
        pl.col("dates").clean_excel_dates(format="%d-%m-%Y")
    )

    expected = pl.DataFrame({"dates": ["11-10-2023", "12-11-2023", None]})
    assert_frame_equal(result, expected)


def test_clean_dates_excel_and_formatting():
    """Test Excel numeric dates with formatting"""
    df = pl.DataFrame({"dates": [43831, 43832, None]})
    result = df.with_columns(
        pl.col("dates").clean_excel_dates(excel=True, format="%Y/%m/%d")
    )

    expected = pl.DataFrame({"dates": ["2020/01/01", "2020/01/02", None]})
    assert_frame_equal(result, expected)


def test_clean_dates_with_kwargs():
    """Test generic date parsing with `dayfirst` argument"""
    df = pl.DataFrame({"dates": ["11/10/2023", "12/11/2023"]})
    result = df.with_columns(pl.col("dates").clean_excel_dates(dayfirst=True))

    expected = pl.DataFrame(
        {
            "dates": [
                datetime(2023, 10, 11).date(),
                datetime(2023, 11, 12).date(),
            ]
        }
    )
    assert_frame_equal(result, expected)
