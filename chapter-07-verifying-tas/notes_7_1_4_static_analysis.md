# Sub-Chapter 7.1.3 — Dealing with Unexpected Test Results

> **Syllabus Reference:** TAE-7.1.3
> **Cognitive Level:** K3 — Apply
> **Chapter:** 7 — Verifying the Test Automation Solution
> **Status:** ✅ Complete

---

## 1. Concept Explanation

### What Is an Unexpected Test Result?

An unexpected result is any test outcome that
cannot be immediately explained by known product
behavior or a known test change.

> ⭐ **Not every unexpected result is a product defect.**
> The TAE must investigate before concluding.
> Acting on an unclassified unexpected result
> leads to wrong decisions — either blocking a
> good release or shipping a defective product.

Three root cause categories exist for every
unexpected result:

| Category | Definition | Action |
|----------|-----------|--------|
| Product defect | SUT behavior does not match specification | Raise defect against product |
| Test defect | TAF assertion, logic, or data is wrong | Fix the test — not the product |
| Environment issue | Infrastructure failure — not product or test | Fix environment, re-run |

> ⭐ **Classifying the root cause correctly is
> the core skill of this sub-chapter.**
> Misclassification wastes engineering time or,
> worse, ships a defective product.

---

## 2. The Investigation Process

### Step 1 — Reproduce the Result

Before any investigation, attempt to reproduce
the result in the same environment.

| Reproduction Outcome | Interpretation |
|---------------------|---------------|
| Reproduces consistently | Stable failure — investigate root cause |
| Does not reproduce | Potential flaky test or transient environment issue |
| Reproduces on one rack only | Environment-specific issue |
| Reproduces after specific action | State-dependent failure |

> Never raise a product defect from a single
> non-reproducing failure. Always attempt
> reproduction first.

### Step 2 — Isolate the Failure

Narrow down the failure to the smallest possible
scope before hypothesising root cause.
```python
# Isolation strategy — binary search through test steps
def investigate_abs_activation_failure():
    """
    Full test: setup → drive → brake → assert ABS active
    
    Isolation steps:
    1. Run setup only → verify ECU state
    2. Run setup + drive → verify speed signal
    3. Run setup + drive + brake → verify brake pressure
    4. Run full test → reproduce failure at which step?
    """
    # Step 1: Is the ECU in the correct initial state?
    initial_state = verify_ecu_state()
    assert initial_state.session == "DEFAULT"
    assert initial_state.active_dtcs == []

    # Step 2: Is the wheel speed signal correct?
    simulator.set_vehicle_speed(80.0)
    wheel_speed = can_monitor.read_signal("WheelSpeedFL")
    assert abs(wheel_speed - 80.0) < 0.5  # Passes? → Step 3

    # Step 3: Is brake pressure signal correct?
    simulator.apply_brake(pressure_bar=120)
    brake_pressure = can_monitor.read_signal("BrakePressureFL")
    assert brake_pressure > 100  # Passes? → Step 4

    # Step 4: Full assertion — where does it fail?
    abs_active = can_monitor.read_signal("ABSActivationFlag")
    assert abs_active == 1  # ← Fails here
```

> Isolation identifies the exact step where the
> failure occurs. In this example: setup, speed,
> and brake signals are correct — the ABS activation
> flag is not set. The defect is in ABS activation
> logic — not in signal reading or test setup.

### Step 3 — Classify Root Cause

Apply the three-category classification:

**Classification questions — in order:**

| Question | If Yes → |
|----------|---------|
| Did the environment or tooling change recently? | Environment issue — investigate infrastructure first |
| Does the failure occur with a known-good SUT (simulator)? | Test defect — fix the test |
| Does the failure occur with correct test logic and environment? | Product defect — raise defect |

### Step 4 — Apply the Correct Action

| Root Cause | Action | Who Acts |
|-----------|--------|---------|
| Product defect | Raise defect with evidence | TAE raises, developer fixes |
| Test defect | Fix test code, re-run | TAE fixes |
| Environment issue | Fix infrastructure, re-run | TAE or infrastructure team |
| Flaky test | Quarantine, investigate timing/state | TAE investigates |

