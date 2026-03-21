import glob
import logging
import os
from datetime import datetime
import pandas as pd

try:
    from src.processing import (
        create_visual_summary,
        export_plot_dataset as build_plot_dataset,
        format_for_dashboard as build_dashboard_dataset,
        generate_trend_dataset as build_trend_dataset,
        prepare_chart_ready_data as build_chart_ready_dataset,
    )
except ModuleNotFoundError:
    from processing import (
        create_visual_summary,
        export_plot_dataset as build_plot_dataset,
        format_for_dashboard as build_dashboard_dataset,
        generate_trend_dataset as build_trend_dataset,
        prepare_chart_ready_data as build_chart_ready_dataset,
    )


def setup_logging(log_dir="logs"):
    """Configure logging to file and console."""
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"pipeline_{timestamp}.log")
    
    # Create logger
    logger = logging.getLogger("csv_pipeline")
    logger.setLevel(logging.DEBUG)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


# Initialize logger
logger = setup_logging()


def prepare_chart_ready_data(df, output_dir):
    """Clean missing values and write chart-ready data."""
    df_clean = build_chart_ready_dataset(df)
    save_file(df_clean, "01_chart_ready.csv", output_dir)
    return df_clean


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
    """Generate summary statistics image (SVG)."""
    summary_svg = create_visual_summary(df)
    output_path = os.path.join(output_dir, "05_summary.svg")
    with open(output_path, "w", encoding="utf-8") as svg_file:
        svg_file.write(summary_svg)
    logger.debug(f"Saved: {output_path}")


def save_file(df, filename, output_dir, include_index=False):
    """Helper to save a dataframe to the output directory."""
    output_path = os.path.join(output_dir, filename)
    df.to_csv(output_path, index=include_index)
    logger.debug(f"Saved: {output_path}")


def run_pipeline(input_dir, output_dir):
    """Process every CSV file in input_dir and write transformed outputs."""
    logger.info("="*60)
    logger.info("Starting CSV Automation Pipeline")
    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")
    logger.info("="*60)
    
    os.makedirs(output_dir, exist_ok=True)
    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))

    if not csv_files:
        logger.warning("No CSV files found in input/ folder.")
        return

    logger.info(f"Found {len(csv_files)} CSV file(s) to process")
    
    processed_count = 0
    failed_count = 0

    for filepath in csv_files:
        filename = os.path.basename(filepath)
        try:
            logger.info(f"Processing {filename}...")
            df = pd.read_csv(filepath)
            logger.debug(f"  - Rows: {len(df)}, Columns: {len(df.columns)}")

            file_stem = os.path.splitext(filename)[0]
            file_output_dir = os.path.join(output_dir, file_stem)
            os.makedirs(file_output_dir, exist_ok=True)

            df_clean = prepare_chart_ready_data(df, file_output_dir)
            export_plot_dataset(df_clean, file_output_dir)
            generate_trend_dataset(df_clean, file_output_dir)
            format_for_dashboard(df_clean, file_output_dir)
            create_visual_summary_csv(df, file_output_dir)
            
            logger.info(f"✓ Successfully processed {filename}")
            processed_count += 1
        except Exception as exc:
            logger.error(f"✗ Failed to process {filename}: {exc}", exc_info=True)
            failed_count += 1
    
    logger.info("="*60)
    logger.info(f"Pipeline Complete - Processed: {processed_count}, Failed: {failed_count}")
    logger.info("="*60)
