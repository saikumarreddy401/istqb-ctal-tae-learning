# Sub-Chapter 7.1.2 — Verifying Correct Behavior of the TAS

> **Syllabus Reference:** TAE-7.1.2
> **Cognitive Level:** K3 — Apply
> **Chapter:** 7 — Verifying the Test Automation Solution
> **Status:** ✅ Complete

---

## 1. Concept Explanation

### The Core Problem — Who Tests the Tests?

Test automation is software. Software contains defects.
If the TAF contains defects, it produces wrong results —
and the team trusts those wrong results because they
come from automation.

> ⭐ **The TAF must be verified just as the SUT
> is verified. A TAF that has never been tested
> is an untested quality gate.**
>
> A TAF defect is more dangerous than a product
> defect because it affects every test that uses
> the defective component — silently.

### What "Correct Behavior" Means for a TAS

A TAS behaves correctly when:

| Behavior | Definition |
|----------|-----------|
| True positive | Detects a real product defect — test fails |
| True negative | Confirms correct product behavior — test passes |
| False positive | Reports failure when product is correct — test defect |
| False negative | Reports pass when product is defective — most dangerous |

> ⭐ **False negatives are the critical failure mode.**
> The product is defective. The test passes.
> The defect reaches the field.
> This is the consequence of an unverified TAS.

---

## 2. Methods for Verifying TAS Correct Behavior

### Method 1 — Testing the TAF with Known Inputs

Provide the TAF with inputs where the expected output
is known, and verify the TAF produces the correct result.

This is unit testing applied to the TAF itself:
```python
import pytest
from unittest.mock import MagicMock
from core.can_signal_monitor import CanSignalMonitor

class TestCanSignalMonitorBehavior:
    """
    Unit tests for the CAN signal monitor component.
    Verifies correct behavior with known inputs.
    """

    def test_signal_within_tolerance_passes(self):
        """
        Given: WheelSpeedFL = 50.0 km/h, expected = 50.0 km/h
        Tolerance: ±0.5 km/h
        Expected TAF behavior: PASS assertion
        """
        monitor = CanSignalMonitor(tolerance=0.5)
        result = monitor.assert_signal_value(
            signal_name="WheelSpeedFL",
            actual_value=50.0,
            expected_value=50.0
        )
        assert result.passed is True

    def test_signal_outside_tolerance_fails(self):
        """
        Given: WheelSpeedFL = 51.0 km/h, expected = 50.0 km/h
        Tolerance: ±0.5 km/h
        Expected TAF behavior: FAIL assertion — deviation = 1.0 km/h
        """
        monitor = CanSignalMonitor(tolerance=0.5)
        result = monitor.assert_signal_value(
            signal_name="WheelSpeedFL",
            actual_value=51.0,
            expected_value=50.0
        )
        assert result.passed is False
        assert result.deviation == pytest.approx(1.0)

    def test_boundary_value_at_upper_tolerance(self):
        """
        Given: actual = 50.5 km/h, expected = 50.0 km/h
        Tolerance: ±0.5 km/h — boundary condition
        Expected TAF behavior: PASS — exactly at limit
        """
        monitor = CanSignalMonitor(tolerance=0.5)
        result = monitor.assert_signal_value(
            signal_name="WheelSpeedFL",
            actual_value=50.5,
            expected_value=50.0
        )
        assert result.passed is True

    def test_signal_name_mismatch_raises_error(self):
        """
        Given: Unknown signal name requested
        Expected TAF behavior: raise SignalNotFoundError
        Not silently return zero or None
        """
        monitor = CanSignalMonitor(tolerance=0.5)
        with pytest.raises(SignalNotFoundError):
            monitor.assert_signal_value(
                signal_name="NonExistentSignal",
                actual_value=50.0,
                expected_value=50.0
            )
```

> These tests verify the TAF component — not the ECU.
> The ECU is replaced by known input values.
> The question being answered: does the monitor
> correctly classify pass, fail, and error conditions?

### Method 2 — Mutation Testing

Deliberately introduce a known defect into the SUT
(or a SUT simulator) and verify the TAF detects it.