---

## 3. Common Unexpected Result Patterns

### Pattern 1 — Timing-Dependent Failure

**Symptom:** Test fails intermittently. Passes when
run slowly or in isolation, fails in full suite.

**Root cause:** Hardcoded sleep insufficient for
ECU response time under load.
```python
# DEFECTIVE — hardcoded sleep
def test_abs_activation_timing_defective():
    simulator.apply_brake(pressure_bar=150)
    time.sleep(0.1)  # ← Assumes ECU responds in 100ms
    abs_active = can_monitor.read_signal("ABSActivationFlag")
    assert abs_active == 1  # Flaky — fails when ECU is slow

# CORRECT — signal-based wait
def test_abs_activation_timing_correct():
    simulator.apply_brake(pressure_bar=150)
    
    # Wait for signal change, with timeout
    abs_active = can_monitor.wait_for_signal(
        signal_name="ABSActivationFlag",
        expected_value=1,
        timeout_seconds=2.0
    )
    assert abs_active == 1, (
        "ABS did not activate within 2 seconds of "
        "brake application at 150 bar"
    )
```

> ⭐ Replacing hardcoded sleeps with signal-based
> waits eliminates the most common class of
> timing-dependent flaky tests in HIL automation.

### Pattern 2 — Shared State Contamination

**Symptom:** Test fails when run after a specific
other test, passes when run in isolation.

**Root cause:** Previous test left ECU in an
unexpected state — active DTC, non-default session,
modified calibration parameter.
```python
# DEFECTIVE — no state reset between tests
def test_fault_injection_no_reset():
    fault_injector.inject_wheel_speed_sensor_fault()
    dtc = uds_client.read_dtc()
    assert 0xC0051 in dtc.confirmed_list
    # ← DTC remains active after test — contaminates next test

# CORRECT — fixture ensures clean state
@pytest.fixture(autouse=True)
def reset_ecu_state(uds_client):
    """Reset ECU to clean state before and after each test."""
    uds_client.clear_diagnostic_information(group=0xFFFFFF)
    uds_client.diagnostic_session_control(session=0x01)
    yield
    # Teardown — clean up after test
    uds_client.clear_diagnostic_information(group=0xFFFFFF)
    uds_client.diagnostic_session_control(session=0x01)
```

> ⭐ **Test atomicity:** every test must start from
> and return to a known clean state. A test that
> depends on previous test state is not atomic —
> and will produce unexpected results when
> execution order changes.

### Pattern 3 — Data Mismatch

**Symptom:** Test fails on assertion value only.
Signal is present and readable. Value is wrong.

**Root cause:** Test expected value does not match
current SUT version calibration.
```python
# DEFECTIVE — hardcoded expected value
def test_wheel_speed_scaling_defective():
    simulator.set_vehicle_speed(50.0)
    raw_value = can_monitor.read_raw("WheelSpeedFL")
    assert raw_value == 5000  # ← Hardcoded — breaks when scaling changes

# CORRECT — expected value derived from ARXML
def test_wheel_speed_scaling_correct():
    simulator.set_vehicle_speed(50.0)
    raw_value = can_monitor.read_raw("WheelSpeedFL")
    
    scaling = arxml_loader.get_signal_scaling("WheelSpeedFL")
    expected_raw = int(50.0 / scaling)  # Calculated from spec
    
    assert raw_value == pytest.approx(expected_raw, abs=1), (
        f"WheelSpeedFL scaling mismatch. "
        f"Raw={raw_value}, expected={expected_raw} "
        f"(scaling={scaling} km/h per bit)"
    )
```

### Pattern 4 — Environment Masking Product Defect

**Symptom:** Test passes in CI environment, product
defect exists in field.

**Root cause:** CI environment does not replicate
field conditions accurately. Defect only manifests
under conditions not present in CI.

