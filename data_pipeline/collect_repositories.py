import os
import requests
import psycopg2
from dotenv import load_dotenv

from repository_list import REPOSITORIES

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

GITHUB_API = "https://api.github.com"


def get_repository(owner, repo):

    url = f"{GITHUB_API}/repos/{owner}/{repo}"

    response = requests.get(
        url,
        timeout=30
    )

    if response.status_code != 200:
        print(f"❌ Failed: {owner}/{repo}")
        return None

    return response.json()


def main():

    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()

    print("\n================================")
    print(" Repository Collection")
    print("================================\n")

    successful = 0

    for owner, repo in REPOSITORIES:

        print(f"Collecting {owner}/{repo}...")

        data = get_repository(owner, repo)

        if not data:
            continue

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
                updated_at = EXCLUDED.updated_at;
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

        successful += 1

    connection.commit()

    cursor.close()
    connection.close()

    print("\n================================")
    print(f"Successfully collected: {successful}")
    print("================================")


if __name__ == "__main__":
    main()