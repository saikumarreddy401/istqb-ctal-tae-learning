# Scenarios — Sub-Chapter 7.1.1 — Verifying the Test Automation Environment

> **Syllabus Reference:** TAE-7.1.1
> **Cognitive Level:** K3 — Apply
> **File:** scenarios_7_1_1_verify_environment.md
> **Status:** ✅ Complete

---

## Scenario 1 — Missing Smoke Test (K3)

### Situation

Your ABS nightly regression suite starts at 22:00.
At 00:14 the pipeline fails with:
```
KeyError: 'can_interface'
File: core/can_signal_monitor.py, line 47
```

The suite ran for 134 minutes before this error.
409 test results were already written to the
JUnit XML — all marked as passed.

Investigation reveals the environment config file
for the integration rack was updated by the
infrastructure team at 21:45. They renamed
`can_interface` to `can_channel` in the YAML.
The smoke test does not exist.

### Question

Identify every problem this scenario exposes and
specify exactly what a smoke test would have
prevented, including the pipeline change required.

### Answer

**Problems exposed:**

| Problem | Impact |
|---------|--------|
| No environment smoke test | Config error not detected until mid-suite |
| 134 minutes of compute wasted | Pipeline time lost on invalid run |
| 409 results marked passed without valid config | Results are invalid — cannot be used |
| Config change not communicated | Infrastructure change broke pipeline silently |

**What a smoke test prevents:**

> ⭐ A smoke test running at pipeline start would
> have executed `validate_environment_config()`
> before any test case ran. The missing `can_interface`
> key would have been detected in under 30 seconds.
> Zero test cases would have executed.
> Zero invalid results would have been written.

**Smoke test implementation for this scenario:**
```python
def validate_environment_config(config_path: str) -> None:
    """Validate all required config keys exist before suite runs."""
    required_keys = [
        "can_interface",   # ← Would have caught this immediately
        "ecu_ip",
        "uds_port",
        "arxml_path",
        "calibration_data"
    ]
    with open(config_path) as f:
        config = yaml.safe_load(f)

    missing = [k for k in required_keys if k not in config]
    if missing:
        raise EnvironmentError(
            f"Config validation failed. Missing keys: {missing}\n"
            f"Check: {config_path}"
        )
```

**Pipeline change required:**
```yaml
jobs:
  verify_environment:
    steps:
      - name: Validate config keys
        run: python scripts/validate_config.py

  run_tests:
    needs: verify_environment   # ← Never runs if env fails
```

> Without `needs: verify_environment`, the smoke
> test runs in parallel with or after the suite.
> The dependency enforces the sequence — not just
> the existence of the check.

---

## Scenario 2 — New HIL Rack Discrepancy (K3)

### Situation

A second HIL rack (Rack-2) is added to the CI
pipeline. First nightly run on Rack-2 produces:

| Suite | Rack-1 | Rack-2 |
|-------|--------|--------|
| ABS regression | 97% | 71% |

All 26% failures on Rack-2 involve CAN signal
reading — signals return zero or timeout.
No product changes were made. Same firmware,
same testware, same config file.

### Question

Define the environment verification sequence you
would perform to diagnose the discrepancy.
List each check in the order you would perform it,
the expected result, and what each result tells you.

### Answer

| Step | Check | Tool / Method | Expected | If Different |
|------|-------|--------------|---------|-------------|
| 1 | CAN interface detected by OS | `python -c "import can; print(can.detect_available_configs())"` | Interface appears in list | Interface not installed or wrong driver |
| 2 | CAN bus active — send test frame | `can.send()` + `can.recv()` loopback | Echo received < 10ms | Hardware fault or wrong baud rate |
| 3 | ECU reachable via UDS | UDS default session request | Positive response 0x50 0x01 | ECU not booted, wrong IP |
| 4 | ECU firmware version correct | UDS DID 0xF189 | Matches `expected_sut_version` in config | Wrong firmware on Rack-2 ECU |
| 5 | ARXML version matches firmware | Parse ARXML header vs UDS DID | Version strings match | Stale ARXML on Rack-2 |
| 6 | CAN bus baud rate | CANalyzer bus statistics | 500 kBit/s | Rack-2 configured at wrong baud rate |
| 7 | CAN bus load at idle | CANalyzer message rate | < 5% before test | Bus noise from other device on network |

> ⭐ Step 6 is the most likely root cause here.
> If Rack-2 CAN interface baud rate is 250 kBit/s
> and the ECU transmits at 500 kBit/s, all signal
> reads will fail — producing exactly the symptom
> described (zero or timeout on all CAN signals).

**Implementation — add to smoke test:**
```python
def verify_can_baud_rate(config: dict) -> None:
    """Verify CAN bus baud rate matches config."""
    bus = can.interface.Bus(
        channel=config["can_interface"],
        bustype="vector",
        bitrate=config["can_baud_rate"]
    )
    # Attempt to read one frame — timeout if wrong baud rate
    msg = bus.recv(timeout=2.0)
    if msg is None:
        raise EnvironmentError(
            f"No CAN frames received at "
            f"{config['can_baud_rate']} baud. "
            f"Verify baud rate configuration for "
            f"{config['rack_id']}."
        )
    bus.shutdown()
```

---

## Scenario 3 — SUT State Verification (K3)

### Situation

