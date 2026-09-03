PACKAGE_MANAGERS = {
    "package-lock.json": "npm",
    "yarn.lock": "Yarn",
    "pnpm-lock.yaml": "pnpm",
    "bun.lockb": "Bun",
    "bun.lock": "Bun",
    "requirements.txt": "pip",
    "Pipfile": "pipenv",
    "poetry.lock": "Poetry",
    "uv.lock": "uv",
    "Cargo.lock": "Cargo",
    "go.sum": "Go Modules",
    "Gemfile.lock": "Bundler",
}

PYPROJECT_TOOLS = {
    "[tool.poetry]": "Poetry",
    "[tool.uv]": "uv",
    "[tool.pdm]": "PDM",
    "[tool.hatch]": "Hatch",
}


def detect_package_manager(files, contents):
    names = {
        file.rsplit("/", 1)[-1]
        for file in files
    }

    for filename, manager in PACKAGE_MANAGERS.items():
        if filename in names:
            return manager

    if "package.json" in names:
        return "npm"

    pyproject = next(
        (
            content.lower()
            for file, content in contents.items()
            if file.rsplit("/", 1)[-1] == "pyproject.toml"
        ),
        "",
    )

    for tool, manager in PYPROJECT_TOOLS.items():
        if tool in pyproject:
            return manager

    if "pyproject.toml" in names or "requirements.txt" in names:
        return "pip"

    return None
