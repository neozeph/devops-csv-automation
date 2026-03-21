import pandas as pd
import pytest

from src.processing import (
    create_visual_summary,
    export_plot_dataset,
    format_for_dashboard,
    generate_trend_dataset,
    prepare_chart_ready_data,
)


def test_prepare_chart_ready_data_drops_missing_values():
    df = pd.DataFrame(
        {
            "Date": ["2023-01-01", None, "2023-01-03"],
            "Sales": [10, 20, 30],
        }
    )

    result = prepare_chart_ready_data(df)
    assert len(result) == 2


def test_export_plot_dataset_keeps_only_numeric_columns():
    df = pd.DataFrame(
        {
            "Date": ["2023-01-01", "2023-01-02"],
            "Sales": [100.0, 120.0],
            "Units": [1, 2],
            "Region": ["North", "South"],
        }
    )

    result = export_plot_dataset(df)
    assert list(result.columns) == ["Sales", "Units"]


def test_generate_trend_dataset_sorts_by_date_column():
    df = pd.DataFrame(
        {
            "Transaction Date": ["2023-01-03", "2023-01-01", "2023-01-02"],
            "Sales": [30, 10, 20],
        }
    )

    result = generate_trend_dataset(df)
    assert result["Transaction Date"].iloc[0] == pd.Timestamp("2023-01-01")
    assert result["Transaction Date"].iloc[2] == pd.Timestamp("2023-01-03")


def test_format_for_dashboard_normalizes_column_names():
    df = pd.DataFrame({" Sales Amount ": [100], "Region Name": ["North"]})

    result = format_for_dashboard(df)
    assert list(result.columns) == ["sales_amount", "region_name"]


def test_create_visual_summary_output():
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": [2, 4, 6, 8],
            "Label": ["x", "y", "z", "w"],
        }
    )

    summary = create_visual_summary(df)
    assert summary.startswith("<svg")
    assert "Visual Summary" in summary
    assert "mean" in summary.lower()


def test_create_visual_summary_handles_all_nan_numeric_column():
    df = pd.DataFrame({"A": [float("nan"), float("nan")], "Label": ["x", "y"]})

    summary = create_visual_summary(df)
    assert 'height="nan"' not in summary
    assert 'y="nan"' not in summary


@pytest.mark.parametrize(
    "func",
    [
        prepare_chart_ready_data,
        export_plot_dataset,
        generate_trend_dataset,
        format_for_dashboard,
        create_visual_summary,
    ],
)
@pytest.mark.parametrize("invalid_df", [None, [], {"A": [1, 2]}, "bad_input", 7])
def test_processing_functions_raise_type_error_for_invalid_input(func, invalid_df):
    with pytest.raises(TypeError, match="pandas DataFrame"):
        func(invalid_df)
