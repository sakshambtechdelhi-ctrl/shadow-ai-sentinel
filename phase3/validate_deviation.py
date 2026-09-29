#!/usr/bin/env python3

import sqlite3

DB = "/home/saksham/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"

PROCESS = "x-www-browser"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("=" * 60)
print("       SHADOW AI SENTINEL")
print("       DEVIATION VALIDATION")
print("=" * 60)
print()


def destination_count(destination):

    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE process_name = ?
    AND remote_ip = ?
    """, (PROCESS, destination))

    return cursor.fetchone()[0]


def baseline_average():

    cursor.execute("""
    SELECT AVG(connection_count)
    FROM (
        SELECT remote_ip, COUNT(*) AS connection_count
        FROM events
        WHERE process_name = ?
        GROUP BY remote_ip
    )
    """, (PROCESS,))

    return cursor.fetchone()[0] or 0


# --------------------------------------------------
# TEST 1 — Known destination
# --------------------------------------------------

destination = "34.107.243.93"

count = destination_count(destination)

print("[TEST 1] Known Destination")
print(f"Destination: {destination}")
print(f"Count:       {count}")
print("Expected:    Count > 0")

if count > 0:
    print("PASS")
else:
    print("FAIL")

print()


# --------------------------------------------------
# TEST 2 — New destination
# --------------------------------------------------

destination = "203.0.113.50"

count = destination_count(destination)

print("[TEST 2] New Destination")
print(f"Destination: {destination}")
print(f"Count:       {count}")
print("Expected:    Count = 0")

if count == 0:
    print("PASS")
else:
    print("FAIL")

print()


# --------------------------------------------------
# TEST 3 — Frequency deviation
# --------------------------------------------------

destination = "151.101.105.91"

count = destination_count(destination)
average = baseline_average()

print("[TEST 3] Frequency Deviation")
print(f"Destination: {destination}")
print(f"Frequency:   {count}")
print(f"Average:     {average:.2f}")
print("Expected:    Frequency > Average")

if count > average:
    print("PASS")
else:
    print("FAIL")

print()


print("=" * 60)
print("Behavioral validation completed.")
print("=" * 60)

conn.close()
