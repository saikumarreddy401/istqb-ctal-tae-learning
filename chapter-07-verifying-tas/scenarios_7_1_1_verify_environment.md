# Sub-Chapter 7.1.4 — Static Analysis of Testware

> **Syllabus Reference:** TAE-7.1.4
> **Cognitive Level:** K3 — Apply
> **Chapter:** 7 — Verifying the Test Automation Solution
> **Status:** ✅ Complete

---

## 1. Concept Explanation

### What Static Analysis Is

Static analysis examines source code without
executing it. It finds defects, style violations,
complexity problems, and security issues by
analysing the code structure directly.

> ⭐ **Static analysis applied to testware is
> identical in principle to static analysis
> applied to production code.**
> The TAF is software. It must be held to the
> same code quality standards as the SUT.

Static analysis finds what dynamic testing misses:
- Code that is never executed but contains defects
- Style inconsistencies that reduce maintainability
- Complexity that increases defect probability
- Dead code, unused imports, undefined variables

### Why Testware Specifically Needs Static Analysis

| Reason | Detail |
|--------|--------|
| TAF is rarely reviewed as rigorously as production code | Static analysis compensates for lighter manual review |
| TAF grows over years without refactoring | Complexity accumulates — static analysis detects it |
| Multiple TAEs contribute with different styles | Style enforcement ensures consistency |
| TAF defects cause silent false negatives | Earlier detection = fewer missed product defects |

---

## 2. Categories of Static Analysis

### Category 1 — Style and Formatting

Enforces consistent code style across the TAF.

| Tool (Python) | What It Checks |
|--------------|---------------|
| `flake8` | PEP8 style: line length, spacing, naming |
| `black` | Automatic code formatting |
| `isort` | Import ordering and grouping |
| `pylint` | Style + logic warnings |
```python
# VIOLATION — flake8 E501 line too long, E302 missing blank lines
def test_abs_wheel_speed(can_monitor,simulator,uds_client,arxml_loader,config):
    simulator.set_vehicle_speed(80.0);simulator.apply_brake(150)
    result=can_monitor.read_signal("WheelSpeedFL")
    assert result==80.0

# CORRECT — PEP8 compliant
def test_abs_wheel_speed(
    can_monitor,
    simulator,
    uds_client,
    arxml_loader,
    config
):
    """Verify WheelSpeedFL matches vehicle speed during normal braking."""
    simulator.set_vehicle_speed(80.0)
    simulator.apply_brake(pressure_bar=150)

    result = can_monitor.read_signal("WheelSpeedFL")

    assert result == pytest.approx(80.0, abs=0.5), (
        f"WheelSpeedFL={result}, expected 80.0±0.5 km/h"
    )
```

### Category 2 — Logical Defects and Code Smells

Finds real defects in code that executes incorrectly
or will fail under certain conditions.

| Issue | Example | Risk |
|-------|---------|------|
| Unused variable | `result = can_monitor.read()` then never used | Silent — assertion never executes |
| Bare except clause | `except:` catches everything including KeyboardInterrupt | Masks real errors |
| Mutable default argument | `def setup(config={})` | State shared between calls |
| Unreachable code | Code after `return` statement | Dead code — never executes |
| Comparison to None with `==` | `if result == None` | Should be `is None` |
```python
# DEFECT — unused variable means assertion never executes
def test_abs_activation_defective():
    simulator.apply_brake(150)
    result = can_monitor.read_signal("ABSActivationFlag")
    # ← result assigned but never asserted
    # Static analysis: W0612 unused-variable
    # Dynamic testing: test PASSES silently — false negative

# DEFECT — bare except masks all errors
def test_uds_response_defective():
    try:
        response = uds_client.read_data_by_identifier(0xF401)
        assert response.value > 0
    except:
        pass  # ← Catches everything — test always passes
    # Static analysis: W0702 bare-except
    # Dynamic testing: test passes even when UDS throws exception

# CORRECT — specific exception handling
def test_uds_response_correct():
    response = uds_client.read_data_by_identifier(0xF401)
    assert response.positive_response_code == 0x62
    assert response.value > 0
```

