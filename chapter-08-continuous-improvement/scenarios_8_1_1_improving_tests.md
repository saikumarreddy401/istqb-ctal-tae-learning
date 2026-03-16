# Scenarios — Sub-Chapter 8.1.1 — Improving Tests in the TAS

> **Syllabus Reference:** TAE-8.1.1
> **Cognitive Level:** K4 — Analyze
> **File:** scenarios_8_1_1_improving_tests.md
> **Status:** ✅ Complete

---

## Scenario 1 — Declining Defect Detection Rate (K4)

### Situation

Your ABS test suite metrics over the past year:

| Quarter | Tests | Pass Rate | Defects Found |
|---------|-------|----------|--------------|
| Q1 | 280 | 94% | 18 |
| Q2 | 320 | 95% | 14 |
| Q3 | 380 | 96% | 8 |
| Q4 | 420 | 97% | 3 |

The product is actively developed — two major
SW releases per quarter. No reduction in
development defect injection rate is expected.

### Question

Evaluate what this data pattern indicates and
recommend the highest-impact improvement action.

### Answer

> ⭐ **Pattern: Growing suite with rising pass rate
> but falling defect detection.**
>
> This is the most dangerous pattern in test
> automation. It looks like improving quality —
> but it indicates the suite is losing alignment
> with the product it tests.

**Analysis:**

| Observation | Interpretation |
|-------------|---------------|
| Test count growing Q1→Q4 | Tests being added |
| Pass rate rising | New tests likely testing already-correct behavior |
| Defect detection falling sharply | New tests not covering new functionality or defect-prone areas |
| Active development unchanged | Defects are being introduced — just not found by automation |

> ⭐ The suite is growing in volume but shrinking
> in effectiveness. New tests are being added to
> areas that are already working correctly —
> not to new features or high-risk areas.

**Root cause investigation:**

| Question | Check |
|----------|-------|
| Are new tests linked to new requirements? | Requirements coverage matrix — new Q3/Q4 requirements |
| Are new tests in new feature areas? | Compare new test file names to SW release notes |
| Are manual tests finding defects automation misses? | Compare manual defect list to automated test coverage |

**Highest-impact improvement action:**

> 1. Pull SW release notes for Q3 and Q4
> 2. Identify all new features and changed components
> 3. Map these to test coverage — find the gaps
> 4. Add tests specifically targeting new functionality
>    and components with recent changes
>
> Do NOT add more tests to already-covered areas.
> Quantity without targeting reduces ROI.
> Every new test must be justified by a coverage
> gap in a defect-prone or recently changed area.

---

## Scenario 2 — Flaky Test Improvement (K4)

### Situation

Your ESP suite has 500 tests. Flaky test analysis
over 4 weeks shows:

| Test | W1 | W2 | W3 | W4 | Pattern |
|------|----|----|----|----|---------|
| test_esp_yaw_correction | ✅ | ❌ | ✅ | ❌ | Alternating |
| test_esp_stability_130kmh | ✅ | ✅ | ❌ | ✅ | Rare fail |
| test_esp_dtc_after_reset | ❌ | ✅ | ❌ | ✅ | Alternating |
| test_esp_calibration_eu | ✅ | ❌ | ✅ | ✅ | Rare fail |
| test_esp_calibration_us | ✅ | ✅ | ✅ | ❌ | Rare fail |

Flaky rate: 5/500 = 1.0% — below 2% threshold.
The test manager says: "Under threshold — no action needed."

### Question

Evaluate the test manager's position and recommend
whether action is required. Justify with analysis
of the specific flaky patterns.

### Answer

> ⭐ The test manager's position is **partially
> correct but incomplete.**
>
> 1.0% is below the 2% blocking threshold — true.
> But two of five flaky tests show an alternating
> pattern (fail every other run) which is not
> random noise — it is a systematic defect.

**Pattern analysis:**

| Test | Pattern | Root Cause Hypothesis |
|------|---------|----------------------|
| test_esp_yaw_correction | Alternating W1-W4 | Shared state — previous test leaves ESP in state A or B alternately |
| test_esp_dtc_after_reset | Alternating W1-W4 | Same — DTC not fully cleared before alternate runs |
| test_esp_stability_130kmh | Rare fail | Timing dependency — ECU occasionally slow |
| test_esp_calibration_eu/us | Rare fail | CAN bus load variation causing read timeout |

**Recommendation:**

> The alternating pattern tests (yaw_correction and
> dtc_after_reset) must be investigated immediately —
> regardless of the aggregate flaky rate.
> An alternating pattern is not random — it indicates
> a deterministic shared state defect.
>
> The rare-fail tests can be monitored for one more
> week. If they fail again, investigate timing.
>
> The test manager's threshold argument is valid for
> random flakiness. It does not apply to systematic
> alternating patterns which have a known, fixable
> root cause.

**Fix for alternating pattern:**
```python
# Root cause: test_esp_dtc_after_reset leaves DTC active
# Next run: test_esp_yaw_correction finds unexpected DTC
# Alternates because DTC cleared on even runs by coincidence

# Fix: autouse fixture ensures clean state every run
@pytest.fixture(autouse=True)
def clean_esp_state(uds_client):
    uds_client.clear_diagnostic_information(group=0xFFFFFF)
    uds_client.diagnostic_session_control(0x01)
    yield
    uds_client.clear_diagnostic_information(group=0xFFFFFF)
```

---

## Scenario 3 — Assertion Density Improvement (K4)

### Situation

Assertion density analysis on your ABS test suite:

