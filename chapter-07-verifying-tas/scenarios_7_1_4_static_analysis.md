# Scenarios — Sub-Chapter 7.1.4 — Static Analysis of Testware

> **Syllabus Reference:** TAE-7.1.4
> **Cognitive Level:** K3 — Apply
> **File:** scenarios_7_1_4_static_analysis.md
> **Status:** ✅ Complete

---

## Scenario 1 — Identifying Critical Violations (K3)

### Situation

You run flake8 and pylint on your ABS TAF for
the first time. The output includes these findings:
```
core/can_signal_monitor.py:47: W0612 unused-variable 'result'
core/can_signal_monitor.py:83: W0702 bare-except
tests/test_abs_wheel_speed.py:31: E501 line too long (112 > 100)
tests/test_abs_wheel_speed.py:55: W0612 unused-variable 'dtc_list'
tests/test_abs_activation.py:22: C0301 line too long
core/report_generator.py:91: W0611 unused-import 'datetime'
tests/test_abs_fault_injection.py:67: W0612 unused-variable 'response'
```

### Question A

Classify each finding as Critical, High, Medium,
or Low severity. Justify each classification.

### Answer A

| Finding | Location | Severity | Justification |
|---------|----------|---------|--------------|
| W0612 unused-variable 'result' | can_signal_monitor.py:47 | **Critical** | Variable assigned but never used — assertion likely missing — false negative risk |
| W0702 bare-except | can_signal_monitor.py:83 | **Critical** | Catches all exceptions including infrastructure failures — test always passes even when it should error |
| E501 line too long | test_abs_wheel_speed.py:31 | Low | Style only — no functional impact |
| W0612 unused-variable 'dtc_list' | test_abs_wheel_speed.py:55 | **Critical** | DTC list read but never asserted — false negative on DTC verification |
| C0301 line too long | test_abs_activation.py:22 | Low | Style only — no functional impact |
| W0611 unused-import 'datetime' | report_generator.py:91 | Medium | Dead import — no functional impact but indicates stale code |
| W0612 unused-variable 'response' | test_abs_fault_injection.py:67 | **Critical** | UDS response read but never asserted — test passes regardless of response content |

> ⭐ Three of seven findings are Critical because
> they produce false negatives — tests that pass
> when the product is defective. These must be
> fixed before any test results from this suite
> can be trusted.

### Question B

For each Critical finding, show the defective
code and the correct fix.

### Answer B

**Finding 1 — unused 'result' in can_signal_monitor.py:47**
```python
# DEFECTIVE — result assigned, never used
def check_wheel_speed(self, actual: float, expected: float):
    result = self._compare_with_tolerance(actual, expected)
    # ← result never returned or asserted
    # Every call to check_wheel_speed silently does nothing

# CORRECT — result returned to caller
def check_wheel_speed(self, actual: float, expected: float) -> bool:
    result = self._compare_with_tolerance(actual, expected)
    return result  # ← Caller can now assert on this
```

**Finding 2 — bare-except in can_signal_monitor.py:83**
```python
# DEFECTIVE — bare except swallows all failures
def read_signal(self, signal_name: str) -> float:
    try:
        return self._bus.recv_signal(signal_name)
    except:
        return 0.0  # ← Returns 0 on ANY error — including hardware fault
        # Test sees 0.0, asserts against 0.0 expected → false pass

# CORRECT — specific exception handling
def read_signal(self, signal_name: str) -> float:
    try:
        return self._bus.recv_signal(signal_name)
    except SignalNotFoundError as e:
        raise  # Re-raise — test should fail if signal missing
    except CanBusTimeoutError as e:
        raise EnvironmentError(
            f"CAN bus timeout reading {signal_name}. "
            f"Check hardware connection."
        ) from e
```

