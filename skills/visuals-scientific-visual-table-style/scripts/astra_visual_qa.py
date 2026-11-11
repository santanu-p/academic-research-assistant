#!/usr/bin/env python3
"""Astra hard-gate entry point."""
MIN_BODY_PT=7.5
MAX_GROUPED_BAR_SERIES=4
def reject(*, body_pt, grouped_series=0):
    errors=[]
    if body_pt < MIN_BODY_PT: errors.append("text below 7.5 pt")
    if grouped_series > MAX_GROUPED_BAR_SERIES: errors.append("too many grouped-bar series")
    return errors
