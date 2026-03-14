# Pipeline Strategy — ABS ECU Test Automation

> **Reference:** CTAL-TAE v2.0 Section 5.1.1
> **Purpose:** Document pipeline design decisions
> **Project:** ABS ECU Automation

---

## Pipeline Architecture Decision

### Build Phase — Runs on Every Commit

| Step | What Runs | Pass Required? |
|------|----------|---------------|
| 1 | Compile ABS ECU software | ✅ Yes |
| 2 | SIL component tests | ✅ Yes |
| 3 | MISRA static analysis | ✅ Yes |
| 4 | TAF configuration tests | ✅ Yes |
| 5 | TAF unit tests | ✅ Yes |

**Execution time target:** Under 15 minutes

---

### Deployment Phase — Runs After Successful Build

| Step | What Runs | Pass Required? |
|------|----------|---------------|
| 1 | Flash ECU firmware to HIL rack | ✅ Yes |
| 2 | HIL rack health check | ✅ Yes |
| 3 | System integration tests (50 cases) | ✅ Yes |
| 4 | CAN signal validation suite | ✅ Yes |
| 5 | Deployment verification smoke tests | ✅ Yes |

**Execution time target:** Under 90 minutes
**Approach:** Approach 1 — tests as quality gate
**On failure:** Automatic rollback to previous release

---

### Nightly Pipeline — Runs at 02:00 Daily

| Step | What Runs | Pass Required? |
|------|----------|---------------|
| 1 | Full ABS regression suite (300 cases) | Report only |
| 2 | All calibration variants (12 × 25 = 300) | Report only |
| 3 | All fault mode combinations | Report only |

**Results available:** 06:00 — before team arrives
**On failure:** Email notification + Jira ticket auto-created

---

### Monthly Pipeline — Runs First Monday of Month

| Step | What Runs |
|------|----------|
| 1 | ABS ECU response time performance tests |
| 2 | CAN bus load stress tests |
| 3 | Memory leak detection (24h soak test) |

---

## Test Level to Pipeline Mapping
```
Every commit:
  SIL component tests     → Build phase
  Config tests for TAF    → Build phase

Every successful build:
  HIL system tests        → Deployment phase
  CAN signal validation   → Deployment phase

Every night:
  Full regression         → Nightly pipeline

Every month:
  Performance tests       → Monthly pipeline
```