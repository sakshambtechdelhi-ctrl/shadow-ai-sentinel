import sqlite3
import sys

DB = "/home/saksham/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"

PROCESS = sys.argv[1] if len(sys.argv) > 1 else "x-www-browser"
DESTINATION = sys.argv[2] if len(sys.argv) > 2 else "151.101.105.91"

conn = sqlite3.connect(DB)
cursor = conn.cursor()

print("=" * 60)
print("           SHADOW AI SENTINEL")
print("           BEHAVIORAL DEVIATION")
print("=" * 60)
print()

# --------------------------------------------------
# 1. Historical destination frequency
# --------------------------------------------------

cursor.execute("""
SELECT COUNT(*)
FROM events
WHERE process_name = ?
AND remote_ip = ?
""", (PROCESS, DESTINATION))

current_frequency = cursor.fetchone()[0]

# --------------------------------------------------
# 2. Baseline average destination frequency
# --------------------------------------------------

cursor.execute("""
SELECT AVG(connection_count)
FROM (
    SELECT remote_ip, COUNT(*) AS connection_count
    FROM events
    WHERE process_name = ?
    GROUP BY remote_ip
)
""", (PROCESS,))

baseline_average = cursor.fetchone()[0] or 0

# --------------------------------------------------
# 3. Destination novelty
# --------------------------------------------------

destination_deviation = current_frequency == 0

# --------------------------------------------------
# 4. Frequency deviation
# --------------------------------------------------

frequency_deviation = current_frequency > baseline_average

# --------------------------------------------------
# 5. AI-service evidence
# --------------------------------------------------

cursor.execute("""
SELECT COUNT(*)
FROM events
WHERE process_name = ?
AND remote_ip = ?
AND ai_status = 'YES'
""", (PROCESS, DESTINATION))

ai_events = cursor.fetchone()[0]

ai_detected = ai_events > 0

# --------------------------------------------------
# 6. Unknown hostname evidence
# --------------------------------------------------

cursor.execute("""
SELECT COUNT(*)
FROM events
WHERE process_name = ?
AND remote_ip = ?
AND hostname = 'UNKNOWN'
""", (PROCESS, DESTINATION))

unknown_events = cursor.fetchone()[0]

unknown_hostname = unknown_events > 0

# --------------------------------------------------
# 7. Behavioral assessment
# --------------------------------------------------

deviation_score = 0
indicators = []

if destination_deviation:
    deviation_score += 30
    indicators.append("New destination")

if frequency_deviation:
    deviation_score += 20
    indicators.append("Frequency above baseline")

if ai_detected:
    deviation_score += 30
    indicators.append("AI-service evidence")

if unknown_hostname:
    deviation_score += 10
    indicators.append("Unknown hostname")

if deviation_score > 0:
    deviation_detected = "YES"
else:
    deviation_detected = "NO"

# --------------------------------------------------
# Output
# --------------------------------------------------

print(f"Process:                 {PROCESS}")
print(f"Destination:             {DESTINATION}")
print()

print("Historical Baseline:")
print(f"  Destination Count:     {current_frequency}")
print(f"  Baseline Average:      {baseline_average:.2f}")
print()

print("Behavioral Signals:")
print(f"  Destination Deviation: {'YES' if destination_deviation else 'NO'}")
print(f"  Frequency Deviation:   {'YES' if frequency_deviation else 'NO'}")
print(f"  AI Evidence:           {'YES' if ai_detected else 'NO'}")
print(f"  Unknown Hostname:      {'YES' if unknown_hostname else 'NO'}")
print()

print(f"Deviation Detected:      {deviation_detected}")
print(f"Deviation Score:         {deviation_score}")
print()

if indicators:
    print("Evidence:")
    for indicator in indicators:
        print(f"  [+] {indicator}")
else:
    print("Evidence:")
    print("  No behavioral deviation detected.")

print()
print("-" * 60)

conn.close()