| Test File | Tests | Avg Assertions | Min Assertions |
|-----------|-------|---------------|---------------|
| test_abs_wheel_speed.py | 24 | 3.2 | 1 |
| test_abs_activation.py | 18 | 1.1 | 1 |
| test_abs_fault_injection.py | 22 | 4.1 | 2 |
| test_abs_uds_session.py | 16 | 1.0 | 1 |
| test_abs_calibration.py | 14 | 2.8 | 1 |

`test_abs_activation.py` and `test_abs_uds_session.py`
have average assertion density of 1.0 and 1.1 —
one assertion per test.

### Question

Evaluate which file poses the highest false
negative risk and demonstrate how to strengthen
one specific test from that file.

### Answer

> ⭐ **`test_abs_uds_session.py` poses the highest
> risk.** Average 1.0 means every test has exactly
> one assertion. Combined with a UDS session
> management context — where the product behavior
> is complex — one assertion cannot adequately
> verify the behavior.

**Typical single-assertion UDS session test:**
```python
# CURRENT — 1 assertion, checks session entered
def test_extended_session_entry():
    response = uds_client.diagnostic_session_control(0x03)
    assert response.positive  # Only checks: did ECU respond?
```

**False negative risk:** ECU enters extended session
but with wrong session ID, wrong timeout, or wrong
security level — all undetected.

**Strengthened version:**
```python
# IMPROVED — 5 assertions, checks specific behaviors
def test_extended_session_entry():
    """
    Verify ECU correctly enters UDS extended session.
    Checks response code, session type confirmation,
    timing parameters, and security level.
    """
    response = uds_client.diagnostic_session_control(
        session_type=0x03  # Extended diagnostic session
    )

    # 1. Positive response received
    assert response.service_id == 0x50, (
        f"Expected 0x50 (positive), got {hex(response.service_id)}"
    )

    # 2. Correct session type echoed back
    assert response.session_type == 0x03, (
        f"ECU confirmed session {hex(response.session_type)}, "
        f"expected 0x03 (extended)"
    )

    # 3. P2 server max timing within spec (50ms)
    assert response.p2_server_max_ms <= 50, (
        f"P2 server max {response.p2_server_max_ms}ms exceeds 50ms"
    )

    # 4. ECU reports extended session active
    current = uds_client.read_current_session()
    assert current == 0x03

    # 5. Default session services no longer available
    with pytest.raises(NegativeResponseError) as exc:
        uds_client.ecu_reset(reset_type=0x01)
    assert exc.value.nrc == 0x7E  # serviceNotSupportedInActiveSession
```

---

## Scenario 4 — Coverage Gap Prioritisation (K4)

### Situation

Requirement coverage analysis for ABS SW v2.5:

| Requirement | ASIL | Tests | Last Defect |
|-------------|------|-------|------------|
| ABS-REQ-047 ABS deactivates < 5 km/h | B | 3 | Never |
| ABS-REQ-048 ABS off on ignition off | B | 0 | — |
| ABS-REQ-049 Warning lamp on sensor fault | B | 0 | — |
| ABS-REQ-050 DTC on hydraulic pump fault | B | 1 | Q2 this year |
| ABS-REQ-051 ABS modulation < 10ms response | C | 0 | — |
| ABS-REQ-052 ABS active during cornering | A | 2 | Never |

Three requirements have zero test coverage.
One sprint is available for new test development.
You can write tests for two of the three gaps.

### Question

Prioritise which two gaps to address this sprint.
Justify using ASIL level, defect history, and
safety relevance.

### Answer

> ⭐ **Priority 1: ABS-REQ-049 — Warning lamp
> on sensor fault (ASIL-B)**
>
> Reason: ASIL-B safety requirement. The warning
> lamp is the driver's only indication of ABS
> sensor failure. If the lamp does not activate,
> the driver has no awareness of degraded braking.
> This is a direct safety consequence.
> Zero coverage on a safety-critical human
> interface requirement is unacceptable.

> **Priority 2: ABS-REQ-048 — ABS off on
> ignition off (ASIL-B)**
>
> Reason: ASIL-B. ABS remaining active after
> ignition off could cause unexpected behavior
> during vehicle servicing or towing.
> Zero coverage, safety-relevant, straightforward
> to test — high value per effort.

> **Defer: ABS-REQ-051 — ABS modulation < 10ms
> (ASIL-C)**
>
> Reason: ASIL-C is lower than ASIL-B — lower
> safety integrity requirement.
> Additionally, timing tests require precise
> measurement infrastructure that may not be
> available this sprint.
> Address in next sprint with infrastructure
> preparation.

| Priority | Requirement | Reason |
|----------|-------------|--------|
| 1 | ABS-REQ-049 | ASIL-B + direct driver safety impact |
| 2 | ABS-REQ-048 | ASIL-B + servicing safety impact |
| 3 (defer) | ABS-REQ-051 | Lower ASIL + infrastructure dependency |

---

## Quick Reference — Test Improvement Signals

| Signal | Measurement | Improvement Action |
|--------|------------|-------------------|
| Falling defect detection | Defects per release trend | Coverage gap analysis → targeted new tests |
| High flaky rate | Flaky tests / total > 2% | Quarantine + root cause investigation |
| Low assertion density | < 2 assertions per test | Strengthen assertions — add behavioral checks |
| Slow execution growth | Duration trending up | Profile slow tests → signal-based waits |
| Coverage gaps | Requirements with 0 tests | Prioritise by ASIL + defect history |

---

*Next: Scenarios 8.1.2 — Technical Analysis*