from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Any
import pandas as pd
import numpy as np


app = FastAPI(
    title="AutoEDA API",
    description="Automated Exploratory Data Analysis API",
    version="1.0.0"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class DatasetPayload(BaseModel):
    row_count: int
    data: list[dict[str, Any]]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def detect_column_type(series, column_name=""):

    # ----------------------------------------
    # 1. Already numeric
    # ----------------------------------------

    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    non_null = series.dropna()

    if len(non_null) == 0:
        return "empty"

    # ----------------------------------------
    # 2. Explicit year detection
    # ----------------------------------------

    name = column_name.lower()

    if "year" in name:
        numeric_test = pd.to_numeric(
            non_null.astype("string").str.strip(),
            errors="coerce"
        )

        if numeric_test.notna().mean() >= 0.90:
            return "numeric"

    # ----------------------------------------
    # 3. Numeric conversion
    # ----------------------------------------

    numeric_test = pd.to_numeric(
        non_null.astype("string").str.strip(),
        errors="coerce"
    )

    if numeric_test.notna().mean() >= 0.90:
        return "numeric"

    # ----------------------------------------
    # 4. Only try datetime for date-like names
    # ----------------------------------------

    date_keywords = (
        "date",
        "time",
        "timestamp",
        "created",
        "updated",
        "added"
    )

    looks_like_date = any(
        keyword in name
        for keyword in date_keywords
    )

    if looks_like_date:

        datetime_test = pd.to_datetime(
            non_null,
            errors="coerce",
            format="mixed"
        )

        if datetime_test.notna().mean() >= 0.90:
            return "datetime"

    # ----------------------------------------
    # 5. Categorical vs text
    # ----------------------------------------

    unique_count = series.nunique(dropna=True)
    total_count = series.notna().sum()

    if total_count == 0:
        return "empty"

    unique_ratio = unique_count / total_count

    if unique_ratio > 0.50:
        return "text"

    return "categorical"


def numeric_statistics(series):

    series = series.dropna()

    if len(series) == 0:
        return {}

    # IQR outliers
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = series[
        (series < lower_bound) |
        (series > upper_bound)
    ]

    return {
        "count": int(series.count()),

        "mean": round(float(series.mean()), 2),

        "median": round(float(series.median()), 2),

        "std": round(float(series.std()), 2),

        "min": round(float(series.min()), 2),

        "q1": round(float(q1), 2),

        "q3": round(float(q3), 2),

        "max": round(float(series.max()), 2),

        "skewness": round(float(series.skew()), 2),

        "outlier_count": int(len(outliers)),

        "outlier_percentage": round(
            float(len(outliers) / len(series) * 100),
            2
        )
    }


def categorical_statistics(series, top_n=10):

    value_counts = (
        series
        .dropna()
        .value_counts()
        .head(top_n)
    )

    total = series.notna().sum()

    categories = []

    for value, count in value_counts.items():

        percentage = (
            count / total * 100
            if total > 0
            else 0
        )

        categories.append({
            "value": str(value),
            "count": int(count),
            "percentage": round(
                float(percentage),
                2
            )
        })

    return {
        "unique_count": int(
            series.nunique(dropna=True)
        ),

        "top_values": categories
    }


# ============================================================
# MAIN EDA ENDPOINT
# ============================================================


def detect_type(series):
    if pd.api.types.is_numeric_dtype(series):
        return "numeric"

    non_null = series.dropna()

    if len(non_null) == 0:
        return "empty"

    # Only detect datetime AFTER numeric detection
    dt = pd.to_datetime(non_null, errors="coerce")

    if dt.notna().mean() >= 0.90:
        return "datetime"

    ratio = (
        series.nunique(dropna=True)
        / series.notna().sum()
    )

    return "text" if ratio > 0.50 else "categorical"


@app.post("/analyze")
def analyze_dataset(payload: DatasetPayload):

    try:

        df = pd.DataFrame(payload.data)
        df = df.loc[:, df.columns.str.strip() != ""]
        df = df.loc[:, ~df.columns.str.startswith("Unnamed")]

        # ========================================
        # AUTOMATIC TYPE INFERENCE
        # ========================================

        for column in df.columns:

            if pd.api.types.is_numeric_dtype(df[column]):
                continue

            converted = pd.to_numeric(
                df[column]
                .astype("string")
                .str.strip(),
                errors="coerce"
            )

            original_non_null = df[column].notna().sum()

            if original_non_null > 0:

                conversion_rate = (
                    converted.notna().sum()
                    / original_non_null
                )

                if conversion_rate >= 0.90:
                    df[column] = converted

        # ========================================
        # COLUMN TYPE DETECTION
        # ========================================

        column_types = {}

        for column in df.columns:

            column_types[column] = detect_column_type(
                df[column],
                column
            )

        # ----------------------------------------------------
        # Dataset overview
        # ----------------------------------------------------

        overview = {

            "rows": int(df.shape[0]),

            "columns": int(df.shape[1]),

            "memory_usage_mb": round(
                float(
                    df.memory_usage(
                        deep=True
                    ).sum()
                    / 1024**2
                ),
                2
            ),

            "duplicate_rows": int(
                df.duplicated().sum()
            ),

            "duplicate_percentage": round(
                float(
                    df.duplicated().mean() * 100
                ),
                2
            )
        }

        # ----------------------------------------------------
        # Missing values
        # ----------------------------------------------------

        missing_analysis = []

        for column in df.columns:

            missing_count = int(
                df[column].isna().sum()
            )

            missing_percentage = (
                missing_count
                / len(df)
                * 100
            )

            missing_analysis.append({

                "column": column,

                "missing_count": missing_count,

                "missing_percentage": round(
                    float(missing_percentage),
                    2
                ),

                "present_count": int(
                    df[column].notna().sum()
                )
            })

        # Sort missing values from highest to lowest

        missing_analysis.sort(
            key=lambda x: x["missing_count"],
            reverse=True
        )

        # ----------------------------------------------------
        # Column information
        # ----------------------------------------------------

        columns = []

        for column in df.columns:

            series = df[column]

            columns.append({

                "name": column,

                "dtype": str(
                    series.dtype
                ),

                "detected_type": column_types[column],

                "unique_count": int(
                    series.nunique(
                        dropna=True
                    )
                ),

                "missing_count": int(
                    series.isna().sum()
                ),

                "missing_percentage": round(
                    float(
                        series.isna().mean() * 100
                    ),
                    2
                )
            })

        # ----------------------------------------------------
        # Numerical analysis
        # ----------------------------------------------------

        numerical_analysis = {}

        for column in df.columns:

            if column_types[column] == "numeric":

                numerical_analysis[column] = (
                    numeric_statistics(
                        df[column]
                    )
                )

        # ----------------------------------------------------
        # Categorical analysis
        # ----------------------------------------------------

        categorical_analysis = {}

        for column in df.columns:

            if column_types[column] == "categorical":

                categorical_analysis[column] = (
                    categorical_statistics(
                        df[column]
                    )
                )

        # ----------------------------------------------------
        # Datetime analysis
        # ----------------------------------------------------

        datetime_analysis = {}

        for column in df.columns:

            if column_types[column] == "datetime":

                datetime_series = pd.to_datetime(
                    df[column],
                    errors="coerce"
                )

                datetime_analysis[column] = {

                    "min_date": (
                        str(datetime_series.min())
                        if datetime_series.notna().any()
                        else None
                    ),

                    "max_date": (
                        str(datetime_series.max())
                        if datetime_series.notna().any()
                        else None
                    ),

                    "date_range_days": (
                        int(
                            (
                                datetime_series.max()
                                - datetime_series.min()
                            ).days
                        )
                        if datetime_series.notna().any()
                        else None
                    )
                }

        # ----------------------------------------------------
        # Final response
        # ----------------------------------------------------

        return {

            "status": "success",

            "overview": overview,

            "columns": columns,

            "missing_values": missing_analysis,

            "column_types": column_types,

            "numerical_analysis": numerical_analysis,

            "categorical_analysis": categorical_analysis,

            "datetime_analysis": datetime_analysis

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"EDA failed: {str(e)}"
        )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "status": "online",
        "service": "AutoEDA API",
        "endpoint": "POST /analyze"
    }


