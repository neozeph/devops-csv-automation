import argparse

try:
    from src.pipeline import run_pipeline
except ModuleNotFoundError:
    from pipeline import run_pipeline

# Configuration
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def main():
    """Run CSV automation pipeline."""
    parser = argparse.ArgumentParser(description="DevOps CSV Automation Pipeline")
    parser.add_argument(
        "--input", default=INPUT_DIR, help="Directory containing input CSV files"
    )
    parser.add_argument(
        "--output", default=OUTPUT_DIR, help="Directory to save processed outputs"
    )
    args = parser.parse_args()

    run_pipeline(args.input, args.output)


if __name__ == "__main__":
    main()
