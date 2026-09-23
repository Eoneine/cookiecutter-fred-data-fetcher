import pandas as pd
from fred_data_pipeline.features import clean_data, reshape_data


def test_clean_data_converts_types():
    """Test that clean_data properly converts date and value columns."""
    df_dummy = pd.DataFrame({
        "date": ["2024-01-01", "2024-02-01"],
        "value": ["100.5", "."],   # "." = FRED's missing-value marker
        "series_id": ["GDP", "GDP"],
    })
    result = clean_data(df_dummy)

    assert pd.api.types.is_datetime64_any_dtype(result["date"])
    assert pd.api.types.is_numeric_dtype(result["value"])
    assert result["value"].isna().sum() == 1  # "." must become NaN


def test_reshape_data_wide_has_one_column_per_series():
    """Test that wide format creates one column per series_id."""
    df_long = pd.DataFrame({
        "date": pd.to_datetime(["2024-01-01", "2024-01-01"]),
        "series_id": ["GDP", "UNRATE"],
        "value": [100.5, 3.9],
    })
    df_wide = reshape_data(df_long, output_format="wide")

    assert "GDP" in df_wide.columns
    assert "UNRATE" in df_wide.columns


def test_reshape_data_rejects_unknown_format():
    """Test that an unknown format raises ValueError."""
    df_long = pd.DataFrame({"date": [], "series_id": [], "value": []})
    try:
        reshape_data(df_long, output_format="tall")
        assert False, "should have raised ValueError"
    except ValueError:
        pass
