import pandas as pd
import numpy as np
from src.processing import (
    prepare_chart_ready_data,
    export_plot_dataset,
    generate_trend_dataset,
    format_for_dashboard,
    create_visual_summary,
)

# --- 1. Functional & Negative Testing ---


def test_prepare_chart_ready_data_empty():
    """Test with an empty DataFrame."""
    df = pd.DataFrame()
    result = prepare_chart_ready_data(df)
    assert result.empty


def test_prepare_chart_ready_data_all_null():
    """Test with a DataFrame containing only null values."""
    df = pd.DataFrame({"A": [None, np.nan], "B": [pd.NA, None]})
    result = prepare_chart_ready_data(df)
    assert result.empty


def test_export_plot_dataset_no_numeric():
    """Test with a DataFrame containing no numeric columns."""
    df = pd.DataFrame(
        {
            "A": ["a", "b"],
            "B": [pd.Timestamp("2023-01-01"), pd.Timestamp("2023-01-02")],
        }
    )
    result = export_plot_dataset(df)
    assert result.empty
    assert len(result.columns) == 0


def test_generate_trend_dataset_no_date():
    """Test with a DataFrame containing no date columns."""
    df = pd.DataFrame({"A": [3, 1, 2], "B": ["x", "y", "z"]})
    result = generate_trend_dataset(df)
    # Should return copy, unsorted (or original order)
    pd.testing.assert_frame_equal(result, df)


def test_generate_trend_dataset_garbage_date():
    """Test with a 'date' column that contains garbage (should not crash)."""
    df = pd.DataFrame({"date_col": ["not-a-date", "still-not-a-date"], "val": [1, 2]})
    # Should catch ValueError internally and return original df without sorting/converting
    result = generate_trend_dataset(df)
    pd.testing.assert_frame_equal(result, df)


def test_format_for_dashboard_special_chars():
    """Test column normalization with special characters."""
    df = pd.DataFrame({" User @ Name ": ["Alice"], "# ID": [1], "Plan ($)": [100]})
    result = format_for_dashboard(df)
    expected_cols = ["user_@_name", "#_id", "plan_($)"]
    assert list(result.columns) == expected_cols


# --- 2. Edge Case Testing ---


def test_edge_case_single_row():
    """Test processing with a single row."""
    df = pd.DataFrame({"Date": ["2023-01-01"], "Sales": [100]})

    # Chart ready
    assert len(prepare_chart_ready_data(df)) == 1
    # Plot dataset
    assert len(export_plot_dataset(df).columns) == 1
    # Trend
    trend = generate_trend_dataset(df)
    assert trend.iloc[0]["Date"] == pd.Timestamp("2023-01-01")
    # Summary
    svg = create_visual_summary(df)
    assert "Sales" in svg


def test_edge_case_large_dataset():
    """Test processing with a larger dataset (10,000 rows)."""
    # Create a simple large DF
    df = pd.DataFrame(
        {
            "Date": pd.date_range(start="2020-01-01", periods=10000),
            "Value": np.random.rand(10000),
        }
    )

    # Just ensure it runs without error and returns correct shape
    res = prepare_chart_ready_data(df)
    assert len(res) == 10000


def test_edge_case_all_nan_numeric_summary():
    """Test visual summary generation when numeric columns exist but are all NaN."""
    df = pd.DataFrame({"A": [np.nan, np.nan], "B": ["text", "text"]})
    svg = create_visual_summary(df)
    # Ensure we don't generate invalid SVG attributes like height="nan"
    assert 'height="nan"' not in svg
