#!/usr/bin/env python3

import sqlite3

DB = "/home/saksham/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("=" * 50)
print("       SHADOW AI SENTINEL")
print("       BEHAVIORAL PROFILE")
print("=" * 50)
print()

#!/usr/bin/env python3

import sqlite3

DB = "/home/saksham/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("=" * 55)
print("              SHADOW AI SENTINEL")
print("              BEHAVIORAL BASELINE")
print("=" * 55)
print()

cursor.execute("""
SELECT
    process_name,
    COUNT(*) AS total_events,
    COUNT(DISTINCT remote_ip) AS unique_destinations
FROM events
GROUP BY process_name
""")

processes = cursor.fetchall()

for process_name, total_events, unique_destinations in processes:

    print(f"Process:                   {process_name}")
    print(f"Total Events:              {total_events}")
    print(f"Unique Destinations:       {unique_destinations}")

    # Destination frequency
    cursor.execute("""
    SELECT remote_ip, COUNT(*) AS connection_count
    FROM events
    WHERE process_name = ?
    GROUP BY remote_ip
    ORDER BY connection_count DESC
    """, (process_name,))

    destinations = cursor.fetchall()

    print()
    print("Destination Profile:")

    for remote_ip, count in destinations:
        print(f"  {remote_ip:<22} {count} events")

    # Maximum destination frequency
    max_frequency = max(
        [count for _, count in destinations],
        default=0
    )

    # AI events
    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE process_name = ?
    AND ai_status = 'YES'
    """, (process_name,))

    ai_events = cursor.fetchone()[0]

    # Unknown hostname events
    cursor.execute("""
    SELECT COUNT(*)
    FROM events
    WHERE process_name = ?
    AND hostname = 'UNKNOWN'
    """, (process_name,))

    unknown_events = cursor.fetchone()[0]

    print()
    print("Behavioral Features:")
    print(f"  Maximum Destination Frequency: {max_frequency}")
    print(f"  AI-Service Events:             {ai_events}")
    print(f"  Unknown Hostname Events:       {unknown_events}")

    print()
    print("-" * 55)

conn.close()
