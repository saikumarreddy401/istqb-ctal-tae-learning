# Scenarios — Sub-Chapter 6.1.3 — Test Progress Report Construction

> **Syllabus Reference:** TAE-6.1.3
> **Cognitive Level:** K2 — Understand
> **File:** scenarios_6_1_3_test_progress_report.md
> **Status:** ✅ Complete

---

## Scenario 1 — Mandatory Content Identification (K2)

### Situation

A junior TAE on your team produces the following
test report for the ABS v2.4 release candidate:

---
*ABS Regression Results — Week 12*

Tests run: 409
Passed: 387
Failed: 22

Main failures were in wheel speed signals.
Tests were run on the HIL rack in Stuttgart.
We recommend proceeding with the release.

---

### Question

Identify every mandatory content item that is
missing from this report, and explain the
consequence of each missing item.

### Answer

| Missing Item | Consequence of Absence |
|-------------|----------------------|
| SUT version (ABS v2.4) | Report cannot be linked to specific firmware — unusable for certification |
| Reporting period / date | Cannot determine when testing occurred |
| Test environment identifier | "HIL rack in Stuttgart" is not specific enough — rack ID, config unknown |
| Blocked and error counts | Scope appears complete when it may not be |
| Defects raised | 22 failures with no defect list — no traceability to product issues |
| Requirements coverage | Pass rate without coverage is incomplete for release decision |
| Trend data | Single snapshot — cannot determine if 22 failures is improving or worsening |
| Outstanding risks | Known gaps not communicated to decision-makers |
| Failure detail | "Wheel speed signal" failures — no test IDs, no failure messages |

> ⭐ The report contains a recommendation
> ("proceed with release") but lacks the evidence
> to support it. A recommendation without
> supporting data is an opinion — not a report.

**Minimum acceptable report structure:**

| Section | Must Contain |
|---------|-------------|
| Header | SUT version, test period, environment ID |
| Results summary | Passed, failed, blocked, errors — counts and percentages |
| Defects | New defects raised with severity |
| Coverage | Requirements coverage percentage |
| Trend | Pass rate for last 3-4 runs |
| Risks | Untested areas, blocked items, open critical defects |
| Recommendation | Release readiness with explicit justification |

---

## Scenario 2 — Blocked vs Error vs Failure (K2)

### Situation

Your ABS pipeline produces the following results
after a Monday morning regression run:
```
test_abs_wheel_speed_fl_normal          PASS
test_abs_wheel_speed_fr_normal          PASS
test_abs_fault_injection_can            FAIL  ← assertion failed
test_abs_ecu_reset_sequence             FAIL  ← assertion failed
test_abs_uds_diagnostic_read            ERROR ← CAN interface timeout
test_abs_uds_diagnostic_write           ERROR ← CAN interface timeout
test_abs_calibration_variant_a          SKIP  ← HIL rack not available
test_abs_calibration_variant_b          SKIP  ← HIL rack not available
```

### Question A

How should each result category appear in the
test progress report, and what does each category
communicate to the reader?

### Answer A

| Category | Count | Report Meaning |
|----------|-------|---------------|
| Passed | 2 | Verified — product behaves as specified |
| Failed | 2 | Product defect or test defect — must be investigated |
| Error | 2 | Infrastructure failure — CAN interface issue, not product |
| Blocked/Skipped | 2 | Scope gap — HIL rack unavailable, these requirements untested |

**Report summary table:**

| Result | Count | Percentage | Action |
|--------|-------|-----------|--------|
| Passed | 2 | 25% | None |
| Failed | 2 | 25% | Defect investigation |
| Error | 2 | 25% | Infrastructure investigation |
| Blocked | 2 | 25% | Rerun when rack available |
| **Total** | **8** | **100%** | |

### Question B

Should errors be included in the pass rate
calculation? Justify your answer.

### Answer B

