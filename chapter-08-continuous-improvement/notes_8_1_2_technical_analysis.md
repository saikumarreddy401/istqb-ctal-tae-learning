# Sub-Chapter 8.1.3 — Restructuring Testware

> **Syllabus Reference:** TAE-8.1.3
> **Cognitive Level:** K4 — Analyze
> **Chapter:** 8 — Continuous Improvement of Test Automation
> **Status:** ✅ Complete

---

## 1. Concept Explanation

### What Restructuring Means

Restructuring is the deliberate reorganisation of
testware — its code, folder structure, naming
conventions, and architectural layers — to improve
maintainability, reduce duplication, and restore
alignment with the current product and TAF architecture.

> ⭐ **Restructuring is not rewriting.**
> Rewriting discards working testware and rebuilds
> from scratch — high risk, high cost.
> Restructuring improves existing testware
> incrementally — preserving test coverage while
> reducing technical debt.
>
> The external behaviour of the test suite
> does not change after restructuring.
> The internal quality does.

### When Restructuring Is Needed

| Signal | Meaning |
|--------|---------|
| Requirement change requires updating 20+ test files | Duplication — restructure to single update point |
| New TAE cannot understand test logic without the author | Cohesion failure — restructure for clarity |
| Test suite execution time grows without new tests | Structural inefficiency — restructure setup/teardown |
| Pass rate unstable without product changes | Shared state — restructure fixtures |
| Adding new test cases takes disproportionate effort | Wrong abstraction level — restructure layers |

---

## 2. Restructuring Techniques

### Technique 1 — Extract Business Logic to Dedicated Layer

The most architecturally impactful restructuring.
Moves product-specific knowledge out of test scripts
and into the business logic layer where it belongs.
```python
# BEFORE — business logic embedded in test script
def test_abs_activation_before():
    """
    Product knowledge (speed threshold, pressure threshold,
    signal names, expected flag value) all in test script.
    If ABS activation logic changes — this test changes.
    If CAN signal name changes — this test changes.
    If threshold changes — this test changes.
    Three reasons to change one test.
    """
    # Set up conditions
    can_bus.send_signal("VehicleSpeed", 80.0 / 0.01)  # raw value
    can_bus.send_signal("BrakePressure", 150 / 0.1)    # raw value
    time.sleep(0.2)

    # Read result
    raw_flag = can_bus.read_signal("ABSActivationFlag_0x1A4_B0")
    assert raw_flag == 1

# AFTER — business logic in dedicated layer
# business_logic/abs_signal_flows.py
class AbsActivationFlow:
    """
    Encapsulates all knowledge of ABS activation conditions.
    Test scripts call methods — not signals directly.
    Signal names, thresholds, raw conversions: all here.
    """

    ABS_ACTIVATION_SPEED_THRESHOLD_KMH = 30.0
    ABS_ACTIVATION_PRESSURE_THRESHOLD_BAR = 120.0

    def __init__(self, can_monitor, simulator):
        self._can = can_monitor
        self._sim = simulator

    def create_abs_activation_conditions(
        self, speed_kmh: float = 80.0,
        pressure_bar: float = 150.0
    ) -> None:
        """Set up conditions that should trigger ABS."""
        self._sim.set_vehicle_speed(speed_kmh)
        self._sim.apply_brake(pressure_bar)

    def wait_for_abs_activation(
        self, timeout_seconds: float = 2.0
    ) -> bool:
        """Wait for ABS to activate. Returns True if activated."""
        return self._can.wait_for_signal(
            "ABSActivationFlag", expected_value=1,
            timeout_seconds=timeout_seconds
        )

    def assert_abs_activated(self) -> None:
        """Assert ABS is currently active."""
        flag = self._can.read_signal("ABSActivationFlag")
        assert flag == 1, (
            f"ABS not activated. ABSActivationFlag={flag}. "
            f"Verify speed > {self.ABS_ACTIVATION_SPEED_THRESHOLD_KMH} "
            f"km/h and brake pressure > "
            f"{self.ABS_ACTIVATION_PRESSURE_THRESHOLD_BAR} bar."
        )

# test_scripts/test_abs_activation.py — AFTER restructuring
def test_abs_activation(abs_flow: AbsActivationFlow):
    """
    Verify ABS activates under standard braking conditions.
    All product knowledge in AbsActivationFlow — not here.
    If signal names change: update AbsActivationFlow only.
    If thresholds change: update AbsActivationFlow only.
    This test never changes unless the test intent changes.
    """
    abs_flow.create_abs_activation_conditions()
    abs_flow.wait_for_abs_activation()
    abs_flow.assert_abs_activated()
```

