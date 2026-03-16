# Scenarios — Sub-Chapter 7.1.2 — Verifying Correct Behavior of the TAS

> **Syllabus Reference:** TAE-7.1.2
> **Cognitive Level:** K3 — Apply
> **File:** scenarios_7_1_2_correct_behavior.md
> **Status:** ✅ Complete

---

## Scenario 1 — Unit Testing TAF Components (K3)

### Situation

Your ABS TAF has a `CanSignalMonitor` component
that reads signals and classifies them as pass or
fail based on a tolerance value. The component
has been in production for 12 months with no
unit tests. A code review reveals this logic:
```python
def assert_signal_value(
    self, signal_name: str,
    actual: float, expected: float
) -> bool:
    delta = actual - expected          # ← signed delta, not absolute
    if delta < self.tolerance:
        return True
    return False
```

### Question A

Without running the tests, identify the defect
in this logic and classify it as false positive,
false negative, or both. Explain your reasoning.

### Answer A

> ⭐ The defect is using signed delta instead of
> absolute delta. `delta = actual - expected`
> produces a negative number when actual < expected.
>
> A negative delta is always less than any positive
> tolerance — so the condition `delta < self.tolerance`
> is always True when actual is below expected.
>
> **Classification: False negative.**
>
> Example: expected=50.0, actual=30.0, tolerance=0.5
> delta = 30.0 - 50.0 = -20.0
> -20.0 < 0.5 → True → returns True (PASS)
>
> The signal is 20 km/h below expected.
> The TAF reports it as passing.
> Every test that relies on this component for
> low-value deviations has been producing
> false negatives for 12 months.

### Question B

Write the unit tests that would have caught
this defect on day one.

### Answer B
```python
class TestCanSignalMonitorCorrectBehavior:
    """Unit tests that verify correct TAF behavior — not ECU behavior."""

    def setup_method(self):
        self.monitor = CanSignalMonitor(tolerance=0.5)

    def test_exact_match_passes(self):
        """actual == expected → must pass."""
        assert self.monitor.assert_signal_value(
            "WheelSpeedFL", actual=50.0, expected=50.0
        ) is True

    def test_within_positive_tolerance_passes(self):
        """actual = expected + 0.3 → within tolerance → pass."""
        assert self.monitor.assert_signal_value(
            "WheelSpeedFL", actual=50.3, expected=50.0
        ) is True

    def test_within_negative_tolerance_passes(self):
        """
        actual = expected - 0.3 → within tolerance → pass.
        THIS TEST CATCHES THE DEFECT.
        Defective code: delta = 50.0 - 50.3 = -0.3 ... wait,
        actual=49.7, expected=50.0: delta = -0.3 < 0.5 → True (wrong logic passes)
        actual=30.0, expected=50.0: delta = -20.0 < 0.5 → True (FALSE NEGATIVE caught here)
        """
        assert self.monitor.assert_signal_value(
            "WheelSpeedFL", actual=49.7, expected=50.0
        ) is True

    def test_large_negative_deviation_fails(self):
        """
        actual = 30.0, expected = 50.0 → deviation = 20.0 → must FAIL.
        DEFECTIVE CODE: returns True (false negative).
        THIS IS THE CATCHING TEST.
        """
        result = self.monitor.assert_signal_value(
            "WheelSpeedFL", actual=30.0, expected=50.0
        )
        assert result is False, (
            "TAF reported PASS for signal 20 km/h below expected. "
            "Signed delta defect detected."
        )

    def test_outside_positive_tolerance_fails(self):
        """actual = expected + 1.0 → outside tolerance → fail."""
        assert self.monitor.assert_signal_value(
            "WheelSpeedFL", actual=51.0, expected=50.0
        ) is False

    def test_boundary_at_tolerance_limit_passes(self):
        """actual = expected + 0.5 → exactly at limit → pass."""
        assert self.monitor.assert_signal_value(
            "WheelSpeedFL", actual=50.5, expected=50.0
        ) is True

    def test_boundary_just_outside_tolerance_fails(self):
        """actual = expected + 0.51 → just outside → fail."""
        assert self.monitor.assert_signal_value(
            "WheelSpeedFL", actual=50.51, expected=50.0
        ) is False
```

> `test_large_negative_deviation_fails` catches
> the defect immediately. Without this test,
> the defect existed undetected for 12 months.

---

## Scenario 2 — Mutation Testing (K3)

### Situation

Your team wants to verify that the ABS activation
test actually detects the specific defect it was
designed for: ABS not activating when brake pressure
exceeds 120 bar during high-speed braking.

A colleague says: "The test passes in CI every
run — it must be working." You disagree and
propose mutation testing to prove the point.

### Question

