# Scenarios — Sub-Chapter 6.1.1 — Data Collection Methods

> **Syllabus Reference:** TAE-6.1.1
> **Cognitive Level:** K3 — Apply
> **File:** scenarios_6_1_1_data_collection.md
> **Status:** ✅ Complete

---

## Scenario 1 — Missing Pre-Execution Data (K3)

### Situation

A Bosch ABS TAE runs the full regression suite on
Monday morning. All 409 tests pass. On Wednesday,
the calibration engineer reports that the HIL rack
was running ABS firmware v2.3 — not the v2.4 that
was supposed to be under test. The v2.4 deployment
script had failed silently on Friday.

The test report shows 100% pass rate but cannot
be used for v2.4 certification because there is
no proof of which firmware was actually tested.

### Question

Which pre-execution data collection item was missing,
and how do you implement it in the TAF to prevent
this in future?

### Answer

> ⭐ The missing item is **SUT version recorded
> at pre-test setup time** — before the first
> test case executes.

**Implementation — UDS version query before test run:**
```python
def collect_pre_execution_metadata(
    uds_client, environment_config: dict
) -> dict:
    """
    Query ECU for firmware version before test execution.
    Fails the entire run if version does not match expected.
    """
    ecu_version = uds_client.read_data_by_identifier(
        did=0xF189  # ECU software version DID
    )

    metadata = {
        "sut_version": ecu_version.decode("ascii"),
        "expected_version": environment_config["expected_sut_version"],
        "hil_rack_id": environment_config["rack_id"],
        "collection_timestamp": datetime.utcnow().isoformat()
    }

    # Hard stop if version mismatch
    if metadata["sut_version"] != metadata["expected_version"]:
        raise EnvironmentError(
            f"SUT version mismatch: "
            f"expected {metadata['expected_version']}, "
            f"found {metadata['sut_version']}. "
            f"Aborting test run."
        )

    return metadata
```

> This does two things: records the version as
> evidence, and aborts the run if the wrong
> firmware is present. Silent version mismatches
> are eliminated entirely.

---

## Scenario 2 — Choosing the Right Collection Method (K3)

### Situation

Your ESP test suite currently collects only JUnit
XML pass/fail results via pytest. Three problems
have emerged:

1. Intermittent failures occur on HIL Rack 2 but
   not Rack 1 — impossible to diagnose without
   knowing which rack produced each result
2. A failure last Tuesday cannot be reproduced —
   the CAN signal values at the time of failure
   were never captured
3. Management wants a trend dashboard showing
   pass rate per SW version over the past quarter

### Question

For each problem, identify which data collection
method is missing and what it should collect.

### Answer

| Problem | Missing Collection Method | What to Collect |
|---------|--------------------------|----------------|
| Rack-specific failures | Pre-execution environment metadata | Rack ID, CAN interface name, IP address per test run |
| Cannot reproduce failure | During-execution signal logging on failure | CAN signal trace captured as artifact when test fails |
| No trend dashboard | Time-series metrics collection | Pass rate + SW version pushed to InfluxDB per run |

**Signal capture on failure — implementation:**
```python
@pytest.fixture(autouse=True)
def capture_signals_on_failure(request, can_monitor):
    """Automatically save CAN signal trace if test fails."""
    yield  # Test runs here

    if request.node.rep_call.failed:
        trace_path = f"logs/{request.node.name}_signal_trace.csv"
        can_monitor.save_trace(trace_path)
        pytest.attach(trace_path, name="CAN Signal Trace")
```

> Each problem maps to a different collection timing:
> Problem 1 = before execution,
> Problem 2 = during execution,
> Problem 3 = after execution pushed to storage.

---

## Scenario 3 — Compliance Data Collection (K3)

### Situation

Your ABS team is preparing for ISO 26262 ASIL-B
certification. The safety auditor's checklist
requires the following to be present in every
test execution record:

- ECU serial number (not just firmware version)
- Test environment configuration at execution time
- Tester identification (who triggered the run)
- Retention proof (results stored ≥ 5 years)
- Test case ID linked to safety requirement ID

Your current pipeline stores JUnit XML in GitHub
Actions artifacts with 90-day retention.

### Question

Identify every gap between your current collection
and the auditor's requirements, and specify what
you add to close each gap.

### Answer

