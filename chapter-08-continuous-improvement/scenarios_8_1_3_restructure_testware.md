# Scenarios — Sub-Chapter 8.1.3 — Restructuring Testware

> **Syllabus Reference:** TAE-8.1.3
> **Cognitive Level:** K4 — Analyze
> **File:** scenarios_8_1_3_restructure_testware.md
> **Status:** ✅ Complete

---

## Scenario 1 — Signal Name Coupling Cost (K4)

### Situation

Your ABS TAF has 40 test files. Each test file
references CAN signal names as raw strings:
```python
# Repeated across 40 files
can_monitor.read_signal("WheelSpeedFL_0x1A0_B0_L16")
can_monitor.read_signal("ABSActivationFlag_0x1A4_B0_L1")
can_monitor.read_signal("BrakePressureFL_0x1B2_B2_L12")
```

ABS SW v2.5 renames all signals — the byte
position encoding is removed from signal names:
```
WheelSpeedFL_0x1A0_B0_L16  →  WheelSpeedFL
ABSActivationFlag_0x1A4_B0_L1  →  ABSActivationFlag
BrakePressureFL_0x1B2_B2_L12  →  BrakePressureFL
```

### Question A

Without restructuring, quantify the maintenance
impact of this signal rename across the 40 files.

### Answer A

| Metric | Without Restructuring |
|--------|----------------------|
| Files requiring update | 40 |
| Average signal references per file | ~8 |
| Total string replacements | ~320 |
| Risk per replacement | Each manual change risks typo introducing a new defect |
| Test run required after each file | 40 pipeline runs to verify |
| Estimated total effort | 2–3 days minimum |

> ⭐ And this is only one signal rename event.
> ABS SW evolves continuously. Over three years,
> this maintenance pattern will repeat multiple
> times — compounding the debt.

### Question B

Show the restructured architecture that reduces
this to a single update point, and demonstrate
the maintenance effort after restructuring.

### Answer B
```python
# business_logic/abs_signal_names.py
# SINGLE UPDATE POINT for all ABS signal names

class AbsSignalNames:
    """
    Canonical signal name registry for ABS TAF.
    When signal names change in SW release:
    update this file only — all tests update automatically.
    """
    # Wheel speed signals
    WHEEL_SPEED_FL = "WheelSpeedFL"
    WHEEL_SPEED_FR = "WheelSpeedFR"
    WHEEL_SPEED_RL = "WheelSpeedRL"
    WHEEL_SPEED_RR = "WheelSpeedRR"

    # ABS control signals
    ABS_ACTIVATION_FLAG = "ABSActivationFlag"
    ABS_DEACTIVATION_FLAG = "ABSDeactivationFlag"

    # Brake pressure signals
    BRAKE_PRESSURE_FL = "BrakePressureFL"
    BRAKE_PRESSURE_FR = "BrakePressureFR"
```
```python
# test_abs_wheel_speed.py — AFTER restructuring
from business_logic.abs_signal_names import AbsSignalNames

def test_wheel_speed_fl_at_80kmh():
    simulator.set_vehicle_speed(80.0)
    value = can_monitor.read_signal(AbsSignalNames.WHEEL_SPEED_FL)
    assert value == pytest.approx(80.0, abs=0.5)
```

**Maintenance effort after restructuring:**

| Metric | After Restructuring |
|--------|---------------------|
| Files requiring update | 1 — `abs_signal_names.py` only |
| String replacements | 3 constant values updated |
| Risk | Zero — no test logic touched |
| Test run required | 1 pipeline run to verify |
| Estimated effort | 15 minutes |

> **Reduction: 3 days → 15 minutes.**
> Every future signal rename costs 15 minutes
> regardless of suite size.

---

## Scenario 2 — Fixture Consolidation (K4)

### Situation

Code review of your ESP TAF reveals this pattern
across 28 test files:
```python
# test_esp_yaw_rate.py
def test_yaw_rate_threshold():
    client = UdsClient(ip="192.168.100.10", port=13400)
    client.connect()
    client.clear_diagnostic_information(0xFFFFFF)
    client.diagnostic_session_control(0x01)
    # ... 3 lines of test logic
    client.disconnect()

# test_esp_stability.py — identical setup
def test_stability_at_130kmh():
    client = UdsClient(ip="192.168.100.10", port=13400)
    client.connect()
    client.clear_diagnostic_information(0xFFFFFF)
    client.diagnostic_session_control(0x01)
    # ... 3 lines of test logic
    client.disconnect()
```

