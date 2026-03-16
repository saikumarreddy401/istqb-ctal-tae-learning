# Sub-Chapter 6.1.2 — Data Analysis for Test Results

> **Syllabus Reference:** TAE-6.1.2
> **Cognitive Level:** K4 — Analyze
> **Chapter:** 6 — Test Automation Reporting and Metrics
> **Status:** ✅ Complete

---

## 1. Concept Explanation

### Why Analysis Is Distinct from Collection

Collecting data produces raw numbers.
Analysis transforms raw numbers into decisions.

> ⭐ **K4 means the exam will ask you to evaluate
> a dataset and recommend a course of action —
> not just name metrics.**
> You must know what a metric means, what causes
> it to change, and what action it recommends.

A pass rate of 84% means nothing without context.
Analysis determines whether 84% is:
- A regression caused by a code change
- A flaky test infrastructure problem
- A genuine product quality issue
- An expected result from a new test suite

---

## 2. Core Metrics — Definitions and Interpretation

### Metric 1 — Test Pass Rate

> **Definition:** Percentage of test cases that
> passed in a given execution run or time period.

| Formula | (Passed / Total Executed) × 100 |
|---------|--------------------------------|
| Healthy range | Project-dependent — typically 95%+ for stable releases |
| Trend matters more than snapshot | One run at 84% vs consistent drop from 97% to 84% |

**Interpretation table:**

| Pass Rate Pattern | Likely Cause | Recommended Action |
|------------------|-------------|-------------------|
| Sudden drop, one run | Environment issue or flaky tests | Re-run before investigating product |
| Gradual decline over weeks | Accumulating product defects or test debt | Defect triage + test maintenance review |
| Consistent low rate, new suite | New tests exposing real product gaps | Defect creation, not test fixes |
| High rate, complex new feature | Tests not yet covering new functionality | Coverage gap analysis |

> ⭐ Pass rate alone does not tell you whether the
> product is good. It tells you whether the tests
> that ran, passed. Coverage determines whether
> the right tests ran.

### Metric 2 — Test Execution Time

> **Definition:** Total time to execute a test suite
> or individual test case, measured across runs.

| Concern | Threshold Example |
|---------|-----------------|
| Single test too slow | > 30 seconds for a unit test |
| Suite too slow for CI | > 10 minutes for build-stage suite |
| Suite too slow for nightly | > 4 hours for full regression |

**Analysis questions:**

| Question | What It Reveals |
|----------|----------------|
| Which tests take the longest? | Candidates for parallelization or optimization |
| Is execution time increasing over releases? | Test suite growth without maintenance |
| Does execution time vary between runs? | Environment instability, resource contention |

**Automotive example:**
An ABS HIL regression suite that ran in 90 minutes
in January now runs in 140 minutes in March without
new tests being added. Analysis: test setup/teardown
time increased — likely ECU reset sequence slowed
by a firmware change. Root cause: not in test code
but in ECU boot time.

### Metric 3 — Defect Detection Rate

> **Definition:** Number of defects found by
> automated tests per release or time period.

| Trend | Interpretation |
|-------|---------------|
| High detection rate, new product | Test suite working correctly |
| Falling detection rate, active development | Test coverage not growing with product |
| Zero detection rate | Tests too shallow or product fully mature |
| Spike in detection rate | High-risk change introduced, or new test area added |

> ⭐ A falling defect detection rate in an actively
> developed product is a warning sign — either the
> tests are not covering new functionality, or
> the tests are too weak to find defects.

### Metric 4 — Flaky Test Rate

> **Definition:** Percentage of test cases that
> produce inconsistent results (pass on one run,
> fail on another) without any product change.

| Formula | (Flaky Tests / Total Tests) × 100 |
|---------|----------------------------------|
| Acceptable threshold | < 2% in a mature suite |
| Action threshold | > 5% requires immediate investigation |

**Flaky test root causes in automotive HIL:**

| Root Cause | Symptom | Fix |
|-----------|---------|-----|
| Timing dependency | Test passes when ECU is fast, fails when slow | Add explicit wait with timeout |
| CAN bus congestion | Signal read times out intermittently | Increase timeout, check bus load |
| HIL rack hardware fault | Intermittent connection loss | Hardware check, rack maintenance |
| Shared state between tests | Previous test leaves ECU in unexpected state | Add test fixture reset |
| Hardcoded sleep instead of wait | Works on fast rack, fails on slow rack | Replace sleep with signal-based wait |

> ⭐ **Flaky tests are more dangerous than failing tests.**
> A consistently failing test is investigated and fixed.
> A flaky test erodes trust in the entire test suite —
> engineers start ignoring failures because "it might
> be flaky again." This is the most corrosive quality
> problem in automation.

### Metric 5 — Automation Coverage

> **Definition:** Percentage of test cases or
> requirements covered by automated tests.

| Coverage Type | What It Measures |
|--------------|----------------|
| Test case automation ratio | Automated / total test cases |
| Requirements coverage | Requirements with ≥1 automated test / total requirements |
| Code coverage | Lines or branches executed by tests |
| Risk coverage | High-risk areas with automated tests / total high-risk areas |