| Field Condition | CI Environment Gap |
|----------------|-------------------|
| Cold temperature (-20°C) | Lab rack at room temperature |
| High CAN bus load (80%) | Test bus at 10% load |
| Low battery voltage (11V) | HIL rack at nominal 12V |
| Multiple simultaneous faults | Tests inject one fault at a time |

> This is an environment coverage gap — not a
> test defect or product defect in the traditional
> sense. The product behaves correctly in CI but
> incorrectly in field conditions not tested.
> The fix is environment enhancement, not test fixing.

### Pattern 5 — False Negative — The Silent Failure

**Symptom:** Test passes. Product defect exists.
Usually discovered in field or by manual testing.

**Root cause:** Test assertion is too weak —
it does not check the specific behavior that is defective.
```python
# DEFECTIVE ASSERTION — too weak, produces false negative
def test_abs_response_weak_assertion():
    simulator.apply_brake(pressure_bar=150)
    response = uds_client.read_data_by_identifier(did=0xF401)
    assert response is not None  # ← Only checks response exists
    # Does not check: ABS active flag, wheel speed values,
    # brake pressure modulation, response timing

# CORRECT — strong assertion covering the actual behavior
def test_abs_response_strong_assertion():
    simulator.set_vehicle_speed(80.0)
    simulator.apply_brake(pressure_bar=150)
    
    # Wait for ABS to activate
    can_monitor.wait_for_signal("ABSActivationFlag", 1, timeout=2.0)
    
    # Assert all safety-relevant behaviors
    assert can_monitor.read_signal("ABSActivationFlag") == 1
    assert can_monitor.read_signal("WheelSpeedFL") > 0
    assert can_monitor.read_signal("BrakePressureFL") < 150  # Modulated
    assert can_monitor.read_signal("BrakePressureFR") < 150
```

> ⭐ Weak assertions are the primary cause of
> false negatives. Every assertion must check
> the specific behavior that would be wrong if
> the product defect existed.

---

## 4. Documentation of Unexpected Results

> ⭐ Every investigated unexpected result must
> be documented — even if the conclusion is
> "transient environment issue, no action."
> Undocumented investigations cannot be audited
> and their patterns cannot be identified over time.

**Minimum documentation per unexpected result:**

| Field | Content |
|-------|---------|
| Test case ID | Unique identifier |
| Date and time | When the failure occurred |
| SUT version | Firmware under test |
| Environment | Which rack, which pipeline run |
| Failure message | Exact assertion failure text |
| Reproduction | Reproduced yes/no, under what conditions |
| Root cause classification | Product / test / environment / flaky |
| Evidence | Signal traces, logs, screenshots |
| Action taken | Defect raised / test fixed / environment fixed / quarantined |
| Resolution | Final outcome |

---

## 5. Automotive Domain — Unexpected Result Investigation

### ABS-Specific Investigation Checklist

When an ABS test produces an unexpected result:

| Step | Check | Tool |
|------|-------|------|
| 1 | Is the CAN bus active and within normal load? | CANalyzer bus statistics |
| 2 | Is the ECU in default session? | UDS session query |
| 3 | Are there active DTCs from previous test? | UDS DTC read |
| 4 | Is the ARXML version correct for this firmware? | ARXML header vs UDS DID |
| 5 | Is the expected value derived from spec or hardcoded? | Code review |
| 6 | Does the signal appear on the bus at all? | CANalyzer message filter |
| 7 | Is the failure timing-related? | Add timestamp logging |
| 8 | Does the failure occur on all racks or one? | Cross-rack comparison |

