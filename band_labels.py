"""Utilities for labeling absolute power values."""

from __future__ import annotations

from typing import Dict


def label_power(value: float, thresholds: Dict[str, float]) -> str:
    """Return categorical label for ``value`` based on ``thresholds``.

    Parameters
    ----------
    value:
        Absolute power value in µV².
    thresholds:
        Mapping of label -> threshold. The mapping should be ordered from
        lowest to highest threshold. The function returns the label
        associated with the highest threshold that is less than or equal to
        ``value``.

    Examples
    --------
    >>> t = {"VLO": 0.0, "LO": 1.0, "OK": 5.0, "HI": 10.0, "VHI": 20.0}
    >>> label_power(7.0, t)
    'OK'
    """
    if not thresholds:
        raise ValueError("thresholds mapping cannot be empty")

    sorted_items = sorted(thresholds.items(), key=lambda x: x[1])
    chosen_label = sorted_items[0][0]
    for label, thr in sorted_items:
        if value >= thr:
            chosen_label = label
        else:
            break
    return chosen_label
