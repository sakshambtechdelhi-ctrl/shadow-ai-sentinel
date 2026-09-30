# Shadow AI Sentinel — Live Demonstration

## Objective

Demonstrate that Shadow AI Sentinel can monitor active network connections,
identify the associated process and PID, perform reverse DNS analysis,
track connection state, and generate explainable risk alerts.

## Environment

- Operating System: Kali Linux
- Shell: Bash
- Network Monitor: `ss`
- DNS Analysis: `nslookup`
- Database: SQLite
- Browser Process: `x-www-browser`

## Demonstration 1 — Normal Connection

Example:

```text
Remote:       34.149.226.178:443
Process:      x-www-browser
PID:          17856
Hostname:     178.226.149.34.bc.googleusercontent.com
AI Service:   NO
Connection:   NEW
Frequent:     NO

Risk Score:   0
Risk Level:  LOW
 

## Demonstration 2 — Unknown Service Detection

Example:

```text
Remote:       151.101.1.91:443
Process:      x-www-browser
PID:          17856
Hostname:     UNKNOWN
AI Service:   NO
Connection:   NEW
Frequent:     NO

Risk Score:   20
Risk Level:   LOW

```text
SHADOW AI SECURITY ALERT

Risk Indicators:
[+] Unknown Service +20
```

This demonstrates explainable risk scoring when reverse DNS information is unavailable.

`UNKNOWN` does not mean that the destination is malicious. It means that the Sentinel could not obtain a reverse-DNS hostname for the destination.


## Demonstration 3 — Connection State Tracking

The same destination was observed as:

```text
Connection: NEW

```

and during later monitoring:

```text
Connection: EXISTING

## Observed Detection Pipeline

```text
Network Connection
        ↓
Remote IP / Port
        ↓
Process + PID
        ↓
Reverse DNS
        ↓
AI-Service Classification
        ↓
Behavioral / Frequency Analysis
        ↓
Risk Engine
        ↓
Risk Score + Risk Level
        ↓
Security Alert

```

## Important Interpretation

Shadow AI Sentinel uses explainable heuristic detection.

An unknown hostname or elevated connection frequency is treated as a risk signal, not proof of malicious activity.

AI-service detection is list-based and does not use a machine-learning model.

## Result

The live demonstration successfully showed:

- Network connection monitoring
- Process and PID identification
- Reverse DNS analysis
- AI-service classification
- New/existing connection tracking
- Explainable risk scoring
- Security alert generation


