from .detectors.framework import detect_framework
from .detectors.language import detect_language
from .detectors.package_manager import detect_package_manager
from .detectors.structure import detect_structure
from .formatter import TreeFormatter
from .github import GitHubClient
from .tree import TreeBuilder


class RepositoryEngine:
    def __init__(self):
        self.github = GitHubClient()
        self.builder = TreeBuilder()
        self.formatter = TreeFormatter()

    def generate(self, url):
        name, files = self.github.fetch_tree(url)
        tree = self.builder.build(files)
        contents = self.github.fetch_contents(url, files)

        analysis = {
            "language": detect_language(files),
            "package_manager": detect_package_manager(files),
            "structure": detect_structure(files),
            "framework": detect_framework(files, contents),
        }

        return self.formatter.format(
            name,
            tree,
            analysis,
        )

