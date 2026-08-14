import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# ============================================================
# CONFIG
# ============================================================

st.set_page_config(
    page_title="AutoEDA",
    page_icon="📊",
    layout="wide"
)

N8N_WEBHOOK_URL = "https://exciting-pitch-code-indicates.trycloudflare.com/webhook/auto-eda"


# ============================================================
# THEME / CSS
# ============================================================
# ============================================================
# THEME / BLACK GRADIENT CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');


/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {

    font-family: 'Inter', sans-serif;

    background:
        radial-gradient(
            circle at 15% 10%,
            rgba(70, 70, 90, 0.22),
            transparent 35%
        ),
        radial-gradient(
            circle at 85% 20%,
            rgba(35, 35, 55, 0.30),
            transparent 40%
        ),
        radial-gradient(
            circle at 50% 100%,
            rgba(20, 20, 30, 0.50),
            transparent 45%
        ),
        linear-gradient(
            135deg,
            #050505 0%,
            #0b0b0f 45%,
            #111118 100%
        );

    color: #f5f5f5;
}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.block-container {

    max-width: 1250px;

    padding-top: 2rem;
    padding-bottom: 5rem;
}


/* ============================================================
   HIDE STREAMLIT DEFAULT UI
   ============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}


/* ============================================================
   NAVBAR
   ============================================================ */

.navbar {

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 0.8rem 0 1.4rem;

    margin-bottom: 3rem;

    border-bottom: 1px solid rgba(255,255,255,0.10);
}


.brand {

    font-size: 1.45rem;

    font-weight: 800;

    letter-spacing: -0.03em;

    color: #ffffff;

    display: flex;

    align-items: center;
}


.brand-mark {

    display: inline-flex;

    align-items: center;

    justify-content: center;

    width: 38px;

    height: 38px;

    margin-right: 11px;

    border-radius: 10px;

    background:
        linear-gradient(
            135deg,
            #ffffff,
            #777777
        );

    color: #050505;

    font-weight: 800;

    box-shadow:
        0 0 25px rgba(255,255,255,0.08);
}


.nav-badge {

    padding: 0.45rem 0.85rem;

    border-radius: 999px;

    font-size: 0.72rem;

    font-weight: 600;

    color: #d6d6d6;

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.12);

    backdrop-filter: blur(10px);
}


/* ============================================================
   HERO
   ============================================================ */

.hero {

    margin-bottom: 2.5rem;
}


.eyebrow {

    display: inline-block;

    padding: 0.4rem 0.8rem;

    border-radius: 999px;

    font-size: 0.72rem;

    font-weight: 600;

    letter-spacing: 0.08em;

    text-transform: uppercase;

    color: #cfcfcf;

    background: rgba(255,255,255,0.05);

    border: 1px solid rgba(255,255,255,0.10);

    margin-bottom: 1.2rem;
}


.hero h1 {

    font-size: clamp(2.5rem, 5vw, 4.2rem);

    line-height: 1.05;

    letter-spacing: -0.055em;

    margin: 0;

    font-weight: 800;

    background:
        linear-gradient(
            120deg,
            #ffffff 0%,
            #d7d7d7 45%,
            #777777 100%
        );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;
}


.hero p {

    max-width: 680px;

    margin-top: 1.1rem;

    font-size: 1rem;

    line-height: 1.7;

    color: #929292;
}


/* ============================================================
   UPLOAD CARD
   ============================================================ */

.upload-shell {

    position: relative;

    padding: 1.5rem;

    margin-top: 2rem;

    border-radius: 16px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.07),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 20px 60px rgba(0,0,0,0.35);

    backdrop-filter: blur(18px);
}


.upload-label {

    font-size: 0.78rem;

    color: #8e8e8e;

    margin-bottom: 0.8rem;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {

    border: 1px dashed rgba(255,255,255,0.20);

    border-radius: 12px;

    padding: 0.5rem;

    background: rgba(0,0,0,0.20);
}


[data-testid="stFileUploaderDropzone"] {

    min-height: 140px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.045),
            rgba(255,255,255,0.015)
        ) !important;

    border-radius: 10px;
}


[data-testid="stFileUploaderDropzone"] * {

    color: #eeeeee !important;
}