> ⭐ **Mutation testing answers: "Would this test
> actually catch a defect if one existed?"**
> A test that passes with a deliberately broken
> SUT is not providing value — it has a false
> negative defect.
```python
class AbsEcuSimulator:
    """
    Simulates ABS ECU behavior for TAF verification.
    Can inject known defects to verify TAF detection.
    """

    def __init__(self, inject_defect: bool = False):
        self.inject_defect = inject_defect

    def get_wheel_speed_fl(self, vehicle_speed: float) -> float:
        """
        Return WheelSpeedFL signal value.
        Correct: matches vehicle speed within tolerance.
        Defective: returns zero regardless of vehicle speed.
        """
        if self.inject_defect:
            return 0.0  # ← Known defect: signal stuck at zero
        return vehicle_speed

def test_taf_detects_wheel_speed_stuck_zero():
    """
    Verify that TAF correctly detects WheelSpeedFL
    stuck-at-zero defect using ECU simulator.
    This test verifies the TAF — not the real ECU.
    """
    defective_ecu = AbsEcuSimulator(inject_defect=True)
    monitor = CanSignalMonitor(tolerance=0.5)

    actual = defective_ecu.get_wheel_speed_fl(vehicle_speed=50.0)

    result = monitor.assert_signal_value(
        signal_name="WheelSpeedFL",
        actual_value=actual,
        expected_value=50.0
    )

    # TAF must detect the defect — result must be FAIL
    assert result.passed is False, (
        "TAF failed to detect stuck-at-zero defect. "
        "False negative in signal monitor component."
    )
```

### Method 3 — Dual Verification

Run two independent implementations of the same
assertion logic and compare results. If they disagree,
at least one is defective.

| Implementation A | Implementation B | Outcome |
|-----------------|-----------------|---------|
| Custom signal monitor | Direct CAN frame parser | Both agree → high confidence |
| ECUTest built-in assertion | Python assertion | Both agree → cross-validation |
| New TAF version | Previous stable version | Disagree → regression in new version |

> Dual verification is especially useful during
> TAF refactoring. Running old and new versions
> in parallel on the same test inputs reveals
> behavioral regressions before the old version
> is retired.

### Method 4 — Oracle Testing

An oracle is a trusted reference that provides
the expected output for a given input.

| Oracle Type | Automotive Example |
|------------|-------------------|
| Manual calculation | Calculate expected wheel speed from vehicle speed manually, compare to TAF assertion |
| Specification document | ARXML defines signal scaling — verify TAF applies same scaling |
| Reference implementation | ECUTest report vs custom Python report — same test, compare results |
| Historical baseline | Results from stable previous release as reference |
```python
def test_signal_scaling_matches_arxml_specification():
    """
    Oracle: ARXML defines WheelSpeedFL scaling as 0.01 km/h per bit.
    Raw value 5000 bits → physical value 50.0 km/h.
    Verify TAF applies correct scaling from ARXML — not hardcoded.
    """
    arxml_loader = ArxmlLoader("config/abs_v2.4.arxml")
    scaling = arxml_loader.get_signal_scaling("WheelSpeedFL")

    # Oracle: manual calculation
    raw_value = 5000
    expected_physical = raw_value * scaling  # = 50.0 km/h

    # TAF calculation
    monitor = CanSignalMonitor(arxml_path="config/abs_v2.4.arxml")
    actual_physical = monitor.raw_to_physical("WheelSpeedFL", raw_value)

    assert actual_physical == pytest.approx(expected_physical, abs=0.01), (
        f"TAF scaling error: expected {expected_physical}, "
        f"got {actual_physical}. "
        f"Check ARXML loader for WheelSpeedFL."
    )
```

---

## 3. What Must Be Verified in a TAS

> ⭐ Every layer of the TAF is a verification target.
> Defects at lower layers affect everything above them.

| TAF Layer | What to Verify | Method |
|-----------|---------------|--------|
| Core libraries | Signal reading, UDS communication, logging | Unit tests with known inputs |
| Business logic | ABS flow sequences, fault injection logic | Unit tests + mutation testing |
| Test scripts | Correct use of business logic, right assertions | Code review + integration test |
| Test data | Calibration values match ARXML scaling | Oracle testing against specification |
| Configuration | Required keys present, correct format | Configuration validation |
| Reporting | Correct pass/fail classification, accurate counts | Known-input report generation test |

### Reporting Layer Verification Example
```python
def test_report_generator_counts_correctly():
    """
    Verify report generator correctly counts
    pass, fail, blocked, and error results.
    Known input: 3 pass, 2 fail, 1 error, 1 blocked.
    Expected output: exact counts in report.
    """
    known_results = [
        TestResult("test_1", "PASS"),
        TestResult("test_2", "PASS"),
        TestResult("test_3", "PASS"),
        TestResult("test_4", "FAIL"),
        TestResult("test_5", "FAIL"),
        TestResult("test_6", "ERROR"),
        TestResult("test_7", "BLOCKED"),
    ]

    report = ReportGenerator().generate(known_results)

    assert report.passed == 3
    assert report.failed == 2
    assert report.errors == 1
    assert report.blocked == 1
    assert report.pass_rate == pytest.approx(60.0)  # 3/5 executed
```

> A report generator that miscounts results
> produces incorrect pass rates. If the pass rate
> is wrong, every release decision based on it
> is made on false data.

---

## 4. TAS Verification in the CI/CD Pipeline

