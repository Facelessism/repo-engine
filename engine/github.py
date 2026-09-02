from urllib.parse import urlparse

import requests


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def parse_url(self, url: str):
        parsed = urlparse(url)
        parts = parsed.path.strip("/").split("/")

        if len(parts) < 2:
            raise ValueError("Invalid GitHub repository URL!!!")

        owner = parts[0]
        repo = parts[1].removesuffix(".git")

        return owner, repo

    def fetch_repository(self, url: str):
        owner, repo = self.parse_url(url)

        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repo}"
        )
        response.raise_for_status()

        return response.json()

    def fetch_tree(self, url: str):
        owner, repo = self.parse_url(url)

        repository = self.fetch_repository(url)
        default_branch = repository["default_branch"]

        response = requests.get(
            f"{self.BASE_URL}/repos/{owner}/{repo}/git/trees/{default_branch}",
            params={"recursive": "1"},
        )
        response.raise_for_status()

        entries = response.json()["tree"]

        files = [
            entry["path"]
            for entry in entries
            if entry["type"] == "blob"
        ]

        return repo, files

    def fetch_contents(self, url: str, files):
        owner, repo = self.parse_url(url)
        contents = {}

        for file in files:
            try:
                response = requests.get(
                    f"{self.BASE_URL}/repos/{owner}/{repo}/contents/{file}"
                )

                if response.status_code != 200:
                    continue

                data = response.json()

                if data.get("encoding") != "base64":
                    continue

                import base64

                contents[file] = base64.b64decode(
                    data["content"]
                ).decode("utf-8", errors="ignore")

            except (requests.RequestException, UnicodeDecodeError):
                continue

        return contents