> ⭐ **The unused variable pattern is the most
> dangerous static analysis finding in testware.**
> A variable assigned but never used in an assertion
> means the assertion does not exist. The test
> produces a false negative on every run.

### Category 3 — Complexity Analysis

High complexity correlates with high defect probability.
Measures cyclomatic complexity — the number of
independent paths through a function.

| Complexity Score | Interpretation | Action |
|-----------------|---------------|--------|
| 1–5 | Simple — low risk | No action |
| 6–10 | Moderate — review recommended | Consider refactoring |
| 11–15 | Complex — refactoring advised | Refactor before release |
| 16+ | Very complex — high defect risk | Mandatory refactoring |
```python
# HIGH COMPLEXITY — cyclomatic complexity = 12
# Too many branches — hard to test, high defect risk
def validate_abs_response(response, config, mode, rack_id):
    if response is None:
        if config.get("strict_mode"):
            raise ValueError("Null response in strict mode")
        else:
            return False
    if mode == "extended":
        if rack_id == "rack_1":
            if response.value > config["threshold_rack1"]:
                return True
            elif response.value == 0:
                if config.get("allow_zero"):
                    return True
                return False
        elif rack_id == "rack_2":
            # ... more branches
    # ... continues

# REFACTORED — cyclomatic complexity = 3
def validate_abs_response(response, threshold: float) -> bool:
    """Validate ABS response value against threshold."""
    if response is None:
        return False
    return response.value > threshold
```

### Category 4 — Security and Dependency Analysis

Checks for known vulnerabilities in dependencies
and insecure coding patterns.

| Tool | What It Checks |
|------|---------------|
| `bandit` | Python security issues — hardcoded passwords, SQL injection |
| `safety` | Known CVEs in installed packages |
| `pip-audit` | Dependency vulnerability audit |
```bash
# Check for security issues in TAF code
bandit -r framework-prototype/ -ll

# Check dependencies for known vulnerabilities
safety check -r requirements.txt
```

> In automotive TAF, security analysis of testware
> is relevant when the TAF connects to ECU diagnostic
> interfaces, cloud reporting systems, or external
> APIs. Hardcoded credentials in test configuration
> files are a common security finding.

---

## 3. Static Analysis Tools for Python TAF

| Tool | Category | Command | Pipeline Integration |
|------|---------|---------|---------------------|
| `flake8` | Style + logical | `flake8 src/ tests/` | Fast — runs in seconds |
| `pylint` | Style + logic + complexity | `pylint src/ tests/` | Slower — detailed output |
| `mypy` | Type checking | `mypy src/` | Catches type errors |
| `radon` | Complexity metrics | `radon cc src/ -s` | Reports per-function complexity |
| `bandit` | Security | `bandit -r src/` | Security-focused |
| `black --check` | Formatting | `black --check src/` | Formatting enforcement |

### Configuration — `.flake8`
```ini
# .flake8 — project-wide style configuration
[flake8]
max-line-length = 100
max-complexity = 10
exclude =
    .git,
    __pycache__,
    build/
ignore =
    E203,  # whitespace before ':'
    W503   # line break before binary operator
per-file-ignores =
    tests/*:S101  # allow assert in test files
```

### Configuration — `pyproject.toml`
```toml
# pyproject.toml — pylint and mypy configuration
[tool.pylint.messages_control]
disable = [
    "missing-module-docstring",  # Not required for test files
    "too-few-public-methods"     # Single-method test classes allowed
]

[tool.pylint.design]
max-complexity = 10
max-line-length = 100

[tool.mypy]
python_version = "3.11"
warn_unused_imports = true
warn_return_any = true
disallow_untyped_defs = true
```

---

## 4. Static Analysis in the CI/CD Pipeline

