import requests

BASE_URL = "https://api.github.com"


def get_commits(owner, repo, limit=20):
    url = f"{BASE_URL}/repos/{owner}/{repo}/commits"

    response = requests.get(
        url,
        params={"per_page": limit},
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(f"GitHub API Error: {response.status_code}")

    return response.json()


if __name__ == "__main__":
    commits = get_commits("react", "react")

    print(f"\nCollected {len(commits)} commits\n")

    for commit in commits:
        sha = commit["sha"][:7]
        message = commit["commit"]["message"].split("\n")[0]
        author = commit["commit"]["author"]["name"]

        print(f"{sha} | {author} | {message}")