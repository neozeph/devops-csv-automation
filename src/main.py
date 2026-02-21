import os
import glob
import pandas as pd

# Configuration
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def prepare_chart_ready_data(df, output_dir):
    """Cleans missing values and prepares data for visualization."""
    df_clean = df.dropna()
    save_file(df_clean, "01_chart_ready.csv", output_dir)


def export_plot_dataset(df, output_dir):
    """Extracts numeric columns for plotting."""
    df_numeric = df.select_dtypes(include=["number"])
    save_file(df_numeric, "02_plot_dataset.csv", output_dir)


def generate_trend_dataset(df, output_dir):
    """Sorts and formats date columns for trend analysis."""
    df_trend = df.copy()
    # Attempt to identify date columns automatically
    for col in df_trend.columns:
        if "date" in col.lower() or "time" in col.lower():
            try:
                df_trend[col] = pd.to_datetime(df_trend[col])
                df_trend = df_trend.sort_values(by=col)
                break
            except (ValueError, TypeError):
                continue
    save_file(df_trend, "03_trend.csv", output_dir)


def format_for_dashboard(df, output_dir):
    """Standardizes column names for dashboard compatibility."""
    df_dash = df.copy()
    df_dash.columns = [c.strip().lower().replace(" ", "_") for c in df_dash.columns]
    save_file(df_dash, "04_dashboard.csv", output_dir)


def create_visual_summary_csv(df, output_dir):
    """Generates summary statistics."""
    summary = df.describe()
    save_file(summary, "05_summary.csv", output_dir, include_index=True)


def generate_correlation_matrix(df, output_dir):
    """Generates a correlation matrix for numeric columns (heatmap ready)."""
    df_numeric = df.select_dtypes(include=["number"])
    if df_numeric.shape[1] > 1:
        corr_matrix = df_numeric.corr()
        save_file(corr_matrix, "06_correlation.csv", output_dir, include_index=True)


def save_file(df, filename, output_dir, include_index=False):
    """Helper to save dataframe to output directory."""
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=include_index)
    print(f"Saved: {output_path}")


def main():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Find all CSV files in input directory
    csv_files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))

    if not csv_files:
        print("No CSV files found in input/ folder.")
        return

    for filepath in csv_files:
        try:
            filename = os.path.basename(filepath)
            print(f"Processing {filename}...")
            df = pd.read_csv(filepath)

            # Create a specific directory for this file's outputs
            file_stem = os.path.splitext(filename)[0]
            file_output_dir = os.path.join(OUTPUT_DIR, file_stem)
            os.makedirs(file_output_dir, exist_ok=True)

            prepare_chart_ready_data(df, file_output_dir)
            export_plot_dataset(df, file_output_dir)
            generate_trend_dataset(df, file_output_dir)
            format_for_dashboard(df, file_output_dir)
            create_visual_summary_csv(df, file_output_dir)
            generate_correlation_matrix(df, file_output_dir)

        except Exception as e:
            print(f"Failed to process {filename}: {e}")


if __name__ == "__main__":
    main()
