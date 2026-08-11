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
    relevant = []

    for file, content in contents.items():
        name = file.split("/")[-1]

        if name in {
            "package.json",
            "requirements.txt",
            "pyproject.toml",
            "Pipfile",
            "composer.json",
        }:
            relevant.append(content.lower())

    text = "\n".join(relevant)

    for package, framework in FRAMEWORKS.items():
        if package in text:
            return framework

    return None
