#!/bin/bash

BASE="$HOME/Projects/shadow-ai-sentinel"
CORE="$BASE/core"
DB="$BASE/phase3/data/sentinel.db"

STATE="$BASE/phase3/connection_state.txt"
HISTORY="$BASE/phase3/connection_history.txt"

touch "$STATE"
touch "$HISTORY"

while true
do

    echo
    echo "================================================"
    echo "          SHADOW AI SENTINEL"
    echo "================================================"
    echo

    sudo ss -tnp | grep ESTAB | grep -v '127.0.0.1' |
awk '!seen[$5]++' |
while read -r line
do

        remote=$(echo "$line" | awk '{print $5}')

        process_info=$(echo "$line" | grep -o 'users:(.*)' | head -1)

        process=$(echo "$process_info" | grep -o '"[^"]*"' | head -1 | tr -d '"')

        pid=$(echo "$process_info" | grep -o 'pid=[0-9]*' | head -1 | cut -d= -f2)

        if [ -z "$remote" ] || [ -z "$process" ]; then
            continue
        fi

        ip="${remote%:*}"
        remote_port="${remote##*:}"

        hostname=$(nslookup "$ip" 2>/dev/null |
            awk -F'name = ' '/name = / {print $2; exit}' |
            sed 's/\.$//')

        if [ -z "$hostname" ]; then
            hostname="UNKNOWN"
        fi

        detector_output=$("$CORE/detector.sh" "$hostname")

        if echo "$detector_output" | grep -q "\[AI DETECTED\]"; then
            ai_status="YES"
            ai_score="YES"
        else
            ai_status="NO"
            ai_score="NO"
        fi

        if [ "$hostname" = "UNKNOWN" ]; then
            unknown_score="YES"
        else
            unknown_score="NO"
        fi

        now=$(date +%s)

        if ! grep -Fxq "$remote" "$STATE"
        then
            connection_event="NEW"
            echo "$now $remote" >> "$HISTORY"
        else
            connection_event="EXISTING"
        fi

        count=$(awk -v now="$now" -v remote="$remote" \
        '$1 >= now-60 && $2 == remote {count++} END {print count+0}' \
        "$HISTORY")

        if [ "$count" -ge 3 ]; then
            frequent_score="YES"
        else
            frequent_score="NO"
        fi

        risk_output=$("$CORE/risk_engine.sh" \
            "$ai_score" \
            "$unknown_score" \
            "NO" \
            "$frequent_score" \
            "NO")

        risk_score=$(echo "$risk_output" |
            grep "Risk Score:" | awk '{print $3}')

        risk_level=$(echo "$risk_output" |
            grep "Risk Level:" | awk '{print $3}')

        echo "Remote:       $remote"
        echo "Process:      $process"
        echo "PID:          $pid"
        echo "Hostname:     $hostname"
        echo "AI Service:   $ai_status"
        echo "Connection:   $connection_event"
        echo "Frequent:     $frequent_score"
        echo
        echo "Risk Score:   $risk_score"
        echo "Risk Level:   $risk_level"

        echo

        if [ "$connection_event" = "NEW" ]; then

            timestamp=$(date '+%Y-%m-%d %H:%M:%S')

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
    '$process',
    $pid,
    '$ip',
    $remote_port,
    '$hostname',
    '$ai_status',
    '$connection_event',
    '$frequent_score'
);
EOF

        fi

        if [ "$risk_score" -gt 0 ]; then

            echo "================================================"
            echo "          SHADOW AI SECURITY ALERT"
            echo "================================================"

            echo
            echo "Risk Indicators:"
            echo "$risk_output" |
                sed -n '/Risk Indicators:/,$p' |
                tail -n +2

        fi

        echo
        echo "------------------------------------------------"

    done

    sudo ss -tnp | grep ESTAB | grep -v '127.0.0.1' |
    awk '{
        remote=$5
        print remote
    }' |
    sort -u > "$STATE"

    sleep 2

done