> ⭐ After restructuring, the test script is
> three lines. The business logic is in one place.
> A signal name change requires one update —
> not 40 test file updates.

### Technique 2 — Consolidate Fixtures

Replace duplicated setup code scattered across
test files with shared fixtures in `conftest.py`.
```python
# BEFORE — setup duplicated in every test file
# test_abs_wheel_speed.py
def test_wheel_speed_fl():
    client = UdsClient(ip="192.168.100.10", port=13400)
    client.connect()
    client.clear_dtcs()
    client.set_session(0x01)
    # ... test logic
    client.disconnect()

# test_abs_fault_injection.py
def test_fault_injection():
    client = UdsClient(ip="192.168.100.10", port=13400)
    client.connect()
    client.clear_dtcs()
    client.set_session(0x01)
    # ... test logic
    client.disconnect()

# AFTER — single fixture in conftest.py
# conftest.py
@pytest.fixture(scope="session")
def uds_client(config):
    """
    Session-scoped UDS client.
    Created once — shared across all tests.
    Handles connect, initial state, and disconnect.
    """
    client = UdsClient(
        ip=config["ecu_ip"],
        port=config["uds_port"]
    )
    client.connect()
    client.clear_diagnostic_information(group=0xFFFFFF)
    client.diagnostic_session_control(0x01)
    yield client
    client.disconnect()

@pytest.fixture(autouse=True)
def reset_ecu_per_test(uds_client):
    """Function-scoped reset — runs before each test."""
    uds_client.clear_diagnostic_information(group=0xFFFFFF)
    uds_client.diagnostic_session_control(0x01)
    yield
    uds_client.clear_diagnostic_information(group=0xFFFFFF)
```

> Fixture consolidation has three benefits:
> 1. Setup defect fixed in one place — not 40
> 2. Session-scoped client reduces connect/disconnect overhead
> 3. autouse reset ensures test atomicity without test modification

### Technique 3 — Replace Magic Numbers with Named Constants
```python
# BEFORE — magic numbers everywhere
def test_wheel_speed_scaling():
    assert monitor.raw_to_physical("WheelSpeedFL", 5000) == 50.0
    assert monitor.raw_to_physical("WheelSpeedFL", 8000) == 80.0
    assert 0 <= raw_value <= 25000

# AFTER — named constants from specification
# constants/abs_signal_constants.py
class WheelSpeedSignal:
    """
    Constants derived from ARXML specification.
    Update here when specification changes —
    all tests using these constants update automatically.
    """
    SCALING_FACTOR_KMH_PER_BIT = 0.01
    RAW_MIN = 0
    RAW_MAX = 25000
    PHYSICAL_MIN_KMH = 0.0
    PHYSICAL_MAX_KMH = 250.0

    @classmethod
    def physical_to_raw(cls, physical_kmh: float) -> int:
        """Convert physical km/h to raw CAN value."""
        return int(physical_kmh / cls.SCALING_FACTOR_KMH_PER_BIT)

# test using constants
from constants.abs_signal_constants import WheelSpeedSignal

def test_wheel_speed_scaling():
    raw_50kmh = WheelSpeedSignal.physical_to_raw(50.0)
    raw_80kmh = WheelSpeedSignal.physical_to_raw(80.0)

    assert monitor.raw_to_physical("WheelSpeedFL", raw_50kmh) == \
        pytest.approx(50.0, abs=0.01)
    assert monitor.raw_to_physical("WheelSpeedFL", raw_80kmh) == \
        pytest.approx(80.0, abs=0.01)
    assert WheelSpeedSignal.RAW_MIN <= raw_value \
        <= WheelSpeedSignal.RAW_MAX
```

