from html import escape

import pandas as pd


def prepare_chart_ready_data(df):
    """Return dataframe with rows containing any missing values dropped."""
    _ensure_dataframe(df)
    df_clean = df.copy()
    # Drop rows with any missing values
    df_clean = df_clean.dropna()
    return df_clean


def export_plot_dataset(df):
    """Return numeric columns suitable for plotting."""
    _ensure_dataframe(df)
    df_numeric = df.select_dtypes(include=["number"])
    # Fill NaN values in numeric columns with 0
    df_numeric = df_numeric.fillna(0)
    return df_numeric


def generate_trend_dataset(df):
    """Return dataframe sorted by the first detected date/time column, or unchanged if all date parsing fails."""
    _ensure_dataframe(df)
    df_trend = df.copy()

    for col in df_trend.columns:
        if "date" in col.lower() or "time" in col.lower():
            try:
                # Try to parse as datetime
                df_trend[col] = pd.to_datetime(df_trend[col], errors="raise")
                # Sort by this column
                df_trend = df_trend.sort_values(by=col)
                return df_trend
            except (ValueError, TypeError):
                # This column can't be parsed; try the next one
                continue

    # If no date column was found or all failed, return original unchanged data
    return df


def format_for_dashboard(df):
    """Return dataframe with normalized, dashboard-friendly column names."""
    _ensure_dataframe(df)
    df_dash = df.copy()
    df_dash.columns = [c.strip().lower().replace(" ", "_") for c in df_dash.columns]
    return df_dash


def create_visual_summary(df):
    """Return a visual summary image (SVG) for numeric columns."""
    _ensure_dataframe(df)
    df_numeric = df.select_dtypes(include=["number"])
    return _dashboard_svg(df, df_numeric)


