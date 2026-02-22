import pandas as pd


def prepare_chart_ready_data(df):
    """Return rows with missing values removed."""
    return df.dropna()


def export_plot_dataset(df):
    """Return numeric columns suitable for plotting."""
    return df.select_dtypes(include=["number"])


def generate_trend_dataset(df):
    """Return dataframe sorted by the first detected date/time column."""
    df_trend = df.copy()

    for col in df_trend.columns:
        if "date" in col.lower() or "time" in col.lower():
            try:
                df_trend[col] = pd.to_datetime(df_trend[col])
                df_trend = df_trend.sort_values(by=col)
                break
            except (ValueError, TypeError):
                continue

    return df_trend


def format_for_dashboard(df):
    """Return dataframe with normalized, dashboard-friendly column names."""
    df_dash = df.copy()
    df_dash.columns = [c.strip().lower().replace(" ", "_") for c in df_dash.columns]
    return df_dash


def create_visual_summary(df):
    """Return descriptive statistics for numeric columns."""
    return df.describe()


def generate_correlation_matrix(df):
    """Return correlation matrix for numeric columns when possible."""
    df_numeric = df.select_dtypes(include=["number"])
    if df_numeric.shape[1] > 1:
        return df_numeric.corr()
    return None
