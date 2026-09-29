



#!/bin/bash

ai_detected="$1"
unknown_service="$2"
suspicious_process="$3"
frequent_connection="$4"
sensitive_data="$5"

score=0

if [ "$ai_detected" = "YES" ]; then
    score=$((score + 30))
fi

if [ "$unknown_service" = "YES" ]; then
    score=$((score + 20))
fi

if [ "$suspicious_process" = "YES" ]; then
    score=$((score + 20))
fi

if [ "$frequent_connection" = "YES" ]; then
    score=$((score + 10))
fi

if [ "$sensitive_data" = "YES" ]; then
    score=$((score + 20))
fi

echo "Risk Score: $score"

if [ "$score" -le 20 ]; then
    risk_level="LOW"
elif [ "$score" -le 40 ]; then
    risk_level="MEDIUM"
elif [ "$score" -le 70 ]; then
    risk_level="HIGH"
else
    risk_level="CRITICAL"
fi

echo "Risk Level: $risk_level"

echo
echo "Risk Indicators:"

if [ "$ai_detected" = "YES" ]; then
    echo "[+] AI Service Detected       +30"
fi

if [ "$unknown_service" = "YES" ]; then
    echo "[+] Unknown Service            +20"
fi

if [ "$suspicious_process" = "YES" ]; then
    echo "[+] Suspicious Process         +20"
fi

if [ "$frequent_connection" = "YES" ]; then
    echo "[+] Frequent Connection         +10"
fi

if [ "$sensitive_data" = "YES" ]; then
    echo "[+] Sensitive Data              +20"
fi