> ⭐ Static analysis must run in the build pipeline
> on every commit — not as an occasional manual step.
> Pipeline enforcement ensures no violation is
> committed without detection.
```yaml
# GitHub Actions — static analysis stage for TAF
jobs:
  static_analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install analysis tools
        run: pip install flake8 pylint mypy bandit radon black

      - name: Check code formatting
        run: black --check framework-prototype/ tests/

      - name: Run flake8 style check
        run: flake8 framework-prototype/ tests/
          --max-line-length=100
          --max-complexity=10

      - name: Run pylint
        run: pylint framework-prototype/
          --fail-under=8.0  # Score out of 10 — fail below 8.0

      - name: Run type checking
        run: mypy framework-prototype/
          --ignore-missing-imports

      - name: Run security check
        run: bandit -r framework-prototype/ -ll

      - name: Check complexity
        run: radon cc framework-prototype/ -s -n C
          # Report functions with complexity grade C or worse

  run_taf_tests:
    needs: static_analysis  # ← Tests only run if analysis passes
    steps:
      - name: Run TAF unit tests
        run: pytest tests/taf_unit_tests/
```

> The `needs: static_analysis` dependency means
> a TAF with style violations, unused variables,
> or security issues cannot be used for testing.
> This is enforcement — not a suggestion.

---

## 5. Applying Static Analysis Results

### Severity Classification

Not all findings are equal. Define severity levels
to prioritise action:

| Severity | Examples | Pipeline Action |
|----------|---------|----------------|
| Critical | Unused variable in assertion, bare except, security vulnerability | Block pipeline immediately |
| High | Cyclomatic complexity > 15, undefined name | Block pipeline |
| Medium | Line length violation, missing docstring | Warning — does not block |
| Low | Import ordering, minor style | Informational only |

> ⭐ Critical findings in testware are any finding
> that could produce a false negative — a test
> that passes when it should fail. These must
> block the pipeline without exception.

### Baseline Management

When introducing static analysis to an existing
codebase with many existing violations:

| Approach | How It Works | When To Use |
|----------|-------------|------------|
| Fix all violations first | Full cleanup before enforcement | Small codebase, dedicated sprint |
| Baseline file | Record existing violations — only new ones block | Large legacy codebase |
| Incremental enforcement | Enforce on new files only initially | Ongoing migration |
```bash
# Generate baseline — existing violations recorded, not blocked
flake8 framework-prototype/ --statistics > .flake8_baseline

# Future runs compare against baseline
# Only new violations above baseline block the pipeline
```

---

## 6. Automotive Domain — Static Analysis for TAF

### ECUTest Python API — Common Static Analysis Findings

When writing ECUTest-integrated Python automation,
common static analysis findings include:

| Finding | Code Pattern | Risk |
|---------|-------------|------|
| Unchecked return value | `ecu_test.execute_test_case("abs_test")` without checking result | Execution failure silently ignored |
| Hardcoded file path | `arxml_path = "C:\\Users\\ioa1cob\\abs.arxml"` | Works on one machine only |
| Missing timeout | `can_bus.wait_for_message(0x1A0)` with no timeout parameter | Test hangs indefinitely |
| Magic number | `assert signal_value == 5000` | Meaning unclear — should be named constant |
```python
# VIOLATIONS — static analysis catches all four
def test_abs_signal_defective():
    ecu_test.execute_test_case("abs_wheel_speed")  # W0611 return not checked
    arxml = load_arxml("C:\\Users\\ioa1cob\\config\\abs.arxml")  # S603 hardcoded path
    msg = can_bus.wait_for_message(0x1A0)  # missing timeout — hangs
    assert msg.data[0] == 5000  # W0104 magic number

# CORRECT — all violations resolved
WHEEL_SPEED_FL_RAW_50KMH = 5000  # Named constant — meaning clear

def test_abs_signal_correct(config: dict) -> None:
    """Verify WheelSpeedFL raw value at 50 km/h."""
    result = ecu_test.execute_test_case("abs_wheel_speed")
    assert result.passed, f"ECUTest execution failed: {result.error}"

    arxml = load_arxml(config["arxml_path"])  # From config — not hardcoded
    msg = can_bus.wait_for_message(
        message_id=0x1A0,
        timeout_seconds=2.0  # Explicit timeout
    )
    assert msg.data[0] == WHEEL_SPEED_FL_RAW_50KMH  # Named constant
```

