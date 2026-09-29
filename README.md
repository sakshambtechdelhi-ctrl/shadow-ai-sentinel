# Shadow AI Sentinel

A Bash-based network monitoring and behavioral detection system designed to identify potentially interesting or unexpected connections made by local processes, including connections to known AI services.

## Overview

Shadow AI Sentinel monitors established network connections and collects information such as:

* Remote IP address and port
* Local process name
* Process ID (PID)
* Reverse-DNS hostname
* AI-service classification
* New/existing connection status
* Connection frequency
* Risk score and risk level

The project combines **network telemetry, service identification, historical connection data, behavioral analysis, and risk scoring**.

The goal is not to declare that a connection is malicious solely from one indicator. Instead, the system provides additional behavioral evidence that can be investigated.

---

## Architecture

```text
Network Connections
        |
        v
     ss -tnp
        |
        v
Process / PID / Remote IP
        |
        v
    Reverse DNS
        |
        +------------------+
        |                  |
        v                  v
 AI Service Detection   Behavioral Analysis
        |                  |
        |             +----+----+
        |             |         |
        |          New Dest.  Frequency
        |             |         |
        +-------------+---------+
                      |
                      v
                 Risk Engine
                      |
                      v
              Risk Score / Level
                      |
                      v
                Security Alert
```

---

## Project Structure

```text
shadow-ai-sentinel/
│
├── core/
│   ├── ai_services.txt
│   ├── detector.sh
│   ├── risk_engine.sh
│   └── sentinel.sh
│
└── phase3/
    ├── behavior_analyzer.py
    ├── deviation_engine.py
    ├── phase3_detection_validation.py
    ├── phase3_validation.py
    ├── test_behavior_engine.py
    ├── test_deviation.py
    ├── validate_behavior.py
    └── validate_deviation.py
```

Runtime files, databases, Python bytecode, and backup files are excluded from version control.

---

## Core Components

### `sentinel.sh`

The main monitoring script.

It:

1. Reads established TCP connections using `ss`.
2. Excludes loopback traffic.
3. Extracts the remote endpoint.
4. Identifies the associated process and PID.
5. Performs reverse-DNS lookup.
6. Checks the hostname against the AI-service list.
7. Tracks new and existing connections.
8. Calculates short-term connection frequency.
9. Sends detection signals to the risk engine.
10. Stores new connection telemetry in SQLite.
11. Displays a security alert when the calculated risk score is greater than zero.

### `detector.sh`

Performs simple AI-service identification by comparing a resolved hostname against:

```text
core/ai_services.txt
```

A matching hostname produces:

```text
[AI DETECTED]
```

Otherwise:

```text
[UNKNOWN]
```

This is a **list-based classification mechanism**, not machine-learning-based detection.

### `risk_engine.sh`

Combines several indicators into a weighted risk score.

Current scoring:

| Indicator           | Points |
| ------------------- | -----: |
| AI service detected |    +30 |
| Unknown service     |    +20 |
| Suspicious process  |    +20 |
| Frequent connection |    +10 |
| Sensitive data      |    +20 |

Risk levels:

| Score | Level    |
| ----: | -------- |
|  0–20 | LOW      |
| 21–40 | MEDIUM   |
| 41–70 | HIGH     |
|   71+ | CRITICAL |

The current live monitoring pipeline actively supplies AI-service, unknown-service, and frequency indicators. Suspicious-process and sensitive-data inputs are currently reserved for future integration.

---

# Phase 3 — Behavioral Detection

Phase 3 extends the project beyond static service identification.

The behavioral system compares current connection activity with historical information and detects signals such as:

### 1. New destination

A destination that does not appear in the historical baseline can be identified as a novel connection.

### 2. Frequency deviation

The system compares current connection frequency against a historical average.

Example validation:

```text
Current Frequency: 5
Historical Average: 1.56

5 > 1.56
```

This produces a frequency-deviation signal.