| Auditor Requirement | Current State | Gap | Solution |
|--------------------|--------------|-----|---------|
| ECU serial number | Not collected | Missing entirely | Add UDS DID 0xF18C query to pre-test metadata |
| Environment config at execution time | Config files in repo | Not captured per run | Snapshot config file content into test metadata |
| Tester identification | Not collected | Missing | Record `CI_PIPELINE_TRIGGERED_BY` or Git commit author |
| Retention ≥ 5 years | 90-day GitHub artifact | Fails requirement | Push results to Polarion or long-term S3 storage |
| Test case → requirement traceability | Not in JUnit XML | Missing | Add requirement ID as test case tag, export to TMS |

> ⭐ Pipeline artifact retention is almost never
> sufficient for automotive certification.
> Results must be pushed to a persistent test
> management system — Polarion, ALM, or equivalent —
> with retention matching the product lifetime.

---

## Scenario 4 — Data Volume vs Diagnostic Value (K3)

### Situation

A TAE proposes collecting CAN signal traces for
every test case in every pipeline run. The suite
has 800 test cases. Each trace is approximately
2MB. The pipeline runs 3 times per day.

Storage calculation: 800 × 2MB × 3 runs × 365 days
= approximately 1.75TB per year.

The infrastructure team says this is unsustainable.

### Question

Design a selective data collection strategy that
preserves diagnostic value while reducing storage
to an acceptable level.

### Answer

> ⭐ Collect traces selectively based on result
> and risk — not uniformly for all tests.

**Selective collection strategy:**

| Condition | Action | Rationale |
|-----------|--------|-----------|
| Test passes, low risk | No trace collected | Pass with no anomaly needs no evidence |
| Test passes, safety-critical | Collect abbreviated trace (key signals only) | Compliance evidence required |
| Test fails | Full trace collected | Diagnosis requires complete signal history |
| Test flaky (failed in last 5 runs ≥ 2 times) | Full trace on every run | Intermittent failure needs pattern data |
| Nightly regression, any result | Full trace for subset of tests (smoke suite) | Baseline evidence per night |

**Storage estimate with selective strategy:**

| Category | Count | Frequency | Size | Annual Storage |
|---------|-------|----------|------|---------------|
| Failures (est. 5%) | 40 tests | 3×/day | 2MB | ~87GB |
| Safety-critical passes | 50 tests | 1×/day (nightly) | 0.5MB | ~9GB |
| Flaky tests | 20 tests | 3×/day | 2MB | ~44GB |
| **Total** | | | | **~140GB** |

> Reduction from 1.75TB to ~140GB — 92% reduction —
> with no loss of diagnostic or compliance value.

---

## Scenario 5 — Environment Data Gap (K3)

### Situation

The ABS regression suite produces inconsistent
results across three HIL racks. The pass rate is
97% on Rack 1, 94% on Rack 2, and 89% on Rack 3.
All racks run the same firmware and the same tests.

The test manager asks: "Which rack should we trust
for the release decision?"

The team cannot answer because no environment
data was collected alongside the test results.

### Question

Define exactly which environment data should have
been collected, and explain how it would enable
the team to answer the test manager's question.

### Answer

> ⭐ Environment data collection enables correlation
> between results and infrastructure — which is
> impossible with execution data alone.

**Environment data that should be collected per run:**

| Data Item | How Collected | What It Reveals |
|-----------|--------------|----------------|
| Rack ID | Pre-test config | Which rack produced each result |
| CAN interface hardware version | UDS query or config | Interface firmware differences |
| ECU serial number | UDS DID 0xF18C | Different ECU units may behave differently |
| HIL rack OS and tool versions | Pre-test system query | Software environment differences |
| CAN bus load at test time | CANalyzer measurement | Bus congestion causing timeouts |
| Last rack maintenance date | Maintenance log | Hardware degradation indicator |

**With this data, the analysis becomes possible:**

| Finding | Action |
|---------|--------|
| Rack 3 has older CAN interface firmware | Update interface firmware, rerun |
| Rack 3 ECU is different serial than Rack 1 and 2 | Replace with matched unit |
| Rack 3 shows higher CAN bus load | Investigate bus load source |
| All racks identical — results still differ | Test has timing dependency — fix test |

> Without environment data, all four hypotheses
> remain open and the team cannot make a decision.
> With it, each hypothesis is testable.

---

## Quick Reference — Collection Timing Summary

| Timing | What to Collect | Why |
|--------|----------------|-----|
| Before execution | SUT version, ECU serial, rack ID, config snapshot | Reproducibility, compliance |
| During execution | Signal traces on failure, intermediate state logs | Diagnosis |
| After execution | JUnit XML, duration, coverage, metrics push | Reporting, trend analysis |

---

*Next: Scenarios 6.1.2 — Data Analysis*