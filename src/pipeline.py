import glob
import os
import pandas as pd

try:
    from src.processing import (
        create_visual_summary,
        export_plot_dataset as build_plot_dataset,
        format_for_dashboard as build_dashboard_dataset,
        generate_correlation_matrix as build_correlation_matrix,
        generate_trend_dataset as build_trend_dataset,
        prepare_chart_ready_data as build_chart_ready_dataset,
    )
except ModuleNotFoundError:
    from processing import (
        create_visual_summary,
        export_plot_dataset as build_plot_dataset,
        format_for_dashboard as build_dashboard_dataset,
        generate_correlation_matrix as build_correlation_matrix,
        generate_trend_dataset as build_trend_dataset,
        prepare_chart_ready_data as build_chart_ready_dataset,
    )


def prepare_chart_ready_data(df, output_dir):
    """Clean missing values and write chart-ready data."""
    df_clean = build_chart_ready_dataset(df)
    save_file(df_clean, "01_chart_ready.csv", output_dir)


def export_plot_dataset(df, output_dir):
    """Extract numeric columns and write plot dataset."""
    df_numeric = build_plot_dataset(df)
    save_file(df_numeric, "02_plot_dataset.csv", output_dir)


def generate_trend_dataset(df, output_dir):
    """Sort dataset on date/time columns and write trend data."""
    df_trend = build_trend_dataset(df)
    save_file(df_trend, "03_trend.csv", output_dir)


def format_for_dashboard(df, output_dir):
    """Normalize columns and write dashboard data."""
    df_dash = build_dashboard_dataset(df)
    save_file(df_dash, "04_dashboard.csv", output_dir)


def create_visual_summary_csv(df, output_dir):
    """Generate summary statistics CSV."""
    summary = create_visual_summary(df)
    save_file(summary, "05_summary.csv", output_dir, include_index=True)


def generate_correlation_matrix(df, output_dir):
    """Generate numeric correlation matrix when enough numeric columns exist."""
    corr_matrix = build_correlation_matrix(df)
    if corr_matrix is not None:
        save_file(corr_matrix, "06_correlation.csv", output_dir, include_index=True)


def save_file(df, filename, output_dir, include_index=False):
    """Helper to save a dataframe to the output directory."""
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=include_index)
    print(f"Saved: {output_path}")


def run_pipeline(input_dir, output_dir):
    """Process every CSV file in input_dir and write transformed outputs."""
    os.makedirs(output_dir, exist_ok=True)
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    if not csv_files:
        print("No CSV files found in input/ folder.")
        return

    for filepath in csv_files:
        filename = os.path.basename(filepath)
        try:
            print(f"Processing {filename}...")
            df = pd.read_csv(filepath)

            file_stem = os.path.splitext(filename)[0]
            file_output_dir = os.path.join(output_dir, file_stem)
            os.makedirs(file_output_dir, exist_ok=True)

            prepare_chart_ready_data(df, file_output_dir)
            export_plot_dataset(df, file_output_dir)
            generate_trend_dataset(df, file_output_dir)
            format_for_dashboard(df, file_output_dir)
            create_visual_summary_csv(df, file_output_dir)
            generate_correlation_matrix(df, file_output_dir)
        except Exception as exc:
            print(f"Failed to process {filename}: {exc}")
