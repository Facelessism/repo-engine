from pathlib import Path


SOURCE_DIRECTORIES = {"src", "app", "lib"}
TEST_DIRECTORIES = {"test", "tests"}
DOCUMENTATION_DIRECTORIES = {"docs", "documentation"}
EXAMPLE_DIRECTORIES = {"example", "examples"}
SCRIPT_DIRECTORIES = {"script", "scripts"}
CONFIGURATION_DIRECTORIES = {"config", "configs", "configuration"}


def detect_structure(files):
    directories = {
        part.lower()
        for file in files
        for part in Path(file).parts[:-1]
    }

    return {
        "source": bool(directories & SOURCE_DIRECTORIES),
        "tests": bool(directories & TEST_DIRECTORIES),
        "documentation": bool(directories & DOCUMENTATION_DIRECTORIES),
        "examples": bool(directories & EXAMPLE_DIRECTORIES),
        "scripts": bool(directories & SCRIPT_DIRECTORIES),
        "configuration": bool(directories & CONFIGURATION_DIRECTORIES),
    }
