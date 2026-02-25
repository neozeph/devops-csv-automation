# DevOps CSV Automation

## 📌 Project Title
**DevOps CSV Automation**

## 📌 What the system does
This project implements an automated data processing pipeline for CSV files. It ingests raw sales data, cleans it, formats it for dashboards, generates trend datasets, and creates visual summaries. The project demonstrates a complete DevOps lifecycle with CI/CD integration, automated testing, linting, security scanning, and automated data updates via GitHub Actions.

## 📌 Folder structure
```
devops-csv-automation/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions workflow definition
├── src/
│   ├── main.py              # Main entry point for the pipeline
│   ├── pipeline.py          # Pipeline orchestration logic
│   ├── processing.py        # Core data processing functions
│   └── validate.py          # Output validation script
├── tests/
│   ├── test_main.py         # Integration tests for the pipeline
│   └── test_processing.py   # Unit tests for processing logic
├── output/                  # Directory for processed output files
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## 📌 How to install
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/devops-csv-automation.git
   cd devops-csv-automation
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📌 How to run
To execute the data processing pipeline manually:
```bash
python src/main.py
```
This will read input data, process it, and generate files in the `output/` directory.

## 📌 How to run tests
The project uses `pytest` for testing.
```bash
python -m pytest
```

## 📌 Sample input & output
**Input:** Raw CSV data containing columns like `Date`, `Sales Amount`, and `Region`.

**Output:**
- `01_chart_ready.csv`: Cleaned dataset with missing values removed.
- `04_dashboard.csv`: Dataset with normalized column names (e.g., `Sales Amount` -> `sales_amount`).
- Visual Summary: An SVG representation of data distribution.

---

## 2️⃣ Document Each Function

### `prepare_chart_ready_data(df)`
**Purpose:**
Cleans the raw dataset to ensure it is ready for visualization by removing missing values.
**Input:**
`df` (pandas DataFrame): Raw data.
**Output:**
DataFrame with missing values (NaN) removed.

### `format_for_dashboard(df)`
**Purpose:**
Standardizes column names for compatibility with dashboard tools (lowercase, underscores).
**Input:**
`df` (pandas DataFrame): Data with arbitrary column names.
**Output:**
DataFrame with normalized headers.

### `generate_trend_dataset(df)`
**Purpose:**
Prepares data for time-series trend analysis by sorting by date.
**Input:**
`df` (pandas DataFrame): Data containing date information.
**Output:**
DataFrame sorted by the date column.

---

## 3️⃣ DevOps Workflow

1. **Push to GitHub:** Code changes trigger the CI pipeline defined in `.github/workflows/ci.yml`.
2. **GitHub Actions:**
   - **Linting & Formatting:** Checks code style with `flake8` and `black`.
   - **Security:** Scans for vulnerabilities using `bandit` and `safety`.
   - **Testing:** Runs unit tests with `pytest`.
3. **Automated Processing:** If tests pass, the pipeline runs `src/main.py` to regenerate output data.
4. **Validation:** `src/validate.py` ensures the output meets quality standards.
5. **Commit & Push:** The bot commits the updated `output/` folder back to the repository.

## 4️⃣ Simple System Flow Diagram

```
User Uploads CSV
        ↓
Data Processing Functions (src/processing.py)
        ↓
Clean Dataset Generated (output/)
        ↓
Export / Dashboard Ready Output
```
