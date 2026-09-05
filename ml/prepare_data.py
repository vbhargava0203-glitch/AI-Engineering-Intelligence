import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def main():

    connection = psycopg2.connect(DATABASE_URL)

    query = """
    SELECT
        r.id AS repository_id,
        r.name,

        COUNT(DISTINCT c.id) AS commit_count,
        COUNT(DISTINCT pr.id) AS pull_request_count,
        COUNT(DISTINCT i.id) AS issue_count,
        COUNT(DISTINCT con.id) AS contributor_count,

        COALESCE(SUM(c.additions), 0) AS lines_added,
        COALESCE(SUM(c.deletions), 0) AS lines_deleted

    FROM repositories r

    LEFT JOIN commits c
        ON r.id = c.repository_id

    LEFT JOIN pull_requests pr
        ON r.id = pr.repository_id

    LEFT JOIN issues i
        ON r.id = i.repository_id

    LEFT JOIN contributors con
        ON c.author_id = con.id

    GROUP BY r.id, r.name;
    """

    df = pd.read_sql(query, connection)

    connection.close()

    if df.empty:
        print("❌ No engineering data found.")
        return

    # Engineering features

    df["code_churn"] = (
        df["lines_added"] +
        df["lines_deleted"]
    )

    df["pr_issue_ratio"] = (
        df["pull_request_count"] /
        (df["issue_count"] + 1)
    )

    df["commit_contributor_ratio"] = (
        df["commit_count"] /
        (df["contributor_count"] + 1)
    )

    # Initial engineering-risk label.
    #
    # This is a rule-based proxy label used to
    # bootstrap the first ML model.
    # Normalize engineering signals
    df["issue_pressure"] = (
    df["issue_count"] /
    (df["commit_count"] + 1)
)

    df["churn_per_commit"] = (
    df["code_churn"] /
    (df["commit_count"] + 1)
)

    df["contributor_pressure"] = (
    1 /
    (df["contributor_count"] + 1)
)

# Relative engineering risk score
    df["risk_score"] = (
    df["issue_pressure"] * 40
    + df["churn_per_commit"] * 0.05
    + df["contributor_pressure"] * 20
    - df["pr_issue_ratio"] * 10
)

# Convert scores into relative risk groups
    df["risk_level"] = pd.qcut(
    df["risk_score"].rank(method="first"),
    q=3,
    labels=["LOW", "MEDIUM", "HIGH"]
)

    os.makedirs("ml/data", exist_ok=True)

    output_file = "ml/data/training_data.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print("\n================================")
    print(" ML DATASET CREATED")
    print("================================")

    print(f"\nRows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nFeatures:")

    for column in df.columns:
        print(f"  ✓ {column}")

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