> ⭐ High automation ratio with low requirements
> coverage means many tests exist but they do not
> cover what matters. Coverage must be measured
> against requirements — not just against test case count.

### Metric 6 — Mean Time to Detect (MTTD)

> **Definition:** Average time from when a defect
> is introduced into the codebase to when automated
> testing detects it.

| MTTD | Pipeline Stage | Meaning |
|------|---------------|---------|
| Minutes | Build stage | Defect caught at commit — ideal |
| Hours | Integration stage | Defect caught same day |
| Days | Nightly regression | Defect survives overnight before detection |
| Weeks | Manual testing only | Automation not providing early detection |

> ⭐ Reducing MTTD is the primary value proposition
> of CI/CD test automation. Metrics must demonstrate
> this reduction over time.

---

## 3. Trend Analysis vs Snapshot Analysis

> ⭐ This is a K4 distinction — a single snapshot
> metric rarely justifies a decision. Trend analysis
> is required for actionable insights.

| Analysis Type | What It Shows | When to Use |
|--------------|--------------|-------------|
| Snapshot | Current state at one point in time | Status report, go/no-go decision |
| Trend | Change over multiple data points | Process improvement, early warning |
| Comparative | Two environments or releases side by side | Root cause isolation |
| Distribution | Spread of values (e.g. test duration) | Identify outliers and instability |

**Trend analysis example — ABS pass rate:**

| Week | Pass Rate | Event |
|------|----------|-------|
| W1 | 97% | Baseline |
| W2 | 96% | Normal variation |
| W3 | 91% | ABS SW v2.4 deployed |
| W4 | 88% | No new deployment |
| W5 | 84% | No new deployment |

Analysis: Pass rate declining continuously after v2.4
deployment — not a one-time event. Three possible
conclusions to evaluate:

1. v2.4 introduced latent defects surfacing over time
2. Test environment degrading (HIL rack hardware)
3. Test data becoming stale relative to v2.4 calibration

Each hypothesis requires a different investigation path.
This is K4 thinking — not just identifying the metric,
but reasoning to the root cause.

---

## 4. Root Cause Analysis Using Test Data

### The Four-Question Framework

> ⭐ When a metric deviates, apply this framework
> before drawing conclusions:

| Question | Purpose |
|----------|---------|
| Is the deviation real or noise? | Single data point vs sustained trend |
| Is it product, environment, or test? | Isolate the root cause category |
| Did anything change at that point? | Correlate with deployments, config changes |
| Which specific tests are failing? | Identify failure cluster |

### Root Cause Categories

| Category | Indicators | Action |
|----------|-----------|--------|
| Product defect | New tests fail after specific SW change | Raise defect, block release |
| Test defect | Tests that passed before fail with no SW change | Fix test, mark as test bug |
| Environment issue | Failures cluster on one rack or pipeline run | Infrastructure investigation |
| Data issue | Failures involve assertion values only | Verify test data matches SUT version |
| Coverage gap | Pass rate high but defects found in manual testing | Expand test coverage |

**Automotive example — failure cluster analysis:**
```
ABS regression results — W3 failures:

test_wheel_speed_fl_normal_braking     FAIL
test_wheel_speed_fl_abs_activation     FAIL
test_wheel_speed_fl_fault_injection    FAIL
test_wheel_speed_fr_normal_braking     PASS
test_wheel_speed_fr_abs_activation     PASS
test_abs_ecu_reset                     PASS
test_abs_fault_memory                  PASS
```

Analysis: All failures involve WheelSpeedFL signal.
WheelSpeedFR (same test logic) passes.
Root cause: FL sensor hardware on HIL rack, or
ARXML signal definition for FL changed in v2.4.
This is a failure cluster — not a random distribution.
Cluster analysis directs investigation to one component.

---

## 5. Metrics for Different Stakeholders

> ⭐ Different stakeholders need different metrics.
> The TAE must select and present the right data
> for the right audience — K4 application.

| Stakeholder | Metrics They Need | Why |
|-------------|-----------------|-----|
| Development team | Failing tests, failure messages, signal traces | Fix defects |
| Test manager | Pass rate trend, coverage, MTTD | Release decisions |
| Project manager | Automation ratio, schedule risk | Resource allocation |
| Safety auditor | Requirement coverage, traceability, retention | Compliance |
| Infrastructure team | Execution time, environment stability, flaky rate | Pipeline maintenance |

> Presenting flaky test rates to a safety auditor
> without context is confusing. Presenting pass rate
> trends without coverage data to a test manager
> is incomplete. Know your audience.

---

## 6. Thresholds and Quality Gates

> ⭐ Metrics become actionable when paired with
> thresholds. A threshold converts a metric into
> a decision.

