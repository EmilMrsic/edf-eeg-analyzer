import pytest

from band_labels import label_power


THRESHOLDS = {"VLO": 0.0, "LO": 1.0, "OK": 5.0, "HI": 10.0, "VHI": 20.0}


@pytest.mark.parametrize(
    "value,expected",
    [
        (0.0, "VLO"),
        (1.0, "LO"),
        (4.9, "LO"),
        (5.0, "OK"),
        (9.9, "OK"),
        (10.0, "HI"),
        (19.9, "HI"),
        (20.0, "VHI"),
        (25.0, "VHI"),
    ],
)
def test_label_power(value, expected):
    assert label_power(value, THRESHOLDS) == expected
