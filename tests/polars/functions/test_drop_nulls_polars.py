import polars as pl
import pytest
from polars.testing import assert_frame_equal

from janitor import polars  # noqa: F401


@pytest.mark.functions
def test_drop_nulls_full_null_cols_1():
    """Tests dropping rows with all null values in all columns."""
    df = pl.DataFrame(
        {
            "A": [None, "value1", None, "valid"],
            "B": [None, "123", None, "456"],
            "C": [None, None, "value3", "value4"],
        }
    )

    expected_data = pl.DataFrame(
        {
            "A": ["value1", None, "valid"],
            "B": ["123", None, "456"],
            "C": [None, "value3", "value4"],
        }
    )

    df = df.drop_nulls(full_null_cols=1)
    assert_frame_equal(df, expected_data)


@pytest.mark.functions
def test_drop_nulls_full_null_cols_0():
    """Tests dropping rows with any null values in any column."""
    df = pl.DataFrame(
        {
            "A": [None, "value1", None, "valid"],
            "B": [None, "123", None, "456"],
            "C": [None, None, "value3", "value4"],
        }
    )

    expected_data = pl.DataFrame(
        {
            "A": ["valid"],
            "B": ["456"],
            "C": ["value4"],
        }
    )

    df = df.drop_nulls(full_null_cols=0)
    assert_frame_equal(df, expected_data)


@pytest.mark.functions
def test_drop_nulls_invalid_param():
    """Tests that an invalid parameter value raises a ValueError."""
    df = pl.DataFrame(
        {
            "A": [None, "value1", None, "valid"],
            "B": [None, "123", None, "456"],
            "C": [None, None, "value3", "value4"],
        }
    )

    with pytest.raises(ValueError, match="full_null_cols must be 0 or 1"):
        df.drop_nulls(full_null_cols=2)