> ⭐ **No. Errors must not be included in pass
> rate calculation.**
>
> Pass rate = Passed / (Passed + Failed)
> = 2 / (2 + 2) = 50%
>
> If errors are included in the denominator:
> Pass rate = 2 / 8 = 25%
>
> Including errors understates the pass rate and
> incorrectly penalises the product for an
> infrastructure failure. The product did not
> fail — the test environment failed.
>
> Errors must be reported separately with their
> own investigation action. They are a pipeline
> health metric — not a product quality metric.

---

## Scenario 3 — Audience-Specific Report Design (K2)

### Situation

The ABS v2.4 release candidate produces this data:

- Pass rate: 94.6% (threshold: 95%)
- Failed: 18 tests
- Blocked: 4 tests (HIL rack Rack-3 offline)
- Safety requirements coverage: 88% (target: 90%)
- New defects raised: 12 (2 critical, 7 major, 3 minor)
- Open critical defects: 2
- Flaky tests quarantined: 6
- Execution time: 118 minutes
- Trend: declining from 97% over 4 weeks

Three people request reports:
- **Person A:** Release manager making go/no-go decision
- **Person B:** Developer assigned to fix failures
- **Person C:** ISO 26262 safety auditor

### Question

For each person, specify the report structure and
the single most important message they need.

### Answer

**Person A — Release Manager:**

| Section | Content |
|---------|---------|
| Executive summary | Pass rate 94.6% — 0.4% below 95% threshold |
| Critical blockers | 2 critical open defects — release blocked |
| Coverage risk | Safety requirements at 88% — below 90% target |
| Trend | Declining from 97% over 4 weeks — not yet stable |
| Blocked scope | 4 tests blocked — Rack-3 offline — scope gap |
| **Recommendation** | **Do not release. Resolve 2 critical defects. Rerun Rack-3 tests.** |

> Most important message: Do not release — and here
> are exactly two conditions that must be met first.

**Person B — Developer:**

| Section | Content |
|---------|---------|
| Failing test list | 18 test IDs with full failure messages |
| Signal traces | CAN trace links per failure for diagnosis |
| Failure cluster | 14 of 18 failures involve WheelSpeedFL |
| Defect tickets | 12 defect IDs — 2 critical assigned to developer |
| Flaky tests | 6 quarantined — root cause investigation needed |

> Most important message: 14 failures cluster on
> WheelSpeedFL — investigate this signal first.

**Person C — Safety Auditor:**

| Section | Content |
|---------|---------|
| Safety requirements coverage | 88% — 12 requirements without test coverage listed |
| Traceability matrix | Safety req ID → test case ID → result → timestamp |
| Critical defects | 2 open critical defects with ASIL classification |
| Test environment evidence | ECU serial, firmware version, rack configuration per run |
| Retention confirmation | Results stored in Polarion — 10-year retention |
| Deviation report | 4 tests blocked — reason documented, retest planned |

> Most important message: 88% safety coverage with
> 2 open critical defects — certification cannot
> proceed until both are resolved.

---

## Scenario 4 — Report Frequency Strategy (K2)

### Situation

Your team currently generates one test report per
week — produced manually every Friday. Problems
reported by the team:

- Developers do not know their commit broke tests
  until Friday — 4 days after the commit
- The test manager cannot make a release decision
  mid-week because there is no current data
- The safety auditor requires a report for every
  deployment to the integration environment

### Question

Design a report frequency strategy with a different
report type for each trigger, and specify who
receives each report.

### Answer

> ⭐ Report frequency must match the decision
> frequency of the audience — not the convenience
> of the TAE producing it.

| Report Type | Trigger | Audience | Content |
|------------|---------|---------|---------|
| Per-commit report | Every pipeline run | Developer who committed | Pass/fail for affected tests only, failure messages, link to logs |
| Nightly summary | Nightly regression completion | Test manager, team lead | Pass rate, new failures since yesterday, trend update |
| Integration deployment report | Every deployment to integration | Safety auditor (archive), test manager | Full results, environment config, SUT version, traceability |
| Weekly trend report | Friday automated generation | Project manager, management | 7-day trend, coverage status, open defect count |
| Release report | Pre-release trigger | All stakeholders | Full mandatory content per ISO 26262 |

