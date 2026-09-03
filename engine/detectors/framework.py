import json
import re


FRAMEWORKS = {
    "react": "React",
    "next": "Next.js",
    "vue": "Vue",
    "nuxt": "Nuxt",
    "express": "Express",
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "angular": "Angular",
    "svelte": "Svelte",
    "astro": "Astro",
    "laravel": "Laravel",
}


def detect_framework(files, contents):
    for file, content in contents.items():
        name = file.rsplit("/", 1)[-1]

        if name == "package.json":
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                continue

            dependencies = {}
            dependencies.update(data.get("dependencies", {}))
            dependencies.update(data.get("devDependencies", {}))

            for package, framework in FRAMEWORKS.items():
                if any(
                    package == dependency.lower()
                    or dependency.lower().startswith(f"{package}/")
                    for dependency in dependencies
                ):
                    return framework

        elif name in {"requirements.txt", "Pipfile", "pyproject.toml"}:
            text = content.lower()

            for package, framework in FRAMEWORKS.items():
                pattern = rf"(?<![\w-]){re.escape(package)}(?![\w-])"

                if re.search(pattern, text):
                    return framework

        elif name == "composer.json":
            try:
                data = json.loads(content)
            except json.JSONDecodeError:
                continue

            dependencies = {}
            dependencies.update(data.get("require", {}))
            dependencies.update(data.get("require-dev", {}))

            for package, framework in FRAMEWORKS.items():
                if any(package in dependency.lower() for dependency in dependencies):
                    return framework

    return None
