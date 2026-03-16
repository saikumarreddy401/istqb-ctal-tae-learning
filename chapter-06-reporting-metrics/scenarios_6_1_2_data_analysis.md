# Scenarios — Sub-Chapter 6.1.2 — Data Analysis for Test Results

> **Syllabus Reference:** TAE-6.1.2
> **Cognitive Level:** K4 — Analyze
> **File:** scenarios_6_1_2_data_analysis.md
> **Status:** ✅ Complete

---

## Scenario 1 — Four-Question Framework Applied (K4)

### Situation

Your ABS nightly regression suite produces the
following pass rates over six consecutive weeks:

| Week | Pass Rate | Event |
|------|----------|-------|
| W1 | 97% | Baseline — ABS SW v2.3 |
| W2 | 97% | No change |
| W3 | 93% | ABS SW v2.4 deployed |
| W4 | 91% | No new deployment |
| W5 | 89% | No new deployment |
| W6 | 87% | No new deployment |

The test manager asks for your analysis and
recommendation before the release decision meeting.

### Question

Apply the four-question framework to this dataset.
State your conclusion and recommendation.

### Answer

**Question 1 — Is the deviation real or noise?**

> The decline is sustained over four consecutive weeks
> following a single event (v2.4 deployment).
> A one-week dip at W3 could be noise.
> A 10-percentage-point decline over four weeks is
> a real signal — not statistical variation.

**Question 2 — Is it product, environment, or test?**

> Three hypotheses to evaluate:
>
> | Hypothesis | Evidence For | Evidence Against |
> |-----------|-------------|-----------------|
> | Product defect in v2.4 | Decline starts exactly at v2.4 deployment | Not yet confirmed by defect investigation |
> | Environment degradation | Possible — no rack maintenance data | Would expect random failures, not systematic decline |
> | Test data mismatch | v2.4 changed calibration values | Needs verification against test data versions |

**Question 3 — Did anything change at that point?**

> Yes — ABS SW v2.4 deployed at W3.
> No other changes recorded.
> This is the primary correlation.

**Question 4 — Which specific tests are failing?**

> This data is not yet available in the scenario.
> This is the next investigation step — identify
> whether failures cluster by signal, by test type,
> or are randomly distributed.

**Recommendation:**

> ⭐ Do not release until:
> 1. Failing test cases are identified and clustered
> 2. Each cluster is investigated: product defect vs test issue
> 3. Pass rate trend is reversed — not just stable
>
> A declining trend that has not stabilized at W6
> indicates the root cause has not been resolved.
> Releasing at 87% with a declining trend is a
> higher risk than releasing at 87% with a stable trend.

---

## Scenario 2 — Flaky Test Identification and Action (K4)

### Situation

Your ESP regression suite has 600 tests. Over the
past four weeks, test results show:

| Test Case | W1 | W2 | W3 | W4 |
|-----------|----|----|----|----|
| test_esp_stability_high_speed | ✅ | ❌ | ✅ | ❌ |
| test_esp_yaw_rate_threshold | ✅ | ✅ | ✅ | ✅ |
| test_esp_fault_injection_can | ❌ | ✅ | ❌ | ✅ |
| test_esp_ecu_reset_sequence | ✅ | ✅ | ❌ | ✅ |
| test_esp_calibration_variant_a | ❌ | ❌ | ❌ | ❌ |

No product changes were made between W1 and W4.

### Question A

Classify each test as: stable passing, stable failing,
or flaky. Explain your classification criteria.

### Answer A

| Test Case | Classification | Reason |
|-----------|--------------|--------|
| test_esp_stability_high_speed | Flaky | Alternates pass/fail with no product change |
| test_esp_yaw_rate_threshold | Stable passing | Passes every run |
| test_esp_fault_injection_can | Flaky | Alternates fail/pass consistently |
| test_esp_ecu_reset_sequence | Flaky | Three passes, one unexplained failure |
| test_esp_calibration_variant_a | Stable failing | Fails every run — consistent product or test defect |

> ⭐ Classification rule:
> - Stable failing = fails consistently → raise defect or fix test
> - Flaky = inconsistent result without product change → investigate test
> - Stable passing = passes consistently → no action needed

### Question B

What is the correct action for each classification,
and why is flaky more dangerous than stable failing?

### Answer B

| Classification | Action |
|--------------|--------|
| Stable failing | Investigate immediately — product defect or broken test |
| Flaky | Quarantine from pass rate calculation, investigate root cause |
| Stable passing | No action — monitor for regression |

