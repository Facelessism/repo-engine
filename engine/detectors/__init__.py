from .framework import detect_framework
from .language import detect_language
from .package_manager import detect_package_manager
from .structure import detect_structure

__all__ = [
    "detect_framework",
    "detect_language",
    "detect_package_manager",
    "detect_structure",
]
