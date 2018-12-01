#!/usr/bin/env python

drift_start = 0

with open("drift_values.pi", "r") as f:
    for drift_value in f:
        drift_int = int(drift_value)

        drift_start += drift_int

print("Calculated drift to be", drift_start)