**Finding 3 — unused 'dtc_list' in test_abs_wheel_speed.py:55**
```python
# DEFECTIVE — DTC list read but never asserted
def test_abs_wheel_speed_no_fault():
    simulator.set_vehicle_speed(50.0)
    dtc_list = uds_client.read_dtc()  # ← Read but never asserted
    signal = can_monitor.read_signal("WheelSpeedFL")
    assert signal == pytest.approx(50.0, abs=0.5)
    # DTC check silently skipped — test passes with active DTCs

# CORRECT — DTC assertion included
def test_abs_wheel_speed_no_fault():
    simulator.set_vehicle_speed(50.0)
    dtc_list = uds_client.read_dtc()
    assert dtc_list.confirmed_count == 0, (
        f"Unexpected DTCs active: {dtc_list.confirmed_list}"
    )
    signal = can_monitor.read_signal("WheelSpeedFL")
    assert signal == pytest.approx(50.0, abs=0.5)
```

**Finding 4 — unused 'response' in test_abs_fault_injection.py:67**
```python
# DEFECTIVE — UDS response read but never asserted
def test_abs_fault_injection_uds():
    fault_injector.inject_wheel_speed_sensor_fault()
    response = uds_client.read_data_by_identifier(did=0xF401)
    # ← response never asserted — test always passes

# CORRECT — response content asserted
def test_abs_fault_injection_uds():
    fault_injector.inject_wheel_speed_sensor_fault()
    response = uds_client.read_data_by_identifier(did=0xF401)
    assert response.positive_response_code == 0x62
    assert response.wheel_speed_fl_valid is False
    assert 0xC0051 in uds_client.read_dtc().confirmed_list
```

---

## Scenario 2 — Introducing Static Analysis to Legacy Codebase (K3)

### Situation

Your ABS TAF has 6,200 lines across 34 files.
It has never had static analysis applied.
First flake8 run reports 623 violations.

The project manager says: "We cannot stop feature
development for two weeks to fix 623 violations.
Either skip static analysis or enforce it later."

### Question

Design a strategy to introduce static analysis
enforcement immediately without blocking the
pipeline for two weeks. Include the implementation.

### Answer

> ⭐ **Baseline approach:** record existing violations
> as accepted baseline. Only new violations block
> the pipeline. Existing violations are fixed
> incrementally over sprints.

**Implementation — three steps:**

**Step 1 — Generate baseline file:**
```bash
# Record all existing violations — these are accepted for now
flake8 framework-prototype/ tests/ \
  --statistics \
  --output-file=.flake8_baseline.txt

# Count: 623 violations in baseline
wc -l .flake8_baseline.txt
```

**Step 2 — Pipeline enforces zero NEW violations:**
```yaml
# Pipeline — static analysis with baseline comparison
- name: Run static analysis
  run: |
    flake8 framework-prototype/ tests/ \
      --statistics \
      --output-file=.flake8_current.txt

    # Compare: fail if current exceeds baseline
    python scripts/compare_violations.py \
      --baseline .flake8_baseline.txt \
      --current .flake8_current.txt
```
```python
# compare_violations.py
def compare_violations(baseline_path: str, current_path: str) -> None:
    """Fail pipeline only if violation count increased."""
    baseline_count = count_violations(baseline_path)
    current_count = count_violations(current_path)

    if current_count > baseline_count:
        raise SystemExit(
            f"Static analysis violations increased: "
            f"{baseline_count} → {current_count}. "
            f"New violations must be fixed before merging."
        )
    print(
        f"✅ Violations: {current_count} "
        f"(baseline: {baseline_count}). No new violations."
    )
```

**Step 3 — Incremental reduction plan:**

| Sprint | Target | Focus |
|--------|--------|-------|
| Sprint 1 | Fix all Critical (W0612, W0702) | False negative risk eliminated |
| Sprint 2 | Fix all High (complexity, undefined names) | Defect risk reduced |
| Sprint 3–6 | Fix Medium and Low in batches | Style consistency |
| Sprint 7 | Remove baseline file — full enforcement | Zero tolerance from this point |

> This approach gives immediate protection against
> new violations while allowing the team to continue
> feature development. The Critical findings are
> fixed in Sprint 1 — eliminating false negative
> risk within two weeks without stopping all work.

---

## Scenario 3 — Complexity Refactoring (K3)

### Situation

