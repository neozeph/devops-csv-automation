import re

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


def test_create_visual_summary_places_quick_stats_above_trend_preview():
    df = pd.DataFrame(
        {
            "A": [1, 2, 3, 4],
            "B": [2, 4, 6, 8],
            "Label": ["x", "y", "z", "w"],
        }
    )

    summary = create_visual_summary(df)
    quick_stats = re.search(
        r'<text x="(?P<x>[\d.]+)" y="(?P<y>[\d.]+)"[^>]*>Quick Stats</text>',
        summary,
    )
    trend_preview = re.search(
        r'<text x="(?P<x>[\d.]+)" y="(?P<y>[\d.]+)"[^>]*>Trend Preview</text>',
        summary,
    )

    assert quick_stats is not None
    assert trend_preview is not None
    assert float(quick_stats.group("x")) > float(trend_preview.group("x"))
    assert float(quick_stats.group("y")) < float(trend_preview.group("y"))


def test_create_visual_summary_renders_y_axis_labels_for_trend_preview():
    df = pd.DataFrame(
        {
            "A": [2, 4, 6, 8],
            "B": [1, 3, 5, 7],
            "Label": ["x", "y", "z", "w"],
        }
    )

    summary = create_visual_summary(df)
    y_axis_labels = re.findall(
        r'font-size="11" fill="#94a3b8" text-anchor="end" dominant-baseline="middle">([^<]+)</text>',
        summary,
    )

    assert len(y_axis_labels) == 5
    assert y_axis_labels[0] == "8"
    assert y_axis_labels[-1] == "2"


def test_create_visual_summary_compacts_quick_stats_for_many_numeric_columns():
    df = pd.DataFrame({f"Metric {idx}": [idx, idx + 1, idx + 2] for idx in range(1, 9)})

    summary = create_visual_summary(df)

    assert "Showing 6 of 8 numeric columns" in summary
    assert "+2 more numeric columns not shown" in summary


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
