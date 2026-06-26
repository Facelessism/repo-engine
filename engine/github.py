from urllib.parse import urlparse
import requests


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def parse_url(self, url: str):
        parsed = urlparse(url)
        parts = parsed.path.strip("/").split("/")

        if len(parts) < 2:
            raise ValueError("Invalid GitHub repository URL.")

        owner = parts[0]
        repo = parts[1].removesuffix(".git")

        return owner, repo

    def fetch_tree(self, url: str):
        owner, repo = self.parse_url(url)

        repo_info = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repo}"
        )
        repo_info.raise_for_status()

        default_branch = repo_info.json()["default_branch"]

        tree = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repo}/git/trees/{default_branch}",
            params={"recursive": "1"},
        )
        tree.raise_for_status()

        return repo, tree.json()["tree"]
