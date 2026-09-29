#!/bin/bash

DB="$HOME/Projects/shadow-ai-sentinel/phase3/data/sentinel.db"

timestamp=$(date '+%Y-%m-%d %H:%M:%S')
process_name="telemetry_test"
pid=$$
remote_ip="192.0.2.1"
remote_port=443
hostname="test.example"
ai_status="NO"
connection_event="TEST"
frequency="NO"

sqlite3 "$DB" <<EOF
INSERT INTO events (
    timestamp,
    process_name,
    pid,
    remote_ip,
    remote_port,
    hostname,
    ai_status,
    connection_event,
    frequency
)
VALUES (
    '$timestamp',
    '$process_name',
    $pid,
    '$remote_ip',
    $remote_port,
    '$hostname',
    '$ai_status',
    '$connection_event',
    '$frequency'
);
EOF

echo "Test telemetry event stored successfully."