### Technique 4 — Reorganise Folder Structure

A testware folder structure that does not reflect
the current product and TAF architecture becomes
a navigation and maintenance burden.
```
# BEFORE — flat, unorganised structure
tests/
├── test_abs.py              ← 800 lines, all ABS tests
├── test_esp.py              ← 600 lines, all ESP tests
├── helper.py                ← Unclear purpose
├── utils.py                 ← Unclear purpose
└── conftest.py

# AFTER — mirrors TAF layer structure
tests/
├── conftest.py              ← Session + function fixtures
├── abs/
│   ├── conftest.py          ← ABS-specific fixtures
│   ├── test_wheel_speed.py  ← One behavior per file
│   ├── test_abs_activation.py
│   ├── test_fault_injection.py
│   └── test_calibration_variants.py
├── esp/
│   ├── conftest.py
│   ├── test_yaw_rate.py
│   └── test_stability_control.py
└── shared/
    ├── test_uds_session.py
    └── test_can_signal_baseline.py
```

> ⭐ Folder structure is architecture made visible.
> A TAE who cannot find the test for a specific
> requirement within 30 seconds is working in
> a structure that needs restructuring.

### Technique 5 — Introduce Data-Driven Tests for Variants

Replace explicit test functions per calibration
variant with DDT from CSV.
```python
# BEFORE — one test function per variant (not scalable)
def test_abs_calibration_variant_a():
    assert abs_flow.get_activation_threshold() == 118.5

def test_abs_calibration_variant_b():
    assert abs_flow.get_activation_threshold() == 121.0

def test_abs_calibration_variant_c():
    assert abs_flow.get_activation_threshold() == 115.0
# Adding variant D requires new test function

# AFTER — DDT from CSV
# data/abs_calibration_variants.csv
# variant_id, activation_threshold_bar, market
# A, 118.5, EU
# B, 121.0, US
# C, 115.0, JP

import csv
import pytest

def load_calibration_variants(csv_path: str) -> list:
    """Load calibration variants from CSV for parametrize."""
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        return [
            pytest.param(
                row["variant_id"],
                float(row["activation_threshold_bar"]),
                id=f"variant_{row['variant_id']}"
            )
            for row in reader
        ]

@pytest.mark.parametrize(
    "variant_id, expected_threshold",
    load_calibration_variants("data/abs_calibration_variants.csv")
)
def test_abs_calibration_variant(
    variant_id: str, expected_threshold: float
):
    """
    Verify ABS activation threshold per calibration variant.
    Adding variant D: add one row to CSV — no code change.
    """
    abs_flow.load_calibration_variant(variant_id)
    actual = abs_flow.get_activation_threshold()
    assert actual == pytest.approx(expected_threshold, abs=0.1), (
        f"Variant {variant_id}: threshold={actual}, "
        f"expected={expected_threshold} bar."
    )
```

---

## 3. Restructuring Without Breaking Coverage

> ⭐ **The cardinal rule of restructuring:**
> Pass rate must not decrease during or after
> restructuring. If tests break during restructuring,
> the restructuring introduced a defect.

**Safe restructuring workflow:**

| Step | Action | Verification |
|------|--------|-------------|
| 1 | Run suite — record baseline pass rate | Baseline: 96.2% |
| 2 | Restructure one component at a time | Never restructure entire suite at once |
| 3 | Run suite after each component | Pass rate must match or exceed baseline |
| 4 | Commit each component separately | Enables rollback to last good state |
| 5 | Update documentation after each commit | Structure reflects new organisation |
```yaml
# Pipeline protection during restructuring
jobs:
  restructuring_validation:
    steps:
      - name: Run full suite after restructuring
        run: pytest tests/ --junit-xml=results/post_restructure.xml

      - name: Validate pass rate not decreased
        run: python scripts/compare_pass_rates.py
          --baseline results/pre_restructure_baseline.xml
          --current results/post_restructure.xml
          --tolerance 0.5  # Allow 0.5% variance
```