The IP address `192.168.100.10` appears 112 times
across the 28 files.

### Question

Evaluate the risk this structure creates and
implement the restructured fixture solution.

### Answer

**Risk analysis:**

| Risk | Consequence |
|------|------------|
| IP hardcoded 112 times | Environment change requires 112 replacements |
| Setup code duplicated 28 times | Setup defect requires 28 fixes |
| No session-scoped client | 28 × connect/disconnect per suite run — significant overhead |
| Disconnect missing on test failure | Resource leak if test throws before disconnect |
| No autouse reset | Test atomicity depends on developer discipline |

**Restructured solution:**
```python
# conftest.py — project root
import pytest
import yaml
from core.uds_handler import UdsClient

@pytest.fixture(scope="session")
def config():
    """Load environment config once per session."""
    with open("config/integration.yaml") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def uds_client(config):
    """
    Session-scoped UDS client.
    Created once — shared across all 28 test files.
    Handles connect and disconnect via yield.
    IP address from config — never hardcoded.
    """
    client = UdsClient(
        ip=config["ecu_ip"],       # ← from config, not hardcoded
        port=config["uds_port"]
    )
    client.connect()
    yield client
    client.disconnect()           # ← guaranteed even on failure

@pytest.fixture(autouse=True)
def reset_esp_state(uds_client):
    """
    Function-scoped — runs before and after every test.
    autouse=True — no test needs to request it explicitly.
    Guarantees atomic test state across all 28 files.
    """
    uds_client.clear_diagnostic_information(0xFFFFFF)
    uds_client.diagnostic_session_control(0x01)
    yield
    uds_client.clear_diagnostic_information(0xFFFFFF)
```
```python
# test_esp_yaw_rate.py — AFTER restructuring
# No setup, no teardown, no IP address, no connect/disconnect

def test_yaw_rate_threshold(uds_client, can_monitor):
    """3 lines of test logic — nothing else."""
    simulator.apply_yaw_rate(target_deg_per_sec=45.0)
    yaw = can_monitor.read_signal(EspSignalNames.YAW_RATE)
    assert yaw == pytest.approx(45.0, abs=1.0)
```

**After restructuring:**

| Metric | Before | After |
|--------|--------|-------|
| IP address occurrences | 112 | 1 (config file) |
| Setup code locations | 28 | 1 (conftest.py) |
| Connect/disconnect per suite | 28 | 1 |
| Suite execution time saving | — | ~56 seconds (28 × 2s connect overhead) |

---

## Scenario 3 — Safe Restructuring Sequence (K4)

### Situation

You are assigned to restructure the ABS TAF
over two sprints. The current suite has:

- 40 flat test files in one directory
- Signal names hardcoded as strings throughout
- Setup code duplicated in every file
- 12 calibration variant test functions
- Zero business logic abstraction

Sprint 1 constraint: zero coverage regression risk.
Sprint 2 constraint: medium risk acceptable.

### Question

Assign restructuring techniques to each sprint.
Justify the sequence using risk analysis.

### Answer

**Sprint 1 — Zero risk techniques only:**

| Technique | Risk | Justification |
|-----------|------|--------------|
| Folder restructure — move files into component folders | Zero | File moves do not change code — pytest discovers tests by path |
| Extract signal names to `AbsSignalNames` class | Low | Mechanical string replacement — verifiable by search |
| Pin dependency versions in requirements.txt | Zero | No code changes — prevents future breakage |
| Add named constants for magic threshold values | Low | Replace literals with named constants — same values |

> Sprint 1 rule: every change is mechanical and
> independently verifiable. No logic changes.
> Run full suite after each technique — baseline
> must be maintained throughout.

**Sprint 2 — Medium risk techniques:**

| Technique | Risk | Justification |
|-----------|------|--------------|
| Fixture consolidation to conftest.py | Medium | Removing per-test setup risks state issues if autouse fixture behaves differently |
| Business logic extraction to AbsSignalFlows | Medium | Moving logic to new layer — must verify all test scripts use new layer correctly |
| DDT introduction for calibration variants | Low-Medium | Replacing explicit functions with parametrize — coverage must be verified per variant |