| Metric | Threshold Example | Gate Action |
|--------|-----------------|------------|
| Pass rate | < 95% | Block deployment |
| Flaky test rate | > 5% | Mandatory investigation before release |
| Execution time | > 120 minutes | Alert, optimize before next sprint |
| Requirements coverage | < 80% | Block certification submission |
| MTTD | > 24 hours | Pipeline restructure required |

**Automotive quality gate example:**
```yaml
# Pipeline quality gate — ABS release
quality_gates:
  pass_rate_minimum: 95
  flaky_rate_maximum: 2
  requirements_coverage_minimum: 90
  execution_time_maximum_minutes: 120

on_gate_failure:
  action: block_deployment
  notify: [test_manager, project_manager]
  artifact: quality_gate_report.html
```

---

## 7. Automotive Domain — Metrics Architecture

### ABS Test Suite Metrics Dashboard

| Metric | Source | Dashboard View |
|--------|--------|---------------|
| Pass rate per SW version | JUnit XML → InfluxDB | Line chart, 8-week trend |
| Flaky test list | Result comparison tool | Table, sorted by flaky frequency |
| Signal assertion failures | Custom logger | Heatmap by signal name |
| Execution time per suite | Pipeline timestamps | Bar chart by suite |
| Requirements coverage | Polarion integration | Coverage matrix |
| HIL rack utilization | Environment metadata | Rack usage pie chart |

### Failure Heatmap Concept

| Signal \ Week | W1 | W2 | W3 | W4 |
|--------------|----|----|----|----|
| WheelSpeedFL | ✅ | ✅ | ❌ | ❌ |
| WheelSpeedFR | ✅ | ✅ | ✅ | ✅ |
| ABSActivation | ✅ | ✅ | ✅ | ❌ |
| BrakePressure | ✅ | ✅ | ✅ | ✅ |

> A failure heatmap by signal shows at a glance
> which signals are experiencing persistent issues.
> WheelSpeedFL failing since W3 points to a
> specific hardware or ARXML issue introduced
> at that point.

---

## 8. Common Failures in Data Analysis

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| Analyzing snapshots only | Miss gradual degradation trends | Always plot metrics over time |
| Pass rate without coverage | High pass rate masks coverage gaps | Always pair pass rate with coverage |
| No threshold defined | Metrics observed but no action taken | Define quality gates before first release |
| Treating flaky as failing | Defect raised against product for test issue | Categorize failures before triaging |
| Wrong metric for wrong audience | Stakeholder cannot act on the data | Map metrics to stakeholder decisions |
| Ignoring outliers | One very slow test hidden in average | Use distribution analysis, not just averages |

---

## 9. Architect Insights

> ⭐ **Metrics without thresholds are decoration.
> Thresholds without actions are theatre.
> Only metrics + thresholds + automated actions
> constitute a quality gate.**

> **Flaky test management is a first-class
> architectural concern.** A suite with 10% flaky
> tests does not have a 90% reliable signal.
> It has an unreliable signal of unknown value.
> Flaky tests must be quarantined, not ignored.

> **For automotive certification:**
> The auditor does not want to see your Grafana
> dashboard. They want to see a documented mapping
> from each safety requirement to a specific test
> case result, with a timestamp, SUT version, and
> environment identifier. Design for auditability
> from day one.

> **Coverage is the context for pass rate.**
> Never present pass rate without coverage.
> 100% pass rate on 20% coverage is a risk signal,
> not a quality signal.

---

## 10. Reflection Questions

1. Your ABS nightly regression shows 91% pass rate
   this week, down from 97% three weeks ago. The
   decline is gradual — 1-2% per week. No new
   tests were added. Using the four-question
   framework, walk through the analysis and
   identify the most likely root cause categories.

2. A test manager asks you to report automation
   quality to both the development team and the
   ISO 26262 safety auditor. Define what metrics
   you would include in each report and explain
   why the two reports differ.

3. Your pipeline quality gate blocks deployment
   when pass rate drops below 95%. This week the
   gate blocked a release because three flaky tests
   caused the rate to drop to 93%. The defects are
   in the test code — not the product. How do you
   modify the quality gate strategy to prevent
   this while still protecting against real product
   defects?

4. A failure cluster analysis shows that 80% of
   this week's ABS failures involve signal assertion
   values for WheelSpeedFL only. All other signals
   pass. List three hypotheses for the root cause
   and explain what data you would examine to
   confirm or eliminate each.

5. Your suite has grown from 200 to 800 test cases
   over two years. Pass rate remains at 96%.
   Defect detection rate has fallen from 15 defects
   per release to 3. What does this pattern indicate,
   and what analysis would you perform to determine
   whether the test suite is still providing value?

---

## 11. Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Define quality gate thresholds for your current ABS suite (pass rate, flaky rate, coverage) | `chapter-06-reporting-metrics/` |
| 2 | Implement a failure cluster analysis script that groups failures by signal name | `framework-prototype/core/report_generator.py` |
| 3 | Map your top three stakeholders to the specific metrics each needs from your test results | `automotive-domain/hil_automation_architecture.md` |

---

*Next: Sub-Chapter 6.1.3 — Test Progress Report Construction*