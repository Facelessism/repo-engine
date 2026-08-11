import sys

from engine.repository import RepositoryEngine
from engine.formatter import TreeFormatter


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("python main.py <github-repository-url>")
        return

    result = RepositoryEngine().generate(sys.argv[1])

    TreeFormatter().format(
        result["name"],
        result["tree"],
    )


if __name__ == "__main__":
    main()