def _dashboard_svg(df, df_numeric):
    """Render a dashboard-style summary with charts and rounded cards."""
    width = 1200
    height = 760
    pad = 24

    rows_count = len(df)
    numeric_cols = len(df_numeric.columns)
    missing_cells = int(df.isna().sum().sum())
    completeness = 100.0
    if df.size:
        completeness = max(0.0, ((df.size - missing_cells) / df.size) * 100)

    summary_df = (
        df_numeric.describe().round(2) if not df_numeric.empty else pd.DataFrame()
    )

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        'font-family="Poppins, Segoe UI, Arial, sans-serif">',
        (
            '<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0%" stop-color="#060b17"/><stop offset="100%" stop-color="#111b30"/>'
            '</linearGradient><linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0%" stop-color="#2dd4bf"/><stop offset="100%" stop-color="#0ea5e9"/>'
            "</linearGradient></defs>"
        ),
        f'<rect width="{width}" height="{height}" fill="url(#bg)"/>',
        '<circle cx="1080" cy="60" r="160" fill="#22d3ee" opacity="0.08"/>',
        '<circle cx="980" cy="20" r="120" fill="#34d399" opacity="0.07"/>',
        f'<text x="{pad}" y="{pad + 10}" font-size="34" font-weight="700" fill="#f8fafc">Visual Summary Dashboard</text>',
        (
            f'<text x="{pad}" y="{pad + 40}" font-size="15" fill="#94a3b8">'
            "Automated Profile for Incoming CSV Data</text>"
        ),
    ]

    card_y = 86
    card_h = 124
    gap = 24
    left_x = pad
    left_w = 744
    panel_h = 280
    right_x = left_x + left_w + gap
    right_w = width - right_x - pad

    # Match KPI row width to the two-panel grid below for exact alignment.
    kpi_layout = [
        (left_x, 360),
        (left_x + 360 + gap, 360),
        (right_x, right_w),
    ]
    kpis = [
        ("Rows", str(rows_count), "#38bdf8", "rows"),
        ("Numeric Columns", str(numeric_cols), "#34d399", "columns"),
        ("Data Completeness", f"{completeness:.1f}%", "#f59e0b", "check"),
    ]

    for idx, (label, value, color, icon_name) in enumerate(kpis):
        x, card_w = kpi_layout[idx]
        svg.append(
            f'<rect x="{x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="18" '
            'fill="#0f1b2e" stroke="#2a3a56"/>'
        )
        svg.append(
            f'<rect x="{x + 16}" y="{card_y + 10}" width="{card_w - 32}" height="6" '
            f'rx="3" fill="{color}" opacity="0.95"/>'
        )
        svg.append(
            f'<circle cx="{x + card_w - 50}" cy="{card_y + 64}" r="27" fill="{color}" opacity="0.18"/>'
        )
        svg.extend(_kpi_icon(icon_name, x + card_w - 50, card_y + 64, color))
        svg.append(
            f'<text x="{x + 20}" y="{card_y + 46}" font-size="18" font-weight="500" fill="#94a3b8">{label}</text>'
        )
        svg.append(
            f'<text x="{x + 20}" y="{card_y + 98}" font-size="46" font-weight="700" '
            f'fill="#f8fafc">{escape(value)}</text>'
        )

    top_y = card_y + card_h + 22

    svg.append(
        f'<rect x="{left_x}" y="{top_y}" width="{left_w}" height="{panel_h}" rx="20" '
        'fill="#0f1b2e" stroke="#2a3a56"/>'
    )
    svg.append(
        f'<text x="{left_x + 20}" y="{top_y + 34}" font-size="20" font-weight="600" fill="#e2e8f0">'
        "Column Mean Values</text>"
    )

    if not df_numeric.empty:
        means = df_numeric.mean().sort_values(ascending=False).head(7)
        bar_area_x = left_x + 52
        bar_area_y = top_y + 58
        bar_area_w = left_w - 84
        bar_area_h = panel_h - 96

        # Fix: Handle case where means.max() is NaN (all data is null)
        raw_max = float(means.max())
        max_mean = raw_max if (raw_max != 0 and raw_max == raw_max) else 1.0

        bar_slot = bar_area_w / max(1, len(means))
        bar_w = min(58, bar_slot * 0.62)

        for i, (name, val) in enumerate(means.items()):
            x = bar_area_x + (i * bar_slot) + ((bar_slot - bar_w) / 2)

            val_float = float(val)
            if val_float != val_float:  # Check for NaN
                val_float = 0.0

            h = (val_float / max_mean) * (bar_area_h - 8)
            y = bar_area_y + bar_area_h - h
            svg.append(
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_w:.2f}" height="{h:.2f}" rx="9" '
                'fill="url(#bar)"/>'
            )
            svg.append(
                f'<text x="{x + (bar_w / 2):.2f}" y="{bar_area_y + bar_area_h + 18}" '
                'font-size="12" fill="#cbd5e1" text-anchor="middle">'
                f"{_format_label(str(name)[:10])}</text>"
            )
            svg.append(
                f'<text x="{x + (bar_w / 2):.2f}" y="{max(top_y + 52, y - 6):.2f}" '
                'font-size="12" fill="#e2e8f0" text-anchor="middle">'
                f"{_fmt_num(val)}</text>"
            )
    else:
        svg.append(
            f'<text x="{left_x + 20}" y="{top_y + 68}" font-size="14" fill="#94a3b8">'
            "No Numeric Columns Available for Mean Chart.</text>"
        )

    svg.append(
        f'<rect x="{right_x}" y="{top_y}" width="{right_w}" height="{panel_h}" rx="20" '
        'fill="#0f1b2e" stroke="#2a3a56"/>'
    )
    svg.append(
        f'<text x="{right_x + 20}" y="{top_y + 34}" font-size="20" font-weight="600" fill="#e2e8f0">'
        "Trend Preview</text>"
    )

    if not df_numeric.empty:
        series = df_numeric.iloc[:, 0].dropna().head(40)
        if len(series) > 1:
            chart_x = right_x + 24
            chart_y = top_y + 54
            chart_w = right_w - 48
            chart_h = panel_h - 88
            s_min = float(series.min())
            s_max = float(series.max())
            span = s_max - s_min if s_max != s_min else 1.0

            points = []
            for i, val in enumerate(series):
                px = chart_x + (i * (chart_w / (len(series) - 1)))
                ratio = (float(val) - s_min) / span
                py = chart_y + chart_h - (ratio * chart_h)
                points.append(f"{px:.2f},{py:.2f}")
            polyline_points = " ".join(points)

            svg.append(
                f'<rect x="{chart_x}" y="{chart_y}" width="{chart_w}" height="{chart_h}" '
                'rx="12" fill="#0a1528" stroke="#2a3a56"/>'
            )
            svg.append(
                f'<polyline points="{polyline_points}" fill="none" stroke="#f59e0b" '
                'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            )
            trend_col_name = _format_label(str(series.name)[:20])
            svg.append(
                f'<text x="{chart_x}" y="{chart_y + chart_h + 20}" font-size="12" fill="#cbd5e1">'
                f"Trend: {trend_col_name}</text>"
            )
            svg.append(
                f'<text x="{chart_x + chart_w}" y="{chart_y + chart_h + 20}" '
                'font-size="12" fill="#cbd5e1" text-anchor="end">'
                f"Min {_fmt_num(s_min)}  Max {_fmt_num(s_max)}</text>"
            )
        else:
            svg.append(
                f'<text x="{right_x + 20}" y="{top_y + 68}" font-size="14" fill="#94a3b8">'
                "Not Enough Points to Draw a Trend Line.</text>"
            )
    else:
        svg.append(
            f'<text x="{right_x + 20}" y="{top_y + 68}" font-size="14" fill="#94a3b8">'
            "No Numeric Columns Available for Trend Preview.</text>"
        )

    bottom_y = top_y + panel_h + 22
    bottom_h = 220
    svg.append(
        f'<rect x="{pad}" y="{bottom_y}" width="{width - (pad * 2)}" height="{bottom_h}" rx="20" '
        'fill="#0f1b2e" stroke="#2a3a56"/>'
    )
    svg.extend(_quick_stats_icon(pad + 176, bottom_y + 26))
    svg.append(
        f'<text x="{pad + 20}" y="{bottom_y + 34}" font-size="20" font-weight="600" fill="#e2e8f0">'
        "Quick Stats</text>"
    )
    svg.append(f'<circle cx="{pad + 28}" cy="{bottom_y + 54}" r="4" fill="#f59e0b"/>')
    svg.append(
        f'<text x="{pad + 40}" y="{bottom_y + 58}" font-size="13" fill="#94a3b8">'
        f"Missing Cells: {missing_cells}</text>"
    )

    if not summary_df.empty:
        stats_cols = list(summary_df.columns[:4])
        start_x = pad + 20
        start_y = bottom_y + 102
        col_w = (width - (pad * 2) - 40) / max(1, len(stats_cols))
        for i, col_name in enumerate(stats_cols):
            x = start_x + (i * col_w)
            mean_val = (
                summary_df.at["mean", col_name] if "mean" in summary_df.index else "n/a"
            )
            min_val = (
                summary_df.at["min", col_name] if "min" in summary_df.index else "n/a"
            )
            max_val = (
                summary_df.at["max", col_name] if "max" in summary_df.index else "n/a"
            )
            svg.append(
                f'<rect x="{x:.2f}" y="{start_y - 26}" width="{col_w - 12:.2f}" height="122" rx="14" '
                'fill="#0a1528" stroke="#2a3a56"/>'
            )
            svg.extend(_quick_metric_icon(x + col_w - 34, start_y - 6, i))
            svg.append(
                f'<text x="{x + 14:.2f}" y="{start_y}" font-size="15" font-weight="600" fill="#f8fafc">'
                f"{_format_label(str(col_name)[:24])}</text>"
            )

            inner_x = x + 14
            inner_w = col_w - 42
            stat_w = inner_w / 3
            stat_y = start_y + 22
            stats = [
                ("Mean", mean_val, "mean"),
                ("Min", min_val, "min"),
                ("Max", max_val, "max"),
            ]
            for stat_idx, (label, value, kind) in enumerate(stats):
                sx = inner_x + (stat_idx * stat_w)
                svg.extend(_quick_stat_icon(kind, sx + 12, stat_y - 5))
                svg.append(
                    f'<text x="{sx + 30:.2f}" y="{stat_y + 4}" font-size="14" fill="#94a3b8">{label}</text>'
                )
                svg.append(
                    f'<text x="{sx + 30:.2f}" y="{stat_y + 28}" font-size="18" fill="#cbd5e1">'
                    f"{_fmt_num(value)}</text>"
                )
    else:
        svg.append(
            f'<text x="{pad + 20}" y="{bottom_y + 90}" font-size="14" fill="#94a3b8">'
            "No Numeric Summary Available.</text>"
        )

    svg.append("</svg>")
    return "\n".join(svg)


def _fmt_num(value):
    """Format numeric values for compact labels."""
    if isinstance(value, str):
        return value
    try:
        val = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(val) >= 1000:
        return f"{val:,.0f}"
    if abs(val) >= 10:
        return f"{val:.2f}".rstrip("0").rstrip(".")
    return f"{val:.3f}".rstrip("0").rstrip(".")


def _format_label(text):
    """Format text to appear formal: capitalize and replace underscores with spaces."""
    if not isinstance(text, str):
        text = str(text)
    # Replace underscores with spaces
    text = text.replace("_", " ")
    # Title case: capitalize first letter of each word
    text = text.title()
    return escape(text)


def _ensure_dataframe(df):
    """Raise a clear error when processing input is not a dataframe."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")


def _kpi_icon(icon_name, cx, cy, color):
    """Return simple inline SVG icon primitives for KPI cards."""
    if icon_name == "rows":
        return [
            (
                f'<rect x="{cx - 10}" y="{cy - 10}" width="20" height="20" rx="3.5" '
                f'fill="none" stroke="{color}" stroke-width="2.4"/>'
            ),
            f'<line x1="{cx - 10}" y1="{cy - 2}" x2="{cx + 10}" y2="{cy - 2}" stroke="{color}" stroke-width="2.4"/>',
            f'<line x1="{cx - 10}" y1="{cy + 5}" x2="{cx + 10}" y2="{cy + 5}" stroke="{color}" stroke-width="2.4"/>',
        ]
    if icon_name == "columns":
        return [
            (
                f'<rect x="{cx - 11}" y="{cy - 10}" width="7" height="20" rx="2.2" '
                f'fill="{color}" opacity="0.95"/>'
            ),
            (
                f'<rect x="{cx - 2}" y="{cy - 7}" width="7" height="17" rx="2.2" '
                f'fill="{color}" opacity="0.8"/>'
            ),
            f'<rect x="{cx + 7}" y="{cy - 13}" width="7" height="23" rx="2.2" fill="{color}" opacity="0.65"/>',
        ]
    return [
        (
            f'<line x1="{cx - 10}" y1="{cy}" x2="{cx - 2}" y2="{cy + 8}" '
            f'stroke="{color}" stroke-width="2.8" stroke-linecap="round"/>'
        ),
        (
            f'<line x1="{cx - 2}" y1="{cy + 8}" x2="{cx + 12}" y2="{cy - 10}" '
            f'stroke="{color}" stroke-width="2.8" stroke-linecap="round"/>'
        ),
    ]


def _quick_stats_icon(x, y):
    """Header icon for the quick-stats section."""
    return [
        f'<circle cx="{x}" cy="{y}" r="11" fill="#22d3ee" opacity="0.2"/>',
        f'<rect x="{x - 5}" y="{y - 3}" width="3" height="6" rx="1.5" fill="#22d3ee"/>',
        f'<rect x="{x - 1}" y="{y - 6}" width="3" height="9" rx="1.5" fill="#34d399"/>',
        f'<rect x="{x + 3}" y="{y - 1}" width="3" height="4" rx="1.5" fill="#f59e0b"/>',
    ]


def _quick_metric_icon(x, y, index):
    """Small decorative icon for each quick-stat card."""
    colors = ["#22d3ee", "#34d399", "#f59e0b", "#a78bfa"]
    color = colors[index % len(colors)]
    return [
        f'<circle cx="{x}" cy="{y}" r="11" fill="{color}" opacity="0.18"/>',
        (
            f'<line x1="{x - 5}" y1="{y + 2}" x2="{x}" y2="{y - 3}" '
            f'stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>'
        ),
        f'<line x1="{x}" y1="{y - 3}" x2="{x + 5}" y2="{y + 1}" stroke="{color}" stroke-width="2.4" stroke-linecap="round"/>',
    ]


def _quick_stat_icon(kind, cx, cy):
    """Per-metric icon for Mean/Min/Max in quick-stat cards."""
    if kind == "mean":
        return [
            f'<circle cx="{cx}" cy="{cy}" r="8.5" fill="#22d3ee" opacity="0.22"/>',
            (
                f'<line x1="{cx - 5}" y1="{cy}" x2="{cx + 5}" y2="{cy}" '
                'stroke="#22d3ee" stroke-width="2.4" stroke-linecap="round"/>'
            ),
        ]
    if kind == "min":
        return [
            f'<circle cx="{cx}" cy="{cy}" r="8.5" fill="#34d399" opacity="0.22"/>',
            (
                f'<polyline points="{cx - 5},{cy - 1} {cx},{cy + 4} {cx + 5},{cy - 4}" '
                'fill="none" stroke="#34d399" stroke-width="2.4" stroke-linecap="round" '
                'stroke-linejoin="round"/>'
            ),
        ]
    return [
        f'<circle cx="{cx}" cy="{cy}" r="8.5" fill="#f59e0b" opacity="0.22"/>',
        (
            f'<polyline points="{cx - 5},{cy + 4} {cx},{cy - 4} {cx + 5},{cy + 1}" '
            'fill="none" stroke="#f59e0b" stroke-width="2.4" stroke-linecap="round" '
            'stroke-linejoin="round"/>'
        ),
    ]
