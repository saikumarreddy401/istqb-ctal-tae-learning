# Scenarios — Sub-Chapter 7.1.3 — Dealing with Unexpected Test Results

> **Syllabus Reference:** TAE-7.1.3
> **Cognitive Level:** K3 — Apply
> **File:** scenarios_7_1_3_unexpected_results.md
> **Status:** ✅ Complete

---

## Scenario 1 — Root Cause Classification (K3)

### Situation

Monday morning ABS regression produces this result:
```
test_abs_wheel_speed_fl_normal_braking   FAIL
AssertionError: WheelSpeedFL=0.0, expected=50.0±0.5
```

This test passed every run for the previous
six weeks. No product changes were deployed
over the weekend. The test runs on HIL Rack-2.

You run the test again immediately — it fails again.
You run the same test on Rack-1 — it passes.

### Question

Walk through the three-category classification.
State your conclusion and the exact action you take.
Specify what you do NOT do and why.

### Answer

**Step 1 — Reproduce:**
> Reproduced consistently on Rack-2.
> Does not reproduce on Rack-1.
> This is a rack-specific failure — not random.

**Step 2 — Classify using the three questions:**

| Question | Answer |
|----------|--------|
| Did environment change recently? | Unknown — check Rack-2 maintenance log |
| Does failure occur on known-good rack? | No — Rack-1 passes |
| Same test logic, same firmware — different rack? | Yes → points to environment |

> ⭐ **Classification: Environment issue.**
>
> Evidence: identical test, identical firmware,
> identical test code — different result on
> different rack. The variable is the environment.

**Step 3 — Action:**

| Action | Rationale |
|--------|-----------|
| Remove Rack-2 from pipeline rotation | Prevent further invalid results |
| Notify infrastructure team | Rack-2 hardware investigation required |
| Re-run full suite on Rack-1 | Produce valid results for release decision |
| Document investigation | Record evidence and classification |

**What you do NOT do:**

> Do NOT raise a product defect. The product is
> correct — Rack-1 proves this.
>
> Do NOT fix the test. The test is correct —
> it passes on Rack-1 with the same assertion.
>
> Do NOT re-run on Rack-2 hoping it will pass.
> The failure is consistent on Rack-2 — re-running
> wastes time without resolving the root cause.

---

## Scenario 2 — Shared State Contamination (K3)

### Situation

`test_abs_fault_memory_read` passes when run alone.
It fails when run as part of the full suite with:
```
AssertionError: Expected 0 confirmed DTCs.
Found: [0xC0051] confirmed.
```

You examine the test execution order. The test
that runs immediately before it is:
`test_abs_fault_injection_wheel_speed_sensor`

### Question A

Identify the root cause pattern and the TAF
design principle that was violated.

### Answer A

> ⭐ **Pattern: Shared state contamination.**
>
> `test_abs_fault_injection_wheel_speed_sensor`
> injects a fault — DTC 0xC0051 is created.
> The test does not clean up after itself.
> The next test finds a pre-existing DTC and fails.
>
> **Violated principle: Test atomicity.**
> Each test must start from and return to a
> known clean state — independent of execution order.
> A test that depends on the previous test's
> teardown is not atomic.

### Question B

Implement the fixture that resolves this
without modifying either test case.

### Answer B
```python
# conftest.py — project-wide fixture
import pytest

@pytest.fixture(autouse=True)
def reset_ecu_state_per_test(uds_client):
    """
    autouse=True — applies to every test automatically.
    Setup: verify clean state before test.
    Teardown: restore clean state after test.
    Neither test case needs modification.
    """
    # Setup — clear any DTCs from previous test
    uds_client.clear_diagnostic_information(group=0xFFFFFF)
    uds_client.diagnostic_session_control(session_type=0x01)

    yield  # Test executes here

    # Teardown — clean up after this test
    uds_client.clear_diagnostic_information(group=0xFFFFFF)
    uds_client.diagnostic_session_control(session_type=0x01)
```

> `autouse=True` applies the fixture to every
> test without requiring each test to request it.
> The fault injection test now leaves a clean ECU.
> The fault memory test always starts with no DTCs.
> Execution order no longer affects results.

### Question C

After adding this fixture, `test_abs_fault_injection`
now fails. Explain why and what the correct fix is.

### Answer C

