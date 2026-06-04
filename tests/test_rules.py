from pyqicharts import anhoej_rules


def test_anhoej_rules_returns_expected_fields():
    result = anhoej_rules([1, 2, 3, 4, 5, 6])
    assert result.median == 3.5
    assert result.n_used == 6
    assert result.longest_run >= 1
    assert isinstance(result.signal_long_run, bool)
    assert isinstance(result.signal_few_crossings, bool)