> ⭐ **Flaky is more dangerous than stable failing because:**
>
> A stable failing test is investigated and resolved.
> A flaky test erodes trust. Engineers learn to
> re-run failures rather than investigate them.
> When a real product defect produces a failure,
> it is dismissed as "probably flaky again."
> The defect reaches production.
>
> Flaky tests must be quarantined — not ignored.
> Quarantine means: excluded from quality gate
> calculation, tracked separately, and assigned
> for mandatory root cause investigation.

---

## Scenario 3 — Metrics for Different Stakeholders (K4)

### Situation

You have the following ABS test data for the
release candidate build:

- Total tests: 409
- Passed: 387 (94.6%)
- Failed: 18 (4.4%)
- Blocked: 4 (1.0%)
- Flaky tests quarantined: 6
- Requirements coverage: 91%
- Safety requirements coverage: 88%
- New defects raised: 12
- Critical defects open: 2
- Execution time: 118 minutes
- Quality gate threshold: 95% pass rate

You must present this data to three audiences:
the development team, the release manager, and
the ISO 26262 safety auditor.

### Question

For each audience, specify which metrics you
present, which you omit, and what your key message is.

### Answer

**Development Team Report:**

| Metric | Include | Key Message |
|--------|---------|------------|
| 18 failing test IDs with failure messages | ✅ | Here is exactly what to fix |
| 12 new defects with severity | ✅ | Defects raised — assign to developers |
| 2 critical open defects | ✅ | These block release — priority fix |
| 6 flaky tests with root cause hypotheses | ✅ | These need investigation this sprint |
| Pass rate 94.6% | ✅ | Below threshold — action needed |
| ISO 26262 coverage matrix | ❌ | Not actionable for developers |

**Release Manager Report:**

| Metric | Include | Key Message |
|--------|---------|------------|
| Pass rate 94.6% vs 95% threshold | ✅ | 0.4% below gate — conditional hold |
| 2 critical open defects | ✅ | Release blocked until resolved |
| Requirements coverage 91% | ✅ | Coverage acceptable for non-safety reqs |
| Safety requirements coverage 88% | ✅ | Below 90% target — risk item |
| Recommendation | ✅ | Do not release until 2 critical defects resolved |
| Individual failing test details | ❌ | Too granular — not a release decision input |

**ISO 26262 Safety Auditor Report:**

| Metric | Include | Key Message |
|--------|---------|------------|
| Safety requirements coverage 88% | ✅ | 12% of safety reqs have no automated coverage |
| Traceability matrix: req → test → result | ✅ | Proof that each safety req was tested |
| 2 critical open defects with ASIL classification | ✅ | Open safety defects must be resolved |
| ECU serial and firmware version per test | ✅ | Compliance evidence |
| Retention confirmation | ✅ | Results stored per compliance requirement |
| Execution time 118 minutes | ❌ | Not a compliance concern |

> ⭐ The same dataset produces three different
> reports. The auditor does not need flaky test
> counts. The developer does not need retention
> confirmation. Audience determines content —
> not data availability.

---

## Scenario 4 — Failure Cluster Analysis (K4)

### Situation

This week's ABS regression produced 22 failures
from 409 tests. The failing test IDs are:
```
test_wheel_speed_fl_normal_braking
test_wheel_speed_fl_abs_activation
test_wheel_speed_fl_fault_injection
test_wheel_speed_fl_sensor_plausibility
test_wheel_speed_fl_calibration_variant_a
test_wheel_speed_fl_calibration_variant_b
test_wheel_speed_fl_calibration_variant_c
test_abs_activation_all_wheels          ← involves FL
test_abs_deactivation_speed_threshold   ← involves FL
test_brake_pressure_normal              PASS
test_brake_pressure_abs_active          PASS
test_wheel_speed_fr_normal_braking      PASS
test_wheel_speed_rl_normal_braking      PASS
test_wheel_speed_rr_normal_braking      PASS
test_esp_stability_normal               PASS
test_uds_fault_memory_read              PASS
```

### Question

Perform failure cluster analysis. State your
three hypotheses, the data that confirms or
eliminates each, and your recommended action.

### Answer

**Cluster identification:**

> 20 of 22 failures involve WheelSpeedFL.
> Tests for FR, RL, RR (identical logic) pass.
> Tests with no FL dependency pass.
> This is a tight, single-signal cluster —
> not a random distribution.