Monday morning ABS regression runs at 07:00.
Results show 8 failures all in fault injection tests:
```
test_abs_fault_injection_wheel_speed_fl   FAIL
test_abs_fault_injection_wheel_speed_fr   FAIL
test_abs_fault_injection_brake_pressure   FAIL
...
```

Failure message for each:
```
AssertionError: Expected DTC 0xC0051 not present.
Active DTCs found: [0xC0051, 0xC0052, 0xC0053, 0xC0071]
```

Investigation reveals Friday's regression run
ended abruptly at 23:55 due to a pipeline timeout.
The fault injection tests had run — but the teardown
fixture that clears DTCs never executed.

The Monday suite found pre-existing DTCs at startup
and the fault injection tests could not distinguish
newly injected from pre-existing faults.

### Question

Define the SUT state verification that would have
detected and resolved this before the Monday suite
began executing test cases.

### Answer

> ⭐ SUT state verification at suite start must
> include a DTC check and clear — before any
> test case executes.
```python
@pytest.fixture(scope="session", autouse=True)
def verify_and_reset_sut_state(uds_client, config):
    """
    Session-scoped fixture — runs once before all tests.
    Verifies ECU is in clean initial state.
    If DTCs present from previous run: logs and clears them.
    If ECU in wrong session: resets to default.
    Aborts suite if state cannot be established.
    """
    # Check for pre-existing DTCs
    dtc_response = uds_client.read_dtc_information(
        sub_function=0x02,
        status_mask=0x08
    )

    if dtc_response.dtc_list:
        # Log pre-existing DTCs — not a failure, but must be cleared
        print(
            f"⚠️  Pre-existing DTCs detected before suite start: "
            f"{[hex(d) for d in dtc_response.dtc_list]}. "
            f"Clearing before suite execution."
        )
        uds_client.clear_diagnostic_information(group=0xFFFFFF)

        # Verify clear succeeded
        verify = uds_client.read_dtc_information(
            sub_function=0x02, status_mask=0x08
        )
        if verify.dtc_list:
            raise EnvironmentError(
                "DTCs could not be cleared before suite start. "
                "Abort — fault injection tests will be invalid."
            )

    # Verify default session
    session = uds_client.diagnostic_session_control(0x01)
    if not session.positive:
        raise EnvironmentError(
            "ECU did not enter default session at suite start."
        )

    print("✅ SUT initial state verified — no active DTCs.")
    yield
```

> This fixture detects the Monday scenario at 07:00:02
> rather than at 07:45 after 8 test failures.
> It logs the pre-existing DTCs as evidence,
> clears them, and proceeds — without blocking
> the suite unnecessarily.

---

## Scenario 4 — Dependency Version Conflict (K3)

### Situation

Your ABS TAF runs correctly on developer laptops
and on the local HIL rack. When deployed to the
CI server, tests fail immediately:
```
ImportError: cannot import name 'CanSignalMonitor'
from 'can_tools' (version 2.1.0)
```

Investigation reveals:
- Developer laptops: `can_tools==3.0.0`
- CI server: `can_tools==2.1.0`
- `requirements.txt` in the repo: no version pinned
  (`can_tools` with no version specifier)

### Question A

Which environment verification method would have
detected this before the first test ran?

### Answer A

> ⭐ Dependency version verification — checking
> installed versions against a pinned requirements
> file before suite execution.

**Fix — pin all versions in requirements.txt:**
```
# requirements.txt — all versions pinned
can_tools==3.0.0
pytest==7.4.0
pyyaml==6.0.1
python-can==4.2.0
influxdb-client==1.36.1
```

**Verification in smoke test:**
```python
def verify_dependency_versions(requirements_path: str) -> None:
    """Fail fast if any dependency version mismatches."""
    import pkg_resources
    with open(requirements_path) as f:
        reqs = [
            line.strip() for line in f
            if line.strip() and not line.startswith("#")
        ]
    for req in reqs:
        try:
            pkg_resources.require(req)
        except pkg_resources.VersionConflict as e:
            raise EnvironmentError(
                f"Dependency version conflict: {e}\n"
                f"Run: pip install -r {requirements_path}"
            )
```

### Question B

Why is an unpinned `requirements.txt` an
environment configuration management failure
as well as an environment verification failure?

### Answer B

> Unpinned requirements violate the configuration
> management principle that testware must be
> reproducible across environments and time.
>
> `can_tools` without a version pin means:
> - Different versions install on different machines
> - `pip install` six months from now installs a
>   different version than today
> - Test results cannot be reproduced because
>   the tool version that produced them is unknown
>
> This is a configuration management failure
> (Chapter 5.1.2) that also requires environment
> verification (Chapter 7.1.1) to detect.
> Both are needed — config management prevents
> the problem, verification detects it when
> it occurs anyway.

---

## Quick Reference — Smoke Test Coverage

| Check | Detects | Timing |
|-------|---------|--------|
| Config key validation | Missing or renamed config keys | Pre-suite |
| Dependency version check | Wrong library versions | Pre-suite |
| CAN interface available | Interface missing or wrong driver | Pre-suite |
| ECU reachable | Network or power issue | Pre-suite |
| Firmware version correct | Wrong firmware deployed | Pre-suite |
| Active DTC check and clear | State contamination from previous run | Pre-suite |
| ARXML version match | Stale ARXML file | Pre-suite |

---

*Next: Scenarios 7.1.2 — Verifying Correct Behavior*