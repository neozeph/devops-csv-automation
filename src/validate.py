import glob
import os
import sys
import pandas as pd
import defusedxml.ElementTree as ET


def validate_visual_summary(df, output_dir):
    """Validate that the generated SVG matches the input dataframe stats."""
    svg_path = os.path.join(output_dir, "05_summary.svg")
    if not os.path.exists(svg_path):
        raise FileNotFoundError(f"Validation failed: {svg_path} not found.")

    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
    except ET.ParseError as e:
        raise ValueError(f"Validation failed: Invalid SVG format. Error: {e}")

    # SVG namespace handling
    ns = {"svg": "http://www.w3.org/2000/svg"}
    # Extract all text content from the SVG
    text_elements = [elem.text for elem in root.findall(".//svg:text", ns) if elem.text]

    rows_count = len(df)
    if str(rows_count) not in text_elements:
        raise ValueError(f"Validation failed: Row count {rows_count} not found in SVG.")

    df_numeric = df.select_dtypes(include=["number"])
    num_cols = len(df_numeric.columns)
    if str(num_cols) not in text_elements:
        raise ValueError(
            f"Validation failed: Numeric column count {num_cols} not found in SVG."
        )

    missing_cells = int(df.isna().sum().sum())
    completeness = 100.0
    if df.size:
        completeness = max(0.0, ((df.size - missing_cells) / df.size) * 100)

    comp_str = f"{completeness:.1f}%"
    if comp_str not in text_elements:
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
