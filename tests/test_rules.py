from pyqicharts.rules import anhoej_rules, shewhart_rule


def test_anhoej_rules_basic_counts():
    result = anhoej_rules([1, 2, 3, 4, 5, 6], centre=3.5)
    assert result.n_used == 6
    assert result.runs == 2
    assert result.crossings == 1
    assert result.longest_run == 3


def test_shewhart_rule_flags_outside_limits():
    result = shewhart_rule([0, 1, 10], centre=0, sigma=2)
    assert list(result) == [False, False, True]
