"""Chart themes used by pyqicharts."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Theme:
    """Visual styling options for matplotlib charts."""
    line: str
    marker: str
    centre: str
    limits: str
    signal: str
    grid_alpha: float = 0.25

_THEMES = {
    "default": Theme("#1f77b4", "#1f77b4", "#ff7f0e", "#7f7f7f", "#d62728"),
    "nhs": Theme("#005EB8", "#005EB8", "#007F3B", "#768692", "#DA291C"),
    "publication": Theme("#222222", "#222222", "#555555", "#999999", "#000000", 0.18),
    "dark": Theme("#7FDBFF", "#7FDBFF", "#2ECC40", "#AAAAAA", "#FF4136", 0.18),
}

def list_themes() -> list[str]:
    """Return available built-in theme names."""
    return sorted(_THEMES)

def get_theme(theme: str | Theme = "default") -> Theme:
    """Return a built-in Theme object or validate a custom Theme."""
    if isinstance(theme, Theme):
        return theme
    key = str(theme).lower()
    if key not in _THEMES:
        raise ValueError(f"Unknown theme {theme!r}. Available themes: {', '.join(list_themes())}")
    return _THEMES[key]