### 3. Unknown hostname

A destination for which reverse DNS does not provide a hostname can contribute an additional behavioral signal.

### 4. Combined behavioral signals

Multiple signals can be considered together rather than relying on a single indicator.

---

# Phase 3 Validation

The behavioral engine was tested using three scenarios:

| Test                                    | Result |
| --------------------------------------- | ------ |
| Known destination + frequency deviation | PASS   |
| New destination                         | PASS   |
| High frequency + unknown hostname       | PASS   |

Validation result:

```text
Passed: 3
Failed: 0

ALL BEHAVIORAL TESTS PASSED
```

The overall Phase 3 validation also passed four tests:

| Test                   | Result |
| ---------------------- | ------ |
| Known destination      | PASS   |
| Destination novelty    | PASS   |
| Frequency deviation    | PASS   |
| Telemetry completeness | PASS   |

Telemetry validation recorded:

```text
Complete events: 14
Total events:    14
```

Additional database validation recorded:

```text
Process:       x-www-browser
Events:        14
Destinations:  9
```

---

## Example Behavioral Validation

### Known destination

```text
Destination: 34.107.243.93
Observed:    2
Expected:    > 0

PASS
```

### Destination novelty

A test destination was absent from the historical baseline:

```text
Destination: 203.0.113.50
Observed:    0
Expected:    0

PASS
```

### Frequency deviation

```text
Destination: 151.101.105.91
Frequency:   5
Average:     1.56

Expected: Frequency > Average

PASS
```

---

## Technologies Used

* Bash
* Python
* Linux
* `ss`
* `awk`
* `grep`
* `nslookup`
* SQLite
* TCP networking
* Reverse DNS
* Process/PID inspection
* Behavioral baseline analysis

The project was developed and tested in a Linux/Kali environment.

---

## Running the Project

Clone the repository and enter the project directory:

```bash
cd shadow-ai-sentinel
```

Make the shell scripts executable:

```bash
chmod +x core/*.sh
```

Run the main monitor:

```bash
./core/sentinel.sh
```

The monitoring process requires appropriate privileges for process-aware socket inspection.

---

## Phase 3 Validation Commands

Behavior engine validation:

```bash
cd phase3
python3 test_behavior_engine.py
```

Overall Phase 3 validation:

```bash
python3 phase3_validation.py
```

---

## Limitations

Shadow AI Sentinel is a **monitoring and behavioral-analysis project**, not a complete enterprise security product.

Current limitations include:

* AI-service detection depends on the maintained hostname list.
* Reverse DNS is not always available.
* An unknown hostname does not necessarily indicate malicious activity.
* High connection frequency does not by itself prove malicious behavior.
* Current process and sensitive-data risk inputs are placeholders for future integration.
* The system currently focuses on established TCP connections.
* Risk scores are heuristic and should be interpreted as indicators rather than definitive classifications.
* IPv6 and additional protocol coverage can be expanded further.

---

## Future Improvements

Potential future development includes:

* Expanded AI-service intelligence
* More robust destination reputation analysis
* Improved behavioral baselines
* Time-based behavioral profiling
* Process-specific baselines
* IPv6-focused analysis
* Additional protocol monitoring
* Configurable risk weights
* Alert logging
* Visualization/dashboard support
* More extensive false-positive testing

---

## Project Goal

Shadow AI Sentinel was developed as a practical cybersecurity project to explore how **Linux networking, process monitoring, Bash scripting, DNS analysis, SQLite, and behavioral detection** can be combined into a single security-monitoring workflow.

The project emphasizes practical telemetry collection and explainable detection signals rather than treating a single network indicator as proof of malicious activity.

---

## Status

**Phase 3 behavioral detection: COMPLETE**

Validation status:

```text
Behavior Engine:       3/3 PASS
Phase 3 Validation:    4/4 PASS
Telemetry Completeness: 14/14 PASS
```
