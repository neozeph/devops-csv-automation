import pandas as pd

from src.processing import (
    create_visual_summary,
    export_plot_dataset,
    format_for_dashboard,
    generate_correlation_matrix,
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


def test_create_visual_summary_and_correlation_outputs():
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": [2, 4, 6, 8],
            "Label": ["x", "y", "z", "w"],
        }
    )

    summary = create_visual_summary(df)
    corr = generate_correlation_matrix(df)
    assert "mean" in summary.index
    assert corr is not None
    assert list(corr.columns) == ["A", "B"]


def test_generate_correlation_matrix_returns_none_with_single_numeric_column():
    df = pd.DataFrame({"A": [1, 2, 3], "Label": ["x", "y", "z"]})
    assert generate_correlation_matrix(df) is None