**Hypothesis 1 — FL signal ARXML definition changed:**

| | Detail |
|-|--------|
| Evidence for | ARXML update coinciding with recent SW release |
| Evidence against | Other signals from same ARXML file pass |
| Confirming data | Compare abs_v2.4.arxml WheelSpeedFL definition against abs_v2.3.arxml |
| Elimination | If ARXML unchanged, eliminate this hypothesis |

**Hypothesis 2 — FL wheel speed sensor hardware fault on HIL rack:**

| | Detail |
|-|--------|
| Evidence for | All FL tests fail regardless of test logic |
| Evidence against | Signal may still produce values — just wrong ones |
| Confirming data | Read WheelSpeedFL raw value via CANalyzer during bench test |
| Elimination | If raw value is correct, eliminate hardware fault |

**Hypothesis 3 — Test data for FL calibration variants is stale:**

| | Detail |
|-|--------|
| Evidence for | Three calibration variant tests all fail — same signal |
| Evidence against | Non-calibration FL tests also fail |
| Confirming data | Check calibration_v2.4 data file for WheelSpeedFL expected values |
| Elimination | If calibration data matches ARXML, eliminate |

**Recommended action:**

> 1. Check ARXML diff between v2.3 and v2.4 for WheelSpeedFL — 5 minutes
> 2. If ARXML unchanged, read raw CAN signal on rack — 10 minutes
> 3. If signal correct, check calibration data file — 5 minutes
>
> Cluster analysis reduces investigation from
> 22 individual failures to one root cause with
> three ordered checks. Total diagnosis time:
> 20 minutes maximum.

---

## Scenario 5 — Quality Gate Design (K4)

### Situation

Your ABS team currently has no automated quality
gate. The release decision is made manually by
reviewing the test report before each release.
In the last six months, two releases were approved
despite declining pass rate trends, and both
resulted in field defects.

You are asked to design a quality gate strategy
for the ABS CI/CD pipeline.

### Question

Define the quality gate thresholds, which pipeline
stage each gate applies to, and what action the
pipeline takes on gate failure.

### Answer

> ⭐ Quality gates must be defined per pipeline
> stage — build gates are stricter and faster
> than deployment gates.

**Build stage gates (per commit):**

| Metric | Threshold | On Failure |
|--------|----------|-----------|
| Unit + component test pass rate | 100% | Block merge |
| Static analysis violations | 0 critical | Block merge |
| Contract test pass rate | 100% | Block merge |

**Integration stage gates (nightly):**

| Metric | Threshold | On Failure |
|--------|----------|-----------|
| Integration test pass rate | ≥ 95% | Block deployment to preproduction |
| Flaky test rate | ≤ 2% | Alert — investigation required |
| Execution time | ≤ 120 minutes | Alert — optimization required |
| New critical defects | 0 | Block deployment |

**Release gates (pre-release):**

| Metric | Threshold | On Failure |
|--------|----------|-----------|
| Full regression pass rate | ≥ 95% | Block release |
| Safety requirements coverage | ≥ 90% | Block release |
| Open critical defects | 0 | Block release |
| Pass rate trend (last 4 runs) | Not declining | Human review required |
| Flaky test rate | ≤ 2% | Block release |

**Pass rate trend gate — the gate that was missing:**

> ⭐ The two field defects resulted from releasing
> despite a declining trend. The trend gate catches
> this case even when the snapshot value is above
> threshold.
```python
def evaluate_trend_gate(pass_rates: list) -> bool:
    """
    Block release if pass rate has declined in
    3 or more of the last 4 runs.
    A single dip is noise. Sustained decline is a signal.
    """
    if len(pass_rates) < 4:
        return True  # Insufficient data — allow with warning

    declines = sum(
        1 for i in range(1, len(pass_rates))
        if pass_rates[i] < pass_rates[i-1]
    )
    return declines < 3  # True = gate passes
```

---

## Quick Reference — K4 Analysis Checklist

| Step | Question | Purpose |
|------|----------|---------|
| 1 | Is deviation real or noise? | Avoid acting on single-run variation |
| 2 | Product, environment, or test? | Direct investigation to correct team |
| 3 | What changed at that point? | Find correlation with deployments |
| 4 | Which tests are failing? | Cluster analysis for root cause |
| 5 | What does the trend say? | Snapshot vs sustained pattern |
| 6 | What is the recommendation? | Convert analysis into decision |

---

*Next: Scenarios 6.1.3 — Test Progress Report*