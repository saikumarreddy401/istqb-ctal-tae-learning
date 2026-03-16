# Scenarios — Sub-Chapter 8.1.2 — Technical Analysis of the TAF

> **Syllabus Reference:** TAE-8.1.2
> **Cognitive Level:** K4 — Analyze
> **File:** scenarios_8_1_2_technical_analysis.md
> **Status:** ✅ Complete

---

## Scenario 1 — Prioritising Technical Debt Findings (K4)

### Situation

Monthly technical analysis of your ABS TAF
produces these findings:

| Finding | Severity | Count | Evidence |
|---------|----------|-------|---------|
| Unused variables in assertions | Critical | 4 | pylint W0612 |
| Layer violations — test scripts import `can` directly | High | 11 | Dependency scan |
| Functions with complexity > 15 | High | 6 | radon output |
| TAF unit test coverage | Medium | 58% | pytest-cov |
| Unpinned dependencies | High | 3 | requirements.txt |
| Magic numbers in assertions | Medium | 134 | AST analysis |
| TODO/FIXME comments | Low | 28 | grep output |

One sprint is available. Capacity: 40 hours.

### Question

Prioritise the findings into this sprint and
next sprint. Justify each decision using risk
impact analysis.

### Answer

**This sprint — address immediately:**

| Finding | Hours | Justification |
|---------|-------|--------------|
| Unused variables (4 cases) | 4h | Critical — active false negatives. Tests passing that should fail. Fix before any release. |
| Unpinned dependencies (3) | 2h | High — silent version upgrades may break CAN layer at any CI run. Pin takes 30 min per dependency. |
| Layer violations — subset (5 of 11) | 8h | High — each violation is a future maintenance event. Fix highest-impact files first. |
| Complexity > 15 functions (3 of 6) | 10h | High — refactor the three worst. Remaining three next sprint. |
| **Total** | **24h** | |

**Next sprint — schedule and assign:**

| Finding | Hours | Justification |
|---------|-------|--------------|
| Layer violations — remaining (6 of 11) | 10h | High — complete the layer cleanup |
| Complexity > 15 — remaining (3 of 6) | 10h | High — complete refactoring |
| TAF unit test coverage (58% → 75%) | 12h | Medium — write unit tests for untested core components |
| Magic numbers — first batch | 8h | Medium — start with assertion-critical values |
| **Total** | **40h** | |

**Defer until Q3:**

| Finding | Justification |
|---------|--------------|
| Magic numbers — full replacement | 134 items requires dedicated sprint |
| TODO/FIXME comments | Low severity — no functional impact |

> ⭐ The four unused variable findings are fixed
> in hour one of the sprint — before anything else.
> They are actively producing false negatives
> right now. Every other finding is future risk.
> These are present risk.

---

## Scenario 2 — Layer Violation Analysis (K4)

### Situation

Dependency scan on your ABS TAF finds:
```
LAYER VIOLATION REPORT
─────────────────────────────────────────
tests/test_abs_wheel_speed.py
  imports: can (python-can)          ← VIOLATION
  imports: core.can_signal_monitor   ← correct

tests/test_abs_fault_injection.py
  imports: udsoncan                  ← VIOLATION
  imports: core.uds_handler          ← correct

tests/test_abs_calibration.py
  imports: core.can_signal_monitor   ← correct
  imports: business_logic.abs_flows  ← correct

business_logic/abs_signal_flows.py
  imports: can (python-can)          ← correct (business logic layer)
  imports: core.can_signal_monitor   ← correct
─────────────────────────────────────────
2 violations found in test scripts
```

### Question A

Explain why `business_logic/abs_signal_flows.py`
importing `can` directly is correct, but
`tests/test_abs_wheel_speed.py` importing `can`
directly is a violation.

### Answer A

> ⭐ The TAF layer hierarchy defines which layers
> may depend on which:
>
> ```
> test_scripts → business_logic → core_libraries → external_tools
> ```
>
> `business_logic` is permitted to import `core`
> and external libraries because it IS a lower
> layer — it implements the abstractions that
> test scripts use.
>
> `test_scripts` must ONLY import from
> `business_logic` and `core` — never from
> external libraries directly.
>
> When `test_abs_wheel_speed.py` imports `can`,
> it bypasses the abstraction layer. If `python-can`
> changes its API, the test script breaks directly
> — instead of only `core.can_signal_monitor`
> needing an update.

### Question B

What is the concrete maintenance consequence
of the 11 layer violations in this TAF when
the team upgrades from `python-can 4.2.0`
to `python-can 4.3.0`?

### Answer B

| Scenario | With Violations | Without Violations |
|----------|---------------|-------------------|
| `python-can` API change | 11 test files break directly | Only `core.can_signal_monitor` breaks |
| Files to update | 11 test files + core layer | 1 core file only |
| Risk of missing an update | High — 11 scattered files | Zero — single update point |
| Time to update | Hours | Minutes |

> ⭐ 11 violations means a library upgrade
> touches 11 files instead of 1.
> Each file touched is a regression risk.
> The abstraction layer exists precisely to
> reduce this to a single change point.

---

## Scenario 3 — Runtime Metric Analysis (K4)

### Situation

Runtime metrics for ABS suite over 6 months:

| Month | Mean Duration | P95 Duration | Total Time | Tests |
|-------|--------------|-------------|-----------|-------|
| Jan | 12.1s | 28s | 87 min | 280 |
| Feb | 12.4s | 29s | 89 min | 281 |
| Mar | 13.8s | 35s | 102 min | 283 |
| Apr | 15.2s | 42s | 115 min | 285 |
| May | 17.1s | 51s | 130 min | 286 |
| Jun | 19.4s | 68s | 148 min | 287 |

Test count grew by 7 tests (2.5%).
Execution time grew by 70% (87 → 148 min).

### Question

Evaluate the root cause of execution time growth
and recommend the investigation and improvement steps.

### Answer

> ⭐ 2.5% test count growth cannot explain 70%
> execution time growth. The growth is in
> individual test duration — not suite size.

**Evidence from data:**

| Metric | Jan | Jun | Change |
|--------|-----|-----|--------|
| Mean duration | 12.1s | 19.4s | +60% |
| P95 duration | 28s | 68s | +143% |
| Total time | 87 min | 148 min | +70% |

> P95 growing faster than mean (143% vs 60%)
> means a subset of tests is growing much
> faster than the average. The distribution
> is widening — not shifting uniformly.

**Three hypotheses:**

| Hypothesis | Evidence | Investigation |
|-----------|---------|--------------|
| ECU setup/teardown time growing | Mean grows steadily | Measure fixture duration separately with `pytest --setup-show` |
| Hardcoded sleeps accumulating | P95 growing faster | Search codebase for `time.sleep()` — count and total |
| CAN bus timeout threshold increased | Specific tests slow | Compare slow test list Jan vs Jun |

**Investigation steps:**
```bash
# Step 1: identify slowest tests June vs January
python scripts/identify_slow_tests.py \
  --junit results/jan_baseline.xml \
  --junit results/jun_current.xml \
  --compare

# Step 2: measure fixture overhead
pytest tests/ --setup-show --junit-xml=fixture_timing.xml

# Step 3: count hardcoded sleeps
grep -rn "time.sleep" tests/ --include="*.py" | wc -l
```

**Recommended action:**

> 1. Profile top 10 slowest tests — identify
>    whether slowdown is in setup, execution, or teardown
> 2. Replace all `time.sleep()` with signal-based waits
> 3. Check ECU reset sequence duration — firmware
>    change may have slowed boot time
> 4. Set execution time threshold alert at 120 min
>    in pipeline — catch further growth early

---

## Scenario 4 — TAF Coverage Gap (K4)

### Situation

TAF unit test coverage report:

| Module | Lines | Covered | Coverage |
|--------|-------|---------|---------|
| core/can_signal_monitor.py | 180 | 98 | 54% |
| core/uds_handler.py | 220 | 108 | 49% |
| core/test_logger.py | 90 | 81 | 90% |
| business_logic/abs_signal_flows.py | 310 | 148 | 48% |
| business_logic/fault_injection.py | 140 | 119 | 85% |
| report_generator.py | 120 | 72 | 60% |

Overall TAF coverage: 58%

### Question

Evaluate which modules to prioritise for unit
test improvement and justify using false negative
risk analysis.

### Answer

**Risk assessment per module:**

| Module | Coverage | False Negative Risk | Priority |
|--------|---------|-------------------|---------|
| core/uds_handler.py | 49% | **Critical** — UDS handler used by every diagnostic test. Defect here = false negative across entire UDS test suite | 1 |
| core/can_signal_monitor.py | 54% | **Critical** — signal monitor used by every CAN test. Scaling defect = wrong values accepted silently | 2 |
| business_logic/abs_signal_flows.py | 48% | **High** — ABS activation logic. Incorrect flow sequence = safety-critical false negative | 3 |
| report_generator.py | 60% | **High** — incorrect pass rate = wrong release decision | 4 |
| core/test_logger.py | 90% | Low — logging failure does not cause false negative | 5 |
| business_logic/fault_injection.py | 85% | Low — already well covered | 6 |

**Coverage improvement targets:**

| Module | Current | Target | New Tests Needed (est.) |
|--------|---------|--------|------------------------|
| core/uds_handler.py | 49% | 90% | ~18 unit tests |
| core/can_signal_monitor.py | 54% | 90% | ~15 unit tests |
| business_logic/abs_signal_flows.py | 48% | 85% | ~20 unit tests |
| report_generator.py | 60% | 90% | ~8 unit tests |

> ⭐ UDS handler at 49% coverage means half
> of the diagnostic communication logic has
> never been unit tested. Every test that
> uses UDS — fault injection, DTC reading,
> session management — depends on unverified
> code. This is the highest-risk gap in the suite.

---

## Quick Reference — Technical Analysis Decision Framework

| Metric | Action Threshold | Immediate Action |
|--------|-----------------|-----------------|
| Unused variables in assertions | Any | Fix before next release — active false negative |
| Layer violations | Any new | Fix in current sprint |
| Cyclomatic complexity | > 15 | Refactor before next feature addition |
| TAF unit test coverage | < 70% | Add tests targeting critical path |
| Unpinned dependencies | Any | Pin within 1 sprint |
| Flaky rate | > 5% | Quarantine + investigation sprint |
| Mean test duration growth | > 20% without new tests | Profile and investigate |

---

*Next: Scenarios 8.1.3 — Restructuring Testware*