import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

OWNER = "react"
REPO = "react"

GITHUB_API = "https://api.github.com"


def github_get(endpoint, params=None):
    url = f"{GITHUB_API}{endpoint}"

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"GitHub API Error {response.status_code}: {response.text}"
        )

    return response.json()


def connect_database():
    return psycopg2.connect(DATABASE_URL)


def insert_repository(cursor):
    data = github_get(f"/repos/{OWNER}/{REPO}")

    cursor.execute(
        """
        INSERT INTO repositories (
            github_id,
            name,
            full_name,
            description,
            language,
            stars,
            forks,
            open_issues,
            created_at,
            updated_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (github_id)
        DO UPDATE SET
            stars = EXCLUDED.stars,
            forks = EXCLUDED.forks,
            open_issues = EXCLUDED.open_issues,
            updated_at = EXCLUDED.updated_at
        RETURNING id;
        """,
        (
            data["id"],
            data["name"],
            data["full_name"],
            data["description"],
            data["language"],
            data["stargazers_count"],
            data["forks_count"],
            data["open_issues_count"],
            data["created_at"],
            data["updated_at"]
        )
    )

    repository_id = cursor.fetchone()[0]

    print("Repository       ✓")

    return repository_id


def insert_contributors(cursor, repository_id):
    contributors = github_get(
        f"/repos/{OWNER}/{REPO}/contributors",
        {"per_page": 30}
    )

    contributor_map = {}

    for contributor in contributors:
        github_id = contributor["id"]
        username = contributor["login"]

        cursor.execute(
            """
            INSERT INTO contributors (
                github_id,
                username,
                profile_url
            )
            VALUES (%s,%s,%s)
            ON CONFLICT (github_id)
            DO UPDATE SET
                username = EXCLUDED.username,
                profile_url = EXCLUDED.profile_url
            RETURNING id;
            """,
            (
                github_id,
                username,
                contributor["html_url"]
            )
        )

        contributor_id = cursor.fetchone()[0]

        contributor_map[username] = contributor_id

    print(f"Contributors    ✓ ({len(contributors)})")

    return contributor_map


def insert_commits(cursor, repository_id, contributor_map):
    commits = github_get(
        f"/repos/{OWNER}/{REPO}/commits",
        {"per_page": 30}
    )

    count = 0

    for commit in commits:

        sha = commit["sha"]

        author = commit["author"]

        author_id = None

        if author:
            username = author["login"]
            author_id = contributor_map.get(username)

        commit_data = commit["commit"]

        cursor.execute(
            """
            INSERT INTO commits (
                repository_id,
                sha,
                message,
                author_id,
                commit_date
            )
            VALUES (%s,%s,%s,%s,%s)
            ON CONFLICT (sha)
            DO NOTHING;
            """,
            (
                repository_id,
                sha,
                commit_data["message"],
                author_id,
                commit_data["author"]["date"]
            )
        )

        count += 1

    print(f"Commits         ✓ ({count})")


def insert_pull_requests(cursor, repository_id, contributor_map):
    pull_requests = github_get(
        f"/repos/{OWNER}/{REPO}/pulls",
        {
            "state": "all",
            "per_page": 30
        }
    )

    count = 0

    for pr in pull_requests:

        author = pr["user"]

        author_id = contributor_map.get(
            author["login"]
        )

        cursor.execute(
            """
            INSERT INTO pull_requests (
                repository_id,
                github_id,
                number,
                title,
                state,
                author_id,
                created_at,
                closed_at,
                merged_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (github_id)
            DO NOTHING;
            """,
            (
                repository_id,
                pr["id"],
                pr["number"],
                pr["title"],
                pr["state"],
                author_id,
                pr["created_at"],
                pr["closed_at"],
                pr.get("merged_at")
            )
        )

        count += 1

    print(f"Pull Requests   ✓ ({count})")


def insert_issues(cursor, repository_id, contributor_map):
    issues = github_get(
        f"/repos/{OWNER}/{REPO}/issues",
        {
            "state": "all",
            "per_page": 30
        }
    )

    count = 0

    for issue in issues:

        # GitHub returns pull requests from this endpoint too.
        if "pull_request" in issue:
            continue

        author = issue["user"]

        author_id = contributor_map.get(
            author["login"]
        )

        cursor.execute(
            """
            INSERT INTO issues (
                repository_id,
                github_id,
                number,
                title,
                state,
                author_id,
                created_at,
                closed_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (github_id)
            DO NOTHING;
            """,
            (
                repository_id,
                issue["id"],
                issue["number"],
                issue["title"],
                issue["state"],
                author_id,
                issue["created_at"],
                issue["closed_at"]
            )
        )

        count += 1

    print(f"Issues          ✓ ({count})")


def main():

    print("\n================================")
    print(" GitHub Engineering ETL")
    print("================================\n")

    connection = connect_database()

    cursor = connection.cursor()

    try:

        repository_id = insert_repository(cursor)

        contributor_map = insert_contributors(
            cursor,
            repository_id
        )

        insert_commits(
            cursor,
            repository_id,
            contributor_map
        )

        insert_pull_requests(
            cursor,
            repository_id,
            contributor_map
        )

        insert_issues(
            cursor,
            repository_id,
            contributor_map
        )

        connection.commit()

        print("\n================================")
        print(" ETL COMPLETED SUCCESSFULLY")
        print("================================\n")

    except Exception as error:

        connection.rollback()

        print("\n❌ ETL FAILED")
        print(error)

    finally:

        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()