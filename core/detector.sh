#!/bin/bash

domain="$1"
AI_SERVICES="$HOME/Projects/shadow-ai-sentinel/core/ai_services.txt"

if grep -Fxqi "$domain" "$AI_SERVICES"; then
    echo "[AI DETECTED] $domain"
else
    echo "[UNKNOWN] $domain"
fi
