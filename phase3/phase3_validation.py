#!/usr/bin/env python3

import sqlite3

DB = "/home/saksham/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"

PROCESS = "x-www-browser"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("=" * 65)
print("        SHADOW AI SENTINEL")
print("        PHASE 3 DETECTION VALIDATION")
print("=" * 65)
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


average = baseline_average()


# --------------------------------------------------
# TEST 1 — Known destination
# --------------------------------------------------

destination = "34.107.243.93"

count = destination_count(destination)

print("[TEST 1] Known Destination")
print(f"Destination: {destination}")
print(f"Observed:    {count}")
print("Expected:    > 0")

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

print("[TEST 2] Destination Novelty")
print(f"Destination: {destination}")
print(f"Observed:    {count}")
print("Expected:    0")

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


# --------------------------------------------------
# TEST 4 — Real telemetry completeness
# --------------------------------------------------

cursor.execute("""
SELECT COUNT(*)
FROM events
WHERE timestamp IS NOT NULL
AND timestamp != ''
AND process_name IS NOT NULL
AND process_name != ''
AND remote_ip IS NOT NULL
AND remote_ip != ''
AND remote_port IS NOT NULL
AND hostname IS NOT NULL
AND hostname != ''
AND ai_status IS NOT NULL
AND ai_status != ''
AND connection_event IS NOT NULL
AND connection_event != ''
AND frequency IS NOT NULL
AND frequency != ''
""")

complete_events = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM events")

total_events = cursor.fetchone()[0]

print("[TEST 4] Telemetry Completeness")
print(f"Complete events: {complete_events}")
print(f"Total events:    {total_events}")
print("Expected:        Complete = Total")

if complete_events == total_events:
    print("PASS")
else:
    print("FAIL")

print()
print("=" * 65)
print("Phase 3 validation completed.")
print("=" * 65)

conn.close()