---

## 7. Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| Static analysis only on production code | TAF accumulates defects undetected | Apply same tools to testware as product code |
| No pipeline enforcement | Violations committed under time pressure | Pipeline blocks on critical violations |
| All violations treated equally | Team ignores low-severity noise | Classify severity — only critical blocks |
| No baseline for legacy code | All 500 existing violations block pipeline on day 1 | Create baseline file for existing code |
| Complexity ignored | TAF functions become untestable and defect-prone | Set complexity threshold — refactor above limit |
| Security check skipped | Hardcoded credentials in test config | `bandit` in pipeline catches this class |

---

## 8. Architect Insights

> ⭐ **Static analysis on testware is not optional
> for a professional TAF.** It is the baseline
> quality gate for test code. A team that applies
> static analysis to production code but not to
> testware is applying inconsistent quality standards
> to the very tool that measures product quality.

> **The unused variable finding is worth the entire
> static analysis investment on its own.**
> One unused variable in an assertion means one
> test that has never verified anything — ever.
> In a 400-test suite running for 18 months, that
> is 18 months of false confidence.

> **Complexity thresholds prevent technical debt
> accumulation.** A TAF function with complexity
> 20 cannot be unit tested comprehensively.
> It cannot be maintained without introducing
> new defects. The threshold enforces architectural
> cleanliness before the damage is permanent.

> **For automotive pipelines:**
> Static analysis of testware belongs in the same
> pipeline stage as static analysis of production
> code — the build stage. Both run on every commit.
> Both must pass before any deployment occurs.

---

## 9. Reflection Questions

1. Your team's TAF has been in production for
   two years with no static analysis. You run
   flake8 for the first time and find 847 violations.
   Describe your strategy for introducing static
   analysis enforcement without blocking the
   pipeline for two weeks while all violations
   are fixed.

2. A pylint run on your ABS TAF reports 12 instances
   of W0612 (unused variable). You investigate and
   find that in 4 of the 12 cases, the variable
   was supposed to be used in an assertion that was
   never written. What is the impact on your test
   results, and how do you prioritise fixing these
   versus the other 8 style violations?

3. Your TAF has a function `validate_ecu_response`
   with cyclomatic complexity 18. A code review
   shows it handles 6 different UDS service types
   with nested conditionals. Static analysis flags
   it as critical. How do you refactor it to reduce
   complexity while preserving its functionality?

4. A new TAE argues that static analysis slows
   down the pipeline unnecessarily — "we can just
   do code reviews instead." Compare the effectiveness
   of static analysis versus code review for
   detecting the unused variable pattern in a
   400-line test file, and justify your conclusion.

5. Your pipeline runs flake8 on the TAF and passes.
   It does not run bandit. A security audit of
   the CI server discovers that test configuration
   files contain ECU diagnostic credentials in
   plaintext. Which static analysis tool would
   have caught this, and what is the correct
   fix for credential management in testware?

---

## 10. Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Run `flake8 framework-prototype/` on your current code and categorise findings by severity | `framework-prototype/` |
| 2 | Add `static_analysis` job to your pipeline that blocks on critical violations | `chapter-05-cicd-deployment/pipeline_examples/` |
| 3 | Run `radon cc framework-prototype/ -s` and refactor any function with complexity grade C or worse | `framework-prototype/core/` |

---

*Next: Chapter 7 Scenarios — then Chapter 8 — Continuous Improvement*