try:
    from src.pipeline import run_pipeline
except ModuleNotFoundError:
    from pipeline import run_pipeline

# Configuration
INPUT_DIR = "input"
OUTPUT_DIR = "output"


def main():
    """Run CSV automation pipeline."""
    run_pipeline(INPUT_DIR, OUTPUT_DIR)


if __name__ == "__main__":
    main()