> Sprint 2 rule: run full suite after each
> individual technique — not just at sprint end.
> If coverage drops after any technique,
> revert that technique and investigate before
> continuing.

**Verification gate between sprints:**
```bash
# Sprint 1 exit criteria — must pass before Sprint 2 begins
pytest tests/ --junit-xml=sprint1_exit.xml
python scripts/compare_pass_rates.py \
  --baseline results/pre_restructure_baseline.xml \
  --current sprint1_exit.xml \
  --tolerance 0.0  # Zero tolerance — Sprint 1 must not drop coverage
```

---

## Scenario 4 — DDT Restructuring Value (K4)

### Situation

Your ABS calibration team adds 3 new variants
per SW release. Releases occur 4 times per year.
Current state: one test function per variant.

**Current maintenance cost:**
- Writing new variant test function: 30 min each
- 3 variants × 4 releases = 12 new functions per year
- Annual effort: 12 × 30 min = 360 minutes = 6 hours

**Proposed state:** DDT from CSV.
- Adding new variant: add one CSV row = 2 min each
- 3 variants × 4 releases = 12 new rows per year
- Annual effort: 12 × 2 min = 24 minutes

### Question A

Calculate the 3-year ROI of the DDT restructuring,
given that the restructuring itself takes 4 hours.

### Answer A

| Item | Hours |
|------|-------|
| Restructuring cost (one-time) | 4.0 |
| Annual saving per year (6h - 0.4h) | 5.6 |
| Year 1 net (saving - restructuring cost) | 1.6 |
| Year 2 net | 5.6 |
| Year 3 net | 5.6 |
| **3-year total saving** | **12.8 hours** |

> ⭐ Break-even: less than 1 year.
> 3-year ROI: 12.8 hours saved for 4 hours invested.
> This does not include the additional value of:
> - Reduced defect risk from fewer code changes
> - Consistent test structure across all variants
> - Non-TAE (calibration engineer) can add variants

### Question B

Show the DDT implementation that achieves this.

### Answer B
```python
# data/abs_calibration_variants.csv
# variant_id, market, activation_threshold_bar, deactivation_speed_kmh
# A, EU, 118.5, 4.8
# B, US, 121.0, 5.2
# C, JP, 115.0, 4.5
# D, CN, 119.0, 5.0   ← New variant: one line in CSV, no code change

import csv
import pytest

def load_variants(csv_path: str) -> list:
    """Load calibration variants from CSV."""
    with open(csv_path) as f:
        return [
            pytest.param(
                row["variant_id"],
                float(row["activation_threshold_bar"]),
                float(row["deactivation_speed_kmh"]),
                id=f"variant_{row['variant_id']}_{row['market']}"
            )
            for row in csv.DictReader(f)
        ]

@pytest.mark.parametrize(
    "variant_id, activation_threshold, deactivation_speed",
    load_variants("data/abs_calibration_variants.csv")
)
def test_abs_calibration_variant(
    variant_id: str,
    activation_threshold: float,
    deactivation_speed: float,
    abs_flow
):
    """
    Verify ABS thresholds per calibration variant.
    Adding variant D: add one CSV row — zero code change.
    """
    abs_flow.load_calibration_variant(variant_id)

    assert abs_flow.get_activation_threshold() == \
        pytest.approx(activation_threshold, abs=0.1), (
        f"Variant {variant_id}: activation threshold mismatch"
    )
    assert abs_flow.get_deactivation_speed() == \
        pytest.approx(deactivation_speed, abs=0.1), (
        f"Variant {variant_id}: deactivation speed mismatch"
    )
```

---

## Quick Reference — Restructuring Risk vs Benefit

| Technique | Risk | Benefit | Sprint |
|-----------|------|---------|--------|
| Folder reorganisation | Zero | Navigation + clarity | 1 |
| Named constants extraction | Low | Single update point for values | 1 |
| Dependency pinning | Zero | Prevents silent breakage | 1 |
| Signal name registry | Low | Single update point for names | 1 |
| Fixture consolidation | Medium | Eliminates duplication + atomicity | 2 |
| Business logic extraction | Medium-High | Decouples test intent from implementation | 2 |
| DDT introduction | Low-Medium | Scales with variants, reduces effort | 2 |

---

*Next: Scenarios 8.1.4 — Tool Improvement Opportunities*