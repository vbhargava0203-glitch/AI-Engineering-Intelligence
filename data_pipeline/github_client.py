import requests

BASE_URL = "https://api.github.com"


def get_repository(owner, repo):
    url = f"{BASE_URL}/repos/{owner}/{repo}"

    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception(f"GitHub API Error: {response.status_code}")

    return response.json()


if __name__ == "__main__":
    data = get_repository("facebook", "react")

    print("\n===== REPOSITORY =====")
    print("Name:", data["full_name"])
    print("Description:", data["description"])
    print("Stars:", data["stargazers_count"])
    print("Forks:", data["forks_count"])
    print("Open Issues:", data["open_issues_count"])
    print("Language:", data["language"])