Radon reports this finding in your ABS TAF:
```
core/abs_signal_flows.py
    validate_abs_response - C (complexity: 16)
```

The function:
```python
def validate_abs_response(response, config, mode, env):
    if response is None:
        if config.get("strict"):
            raise ValueError("Null response")
        else:
            return False
    if mode == "extended":
        if env == "integration":
            if response.code == 0x62:
                if response.value > config["threshold_hi"]:
                    return True
                elif response.value == 0:
                    if config.get("allow_zero"):
                        return True
                    return False
                return False
            return False
        elif env == "preproduction":
            if response.code == 0x62:
                return response.value > config["threshold_pp"]
            return False
    elif mode == "basic":
        return response.code == 0x62
    return False
```

### Question

Identify why complexity 16 is a problem for
testware specifically, and refactor the function
to reduce complexity below 10.

### Answer

**Why complexity 16 is a testware problem:**

> ⭐ Cyclomatic complexity = number of independent
> paths through the function.
> Complexity 16 = 16 independent paths to test.
>
> A TAF function with 16 paths:
> - Cannot be unit tested comprehensively without
>   16+ test cases per function
> - Is likely to have untested paths that contain
>   defects — including false negatives
> - Cannot be maintained without introducing
>   new defects — too many interactions to reason about
> - Violates single responsibility principle —
>   doing too many things in one function

**Refactored — complexity reduced to 3 per function:**
```python
def _is_valid_response(response, strict_mode: bool) -> bool:
    """Check response exists. Complexity: 2."""
    if response is None:
        if strict_mode:
            raise ValueError("Null response in strict mode")
        return False
    return True


def _response_meets_threshold(
    response, threshold: float, allow_zero: bool
) -> bool:
    """Check response value against threshold. Complexity: 3."""
    if response.code != 0x62:
        return False
    if response.value > threshold:
        return True
    if response.value == 0 and allow_zero:
        return True
    return False


def validate_abs_response(
    response,
    threshold: float,
    strict_mode: bool = False,
    allow_zero: bool = False
) -> bool:
    """
    Validate ABS UDS response against threshold.
    Complexity: 2 — delegates to focused helpers.
    Environment and mode resolved by caller before calling.
    """
    if not _is_valid_response(response, strict_mode):
        return False
    return _response_meets_threshold(response, threshold, allow_zero)
```

**Usage — caller resolves environment before calling:**
```python
# Caller selects correct threshold for environment
threshold = config["threshold_hi"] if env == "integration" \
            else config["threshold_pp"]

result = validate_abs_response(
    response=response,
    threshold=threshold,
    strict_mode=config.get("strict", False),
    allow_zero=config.get("allow_zero", False)
)
```

> Three functions, each complexity ≤ 3.
> Each is independently unit-testable in 3–4 cases.
> Total test cases needed: 10 instead of 16+.

---

## Scenario 4 — Security Finding in TAF (K3)

### Situation

Bandit reports this finding:
```
tests/conftest.py:23
>> Issue: [B105:hardcoded_password_string]
   Possible hardcoded password: 'Bosch$ECU!2024'
   Severity: High   Confidence: Medium
```

The code:
```python
# conftest.py
ECU_DIAGNOSTIC_PASSWORD = "Bosch$ECU!2024"

@pytest.fixture
def authenticated_uds_client():
    client = UdsClient(
        ip=config["ecu_ip"],
        security_key=ECU_DIAGNOSTIC_PASSWORD
    )
    return client
```

### Question

Explain the security risk, and implement the
correct credential management approach for
testware in a CI/CD pipeline.

### Answer

**Security risk:**

> Hardcoded credentials in test code committed to
> Git are visible to everyone with repository access —
> including anyone who ever clones the repo, past
> contributors, and anyone who gains read access
> to the repository history.
>
> Even if the credential is later removed, it
> remains in Git history unless the history is
> rewritten. The credential is effectively
> permanently compromised once committed.
>
> For automotive ECU diagnostic access, this
> credential may allow: reading proprietary
> calibration data, writing to ECU memory,
> triggering diagnostic routines.

