#!/usr/bin/env python3

import sqlite3

DB = "/home/saksham/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("=" * 60)
print("       SHADOW AI SENTINEL")
print("       TELEMETRY INTEGRITY")
print("=" * 60)
print()

# --------------------------------------------------
# Database integrity
# --------------------------------------------------

cursor.execute("PRAGMA integrity_check;")
integrity = cursor.fetchone()[0]

print(f"Database Integrity:       {integrity}")

# --------------------------------------------------
# Required telemetry fields
# --------------------------------------------------

cursor.execute("""
SELECT
    COUNT(*),
    SUM(CASE WHEN timestamp IS NULL OR timestamp = '' THEN 1 ELSE 0 END),
    SUM(CASE WHEN process_name IS NULL OR process_name = '' THEN 1 ELSE 0 END),
    SUM(CASE WHEN remote_ip IS NULL OR remote_ip = '' THEN 1 ELSE 0 END),
    SUM(CASE WHEN remote_port IS NULL THEN 1 ELSE 0 END),
    SUM(CASE WHEN hostname IS NULL OR hostname = '' THEN 1 ELSE 0 END),
    SUM(CASE WHEN ai_status IS NULL OR ai_status = '' THEN 1 ELSE 0 END),
    SUM(CASE WHEN connection_event IS NULL OR connection_event = '' THEN 1 ELSE 0 END),
    SUM(CASE WHEN frequency IS NULL OR frequency = '' THEN 1 ELSE 0 END)
FROM events;
""")

result = cursor.fetchone()

(
    total_events,
    missing_timestamp,
    missing_process,
    missing_ip,
    missing_port,
    missing_hostname,
    missing_ai_status,
    missing_connection_event,
    missing_frequency
) = result

print()
print("Telemetry Records:")
print(f"  Total Events:             {total_events}")

print()
print("Missing Required Fields:")
print(f"  Timestamp:                {missing_timestamp}")
print(f"  Process Name:             {missing_process}")
print(f"  Remote IP:                {missing_ip}")
print(f"  Remote Port:              {missing_port}")
print(f"  Hostname:                 {missing_hostname}")
print(f"  AI Status:                {missing_ai_status}")
print(f"  Connection Event:         {missing_connection_event}")
print(f"  Frequency:                {missing_frequency}")

# --------------------------------------------------
# Final assessment
# --------------------------------------------------

missing_total = (
    missing_timestamp +
    missing_process +
    missing_ip +
    missing_port +
    missing_hostname +
    missing_ai_status +
    missing_connection_event +
    missing_frequency
)

print()

if integrity == "ok" and missing_total == 0:
    print("Telemetry Integrity:       PASS")
else:
    print("Telemetry Integrity:       FAIL")

print()
print("-" * 60)

conn.close()
