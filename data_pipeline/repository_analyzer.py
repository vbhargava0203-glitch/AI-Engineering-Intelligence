import os
import sys
import requests
import psycopg2
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

HEADERS = {
    "Accept": "application/vnd.github+json"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# ============================================================
# GITHUB
# ============================================================

def parse_repository_url(url):
    url = url.rstrip("/")

    parts = url.split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    owner = parts[-2]
    repo = parts[-1]

    return owner, repo


def github_get(endpoint, params=None):

    url = f"https://api.github.com{endpoint}"

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error {response.status_code}: "
            f"{response.text}"
        )

    return response.json()


# ============================================================
# DATABASE
# ============================================================

def get_database_connection():

    if not DATABASE_URL:
        raise Exception(
            "DATABASE_URL not found in .env"
        )

    return psycopg2.connect(DATABASE_URL)


def save_repository(repository):

    connection = get_database_connection()

    cursor = connection.cursor()

    query = """
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
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )

        ON CONFLICT (github_id)
        DO UPDATE SET
            name = EXCLUDED.name,
            full_name = EXCLUDED.full_name,
            description = EXCLUDED.description,
            language = EXCLUDED.language,
            stars = EXCLUDED.stars,
            forks = EXCLUDED.forks,
            open_issues = EXCLUDED.open_issues,
            updated_at = EXCLUDED.updated_at;
    """

    cursor.execute(
        query,
        (
            repository["id"],
            repository["name"],
            repository["full_name"],
            repository["description"],
            repository["language"],
            repository["stargazers_count"],
            repository["forks_count"],
            repository["open_issues_count"],
            repository["created_at"],
            repository["updated_at"]
        )
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("\n✅ Repository saved to PostgreSQL.")


# ============================================================
# ANALYZER
# ============================================================

def analyze_repository(repository_url):

    owner, repo = parse_repository_url(
        repository_url
    )

    print("\n================================")
    print(" GitHub Repository Analyzer")
    print("================================")

    print(
        f"\nAnalyzing: {owner}/{repo}"
    )

    # --------------------------------------------------------
    # Repository
    # --------------------------------------------------------

    repository = github_get(
        f"/repos/{owner}/{repo}"
    )

    print("\n===== REPOSITORY =====")

    print(
        "Name:",
        repository["name"]
    )

    print(
        "Full Name:",
        repository["full_name"]
    )

    print(
        "Description:",
        repository["description"]
    )

    print(
        "Language:",
        repository["language"]
    )

    print(
        "Stars:",
        repository["stargazers_count"]
    )

    print(
        "Forks:",
        repository["forks_count"]
    )

    print(
        "Open Issues:",
        repository["open_issues_count"]
    )

    # --------------------------------------------------------
    # Contributors
    # --------------------------------------------------------

    contributors = github_get(
        f"/repos/{owner}/{repo}/contributors",
        params={
            "per_page": 100
        }
    )

    print("\n===== CONTRIBUTORS =====")

    print(
        "Contributors:",
        len(contributors)
    )

    # --------------------------------------------------------
    # Commits
    # --------------------------------------------------------

    commits = github_get(
        f"/repos/{owner}/{repo}/commits",
        params={
            "per_page": 100
        }
    )

    print("\n===== COMMITS =====")

    print(
        "Recent commits collected:",
        len(commits)
    )

    # --------------------------------------------------------
    # Pull Requests
    # --------------------------------------------------------

    pull_requests = github_get(
        f"/repos/{owner}/{repo}/pulls",
        params={
            "state": "all",
            "per_page": 100
        }
    )

    print("\n===== PULL REQUESTS =====")

    print(
        "Pull requests collected:",
        len(pull_requests)
    )

    # --------------------------------------------------------
    # Issues
    # --------------------------------------------------------

    issues = github_get(
        f"/repos/{owner}/{repo}/issues",
        params={
            "state": "all",
            "per_page": 100
        }
    )

    real_issues = [
        issue
        for issue in issues
        if "pull_request" not in issue
    ]

    print("\n===== ISSUES =====")

    print(
        "Issues collected:",
        len(real_issues)
    )

    # --------------------------------------------------------
    # Save repository
    # --------------------------------------------------------

    save_repository(repository)

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print("\n================================")
    print(" Engineering Summary")
    print("================================")

    print(
        "Repository:",
        repository["full_name"]
    )

    print(
        "Stars:",
        repository["stargazers_count"]
    )

    print(
        "Forks:",
        repository["forks_count"]
    )

    print(
        "Contributors:",
        len(contributors)
    )

    print(
        "Recent Commits:",
        len(commits)
    )

    print(
        "Pull Requests:",
        len(pull_requests)
    )

    print(
        "Issues:",
        len(real_issues)
    )

    return {
        "repository": repository,
        "contributors": contributors,
        "commits": commits,
        "pull_requests": pull_requests,
        "issues": real_issues
    }


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    url = input(
        "\nEnter GitHub repository URL: "
    ).strip()

    try:

        analyze_repository(url)

        print(
            "\n✅ Repository analysis completed."
        )

    except Exception as error:

        print(
            "\n❌ Analysis failed:"
        )

        print(error)