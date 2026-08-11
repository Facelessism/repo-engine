from pathlib import Path


DIRECTORIES = {
    "src": "Source",
    "app": "Application",
    "lib": "Library",
    "tests": "Tests",
    "test": "Tests",
    "docs": "Documentation",
    "examples": "Examples",
    "scripts": "Scripts",
    "config": "Configuration",
}


def detect_structure(files):
    directories = set()

    for file in files:
        parts = Path(file).parts

        for part in parts[:-1]:
            directories.add(part.lower())

    return {
        "source": any(name in directories for name in ("src", "app", "lib")),
        "tests": any(name in directories for name in ("tests", "test")),
        "documentation": any(
            name in directories for name in ("docs",)
        ),
        "examples": "examples" in directories,
        "scripts": "scripts" in directories,
        "configuration": "config" in directories,
    }
