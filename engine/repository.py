from .github import GitHubClient
from .tree import TreeBuilder


class RepositoryEngine:
    def __init__(self):
        self.github = GitHubClient()
        self.builder = TreeBuilder()

    def generate(self, url):
        name, files = self.github.fetch_tree(url)
        tree = self.builder.build(files)

        return {
            "name": name,
            "tree": tree,
        }

