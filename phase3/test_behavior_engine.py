#!/usr/bin/env python3

import sqlite3
import subprocess

DB = "/home/saksham/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"
ENGINE = "/home/saksham/Projects/shadow-ai-sentinel/phase3/deviation_engine.py"

tests = [
    {
        "name": "Known destination with frequency deviation",
        "process": "x-www-browser",
        "destination": "34.107.243.93",
        "expected": "Frequency Deviation:   YES"
    },
    {
        "name": "New destination",
        "process": "x-www-browser",
        "destination": "203.0.113.50",
        "expected": "Destination Deviation: YES"
    },
    {
        "name": "High frequency with unknown hostname",
        "process": "x-www-browser",
        "destination": "151.101.105.91",
        "expected": "Unknown Hostname:      YES"
    }
]

print("=" * 60)
print("       SHADOW AI SENTINEL")
print("       BEHAVIOR ENGINE VALIDATION")
print("=" * 60)
print()

passed = 0
failed = 0

for test in tests:

    print(f"[TEST] {test['name']}")

    result = subprocess.run(
        [
            "python3",
            ENGINE,
            test["process"],
            test["destination"]
        ],
        capture_output=True,
        text=True
    )

    output = result.stdout

    if test["expected"] in output:
        print("Result: PASS")
        passed += 1
    else:
        print("Result: FAIL")
        failed += 1

    print()

print("=" * 60)
print(f"Passed: {passed}")
print(f"Failed: {failed}")
print("=" * 60)

if failed == 0:
    print()
    print("ALL BEHAVIORAL TESTS PASSED")
else:
    print()
    print("SOME BEHAVIORAL TESTS FAILED")