> The fault injection test now has the fixture
> running teardown after it — which clears the
> DTC the test just injected before the assertion
> can read it.
>
> This reveals a test design problem: the assertion
> was reading the DTC after the teardown boundary.
```python
# DEFECTIVE — assertion after teardown would clear DTC
def test_abs_fault_injection_defective(uds_client, fault_injector):
    fault_injector.inject_wheel_speed_sensor_fault()
    # yield happens here in fixture — teardown clears DTC
    dtc = uds_client.read_dtc()           # ← DTC already cleared
    assert 0xC0051 in dtc.confirmed_list  # ← Fails

# CORRECT — assertion within test body, before teardown
def test_abs_fault_injection_correct(uds_client, fault_injector):
    fault_injector.inject_wheel_speed_sensor_fault()
    dtc = uds_client.read_dtc()           # ← Read BEFORE yield
    assert 0xC0051 in dtc.confirmed_list  # ← Passes
    # Fixture teardown clears DTC after assertion ✅
```

---

## Scenario 3 — Timing-Dependent Flaky Test (K3)

### Situation

`test_abs_activation_response_time` produces
these results over five consecutive runs:

| Run | Result | Duration |
|-----|--------|---------|
| 1 | PASS | 87ms |
| 2 | PASS | 91ms |
| 3 | FAIL | timeout |
| 4 | PASS | 83ms |
| 5 | FAIL | timeout |

Failure message:
```
AssertionError: ABSActivationFlag still 0 after 100ms.
Expected: 1
```

The test code:
```python
def test_abs_activation_response_time():
    simulator.apply_brake(pressure_bar=150)
    time.sleep(0.1)  # 100ms hardcoded sleep
    flag = can_monitor.read_signal("ABSActivationFlag")
    assert flag == 1
```

### Question

Classify this failure, identify the root cause,
and implement the correct fix.

### Answer

> **Classification: Test defect — timing dependency.**
>
> The failure is not a product defect. The ECU
> activates ABS correctly — but sometimes takes
> longer than 100ms depending on CAN bus load
> and ECU processing time. The hardcoded sleep
> is not a reliable wait mechanism.
>
> Root cause: `time.sleep(0.1)` assumes ECU always
> responds within exactly 100ms. This is fragile —
> it fails whenever the ECU is slightly slower.
```python
# CORRECT — signal-based wait with explicit timeout
def test_abs_activation_response_time():
    """
    Verify ABS activates within 2 seconds of
    brake application at 150 bar.
    Uses signal-based wait — not hardcoded sleep.
    """
    simulator.apply_brake(pressure_bar=150)

    # Wait for signal change — poll until value or timeout
    abs_flag = can_monitor.wait_for_signal(
        signal_name="ABSActivationFlag",
        expected_value=1,
        timeout_seconds=2.0,
        poll_interval_seconds=0.01
    )

    assert abs_flag == 1, (
        "ABS did not activate within 2 seconds of "
        "brake application at 150 bar. "
        "Check ABS activation logic in firmware."
    )
```
```python
# wait_for_signal implementation
def wait_for_signal(
    self,
    signal_name: str,
    expected_value: float,
    timeout_seconds: float,
    poll_interval_seconds: float = 0.01
) -> float:
    """
    Poll signal until expected value or timeout.
    Returns actual value — caller asserts.
    """
    import time
    deadline = time.monotonic() + timeout_seconds

    while time.monotonic() < deadline:
        actual = self.read_signal(signal_name)
        if abs(actual - expected_value) < self.tolerance:
            return actual
        time.sleep(poll_interval_seconds)

    # Timeout — return last read value for assertion message
    return self.read_signal(signal_name)
```

> ⭐ The fix changes the wait strategy from
> time-based to signal-based. The test now waits
> as long as needed (up to 2 seconds) and only
> fails if the ECU genuinely did not respond
> within the specified window.
> The 2-second timeout is derived from the
> specification — not from observation.

---

## Scenario 4 — False Negative Investigation (K3)

### Situation

A field defect is reported: ABS does not activate
on WheelSpeedFL dropout (signal stuck at zero
while vehicle is moving). The automated test suite
has been running for 8 months with 100% pass rate
on the `test_abs_fl_dropout` test case.

Code review of the test reveals:
```python
def test_abs_fl_dropout():
    simulator.set_vehicle_speed(80.0)
    simulator.inject_wheel_speed_fl_dropout()

    response = uds_client.read_data_by_identifier(did=0xF401)
    assert response is not None
    assert response.positive_response_code == 0x62
```

### Question A

Identify why this test produced false negatives
for 8 months.

### Answer A

> ⭐ The assertions only verify that the ECU
> responded to the UDS request — not that the
> ECU correctly handled the FL dropout condition.
>
> `response is not None` → ECU is powered on
> `response.positive_response_code == 0x62` → UDS DID read succeeded
>
> Neither assertion checks:
> - Whether ABS activated in response to the dropout
> - Whether DTC C0051 (wheel speed sensor fault) was set
> - Whether the ECU entered a safe state
> - Whether the remaining three wheel speeds were used
>
> The ECU could completely ignore the FL dropout
> and both assertions would still pass.

### Question B

Rewrite the test with assertions that would
have caught the defect.

