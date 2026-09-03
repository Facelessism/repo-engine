from collections import Counter
from pathlib import Path


LANGUAGES = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".c": "C",
    ".h": "C",
    ".hpp": "C++",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
}


SPECIAL_FILES = {
    "Dockerfile": "Dockerfile",
    "Makefile": "Makefile",
}


def detect_language(files):
    counts = Counter()

    for file in files:
        name = file.rsplit("/", 1)[-1]

        if name in SPECIAL_FILES:
            counts[SPECIAL_FILES[name]] += 1
            continue

        extension = Path(name).suffix.lower()

        if extension in LANGUAGES:
            counts[LANGUAGES[extension]] += 1

    return counts.most_common(1)[0][0] if counts else None