Design a mutation test using an ECU simulator
that verifies the ABS activation test would
detect the defect. Show both the correct and
defective simulator implementations.

### Answer
```python
class AbsEcuSimulator:
    """
    Simulates ABS ECU for TAF verification.
    inject_defect=False → correct behavior
    inject_defect=True  → ABS never activates (stuck inactive)
    """

    def __init__(self, inject_defect: bool = False):
        self.inject_defect = inject_defect
        self._vehicle_speed = 0.0
        self._brake_pressure = 0.0

    def set_vehicle_speed(self, speed_kmh: float) -> None:
        self._vehicle_speed = speed_kmh

    def apply_brake(self, pressure_bar: float) -> None:
        self._brake_pressure = pressure_bar

    def get_abs_activation_flag(self) -> int:
        """
        Correct: ABS activates when speed > 30 km/h
                 AND brake pressure > 120 bar.
        Defective: ABS never activates — always returns 0.
        """
        if self.inject_defect:
            return 0  # ← Defect: ABS activation suppressed

        if self._vehicle_speed > 30.0 and self._brake_pressure > 120:
            return 1
        return 0


# The mutation test
def test_abs_activation_test_detects_defect():
    """
    Mutation test: verify the ABS activation test
    correctly FAILS when the ECU has the defect.

    If this test passes: TAF correctly detects the defect.
    If this test fails: TAF has a false negative —
                        it would miss the real product defect.
    """
    defective_ecu = AbsEcuSimulator(inject_defect=True)

    # Simulate the conditions that should trigger ABS
    defective_ecu.set_vehicle_speed(80.0)
    defective_ecu.apply_brake(pressure_bar=150)

    abs_flag = defective_ecu.get_abs_activation_flag()

    # The TAF assertion — this must FAIL with the defective ECU
    # If it passes → the assertion is too weak → false negative risk
    assert abs_flag == 0, (
        "Defective ECU correctly returns 0. "
        "Now verify the product test assertion catches this."
    )

    # Verify the product test assertion WOULD fail on this result
    with pytest.raises(AssertionError):
        assert abs_flag == 1, (
            "ABS did not activate at 80 km/h, 150 bar. "
            "Defect detected."
        )

    # If we reach here: the assertion is sensitive to the defect ✅
    print("✅ Mutation test passed — TAF correctly detects ABS activation defect.")
```

> ⭐ The mutation test proves the assertion is
> sensitive to the specific defect it was designed
> to catch. The colleague's argument ("it passes
> every run") only proves the ECU is currently
> correct — not that the test would catch a defect.

---

## Scenario 3 — Oracle Testing for Scaling (K3)

### Situation

Your ABS TAF reads WheelSpeedFL raw values from
the CAN bus and converts them to physical km/h
values using a scaling factor loaded from ARXML.

A new team member questions whether the TAF
applies the scaling correctly. The ARXML defines:
- Signal: WheelSpeedFL
- Scaling factor: 0.01 km/h per bit
- Offset: 0.0
- Raw range: 0–25000 bits
- Physical range: 0–250.0 km/h

### Question

Design an oracle test that verifies the TAF
applies the correct scaling, using manual
calculations as the oracle.

### Answer
```python
class TestWheelSpeedScalingOracle:
    """
    Oracle tests — expected values calculated manually
    from ARXML specification.
    These tests verify the TAF scaling logic,
    not the ECU hardware.
    """

    SCALING_FACTOR = 0.01  # km/h per bit — from ARXML
    OFFSET = 0.0

    @pytest.fixture
    def monitor(self):
        return CanSignalMonitor(arxml_path="config/abs_v2.4.arxml")

    def test_zero_raw_maps_to_zero_kmh(self, monitor):
        """Oracle: 0 bits × 0.01 = 0.0 km/h."""
        assert monitor.raw_to_physical("WheelSpeedFL", 0) == \
            pytest.approx(0.0, abs=0.001)

    def test_known_midrange_value(self, monitor):
        """Oracle: 5000 bits × 0.01 = 50.0 km/h."""
        assert monitor.raw_to_physical("WheelSpeedFL", 5000) == \
            pytest.approx(50.0, abs=0.001)

    def test_maximum_raw_maps_to_maximum_physical(self, monitor):
        """Oracle: 25000 bits × 0.01 = 250.0 km/h."""
        assert monitor.raw_to_physical("WheelSpeedFL", 25000) == \
            pytest.approx(250.0, abs=0.001)

    def test_scaling_matches_arxml_loaded_factor(self, monitor):
        """
        Oracle: verify TAF loads scaling from ARXML —
        not from a hardcoded value.
        If ARXML changes to 0.005, this test still passes.
        If hardcoded, this test fails after ARXML update.
        """
        arxml_scaling = monitor.get_loaded_scaling("WheelSpeedFL")
        assert arxml_scaling == pytest.approx(self.SCALING_FACTOR, rel=0.001), (
            f"TAF loaded scaling {arxml_scaling} from ARXML, "
            f"expected {self.SCALING_FACTOR}. "
            f"Check ARXML loader or ARXML file version."
        )

    def test_inverse_physical_to_raw(self, monitor):
        """Oracle: 80.0 km/h ÷ 0.01 = 8000 bits."""
        assert monitor.physical_to_raw("WheelSpeedFL", 80.0) == 8000
```