### Answer B
```python
def test_abs_fl_dropout_correct():
    """
    Verify ECU correctly handles WheelSpeedFL dropout:
    1. DTC C0051 must be set (fault detected)
    2. ABS must activate using remaining 3 wheel speeds
    3. ABSActivationFlag must be set
    4. WheelSpeedFL must be marked invalid in ECU data
    """
    simulator.set_vehicle_speed(80.0)
    simulator.apply_brake(pressure_bar=150)
    simulator.inject_wheel_speed_fl_dropout()

    # 1. Verify ECU detected the fault
    dtc_response = uds_client.read_dtc_information(
        sub_function=0x02, status_mask=0x08
    )
    assert 0xC0051 in dtc_response.dtc_list, (
        "DTC C0051 not set after WheelSpeedFL dropout. "
        "ECU may not be detecting sensor fault."
    )

    # 2. Verify ABS activates despite FL dropout
    abs_flag = can_monitor.wait_for_signal(
        "ABSActivationFlag", expected_value=1, timeout_seconds=2.0
    )
    assert abs_flag == 1, (
        "ABS did not activate after WheelSpeedFL dropout "
        "during braking at 80 km/h. Safety-critical failure."
    )

    # 3. Verify FL signal marked invalid in ECU response
    response = uds_client.read_data_by_identifier(did=0xF401)
    assert response.wheel_speed_fl_valid is False, (
        "ECU reports WheelSpeedFL as valid during dropout. "
        "Signal validity flag not set correctly."
    )

    # 4. Verify remaining wheel speeds still valid
    assert response.wheel_speed_fr_valid is True
    assert response.wheel_speed_rl_valid is True
    assert response.wheel_speed_rr_valid is True
```

> ⭐ Each assertion now checks a specific behavior
> that would be wrong if the defect existed.
> The field defect — ABS not activating on FL
> dropout — would have failed assertion 2 on
> day one of the test suite.

---

## Scenario 5 — Investigation Documentation (K3)

### Situation

Your team has 12 unexpected results this week.
The test manager asks for a summary of root
cause classifications. The team has no
investigation log — findings exist only in
engineers' heads and Slack messages.

Three of the twelve results are later found
to involve the same root cause: a hardware
fault on HIL Rack-3. Without documentation,
this pattern is invisible.

### Question

Define the minimum investigation log structure
your team must adopt, and explain how it would
have revealed the Rack-3 pattern earlier.

### Answer

**Minimum investigation log — one row per result:**

| Field | Example Entry |
|-------|-------------|
| Test ID | test_abs_wheel_speed_fl_normal_braking |
| Date | 2024-03-15 |
| Pipeline run | nightly-run-447 |
| SUT version | ABS SW v2.4.0 |
| Environment | HIL Rack-3 |
| Failure message | WheelSpeedFL=0.0, expected=50.0 |
| Reproduced | Yes — consistent on Rack-3 only |
| Classification | Environment |
| Root cause | CAN interface hardware fault on Rack-3 |
| Action | Rack-3 removed from rotation |
| Resolved | Yes — Rack-3 CAN interface replaced |

**How documentation reveals the pattern:**

> With a log, three entries in one week all showing:
> - Environment: HIL Rack-3
> - Classification: Environment
> - Failure: CAN signal read failure
>
> Are immediately visible as a cluster when
> sorted by environment. Without the log,
> engineer A investigates one failure,
> engineer B investigates another, and
> neither knows the other found the same root cause.
>
> The log converts three independent investigations
> into one pattern — identified after the
> first entry, not after all three.

**Implementation — simple CSV log:**
```python
import csv
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class InvestigationEntry:
    test_id: str
    date: str
    pipeline_run: str
    sut_version: str
    environment: str
    failure_message: str
    reproduced: str
    classification: str  # product / test / environment / flaky
    root_cause: str
    action: str
    resolved: str

def log_investigation(entry: InvestigationEntry,
                      log_path: str = "investigation_log.csv") -> None:
    """Append investigation entry to team log."""
    with open(log_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=asdict(entry).keys())
        writer.writerow(asdict(entry))
```

---

## Quick Reference — Root Cause Classification

| Symptom | Most Likely Classification | First Check |
|---------|--------------------------|------------|
| Passes on one rack, fails on another | Environment | Rack hardware and config comparison |
| Passes alone, fails in suite | Test — shared state | DTC or session state after previous test |
| Fails intermittently, no product change | Test — timing dependency | Replace sleep with signal-based wait |
| Passes in CI, defect in field | Test — weak assertion | Review assertion specificity |
| Fails after specific code change only | Product defect | Raise defect — evidence is the code change |
| Fails consistently, same environment | Product or test defect | Isolate step by step |

---

*Next: Scenarios 7.1.4 — Static Analysis*