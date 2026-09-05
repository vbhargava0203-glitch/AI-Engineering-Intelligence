import os
import joblib
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

MODEL_PATH = "ml/models/engineering_risk_model.joblib"


def main():

    print("\n================================")
    print(" Engineering Risk Prediction")
    print("================================\n")

    # Load model
    model = joblib.load(MODEL_PATH)

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            r.id,
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

        GROUP BY r.id, r.name
        ORDER BY r.id;
    """)

    rows = cursor.fetchall()

    if not rows:
        print("❌ No repositories found.")
        return

    columns = [
        "repository_id",
        "name",
        "commit_count",
        "pull_request_count",
        "issue_count",
        "contributor_count",
        "lines_added",
        "lines_deleted"
    ]

    df = pd.DataFrame(
        rows,
        columns=columns
    )

    # Feature engineering

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

    features = [
        "commit_count",
        "pull_request_count",
        "issue_count",
        "contributor_count",
        "lines_added",
        "lines_deleted",
        "code_churn",
        "pr_issue_ratio",
        "commit_contributor_ratio"
    ]

    predictions = model.predict(
        df[features]
    )

    print("--------------------------------")
    print(" Repository Risk Predictions")
    print("--------------------------------\n")

    for name, prediction in zip(
        df["name"],
        predictions
    ):

        print(
            f"{name:<20} → {prediction}"
        )

    # Save predictions to PostgreSQL

    for repository_id, prediction in zip(
        df["repository_id"],
        predictions
    ):

        if prediction == "HIGH":
            score = 80
        elif prediction == "MEDIUM":
            score = 50
        else:
            score = 20

        cursor.execute(
            """
            INSERT INTO risk_predictions
                (
                    repository_id,
                    risk_score,
                    risk_level,
                    model_version,
                    explanation
                )
            VALUES
                (%s, %s, %s, %s, %s);
            """,
            (
                int(repository_id),
                score,
                prediction,
                "v1.0",
                "Prediction generated from GitHub engineering activity features."
            )
        )

    connection.commit()

    cursor.close()
    connection.close()

    print("\n================================")
    print(" Predictions saved to PostgreSQL")
    print("================================")


if __name__ == "__main__":
    main()