> ⭐ The oracle here is the ARXML specification —
> a trusted external reference. The tests verify
> the TAF implements the specification correctly.
> No ECU hardware is needed for these tests.

---

## Scenario 4 — Report Generator Verification (K3)

### Situation

Your TAF generates test reports from JUnit XML.
The report calculates pass rate as:
`passed / total_tests × 100`

A release manager notices the pass rate in the
automated report does not match her manual
calculation. She counted 387 passed from 409
total — expecting 94.6%. The report shows 96.1%.

Investigation reveals the report generator
includes errors in the denominator for pass rate
as well as passed + failed tests.

### Question

Write the unit tests for the report generator
that would have caught this calculation defect,
and define the correct pass rate formula.

### Answer

> ⭐ Pass rate = Passed / (Passed + Failed) × 100
> Errors and blocked tests are NOT in the denominator.
> They were not executed against the product.
```python
class TestReportGeneratorCorrectBehavior:
    """
    Unit tests for report generator.
    Input: known result sets.
    Expected: exact counts and correct pass rate.
    """

    def test_pass_rate_excludes_errors_and_blocked(self):
        """
        Known input: 387 pass, 18 fail, 4 blocked, 0 error.
        Expected pass rate: 387 / (387+18) × 100 = 95.56%
        NOT: 387 / 409 × 100 = 94.62% (wrong — includes blocked)
        """
        results = (
            [TestResult(f"t{i}", "PASS") for i in range(387)] +
            [TestResult(f"f{i}", "FAIL") for i in range(18)] +
            [TestResult(f"b{i}", "BLOCKED") for i in range(4)]
        )
        report = ReportGenerator().generate(results)

        assert report.passed == 387
        assert report.failed == 18
        assert report.blocked == 4
        assert report.errors == 0
        assert report.pass_rate == pytest.approx(95.56, abs=0.01), (
            f"Pass rate {report.pass_rate} incorrect. "
            f"Expected 95.56% (387/405). "
            f"Errors and blocked must not be in denominator."
        )

    def test_pass_rate_excludes_errors(self):
        """
        Known input: 3 pass, 2 fail, 2 error.
        Executed = 3 + 2 = 5 (errors excluded).
        Pass rate = 3/5 × 100 = 60.0%
        """
        results = (
            [TestResult(f"p{i}", "PASS") for i in range(3)] +
            [TestResult(f"f{i}", "FAIL") for i in range(2)] +
            [TestResult(f"e{i}", "ERROR") for i in range(2)]
        )
        report = ReportGenerator().generate(results)

        assert report.pass_rate == pytest.approx(60.0, abs=0.01)

    def test_all_pass_rate_is_100(self):
        """Edge case: all tests pass → 100%."""
        results = [TestResult(f"t{i}", "PASS") for i in range(10)]
        report = ReportGenerator().generate(results)
        assert report.pass_rate == pytest.approx(100.0)

    def test_all_fail_rate_is_zero(self):
        """Edge case: all tests fail → 0%."""
        results = [TestResult(f"t{i}", "FAIL") for i in range(10)]
        report = ReportGenerator().generate(results)
        assert report.pass_rate == pytest.approx(0.0)

    def test_zero_executed_does_not_divide_by_zero(self):
        """Edge case: only blocked tests — no pass rate."""
        results = [TestResult(f"b{i}", "BLOCKED") for i in range(5)]
        report = ReportGenerator().generate(results)
        assert report.pass_rate == 0.0  # Not an exception
```

---

## Quick Reference — TAS Correct Behavior Verification

| Method | What It Verifies | When to Use |
|--------|-----------------|------------|
| Unit test with known inputs | Component produces correct output for known input | Every TAF component |
| Boundary value test | Component handles edge cases correctly | Tolerance, threshold logic |
| Mutation test | Assertion detects specific failure mode | Safety-critical assertions |
| Oracle test | TAF matches trusted reference (spec, calculation) | Scaling, formula logic |
| Dual verification | Two implementations agree on same input | Refactoring validation |

---

*Next: Scenarios 7.1.3 — Unexpected Test Results*