"""NK landscape analysis for Python packages."""

__version__ = "0.1.0"

from nk_analyze.core import analyze_lazy_imports, analyze_package, detect_cycles

__all__ = ["analyze_package", "analyze_lazy_imports", "detect_cycles"]
