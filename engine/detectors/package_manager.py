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


def detect_package_manager(files):
    for file in files:
        name = file.rsplit("/", 1)[-1]

        if name in PACKAGE_MANAGERS:
            return PACKAGE_MANAGERS[name]

    if any(file.endswith("package.json") for file in files):
        return "npm"

    return None
