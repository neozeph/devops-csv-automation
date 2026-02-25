from unittest.mock import patch

from src.pipeline import run_pipeline


@patch("src.pipeline.glob.glob")
@patch("src.pipeline.pd.read_csv")
def test_pipeline_handles_corrupt_csv(mock_read_csv, mock_glob, capsys):
    """
    Negative Testing: Ensure pipeline catches errors for corrupt files
    and continues or exits gracefully without crashing the script.
    """
    # Setup: Mock finding one file, but reading it raises an error
    mock_glob.return_value = ["input/corrupt.csv"]
    mock_read_csv.side_effect = Exception("Corrupt file format")

    # Run
    run_pipeline("input", "output")

    # Verify: Check that the error was logged to stdout
    captured = capsys.readouterr()
    assert "Failed to process corrupt.csv: Corrupt file format" in captured.out


@patch("src.pipeline.glob.glob")
def test_pipeline_handles_empty_input_dir(mock_glob, capsys):
    """Negative Testing: Ensure pipeline handles empty input directory."""
    mock_glob.return_value = []
    run_pipeline("input", "output")
    captured = capsys.readouterr()
    assert "No CSV files found" in captured.out
