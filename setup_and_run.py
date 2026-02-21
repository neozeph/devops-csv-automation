import os
import pandas as pd
from src.main import main


def create_sample_data():
    """Creates a dummy CSV file in the input directory."""
    if not os.path.exists("input"):
        os.makedirs("input")

    # Create a sample dataset with some messy data (unsorted dates, missing values)
    data = {
        "Transaction Date": ["2023-10-01", "2023-10-05", "2023-10-02", None],
        "Product Name": ["Laptop", "Mouse", "Monitor", "HDMI Cable"],
        "Sales Amount": [1200.00, 25.50, 300.00, 15.00],
        "Region": ["North", "South", "East", "West"],
    }

    df = pd.DataFrame(data)
    file_path = os.path.join("input", "sales_data.csv")
    df.to_csv(file_path, index=False)
    print(f"Created sample data: {file_path}")


def create_additional_data():
    """Creates a second dummy CSV file with a different schema."""
    if not os.path.exists("input"):
        os.makedirs("input")

    data = {
        "Feedback Date": ["2023-11-01", "2023-11-03", "2023-11-02", None],
        "User ID": [101, 103, 102, 104],
        "Rating": [5, 4, 3, 1],
        "Comment": ["Great", "Good", "Okay", "Bad"],
    }

    df = pd.DataFrame(data)
    file_path = os.path.join("input", "customer_feedback.csv")
    df.to_csv(file_path, index=False)
    print(f"Created additional data: {file_path}")


def create_employee_data():
    """Creates a third dummy CSV file with employee records."""
    if not os.path.exists("input"):
        os.makedirs("input")

    data = {
        "Hire Date": ["2022-05-15", "2020-08-20", "2023-01-10", "2019-11-05"],
        "Employee ID": [1001, 1002, 1003, 1004],
        "Department": ["Engineering", "HR", "Sales", "Marketing"],
        "Salary": [95000, 65000, 72000, 80000],
        "Performance Score": [4.5, 3.8, 4.2, 4.0],
    }

    df = pd.DataFrame(data)
    file_path = os.path.join("input", "employee_records.csv")
    df.to_csv(file_path, index=False)
    print(f"Created additional data: {file_path}")


if __name__ == "__main__":
    # 1. Setup Data
    create_sample_data()
    create_additional_data()
    create_employee_data()

    # 2. Run the Pipeline
    print("\n--- Running Data Pipeline ---")
    main()

    # 3. Verify Outputs
    print("\n--- Output Files Generated ---")
    if os.path.exists("output"):
        for root, dirs, files in os.walk("output"):
            for file in files:
                print(f" - {os.path.join(root, file)}")