**Correct implementation — environment variables:**
```python
# conftest.py — CORRECT
import os

@pytest.fixture
def authenticated_uds_client(config):
    """
    Load ECU security key from environment variable.
    Never from source code or config files in Git.
    """
    security_key = os.environ.get("ECU_DIAGNOSTIC_KEY")

    if not security_key:
        raise EnvironmentError(
            "ECU_DIAGNOSTIC_KEY environment variable not set. "
            "Set this in your pipeline secrets or local .env file. "
            "Never commit credentials to source code."
        )

    client = UdsClient(
        ip=config["ecu_ip"],
        security_key=security_key
    )
    return client
```

**Pipeline secret configuration:**
```yaml
# GitHub Actions — secrets never appear in source code
jobs:
  run_tests:
    env:
      ECU_DIAGNOSTIC_KEY: ${{ secrets.ECU_DIAGNOSTIC_KEY }}
    steps:
      - name: Run ABS regression suite
        run: pytest tests/
```

**Local development — `.env` file (never committed):**
```bash
# .env — local only, in .gitignore
ECU_DIAGNOSTIC_KEY=Bosch$ECU!2024
```
```
# .gitignore
.env
*.env
```

> ⭐ The credential exists in one place only:
> the CI/CD secrets store and the engineer's
> local `.env` file. It never touches Git.
> Bandit would report no findings on this code.

---

## Scenario 5 — Pipeline Enforcement Design (K3)

### Situation

Your team agrees to introduce static analysis
but cannot agree on severity thresholds.

TAE A: "All violations should block the pipeline —
zero tolerance."

TAE B: "Only security and unused variable findings
should block — style is subjective."

TAE C: "Nothing should block — static analysis
should be informational only."

### Question

Define the correct pipeline enforcement strategy,
justify your severity thresholds, and explain
why each of the three positions is partially
correct or incorrect.

### Answer

**Correct strategy — tiered enforcement:**

| Severity | Examples | Pipeline Action | Justification |
|----------|---------|----------------|--------------|
| Critical | Unused variable in assertion, bare except, hardcoded credentials | **Block — immediate** | Direct false negative or security risk |
| High | Cyclomatic complexity > 15, undefined name | **Block** | High defect probability |
| Medium | Missing docstring, complexity 11–15 | **Warning — does not block** | Quality concern, not safety concern |
| Low | Line length, import order | **Informational only** | Style — no functional impact |

**Evaluating each position:**

**TAE A — zero tolerance:**
> Partially correct: zero tolerance is right for
> Critical and High. Incorrect for Medium and Low —
> blocking on line length violations creates noise
> and encourages engineers to disable the tool
> entirely rather than fix cosmetic issues.
> Zero tolerance applied uniformly reduces adoption.

**TAE B — security and unused variable only:**
> Partially correct: these are the right categories
> to block on. Incorrect to exclude high complexity —
> a function with complexity 18 is a defect waiting
> to happen and should block before it is merged.

**TAE C — informational only:**
> Incorrect for testware. An informational-only
> tool is a tool that will be ignored under
> schedule pressure. The value of static analysis
> is in enforcement — not in producing reports
> that nobody reads. Critical findings that do
> not block will not be fixed.

> ⭐ The correct position combines TAE A's
> enforcement principle with TAE B's category
> focus: enforce strictly on findings that cause
> false negatives or security issues, and
> report without blocking on style issues.

---

## Quick Reference — Static Analysis Severity

| Finding | Tool | Severity | Risk |
|---------|------|---------|------|
| Unused variable in test | pylint W0612 | Critical | False negative |
| Bare except | pylint W0702 | Critical | Masks errors |
| Hardcoded credential | bandit B105 | Critical | Security |
| Undefined name | pylint E0602 | High | Runtime error |
| Complexity > 15 | radon / pylint | High | Defect probability |
| Missing return type | mypy | High | Type safety |
| Line too long | flake8 E501 | Low | Style only |
| Import order | isort | Low | Style only |
| Missing docstring | pylint C0116 | Medium | Maintainability |

---

*Next: Chapter 8 — Continuous Improvement*