---

## 4. Automotive Domain — ABS Testware Restructuring Plan

### Restructuring Priority Matrix

| Component | Current State | Target State | Effort | Risk |
|-----------|--------------|-------------|--------|------|
| Signal names in test scripts | 40 scripts with raw signal names | All signal names in `AbsSignalFlows` | High | High — touch many files |
| Fixture duplication | Setup code in 40 test files | `conftest.py` session fixture | Medium | Medium |
| Magic threshold values | 134 occurrences | `WheelSpeedSignal` constants class | Medium | Low |
| Calibration variant tests | 12 explicit functions | DDT from calibration CSV | Low | Low |
| Flat test folder | 3 large test files | Component-based folder structure | Low | Low |

**Recommended restructuring sequence:**

> 1. Folder structure first — lowest risk, enables parallel work
> 2. Constants extraction — safe, mechanical, low coupling
> 3. Fixture consolidation — medium risk, high maintenance benefit
> 4. Business logic extraction — highest effort, highest long-term benefit
> 5. DDT introduction — last, after structure is stable

---

## 5. Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| Restructure entire suite at once | Coverage drops, root cause hard to find | One component at a time |
| No baseline before restructuring | Cannot verify restructuring preserved coverage | Always record baseline pass rate first |
| Restructure without pipeline | Breakage discovered days later | Pipeline validates after every component |
| Rename signals without updating all references | Runtime errors on signal name | Search entire codebase before renaming |
| Extract business logic but leave old code | Duplication grows | Delete old code after extraction verified |

---

## 6. Architect Insights

> ⭐ **Restructuring is an investment in future
> delivery speed.** A team that spends 20% of
> a sprint restructuring will deliver the
> remaining 80% faster — because the next
> requirement change touches one file instead
> of forty.

> **The business logic layer is the most valuable
> restructuring target in automotive TAF.**
> Every signal name, every threshold, every
> calibration value that lives in a test script
> is a maintenance debt that compounds with
> every SW release. Extract it once — maintain
> it in one place forever.

> **Never restructure under time pressure.**
> Restructuring requires careful, verified,
> incremental steps. Rushed restructuring
> breaks coverage and creates new debt faster
> than it removes old debt. Schedule it as a
> dedicated sprint activity — not as something
> done between feature work.

---

## 7. Reflection Questions

1. Your ABS test suite has 40 test files where
   each file directly references CAN signal names
   as strings. The signal naming convention is
   changing in the next SW release. Without
   restructuring, how many files require updates,
   and what restructuring technique reduces this
   to one update point?

2. You are asked to restructure the ABS test
   suite over two sprints. Sprint 1 must be
   zero-risk. Sprint 2 may carry medium risk.
   Using the restructuring priority matrix,
   assign techniques to each sprint and justify
   the sequence.

3. After extracting business logic to a dedicated
   `AbsSignalFlows` class, the suite pass rate
   drops from 96.2% to 91.4%. The restructuring
   introduced defects. Describe your recovery
   process: what you check first, how you isolate
   the regression, and how you prevent this in
   future restructuring efforts.

4. A project manager argues that restructuring
   has no value because "the tests pass — why
   change them?" Construct a quantified business
   case using the maintenance cost of the current
   40-file signal name coupling versus the
   proposed single-update-point architecture.

5. Your calibration team adds 3 new ABS variants
   per SW release. Currently each variant requires
   a new test function — taking 30 minutes of TAE
   time per variant. After introducing DDT from
   CSV, adding a variant takes 2 minutes. Calculate
   the annual time saving for 4 releases per year
   with 3 new variants each.

---

## 8. Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Extract all ABS signal names from test scripts into `business_logic/abs_signal_flows.py` | `framework-prototype/business_logic/` |
| 2 | Create `WheelSpeedSignal` constants class and replace all magic numbers in wheel speed tests | `framework-prototype/core/` |
| 3 | Restructure flat test folder into component-based structure matching TAF layers | `framework-prototype/tests/` |

---

*Next: Sub-Chapter 8.1.4 — Identifying Tool Improvement Opportunities*