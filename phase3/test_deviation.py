#!/usr/bin/env python3

import sqlite3

DB = "/home/saksham/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"

process_name = "x-www-browser"
test_destination = "151.101.105.91"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

cursor.execute("""
SELECT COUNT(*)
FROM events
WHERE process_name = ?
AND remote_ip = ?
""", (process_name, test_destination))

current_frequency = cursor.fetchone()[0]

cursor.execute("""
SELECT AVG(connection_count)
FROM (
    SELECT remote_ip, COUNT(*) AS connection_count
    FROM events
    WHERE process_name = ?
    GROUP BY remote_ip
)
""", (process_name,))

average_frequency = cursor.fetchone()[0]

print("=" * 55)
print("       SHADOW AI SENTINEL")
print("       FREQUENCY DEVIATION TEST")
print("=" * 55)
print()

print(f"Process:             {process_name}")
print(f"Destination:         {test_destination}")
print(f"Current Frequency:   {current_frequency}")
print(f"Baseline Average:    {average_frequency:.2f}")
print()

if current_frequency > average_frequency:
    deviation = "YES"
else:
    deviation = "NO"

print(f"Frequency Deviation:  {deviation}")

if deviation == "YES":
    print()
    print("Reason:")
    print("Destination frequency is above the historical")
    print("average for this process.")

conn.close()

