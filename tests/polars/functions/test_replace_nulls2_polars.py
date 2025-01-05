import polars as pl
import pytest
from polars.testing import assert_frame_equal

from janitor import polars  # noqa: F401


@pytest.mark.functions
def test_replace_nulls_default():
    """Tests replacing all null values in all data."""
    df = pl.DataFrame(
        {
            "A": ["N/A", "value1", "missing", "valid", "None", "ExtraNull"],
            "B": ["123", "null", "456", "na", "789", "ExtraNull"],
            "C": ["?", "#N/A", "value3", "", "Removed", "UNKNOWN"],
        }
    )

    expected_data = pl.DataFrame(
        {
            "A": [None, "value1", None, "valid", None, "ExtraNull"],
            "B": ["123", None, "456", None, "789", "ExtraNull"],
            "C": [None, None, "value3", None, None, None],
        }
    )

    df = df.replace_nulls2()
    assert_frame_equal(df, expected_data)


@pytest.mark.functions
def test_replace_nulls_addnulls():
    """Tests replacing all null values in all data with additional nulls."""
    df = pl.DataFrame(
        {
            "A": ["N/A", "value1", "missing", "valid", "None", "ExtraNull"],
            "B": ["123", "null", "456", "na", "789", "ExtraNull"],
            "C": ["?", "#N/A", "value3", "", "Removed", "UNKNOWN"],
        }
    )

    expected_data = pl.DataFrame(
        {
            "A": [None, "value1", None, "valid", None, None],
            "B": ["123", None, "456", None, "789", None],
            "C": [None, None, "value3", None, None, None],
        }
    )

    extra_nulls = ["ExtraNull"]

    df = df.replace_nulls2(extra_nulls=extra_nulls)
    assert_frame_equal(df, expected_data)