@app.post("/generate-charts")
def generate_charts(payload: dict):

    try:

        data = payload.get("data", [])
        charts = payload.get("charts", [])

        df = pd.DataFrame(data)

        generated_charts = []

        for chart in charts:

            chart_type = chart.get("type")

            # --------------------------------------------------
            # Single-column chart types
            # --------------------------------------------------

            if chart_type in ("histogram", "boxplot", "bar", "line"):

                column = chart.get("column")

                if column not in df.columns:
                    continue

                # -----------------------------
                # Histogram
                # -----------------------------

                if chart_type == "histogram":

                    values = (
                        pd.to_numeric(
                            df[column],
                            errors="coerce"
                        )
                        .dropna()
                        .tolist()
                    )

                    generated_charts.append({
                        "type": "histogram",
                        "column": column,
                        "title": chart.get(
                            "title",
                            f"Distribution of {column}"
                        ),
                        "values": values
                    })

                # -----------------------------
                # Boxplot
                # -----------------------------

                elif chart_type == "boxplot":

                    values = (
                        pd.to_numeric(
                            df[column],
                            errors="coerce"
                        )
                        .dropna()
                        .tolist()
                    )

                    generated_charts.append({
                        "type": "boxplot",
                        "column": column,
                        "title": chart.get(
                            "title",
                            f"Box Plot of {column}"
                        ),
                        "values": values
                    })

                # -----------------------------
                # Bar chart
                # -----------------------------

                elif chart_type == "bar":

                    counts = (
                        df[column]
                        .dropna()
                        .astype(str)
                        .value_counts()
                        .head(
                            chart.get("top_n", 10)
                        )
                    )

                    generated_charts.append({
                        "type": "bar",
                        "column": column,
                        "title": chart.get(
                            "title",
                            f"Distribution of {column}"
                        ),
                        "labels": counts.index.tolist(),
                        "values": counts.values.tolist()
                    })

                # -----------------------------
                # Line chart
                # -----------------------------

                elif chart_type == "line":

                    dates = pd.to_datetime(
                        df[column],
                        errors="coerce"
                    )

                    counts = (
                        dates
                        .dropna()
                        .dt.to_period("M")
                        .value_counts()
                        .sort_index()
                    )

                    generated_charts.append({
                        "type": "line",
                        "column": column,
                        "title": chart.get(
                            "title",
                            f"{column} Over Time"
                        ),
                        "labels": [
                            str(x)
                            for x in counts.index
                        ],
                        "values": counts.values.tolist()
                    })

            # --------------------------------------------------
            # Scatter — two-column chart type (x, y)
            # --------------------------------------------------

            elif chart_type == "scatter":

                x_col = chart.get("x")
                y_col = chart.get("y")

                if x_col not in df.columns or y_col not in df.columns:
                    continue

                paired = pd.DataFrame({
                    "x": pd.to_numeric(df[x_col], errors="coerce"),
                    "y": pd.to_numeric(df[y_col], errors="coerce")
                }).dropna()

                if paired.empty:
                    continue

                generated_charts.append({
                    "type": "scatter",
                    "x": x_col,
                    "y": y_col,
                    "title": chart.get(
                        "title",
                        f"{x_col} vs {y_col}"
                    ),
                    "x_values": paired["x"].tolist(),
                    "y_values": paired["y"].tolist()
                })

            # --------------------------------------------------
            # Correlation heatmap — multi-column chart type
            # --------------------------------------------------

            elif chart_type == "correlation_heatmap":

                requested_columns = chart.get("columns", [])

                valid_columns = [
                    col for col in requested_columns
                    if col in df.columns
                ]

                if len(valid_columns) < 2:
                    continue

                numeric_df = df[valid_columns].apply(
                    pd.to_numeric,
                    errors="coerce"
                )

                corr_matrix = numeric_df.corr().round(2)

                # Replace NaNs (e.g. from constant columns) so JSON stays valid
                corr_matrix = corr_matrix.where(
                    pd.notna(corr_matrix),
                    None
                )

                generated_charts.append({
                    "type": "correlation_heatmap",
                    "columns": valid_columns,
                    "title": chart.get(
                        "title",
                        "Correlation Matrix"
                    ),
                    "matrix": corr_matrix.values.tolist(),
                    "labels": valid_columns
                })

        return {
            "status": "success",
            "chart_count": len(generated_charts),
            "charts": generated_charts
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Chart generation failed: {str(e)}"
        )
