import requests

BASE_URL = "https://api.github.com"


def get_pull_requests(owner, repo, limit=20):
    url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"

    response = requests.get(
        url,
        params={
            "state": "all",
            "per_page": limit
        },
        timeout=10
    )

    if response.status_code != 200:
        raise Exception(f"GitHub API Error: {response.status_code}")

    return response.json()


if __name__ == "__main__":
    pull_requests = get_pull_requests("react", "react")

    print(f"\nCollected {len(pull_requests)} pull requests\n")

    for pr in pull_requests:
        number = pr["number"]
        title = pr["title"]
        author = pr["user"]["login"]
        state = pr["state"]

        print(f"#{number} | {author} | {state} | {title}")