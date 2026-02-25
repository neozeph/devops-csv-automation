import glob
import os
import sys
import pandas as pd


def validate_visual_summary(df, output_dir):
    """Validate that the generated SVG matches the input dataframe stats."""
    svg_path = os.path.join(output_dir, "05_summary.svg")
    if not os.path.exists(svg_path):
        raise FileNotFoundError(f"Validation failed: {svg_path} not found.")

    with open(svg_path, "r", encoding="utf-8") as f:
        content = f.read()

    rows_count = len(df)
    if f">{rows_count}</text>" not in content:
        raise ValueError(f"Validation failed: Row count {rows_count} not found in SVG.")

    df_numeric = df.select_dtypes(include=["number"])
    num_cols = len(df_numeric.columns)
    if f">{num_cols}</text>" not in content:
        raise ValueError(
            f"Validation failed: Numeric column count {num_cols} not found in SVG."
        )

    missing_cells = int(df.isna().sum().sum())
    completeness = 100.0
    if df.size:
        completeness = max(0.0, ((df.size - missing_cells) / df.size) * 100)

    comp_str = f"{completeness:.1f}%"
    if comp_str not in content:
        raise ValueError(
            f"Validation failed: Completeness {comp_str} not found in SVG."
        )

    print(f"Validated: {svg_path}")


def main():
    input_dir = "input"
    output_dir = "output"

    if not os.path.exists(output_dir) or not os.listdir(output_dir):
        print(
            f"Validation failed: Output directory '{output_dir}' is missing or empty."
        )
        sys.exit(1)

    csv_files = glob.glob(os.path.join(input_dir, "*.csv"))
    if not csv_files:
        print("No CSV files found to validate.")
        return

    has_error = False
    for filepath in csv_files:
        filename = os.path.basename(filepath)
        try:
            df = pd.read_csv(filepath)
            file_stem = os.path.splitext(filename)[0]
            file_output_dir = os.path.join(output_dir, file_stem)
            validate_visual_summary(df, file_output_dir)
        except Exception as exc:
            print(f"Error validating {filename}: {exc}")
            has_error = True

    if has_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
