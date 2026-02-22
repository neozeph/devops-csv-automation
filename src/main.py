try:
    from src.pipeline import (
        create_visual_summary_csv,
        export_plot_dataset,
        format_for_dashboard,
        generate_correlation_matrix,
        generate_trend_dataset,
        prepare_chart_ready_data,
        run_pipeline,
        save_file,
    )
except ModuleNotFoundError:
    from pipeline import (
        create_visual_summary_csv,
        export_plot_dataset,
        format_for_dashboard,
        generate_correlation_matrix,
        generate_trend_dataset,
        prepare_chart_ready_data,
        run_pipeline,
        save_file,
    )

# Configuration
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def main():
    """Run CSV automation pipeline."""
    run_pipeline(INPUT_DIR, OUTPUT_DIR)


if __name__ == "__main__":
    main()