### Failure Investigation Report — Automotive Template
```
UNEXPECTED RESULT INVESTIGATION

Test ID:     test_abs_wheel_speed_fl_normal_braking
Date:        2024-03-15 02:14:33 UTC
Pipeline:    nightly-regression-run-447
SUT:         ABS SW v2.4.0 / ECU SN-20847
Environment: HIL Rack-2 / CAN: VECTOR_CH1

Failure:     AssertionError: WheelSpeedFL=0.0, expected=50.0±0.5

Reproduction:
  - Re-run same test: FAILS
  - Run on Rack-1: PASSES
  - Rack-2 only failure → environment hypothesis

Investigation:
  1. CAN bus load: 12% — normal ✅
  2. ECU session: DEFAULT ✅
  3. Active DTCs: none ✅
  4. ARXML version: v2.4 matches firmware ✅
  5. Raw CAN frame for WheelSpeedFL: NOT PRESENT ❌
     → Signal not transmitted on Rack-2 CAN bus

Root Cause:  Environment — VECTOR_CH1 on Rack-2
             not receiving WheelSpeedFL frames.
             CAN interface hardware fault suspected.

Action:      Infrastructure team notified.
             Rack-2 removed from rotation pending repair.
             Tests re-run on Rack-1 — PASS.

Classification: Environment issue
Defect raised: No (product is correct)
```

---

## 6. Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| Raising product defect without classification | Developer time wasted on non-product issue | Always classify before raising defect |
| Ignoring flaky tests | Trust erosion — real defects dismissed | Quarantine flaky, investigate within sprint |
| Hardcoded sleep instead of signal wait | Timing-dependent failures on slow environments | Signal-based wait with timeout everywhere |
| No state reset between tests | Shared state contamination, order-dependent failures | autouse fixture for ECU reset |
| Weak assertions | False negatives — product defects missed | Every assertion checks specific failure mode |
| No investigation documentation | Cannot identify patterns across incidents | Document every investigation to closure |

---

## 7. Architect Insights

> ⭐ **The classification step is non-negotiable.**
> Never act on an unexpected result before
> classifying it as product, test, or environment.
> Acting without classification is guessing.

> **Signal-based waits are architecture.**
> Hardcoded sleeps are a design smell that indicates
> the test does not understand the system under test.
> A test that knows the ECU should activate ABS
> within 2 seconds should wait up to 2 seconds —
> not sleep for a fixed 100ms and hope.

> **For automotive flaky tests:**
> Flaky tests in HIL environments are almost always
> caused by timing dependencies, CAN bus load
> variations, or ECU state contamination from
> previous tests. These are all fixable. A flaky
> test is a diagnosis waiting to happen — not
> an acceptable permanent state.

> **Document the investigation even when no defect
> is raised.** The most valuable patterns emerge
> from investigations that conclude "environment
> issue." Three environment issues on the same
> rack in one month means the rack needs maintenance
> — but only if the investigations are documented.

---

## 8. Reflection Questions

1. Your ABS test `test_wheel_speed_fl_abs_activation`
   fails in Monday's nightly run. It passed Friday.
   No product changes were deployed over the weekend.
   Walk through the four investigation steps and
   list the first three things you check, in order,
   before classifying the root cause.

2. A TAE on your team immediately raises a product
   defect every time a test fails. Three of the last
   five defects were closed as "not a product issue."
   Define a classification process you would introduce
   to prevent premature defect raising, and specify
   what evidence must exist before a product defect
   is raised.

3. `test_abs_fault_injection` passes when run alone
   but fails when run as part of the full suite.
   The failure message shows an unexpected DTC is
   active at the start of the test. Identify the
   root cause pattern, the affected TAF design
   principle, and the fix.

4. A CAN signal test has been producing a false
   negative for three months — the product defect
   existed but the test passed. Code review reveals
   the assertion only checked `response is not None`.
   Define three specific assertions that would have
   caught the defect, using WheelSpeedFL ABS
   activation as your example.

5. Your team has 15 flaky tests in a 400-test suite.
   The test manager says "just re-run failures —
   it's faster than investigating." Explain the
   architectural and safety risk of this approach
   for an automotive safety project.

---

## 9. Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Replace all `time.sleep()` calls in your test suite with signal-based waits using timeout | `framework-prototype/tests/` |
| 2 | Add `autouse=True` ECU reset fixture to your conftest.py to eliminate state contamination | `framework-prototype/tests/` |
| 3 | Create an investigation log template for your team — one entry per unexpected result | `chapter-07-verifying-tas/` |

---

*Next: Sub-Chapter 7.1.4 — Static Analysis of Testware*