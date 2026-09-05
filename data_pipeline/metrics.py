import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def main():

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    print("\n================================")
    print(" Engineering Metrics")
    print("================================\n")

    # Repository
    cursor.execute("""
        SELECT
            id,
            name,
            stars,
            forks,
            open_issues
        FROM repositories
        LIMIT 1;
    """)

    repo = cursor.fetchone()

    if not repo:
        print("No repository data found.")
        return

    repository_id = repo[0]

    print(f"Repository: {repo[1]}")
    print(f"Stars: {repo[2]}")
    print(f"Forks: {repo[3]}")
    print(f"Open Issues: {repo[4]}")

    # Commits
    cursor.execute("""
        SELECT COUNT(*)
        FROM commits
        WHERE repository_id = %s;
    """, (repository_id,))

    commits = cursor.fetchone()[0]

    # Contributors
    cursor.execute("""
        SELECT COUNT(*)
        FROM contributors;
    """)

    contributors = cursor.fetchone()[0]

    # Pull Requests
    cursor.execute("""
        SELECT COUNT(*)
        FROM pull_requests
        WHERE repository_id = %s;
    """, (repository_id,))

    pull_requests = cursor.fetchone()[0]

    # Issues
    cursor.execute("""
        SELECT COUNT(*)
        FROM issues
        WHERE repository_id = %s;
    """, (repository_id,))

    issues = cursor.fetchone()[0]

    print("\n--------------------------------")
    print(" Activity Metrics")
    print("--------------------------------")

    print(f"Commits:       {commits}")
    print(f"Contributors:  {contributors}")
    print(f"Pull Requests: {pull_requests}")
    print(f"Issues:        {issues}")

    # Health score
    score = 0

    if commits > 20:
        score += 25

    if contributors > 10:
        score += 25

    if pull_requests > 10:
        score += 25

    if issues > 0:
        score += 25

    if score >= 75:
        health = "HEALTHY"
    elif score >= 50:
        health = "MODERATE"
    else:
        health = "LOW ACTIVITY"

    print("\n--------------------------------")
    print(" Repository Health")
    print("--------------------------------")

    print(f"Health Score: {score}/100")
    print(f"Status:       {health}")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()