> ⭐ TAF unit tests must run in the build pipeline —
> before the TAF is used to test the product.
> A TAF with failing unit tests must not be used
> for product testing.
```yaml
# Pipeline: verify TAF before using it
jobs:
  verify_taf:
    steps:
      - name: Run TAF unit tests
        run: pytest tests/taf_unit_tests/
          --junit-xml=results/taf_verification.xml

      - name: Run TAF mutation tests
        run: pytest tests/taf_mutation_tests/
          --junit-xml=results/taf_mutation.xml

  run_product_tests:
    needs: verify_taf  # ← TAF must be verified before use
    steps:
      - name: Run ABS regression suite
        run: pytest tests/abs_regression/
```

---

## 5. Automotive Domain — TAS Verification Architecture

### Verification Targets in ABS TAF

| Component | Verification Method | Defect It Catches |
|-----------|-------------------|------------------|
| `can_signal_monitor.py` | Unit tests with raw CAN frames | Wrong scaling, wrong byte order |
| `xcp_connection_handler.py` | Mock XCP server, known responses | Connection timeout not handled |
| `abs_signal_flows.py` | Mutation test with defective ECU sim | Flow sequence wrong order |
| `fault_injection_sequences.py` | Known-input test, verify DTC appears | Fault not actually injected |
| `test_logger.py` | Known-input log, verify output format | Log level filtering wrong |
| `report_generator.py` | Known results set, verify counts | Pass rate calculation error |

### False Negative Risk in Automotive

> ⭐ In automotive safety testing, a false negative
> means: a safety-relevant defect in the ECU was
> not detected by the test suite. This defect
> reaches production. It may cause injury.
>
> TAF verification is not a quality-of-life
> improvement — in safety-critical automotive
> testing it is a safety obligation.

---

## 6. Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| No unit tests for TAF | TAF defects undetected — silent false negatives | Treat TAF as production code — unit test every component |
| Mutation testing skipped | TAF passes despite defective SUT | Run mutation tests on safety-critical assertion logic |
| TAF tests not in pipeline | TAF defects deployed to CI | Mandatory TAF verification job before product tests |
| Only happy path tested | TAF handles normal input, fails on edge cases | Test boundary values and error conditions |
| Report generator not verified | Incorrect counts in release reports | Unit test report generator with known result sets |

---

## 7. Architect Insights

> ⭐ **Apply the same quality standards to the TAF
> that you apply to the product under test.**
> If the product requires unit tests, code review,
> and static analysis — so does the TAF.
> There is no logical reason to hold test code
> to a lower standard than production code.

> **Mutation testing is the highest-value TAF
> verification technique.** It directly answers:
> "Would this test catch the defect it was designed
> to catch?" All other methods verify structure.
> Mutation testing verifies effectiveness.

> **For automotive:**
> Every assertion in a safety-critical test case
> should have a corresponding mutation test that
> verifies the assertion is sensitive to the
> specific failure mode it is designed to detect.
> Generic assertions are not sufficient.

> **The false negative is the enemy.**
> Design all TAF verification activities around
> preventing false negatives — not just ensuring
> the TAF runs without crashing.

---

## 8. Reflection Questions

1. Your ABS TAF signal monitor has been in use for
   18 months. A code review reveals that the
   tolerance check uses `<` instead of `<=`, meaning
   a signal exactly at the tolerance boundary is
   incorrectly classified as a failure. This is a
   false positive defect. How would a boundary value
   unit test have caught this 18 months ago, and
   what is the cost of finding it now?

2. A TAE argues that TAF verification is unnecessary
   because "if the tests pass in the pipeline,
   the TAF must be working." Explain why this
   reasoning is flawed using the concept of
   false negatives.

3. You are implementing mutation testing for the
   ABS fault injection component. Define three
   specific mutations you would inject into the
   ECU simulator to verify that the TAF correctly
   detects each failure mode.

4. Your team refactors the CAN signal monitor to
   support a new signal encoding format. The old
   unit tests all pass. However, two weeks later
   a field defect is found that the test suite
   missed. Describe a dual verification strategy
   that would have caught the regression during
   the refactoring.

5. A new TAE on your team writes a test that calls
   `assert result is not None` as its only assertion
   for a UDS response. Explain why this assertion
   is insufficient for TAF correctness verification
   and what additional assertions are needed.

---

## 9. Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Write unit tests for `can_signal_monitor.py` covering pass, fail, boundary, and error conditions | `framework-prototype/tests/` |
| 2 | Create one mutation test using `AbsEcuSimulator` for the most safety-critical assertion in your suite | `framework-prototype/tests/` |
| 3 | Add a `verify_taf` pipeline job that runs TAF unit tests before product tests | `chapter-05-cicd-deployment/pipeline_examples/` |

---

*Next: Sub-Chapter 7.1.3 — Dealing with Unexpected Test Results*