**Automation implementation:**
```yaml
# Trigger-based report generation in pipeline
on:
  push:
    branches: [feature/*, bugfix/*]
  schedule:
    - cron: '0 22 * * *'        # Nightly at 22:00
  workflow_dispatch:             # Manual release trigger

jobs:
  per_commit_report:
    if: github.event_name == 'push'
    steps:
      - run: python generate_report.py --type=commit
        # Lightweight — failing tests only

  nightly_report:
    if: github.event_name == 'schedule'
    steps:
      - run: python generate_report.py --type=nightly
        # Full suite summary + trend update

  release_report:
    if: github.event_name == 'workflow_dispatch'
    steps:
      - run: python generate_report.py --type=release
        # Full mandatory content + push to Polarion
```

---

## Scenario 5 — Recommendation Construction (K2)

### Situation

You are the TAE for the ABS v2.4 release.
Final regression results:

- Pass rate: 96.2% (threshold: 95%) ✅
- Safety requirements coverage: 92% (target: 90%) ✅
- Open critical defects: 0 ✅
- Flaky tests quarantined: 3 (rate: 0.7%) ✅
- Execution time: 112 minutes (limit: 120 min) ✅
- Blocked tests: 2 — reason: non-safety, low-risk tests
- Pass rate trend: stable at 96–97% for last 4 runs ✅

### Question

Construct the recommendation section of the
release report. Include the evidence basis,
any conditional items, and your explicit verdict.

### Answer
```
RELEASE RECOMMENDATION — ABS SW v2.4

Verdict: APPROVED FOR RELEASE — with one condition

Evidence basis:
─────────────────────────────────────────────────
Pass rate:              96.2%   ✅  (threshold 95%)
Safety req coverage:    92%     ✅  (target 90%)
Critical open defects:  0       ✅
Flaky test rate:        0.7%    ✅  (limit 2%)
Execution time:         112 min ✅  (limit 120 min)
Pass rate trend:        Stable  ✅  (4-run window)
─────────────────────────────────────────────────

Condition before release:
2 blocked tests must be reviewed and explicitly
accepted as known scope gaps by the test manager.
Both are non-safety, low-risk scenarios.
If accepted: release approved unconditionally.
If not accepted: rerun on available HIL rack.

Signed: TAE — Sai Kumar Reddy
Date: [release date]
Environment: HIL Rack-1, ABS SW v2.4, ECU SN-20847
```

> ⭐ A recommendation section has three components:
> 1. Explicit verdict — not implied
> 2. Evidence basis — metrics with thresholds
> 3. Conditions — what must happen before release
>
> A report that presents all the data but omits
> the verdict forces the reader to interpret the
> data themselves. The TAE's professional judgment
> is the most valuable output of the report.

---

## Quick Reference — Report Mandatory Sections

| Section | Must Contain | Common Omission |
|---------|-------------|----------------|
| Header | SUT version, period, environment | SUT version missing |
| Results | Passed, failed, blocked, errors | Blocked/errors omitted |
| Defects | New defects, open critical | No defect list despite failures |
| Coverage | Requirements coverage % | Coverage omitted entirely |
| Trend | Last N run pass rates | Single snapshot only |
| Risks | Untested areas, open defects | Risk section omitted |
| Recommendation | Explicit verdict + conditions | Data without conclusion |

---

## Blocked vs Error vs Failure — Exam Summary

| Category | Cause | Included in Pass Rate? | Action |
|----------|-------|----------------------|--------|
| Failed | Product or test defect | Yes — in denominator | Defect investigation |
| Error | Infrastructure failure | No — reported separately | Pipeline investigation |
| Blocked | Dependency unavailable | No — reported as scope gap | Rerun when available |
| Flaky | Inconsistent without change | No — quarantined | Root cause investigation |

---

*Next: Chapter 7 — Verifying the Test Automation Solution*