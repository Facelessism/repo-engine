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
    ".c": "C",
    ".h": "C",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
}


def detect_language(files):
    counts = Counter()

    for file in files:
        extension = Path(file).suffix.lower()

        if extension in LANGUAGES:
            counts[LANGUAGES[extension]] += 1

    return counts.most_common(1)[0][0] if counts else None