[data-testid="stFileUploaderDropzoneInstructions"] span,
[data-testid="stFileUploaderDropzoneInstructions"] small {

    color: #888888 !important;
}


[data-testid="stFileUploaderDropzone"] svg {

    fill: #cccccc !important;
}

/* ============================================================
   ANALYZE DATASET BUTTON
   ============================================================ */

div.stButton > button[kind="primary"] {

    width: 100% !important;

    min-height: 52px !important;

    border-radius: 10px !important;

    border: 1px solid rgba(255,255,255,0.15) !important;

    background:
        linear-gradient(
            135deg,
            #242424 0%,
            #111111 50%,
            #050505 100%
        ) !important;

    color: #ffffff !important;

    font-weight: 700 !important;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.35) !important;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease,
        border-color 0.2s ease !important;
}


/* Text inside button */

div.stButton > button[kind="primary"] p,
div.stButton > button[kind="primary"] span {

    color: #ffffff !important;

    font-weight: 700 !important;
}


/* Hover */

div.stButton > button[kind="primary"]:hover {

    background:
        linear-gradient(
            135deg,
            #333333 0%,
            #171717 50%,
            #080808 100%
        ) !important;

    border-color: rgba(255,255,255,0.30) !important;

    color: #ffffff !important;

    transform: translateY(-2px) !important;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.50) !important;
}


/* Click */

div.stButton > button[kind="primary"]:active {

    transform: translateY(0px) !important;

    background: #111111 !important;
}


/* Focus */

div.stButton > button[kind="primary"]:focus {

    outline: none !important;

    box-shadow:
        0 0 0 2px rgba(255,255,255,0.12),
        0 8px 25px rgba(0,0,0,0.4) !important;
}
/* ============================================================
   HEADINGS
   ============================================================ */

h1,
h2,
h3 {

    color: #ffffff !important;

    font-weight: 700 !important;
}


div[data-testid="stHeadingWithActionElements"] h2 {

    border-bottom: 1px solid rgba(255,255,255,0.10);

    padding-bottom: 0.7rem;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

div[data-testid="stMetric"] {

    padding: 1.2rem;

    border-radius: 14px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.07),
            rgba(255,255,255,0.025)
        );

    border: 1px solid rgba(255,255,255,0.10);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25);

    backdrop-filter: blur(15px);
}


div[data-testid="stMetricLabel"] {

    color: #8d8d8d !important;

    font-size: 0.75rem !important;

    text-transform: uppercase;

    letter-spacing: 0.06em;
}


div[data-testid="stMetricValue"] {

    color: #ffffff !important;

    font-weight: 800 !important;
}


/* ============================================================
   TABS
   ============================================================ */

div[data-baseweb="tab-list"] {

    gap: 0.3rem;

    border-bottom: 1px solid rgba(255,255,255,0.10);
}


button[data-baseweb="tab"] {

    color: #777777;

    background: transparent;

    font-weight: 600;

    border-radius: 8px 8px 0 0;
}


button[data-baseweb="tab"][aria-selected="true"] {

    color: #ffffff;

    background: rgba(255,255,255,0.05);
}


div[data-baseweb="tab-highlight"] {

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #666666
        ) !important;

    height: 2px;
}


/* ============================================================
   DATAFRAME
   ============================================================ */

div[data-testid="stDataFrame"] {

    border-radius: 12px;

    overflow: hidden;

    border: 1px solid rgba(255,255,255,0.10);

    background: rgba(255,255,255,0.025);
}


/* ============================================================
   PLOTLY CARDS
   ============================================================ */

div[data-testid="stPlotlyChart"] {

    padding: 0.7rem;

    margin-bottom: 1rem;

    border-radius: 14px;

    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,0.055),
            rgba(255,255,255,0.018)
        );

    border: 1px solid rgba(255,255,255,0.08);

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25);
}


/* ============================================================
   ALERTS
   ============================================================ */

