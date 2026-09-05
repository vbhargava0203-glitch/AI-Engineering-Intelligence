import os
import requests
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GITHUB_API = "https://api.github.com"


def github_get(endpoint, params=None):
    response = requests.get(
        GITHUB_API + endpoint,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        print(f"   API error: {response.status_code}")
        return []

    return response.json()


def main():

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, full_name
        FROM repositories
        ORDER BY id;
    """)

    repositories = cursor.fetchall()

    print("\n================================")
    print(" Engineering Activity Collector")
    print("================================\n")

    for repository_id, full_name in repositories:

        owner, repo = full_name.split("/", 1)

        print(f"\n📦 {full_name}")

        # -------------------------
        # Contributors
        # -------------------------

        contributors = github_get(
            f"/repos/{owner}/{repo}/contributors",
            {"per_page": 30}
        )

        contributor_map = {}

        for contributor in contributors:

            github_id = contributor["id"]
            username = contributor["login"]

            cursor.execute(
                """
                INSERT INTO contributors
                    (github_id, username, profile_url)
                VALUES
                    (%s, %s, %s)
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

        print(f"   Contributors: {len(contributors)}")

        # -------------------------
        # Commits
        # -------------------------

        commits = github_get(
            f"/repos/{owner}/{repo}/commits",
            {"per_page": 30}
        )

        commit_count = 0

        for commit in commits:

            sha = commit["sha"]

            author_id = None

            if commit.get("author"):
                username = commit["author"]["login"]
                author_id = contributor_map.get(username)

            commit_info = commit["commit"]

            cursor.execute(
                """
                INSERT INTO commits
                    (
                        repository_id,
                        sha,
                        message,
                        author_id,
                        commit_date
                    )
                VALUES
                    (%s, %s, %s, %s, %s)
                ON CONFLICT (sha)
                DO NOTHING;
                """,
                (
                    repository_id,
                    sha,
                    commit_info["message"],
                    author_id,
                    commit_info["author"]["date"]
                )
            )

            commit_count += 1

        print(f"   Commits: {commit_count}")

        # -------------------------
        # Pull Requests
        # -------------------------

        pull_requests = github_get(
            f"/repos/{owner}/{repo}/pulls",
            {
                "state": "all",
                "per_page": 30
            }
        )

        pr_count = 0

        for pr in pull_requests:

            author_id = contributor_map.get(
                pr["user"]["login"]
            )

            cursor.execute(
                """
                INSERT INTO pull_requests
                    (
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
                VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s,%s)
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

            pr_count += 1

        print(f"   Pull Requests: {pr_count}")

        # -------------------------
        # Issues
        # -------------------------

        issues = github_get(
            f"/repos/{owner}/{repo}/issues",
            {
                "state": "all",
                "per_page": 30
            }
        )

        issue_count = 0

        for issue in issues:

            # Pull requests also appear in the issues endpoint.
            if "pull_request" in issue:
                continue

            author_id = contributor_map.get(
                issue["user"]["login"]
            )

            cursor.execute(
                """
                INSERT INTO issues
                    (
                        repository_id,
                        github_id,
                        number,
                        title,
                        state,
                        author_id,
                        created_at,
                        closed_at
                    )
                VALUES
                    (%s,%s,%s,%s,%s,%s,%s,%s)
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

            issue_count += 1

        print(f"   Issues: {issue_count}")

        connection.commit()

    cursor.close()
    connection.close()

    print("\n================================")
    print(" ACTIVITY COLLECTION COMPLETE")
    print("================================\n")


if __name__ == "__main__":
    main()