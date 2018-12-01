#!/usr/bin/env python

drift_changes = []
with open("drift_values.pi", "r") as f:
    drift_changes = f.readlines()

def calculate_repeated_frequency(drifts):
    drift_start = 0
    drift_values = set()
    while True:
        for drift_value in drifts:
            if drift_start in drift_values:
                return drift_start

            drift_values.add(drift_start)
            drift_int = int(drift_value)

            drift_start += drift_int


print("Calculated duplicate drift frequency to be", calculate_repeated_frequency(drift_changes))
