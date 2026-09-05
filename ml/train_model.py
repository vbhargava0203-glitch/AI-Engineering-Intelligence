import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


DATA_FILE = "ml/data/training_data.csv"
MODEL_DIR = "ml/models"


def main():

    print("\n================================")
    print(" Engineering Risk ML Model")
    print("================================\n")

    df = pd.read_csv(DATA_FILE)

    if len(df) < 10:
        print("❌ Not enough repositories for reliable training.")
        print(f"Currently available: {len(df)}")
        print("Collect more repositories before training.")
        return

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

    X = df[features]
    y = df["risk_level"]

    print(f"Dataset size: {len(df)} repositories")
    print("\nRisk distribution:")
    print(y.value_counts())

    # Need at least two classes
    if y.nunique() < 2:
        print("\n❌ Only one risk class exists.")
        print("More varied repository data is required.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\n--------------------------------")
    print(" Model Results")
    print("--------------------------------")

    print(f"Accuracy: {accuracy:.2%}")

    print("\nClassification Report:")
    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    # Feature importance

    importance = pd.Series(
        model.feature_importances_,
        index=features
    ).sort_values(
        ascending=False
    )

    print("\nFeature Importance:")

    for feature, value in importance.items():
        print(
            f"{feature:<30} {value:.4f}"
        )

    # Save model

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    model_path = (
        f"{MODEL_DIR}/"
        "engineering_risk_model.joblib"
    )

    joblib.dump(
        model,
        model_path
    )

    print("\n--------------------------------")
    print(" Model Saved")
    print("--------------------------------")

    print(model_path)


if __name__ == "__main__":
    main()