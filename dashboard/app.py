import os
import sys
import subprocess

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import streamlit as st

from dotenv import load_dotenv


# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


st.set_page_config(
    page_title="AI Engineering Intelligence",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

@st.cache_resource
def get_connection():

    if not DATABASE_URL:
        raise Exception(
            "DATABASE_URL is missing from your .env file."
        )

    return psycopg2.connect(DATABASE_URL)


# ============================================================
# LOAD REPOSITORIES
# ============================================================

@st.cache_data(ttl=60)
def load_repositories():

    query = """
        SELECT
            id,
            name,
            full_name,
            description,
            language,
            stars,
            forks,
            open_issues
        FROM repositories
        ORDER BY stars DESC;
    """

    connection = get_connection()

    return pd.read_sql(
        query,
        connection
    )


# ============================================================
# LOAD ENGINEERING METRICS
# ============================================================

@st.cache_data(ttl=60)
def load_metrics():

    query = """
        SELECT
            r.id,
            r.name,

            COUNT(DISTINCT c.id) AS commits,
            COUNT(DISTINCT pr.id) AS pull_requests,
            COUNT(DISTINCT i.id) AS issues,
            COUNT(DISTINCT c.author_id) AS contributors,

            COALESCE(
                SUM(c.additions),
                0
            ) AS lines_added,

            COALESCE(
                SUM(c.deletions),
                0
            ) AS lines_deleted

        FROM repositories r

        LEFT JOIN commits c
            ON r.id = c.repository_id

        LEFT JOIN pull_requests pr
            ON r.id = pr.repository_id

        LEFT JOIN issues i
            ON r.id = i.repository_id

        GROUP BY
            r.id,
            r.name

        ORDER BY commits DESC;
    """

    connection = get_connection()

    return pd.read_sql(
        query,
        connection
    )


# ============================================================
# LOAD RISK PREDICTIONS
# ============================================================

@st.cache_data(ttl=60)
def load_risk():

    query = """
        SELECT DISTINCT ON (r.id)

            r.id,
            r.name,
            rp.risk_score,
            rp.risk_level,
            rp.model_version,
            rp.explanation,
            rp.prediction_date

        FROM risk_predictions rp

        JOIN repositories r
            ON r.id = rp.repository_id

        ORDER BY
            r.id,
            rp.prediction_date DESC;
    """

    connection = get_connection()

    return pd.read_sql(
        query,
        connection
    )


# ============================================================
# LOAD DATABASE DATA
# ============================================================

try:

    repositories = load_repositories()

    metrics = load_metrics()

    risk = load_risk()

except Exception as error:

    st.error(
        f"Database connection failed: {error}"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🧠 AI Engineering")

    st.caption(
        "Engineering Intelligence Platform"
    )

    st.divider()

    st.subheader("Navigation")

    page = st.radio(
        "Select view",
        [
            "Executive Overview",
            "Repository Intelligence",
            "Risk Analysis",
        ]
    )

    st.divider()

    st.subheader("System")

    st.success(
        "Database Online"
    )

    st.success(
        "ML Engine Online"
    )

    st.caption(
        "Model: Engineering Risk v1.0"
    )


# ============================================================
# GITHUB REPOSITORY ANALYZER
# ============================================================

st.header(
    "🔍 Analyze a GitHub Repository"
)

repository_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository"
)


if st.button(
    "🚀 Analyze Repository",
    type="primary"
):

    if not repository_url.strip():

        st.warning(
            "Please enter a GitHub repository URL."
        )

    elif "github.com/" not in repository_url.lower():

        st.error(
            "Please enter a valid GitHub repository URL."
        )

    else:

        with st.spinner(
            "Analyzing GitHub repository..."
        ):

            try:

                analyzer_path = os.path.join(
                    "data_pipeline",
                    "repository_analyzer.py"
                )

                result = subprocess.run(
                    [
                        sys.executable,
                        analyzer_path
                    ],
                    input=repository_url.strip() + "\n",
                    text=True,
                    capture_output=True,
                    timeout=120
                )

                if result.returncode == 0:

                    st.success(
                        "✅ Repository analyzed and saved to PostgreSQL!"
                    )

                    output = result.stdout.strip()

                    if output:

                        with st.expander(
                            "📊 View Analysis Details",
                            expanded=True
                        ):

                            st.code(
                                output,
                                language="text"
                            )

                    st.cache_data.clear()

                    st.info(
                        "Refresh the page to load the newly "
                        "analyzed repository into the dashboard."
                    )

                else:

                    st.error(
                        "❌ Repository analysis failed."
                    )

                    error_output = (
                        result.stderr.strip()
                        if result.stderr.strip()
                        else result.stdout.strip()
                    )

                    if error_output:

                        st.code(
                            error_output,
                            language="text"
                        )

            except subprocess.TimeoutExpired:

                st.error(
                    "⏱️ Repository analysis timed out."
                )

            except Exception as error:

                st.error(
                    f"❌ Unexpected error: {error}"
                )


st.divider()


# ============================================================
# MAIN TITLE
# ============================================================

st.title(
    "🧠 AI Engineering Intelligence"
)

st.caption(
    "GitHub engineering analytics, repository intelligence "
    "and machine-learning-powered risk analysis."
)


# ============================================================
# EMPTY DATABASE CHECK
# ============================================================

if repositories.empty:

    st.warning(
        "No repositories are currently available."
    )

    st.info(
        "Analyze a GitHub repository using the analyzer above."
    )

    st.stop()


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.header(
        "📊 Executive Overview"
    )

    # --------------------------------------------------------
    # Overall statistics
    # --------------------------------------------------------

    total_repositories = len(
        repositories
    )

    total_stars = int(
        repositories["stars"]
        .fillna(0)
        .sum()
    )

    total_commits = int(
        metrics["commits"]
        .fillna(0)
        .sum()
    )

    total_pull_requests = int(
        metrics["pull_requests"]
        .fillna(0)
        .sum()
    )

    total_issues = int(
        metrics["issues"]
        .fillna(0)
        .sum()
    )

    total_contributors = int(
        metrics["contributors"]
        .fillna(0)
        .sum()
    )


    # --------------------------------------------------------
    # Metrics
    # --------------------------------------------------------

    st.subheader(
        "Platform Overview"
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:

        st.metric(
            "Repositories",
            f"{total_repositories:,}"
        )

    with c2:

        st.metric(
            "GitHub Stars",
            f"{total_stars:,}"
        )

    with c3:

        st.metric(
            "Commits",
            f"{total_commits:,}"
        )

    with c4:

        st.metric(
            "Pull Requests",
            f"{total_pull_requests:,}"
        )

    with c5:

        st.metric(
            "Issues",
            f"{total_issues:,}"
        )

    with c6:

        st.metric(
            "Contributors",
            f"{total_contributors:,}"
        )


    st.divider()


    # ========================================================
    # ENGINEERING RISK
    # ========================================================

    st.subheader(
        "⚠️ Engineering Risk"
    )

    if not risk.empty:

        low_count = int(
            (
                risk["risk_level"] == "LOW"
            ).sum()
        )

        medium_count = int(
            (
                risk["risk_level"] == "MEDIUM"
            ).sum()
        )

        high_count = int(
            (
                risk["risk_level"] == "HIGH"
            ).sum()
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "🟢 LOW RISK",
                low_count
            )

        with c2:

            st.metric(
                "🟡 MEDIUM RISK",
                medium_count
            )

        with c3:

            st.metric(
                "🔴 HIGH RISK",
                high_count
            )

    else:

        st.info(
            "No ML risk predictions are available yet."
        )


    st.divider()


    # ========================================================
    # CHARTS
    # ========================================================

    c1, c2 = st.columns(2)


    # --------------------------------------------------------
    # Most Active Repositories
    # --------------------------------------------------------

    with c1:

        st.subheader(
            "📈 Most Active Repositories"
        )

        activity = metrics[
            [
                "name",
                "commits"
            ]
        ].sort_values(
            "commits",
            ascending=False
        ).head(10)


        fig = px.bar(
            activity,
            x="commits",
            y="name",
            orientation="h",
            title="Commit Activity"
        )


        fig.update_layout(
            height=450,
            xaxis_title="Commits",
            yaxis_title=""
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # Risk Distribution
    # --------------------------------------------------------

    with c2:

        st.subheader(
            "🎯 Risk Distribution"
        )

        if not risk.empty:

            distribution = (
                risk["risk_level"]
                .value_counts()
                .reset_index()
            )


            distribution.columns = [
                "Risk Level",
                "Repositories"
            ]


            fig = px.pie(
                distribution,
                names="Risk Level",
                values="Repositories",
                hole=0.55,
                title="Repository Risk"
            )


            fig.update_layout(
                height=450
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )

        else:

            st.info(
                "No risk data available."
            )


    # ========================================================
    # HIGHEST RISK
    # ========================================================

    st.subheader(
        "🚨 Highest Risk Repositories"
    )

    if not risk.empty:

        high_risk = risk.sort_values(
            "risk_score",
            ascending=False
        ).head(10)


        display = high_risk[
            [
                "name",
                "risk_score",
                "risk_level",
                "model_version"
            ]
        ].copy()


        display["risk_score"] = (
            display["risk_score"]
            .round(2)
        )


        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No risk predictions available."
        )


# ============================================================
# REPOSITORY INTELLIGENCE
# ============================================================

elif page == "Repository Intelligence":

    st.header(
        "📦 Repository Intelligence"
    )


    repository_name = st.selectbox(
        "Select Repository",
        repositories["name"].tolist()
    )


    selected_repository = repositories[
        repositories["name"] == repository_name
    ].iloc[0]


    selected_metrics = metrics[
        metrics["name"] == repository_name
    ]


    selected_risk = risk[
        risk["name"] == repository_name
    ]


    # --------------------------------------------------------
    # Repository Information
    # --------------------------------------------------------

    st.subheader(
        f"Repository: {repository_name}"
    )


    if pd.notna(
        selected_repository["description"]
    ):

        st.caption(
            selected_repository["description"]
        )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(
            "⭐ Stars",
            f"{int(selected_repository['stars'] or 0):,}"
        )


    with c2:

        st.metric(
            "🍴 Forks",
            f"{int(selected_repository['forks'] or 0):,}"
        )


    with c3:

        st.metric(
            "🐛 Open Issues",
            f"{int(selected_repository['open_issues'] or 0):,}"
        )


    with c4:

        st.metric(
            "💻 Language",
            selected_repository["language"]
            or "Unknown"
        )


    st.divider()


    # --------------------------------------------------------
    # Engineering Activity
    # --------------------------------------------------------

    st.subheader(
        "⚙️ Engineering Activity"
    )


    if not selected_metrics.empty:

        data = selected_metrics.iloc[0]


        c1, c2, c3, c4 = st.columns(4)


        with c1:

            st.metric(
                "Commits",
                int(data["commits"])
            )


        with c2:

            st.metric(
                "Pull Requests",
                int(data["pull_requests"])
            )


        with c3:

            st.metric(
                "Issues",
                int(data["issues"])
            )


        with c4:

            st.metric(
                "Contributors",
                int(data["contributors"])
            )


        # ----------------------------------------------------
        # Code Churn
        # ----------------------------------------------------

        st.subheader(
            "📊 Code Churn"
        )


        churn = pd.DataFrame(
            {
                "Metric": [
                    "Lines Added",
                    "Lines Deleted"
                ],

                "Lines": [
                    int(data["lines_added"]),
                    int(data["lines_deleted"])
                ]
            }
        )


        fig = px.bar(
            churn,
            x="Metric",
            y="Lines",
            title="Code Churn"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # ML RISK ASSESSMENT
    # ========================================================

    st.subheader(
        "🤖 ML Risk Assessment"
    )


    if not selected_risk.empty:

        risk_data = selected_risk.iloc[0]


        score = float(
            risk_data["risk_score"]
        )


        level = risk_data["risk_level"]


        c1, c2 = st.columns(2)


        # ----------------------------------------------------
        # Risk Gauge
        # ----------------------------------------------------

        with c1:

            fig = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=score,
                    title={
                        "text": "Risk Score"
                    },
                    gauge={
                        "axis": {
                            "range": [0, 100]
                        }
                    }
                )
            )


            fig.update_layout(
                height=350
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # ----------------------------------------------------
        # Risk Details
        # ----------------------------------------------------

        with c2:

            st.metric(
                "Risk Level",
                level
            )


            st.metric(
                "Risk Score",
                f"{score:.2f} / 100"
            )


            st.metric(
                "Model Version",
                risk_data["model_version"]
            )


            if pd.notna(
                risk_data["explanation"]
            ):

                st.info(
                    risk_data["explanation"]
                )


    else:

        st.info(
            "No ML risk prediction is available "
            "for this repository yet."
        )


# ============================================================
# RISK ANALYSIS
# ============================================================

elif page == "Risk Analysis":

    st.header(
        "🚨 Risk Analysis"
    )


    if risk.empty:

        st.warning(
            "No risk predictions are available."
        )

    else:

        # ----------------------------------------------------
        # Risk Table
        # ----------------------------------------------------

        st.subheader(
            "Repository Risk Predictions"
        )


        risk_table = risk[
            [
                "name",
                "risk_score",
                "risk_level",
                "model_version",
                "prediction_date"
            ]
        ].copy()


        risk_table = risk_table.sort_values(
            "risk_score",
            ascending=False
        )


        risk_table["risk_score"] = (
            risk_table["risk_score"]
            .round(2)
        )


        st.dataframe(
            risk_table,
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        # ----------------------------------------------------
        # Risk Scores
        # ----------------------------------------------------

        st.subheader(
            "📊 Repository Risk Scores"
        )


        fig = px.bar(
            risk_table,
            x="name",
            y="risk_score",
            color="risk_level",
            title="Risk Score by Repository"
        )


        fig.update_layout(
            height=500,
            xaxis_title="Repository",
            yaxis_title="Risk Score"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # ----------------------------------------------------
        # Engineering Activity vs Risk
        # ----------------------------------------------------

        st.subheader(
            "🔬 Engineering Activity vs Risk"
        )


        comparison = metrics.merge(
            risk[
                [
                    "name",
                    "risk_score",
                    "risk_level"
                ]
            ],
            on="name",
            how="left"
        )


        fig = px.scatter(
            comparison,
            x="commits",
            y="risk_score",
            size="issues",
            color="risk_level",
            hover_name="name",
            title="Commit Activity vs Risk"
        )


        fig.update_layout(
            height=500,
            xaxis_title="Commits",
            yaxis_title="Risk Score"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Engineering Intelligence • "
    "Python • PostgreSQL • GitHub API • "
    "Machine Learning • Streamlit"
)