div[data-testid="stAlert"] {

    border-radius: 10px !important;

    border: 1px solid rgba(255,255,255,0.10) !important;

    background: rgba(255,255,255,0.04) !important;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {

    border-color: rgba(255,255,255,0.08) !important;
}


/* ============================================================
   JSON
   ============================================================ */

div[data-testid="stJson"] {

    border-radius: 12px;

    border: 1px solid rgba(255,255,255,0.10);

    background: rgba(255,255,255,0.025);
}


/* ============================================================
   SCROLLBAR
   ============================================================ */

::-webkit-scrollbar {

    width: 8px;
}


::-webkit-scrollbar-track {

    background: #050505;
}


::-webkit-scrollbar-thumb {

    background: #333333;

    border-radius: 10px;
}


::-webkit-scrollbar-thumb:hover {

    background: #555555;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# NAVBAR + HEADER
# ============================================================

st.markdown("""
<div class="navbar">
    <div class="brand"><span class="brand-mark">A</span>AutoEDA</div>
    <div class="nav-badge">n8n + Python</div>
</div>
<div class="hero">
    <div class="eyebrow">◆ Dataset in, insight out</div>
    <h1>Automated Exploratory<br>Data Analysis</h1>
    <p>Upload a CSV and get profiling, data quality checks, statistics, and charts — generated automatically.</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# FILE UPLOAD
# ============================================================

st.markdown('<div class="upload-shell"><div class="upload-label">// upload a .csv file to begin your automated EDA</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload your CSV dataset",
    type=["csv"],
    label_visibility="collapsed"
)

st.markdown('</div>', unsafe_allow_html=True)


if uploaded_file:

    st.success(
        f"Dataset ready: {uploaded_file.name}"
    )

    if st.button(
        "🚀 Analyze Dataset",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Running automated EDA..."
        ):

            try:
                file_bytes = uploaded_file.getvalue()
                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        "text/csv"
                    )
                }

                response = requests.post(
                    N8N_WEBHOOK_URL,
                    files=files,
                    timeout=300
                )

                if response.status_code != 200:

                    st.error(
                        f"Analysis failed: {response.text}"
                    )

                    st.stop()

                result = response.json()

                # n8n should return a JSON object
                if isinstance(result, list):
                    if len(result) == 0:
                        st.error("n8n returned an empty response.")
                        st.stop()

                    result = result[0]

                if result is None:
                    st.error("n8n returned null instead of the EDA result.")
                    st.stop()

                if not isinstance(result, dict):
                    st.error(
                        f"Unexpected response format from n8n: {type(result).__name__}"
                    )
                    st.stop()

                st.session_state["eda_result"] = result

                st.success(
                    "Analysis completed successfully!"
                )

            except requests.exceptions.RequestException as e:

                st.error(
                    f"Could not connect to n8n: {e}"
                )


# ============================================================
# DASHBOARD
# ============================================================

result = st.session_state.get(
    "eda_result"
)


if result:

    # --------------------------------------------------------
    # Handle webhook response
    # --------------------------------------------------------

    if isinstance(result, list):

        result = result[0]

    # --------------------------------------------------------
    # OVERVIEW
    # --------------------------------------------------------

    st.divider()

    st.header("📈 Dataset Overview")

    overview = result.get(
        "overview",
        {}
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Rows",
        f"{overview.get('rows', 0):,}"
    )

    col2.metric(
        "Columns",
        overview.get("columns", 0)
    )

    col3.metric(
        "Duplicate Rows",
        f"{overview.get('duplicate_rows', 0):,}"
    )

    col4.metric(
        "Memory",
        f"{overview.get('memory_usage_mb', 0)} MB"
    )

    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Overview",
            "🧱 Columns",
            "⚠️ Missing Values",
            "📈 Statistics",
            "📉 Visualizations"
        ]
    )

    # ========================================================
    # TAB 1 — OVERVIEW
    # ========================================================

    with tab1:

        st.subheader(
            "Dataset Summary"
        )

        st.write(
            f"**Duplicate percentage:** "
            f"{overview.get('duplicate_percentage', 0)}%"
        )

        st.json(overview)

    # ========================================================
    # TAB 2 — COLUMNS
    # ========================================================

    with tab2:

        st.subheader(
            "Column Information"
        )

        columns = result.get(
            "columns",
            []
        )

        if columns:

            columns_df = pd.DataFrame(
                columns
            )

            st.dataframe(
                columns_df,
                use_container_width=True,
                hide_index=True
            )

    # ========================================================
    # TAB 3 — MISSING VALUES
    # ========================================================

    with tab3:

        st.subheader(
            "Missing Value Analysis"
        )

        columns = result.get("columns", [])

        missing = [
            {
                "column": col.get("name"),
                "missing_count": col.get("missing_count", 0),
                "missing_percentage": col.get(
                    "missing_percentage",
                    0
                )
            }
            for col in columns
            if col.get("missing_count", 0) > 0
        ]

        if missing:

            missing_df = pd.DataFrame(
                missing
            )

            st.dataframe(
                missing_df,
                use_container_width=True,
                hide_index=True
            )

            chart_df = missing_df[
                missing_df["missing_count"] > 0
            ]

            if not chart_df.empty:

                fig = px.bar(
                    chart_df,
                    x="column",
                    y="missing_count",
                    title="Missing Values by Column"
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        else:

            st.success(
                "No missing values found."
            )

    # ========================================================
    # TAB 4 — STATISTICS
    # ========================================================

    with tab4:

        st.subheader(
            "Numerical Statistics"
        )

        numerical = result.get(
            "numerical_analysis",
            {}
        )

        if numerical:

            for column, stats in numerical.items():

                st.markdown(
                    f"### {column}"
                )

                stats_df = pd.DataFrame(
                    [stats]
                )

                st.dataframe(
                    stats_df,
                    use_container_width=True,
                    hide_index=True
                )

        else:

            st.info(
                "No numerical columns detected."
            )

        st.subheader(
            "Categorical Analysis"
        )

        categorical = result.get(
            "categorical_analysis",
            {}
        )

        for column, stats in categorical.items():

            st.markdown(
                f"### {column}"
            )

            top_values = stats.get(
                "top_values",
                []
            )

            if top_values:

                cat_df = pd.DataFrame(
                    top_values
                )

                st.dataframe(
                    cat_df,
                    use_container_width=True,
                    hide_index=True
                )

    # ========================================================
    # TAB 5 — VISUALIZATIONS
    # ========================================================

    with tab5:

        st.subheader("Automated Visualizations")

        charts = result.get("charts", [])

        if not charts:

            st.warning("No charts were generated.")

        else:

            st.write(
                f"Generated {len(charts)} visualizations."
            )

            # Read the original uploaded CSV
            uploaded_file.seek(0)

            df_chart = pd.read_csv(uploaded_file)

            # ------------------------------------------------
            # Generate each chart
            # ------------------------------------------------

            for chart in charts:

                chart_type = chart.get("type")

                # ====================================================
                # Single-column chart types
                # ====================================================

                if chart_type in ("histogram", "boxplot", "bar", "line"):

                    column = chart.get("column")
                    title = chart.get(
                        "title",
                        f"{chart_type} — {column}"
                    )

                    # Make sure the column exists
                    if not column or column not in df_chart.columns:

                        st.warning(
                            f"Column '{column}' not found in dataset."
                        )

                        continue

                    # -------------------------------
                    # HISTOGRAM
                    # -------------------------------

                    if chart_type == "histogram":

                        values = pd.to_numeric(
                            df_chart[column],
                            errors="coerce"
                        ).dropna()

                        if values.empty:

                            st.warning(
                                f"No numeric data available for {column}."
                            )

                            continue

                        fig = px.histogram(
                            x=values,
                            title=title,
                            labels={
                                "x": column
                            }
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    # -------------------------------
                    # BOXPLOT
                    # -------------------------------

                    elif chart_type == "boxplot":

                        values = pd.to_numeric(
                            df_chart[column],
                            errors="coerce"
                        ).dropna()

                        if values.empty:

                            st.warning(
                                f"No numeric data available for {column}."
                            )

                            continue

                        fig = px.box(
                            y=values,
                            title=title,
                            labels={
                                "y": column
                            }
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    # -------------------------------
                    # BAR CHART
                    # -------------------------------

                    elif chart_type == "bar":

                        series = (
                            df_chart[column]
                            .dropna()
                            .astype(str)
                            .str.strip()
                        )

                        series = series[
                            series != ""
                        ]

                        # ---------------------------------------
                        # Handle multi-value categorical columns
                        # such as country and listed_in
                        # ---------------------------------------

                        if column in [
                            "country",
                            "listed_in"
                        ]:

                            series = (
                                series
                                .str.split(",")
                                .explode()
                                .str.strip()
                            )

                            series = series[
                                series != ""
                            ]

                        counts = (
                            series
                            .value_counts()
                            .head(10)
                            .reset_index()
                        )

                        counts.columns = [
                            "Category",
                            "Count"
                        ]

                        if counts.empty:

                            st.warning(
                                f"No categorical data available for {column}."
                            )

                            continue

                        fig = px.bar(
                            counts,
                            x="Category",
                            y="Count",
                            title=title
                        )

                        fig.update_layout(
                            xaxis_title=column,
                            yaxis_title="Count"
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                    # -------------------------------
                    # LINE CHART
                    # -------------------------------

                    elif chart_type == "line":

                        # -----------------------------------
                        # Date/time column
                        # -----------------------------------

                        if column == "date_added":

                            dates = pd.to_datetime(
                                df_chart[column],
                                errors="coerce"
                            )

                            date_counts = (
                                dates
                                .dropna()
                                .dt.to_period("M")
                                .value_counts()
                                .sort_index()
                            )

                            line_df = pd.DataFrame({
                                "Date": date_counts.index.astype(str),
                                "Count": date_counts.values
                            })

                        # -----------------------------------
                        # Numeric time-like column
                        # -----------------------------------

                        else:

                            numeric = pd.to_numeric(
                                df_chart[column],
                                errors="coerce"
                            )

                            line_df = (
                                numeric
                                .dropna()
                                .value_counts()
                                .sort_index()
                                .reset_index()
                            )

                            line_df.columns = [
                                "Value",
                                "Count"
                            ]

                        if line_df.empty:

                            st.warning(
                                f"No usable data available for {column}."
                            )

                            continue

                        x_column = (
                            "Date"
                            if "Date" in line_df.columns
                            else "Value"
                        )

                        fig = px.line(
                            line_df,
                            x=x_column,
                            y="Count",
                            title=title,
                            markers=True
                        )

                        st.plotly_chart(
                            fig,
                            use_container_width=True
                        )

                # ====================================================
                # SCATTER — two-column chart type (x, y)
                # ====================================================

                elif chart_type == "scatter":

                    x_col = chart.get("x")
                    y_col = chart.get("y")
                    title = chart.get(
                        "title",
                        f"{x_col} vs {y_col}"
                    )

                    x_values = chart.get("x_values", [])
                    y_values = chart.get("y_values", [])

                    if not x_values or not y_values:

                        st.warning(
                            f"No data available for {x_col} vs {y_col}."
                        )

                        continue

                    fig = px.scatter(
                        x=x_values,
                        y=y_values,
                        title=title,
                        labels={
                            "x": x_col,
                            "y": y_col
                        }
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                # ====================================================
                # CORRELATION HEATMAP — multi-column chart type
                # ====================================================

                elif chart_type == "correlation_heatmap":

                    title = chart.get(
                        "title",
                        "Correlation Matrix"
                    )

                    matrix = chart.get("matrix", [])
                    labels = chart.get("labels", [])

                    if not matrix or not labels:

                        st.warning(
                            "No correlation data available."
                        )

                        continue

                    fig = px.imshow(
                        matrix,
                        x=labels,
                        y=labels,
                        text_auto=True,
                        title=title,
                        color_continuous_scale="RdBu_r",
                        zmin=-1,
                        zmax=1
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                # ====================================================
                # UNKNOWN CHART TYPE
                # ====================================================

                else:

                    st.warning(
                        f"Unsupported chart type: {chart_type}"
                    )
uploaded_file.seek(0)

try:
    df_chart = pd.read_csv(
        uploaded_file,
        encoding="utf-8"
    )
except UnicodeDecodeError:
    uploaded_file.seek(0)

    try:
        df_chart = pd.read_csv(
            uploaded_file,
            encoding="cp1252"
        )
    except UnicodeDecodeError:
        uploaded_file.seek(0)

        df_chart = pd.read_csv(
            uploaded_file,
            encoding="latin1"
        )
