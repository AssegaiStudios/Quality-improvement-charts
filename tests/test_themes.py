import pytest
from pyqicharts import get_theme, list_themes

def test_builtin_themes_are_available():
    assert "default" in list_themes()
    assert "nhs" in list_themes()

def test_unknown_theme_raises():
    with pytest.raises(ValueError): get_theme("not-a-theme")
