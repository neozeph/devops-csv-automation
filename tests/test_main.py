import os
import shutil
import pytest
import pandas as pd
from src.main import (
    prepare_chart_ready_data,
    format_for_dashboard,
    INPUT_DIR,
    OUTPUT_DIR,
)


# Setup and Teardown
@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: Create directories
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    yield
    # Teardown: Clean up output to keep environment clean
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)


@pytest.fixture
def sample_df():
    data = {
        "Date": ["2023-01-01", "2023-01-02", None],
        "Sales Amount": [100, 150, 200],
        "Region": ["North", "South", "East"],
    }
    return pd.DataFrame(data)


def test_prepare_chart_ready_data(sample_df):
    # Create a dummy subdir for the test
    output_subdir = os.path.join(OUTPUT_DIR, "test_file")
    os.makedirs(output_subdir, exist_ok=True)

    prepare_chart_ready_data(sample_df, output_subdir)
    expected_file = os.path.join(output_subdir, "01_chart_ready.csv")

    assert os.path.exists(expected_file)

    # Check if NA was dropped (row with None should be gone)
    df_result = pd.read_csv(expected_file)
    assert len(df_result) == 2


def test_format_for_dashboard(sample_df):
    output_subdir = os.path.join(OUTPUT_DIR, "test_file")
    os.makedirs(output_subdir, exist_ok=True)

    format_for_dashboard(sample_df, output_subdir)
    expected_file = os.path.join(output_subdir, "04_dashboard.csv")

    assert os.path.exists(expected_file)

    df_result = pd.read_csv(expected_file)
    # Check column renaming
    assert "sales_amount" in df_result.columns
    assert "region" in df_result.columns
