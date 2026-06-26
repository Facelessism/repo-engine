import sys

from engine.github import GitHubClient
from engine.tree import TreeBuilder
from engine.formatter import TreeFormatter


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py <github-repository-url>")
        return

    url = sys.argv[1]

    github = GitHubClient()

    repo_name, files = github.fetch_tree(url)

    tree = TreeBuilder().build(files)

    TreeFormatter().format(repo_name, tree)


if __name__ == "__main__":
    main()
