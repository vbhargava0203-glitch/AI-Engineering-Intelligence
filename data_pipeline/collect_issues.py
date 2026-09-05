import requests

BASE_URL = "https://api.github.com"


def get_issues(owner, repo, limit=20):
    url = f"{BASE_URL}/repos/{owner}/{repo}/issues"

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
    issues = get_issues("react", "react")

    print(f"\nCollected {len(issues)} issues\n")

    for issue in issues:
        number = issue["number"]
        title = issue["title"]
        author = issue["user"]["login"]
        state = issue["state"]

        # GitHub's issues endpoint also returns pull requests.
        if "pull_request" in issue:
            item_type = "PR"
        else:
            item_type = "ISSUE"

        print(f"{item_type} #{number} | {author} | {state} | {title}")