# Sub-Chapter 3.1.3 — TAF Layering

> **Syllabus Reference:** TAE-3.1.3
> **Cognitive Level:** K3 — Apply
> **Chapter:** 3 — Test Automation Architecture
> **Status:** ✅ Complete

---

## Why Layers Exist

> *"When the SUT changes, only ONE layer should
> need updating."*

Without layers — 500 test scripts × signal rename
= 500 files to touch = days of work = high defect risk.

With layers — signal names in ONE business logic class
= update ONE file = 30 minutes = zero inconsistency.

> ⭐ TAF layering exists to contain the blast radius
> of SUT changes. This is the entire purpose.

---

## The Three Layers

| Layer | Contains | Changes When |
|-------|---------|-------------|
| **Test Scripts** | Test cases and suite annotations | New test requirements |
| **Business Logic** | SUT-specific abstractions and flows | SUT interface changes |
| **Core Libraries** | SUT-independent reusable utilities | Tool or technology changes |

---

## The Golden Rules

> ⭐ These rules are directly examinable at K3 level.

| Rule | Reason |
|------|--------|
| Scripts call business logic ONLY | Scripts must not depend on tool details |
| Business logic calls core libraries | SUT logic separated from tool logic |
| Scripts NEVER call core directly | Bypassing layers destroys maintainability |
| Core libraries have ZERO SUT knowledge | Must be reusable across all projects |

---

## Layer 1 — Test Scripts

**Contains only:**
- Test case definitions
- Test suite groupings
- Calls to business logic methods

**Must NOT contain:**

| Forbidden | Belongs In |
|-----------|-----------|
| Signal names or CAN IDs | Business logic |
| Tool-specific API calls | Core libraries |
| Connection handling | Core libraries |
| Data file parsing | Business logic or core |

**Correct example:**
```python
# TEST SCRIPTS LAYER
from business_logic.abs_signal_flows import ABSSignalFlows
from business_logic.fault_injection_sequences import FaultInjection

class TestABSWheelSpeedFault:
    def test_front_left_sensor_open_circuit(self):
        abs_flows = ABSSignalFlows()
        fault = FaultInjection()
        abs_flows.set_normal_operating_mode()
        fault.inject_open_circuit("front_left_wheel_speed")
        abs_flows.verify_degraded_mode_activated()
        abs_flows.verify_dtc_set("C0035")
```

---

## Layer 2 — Business Logic

**Contains:**
- SUT-specific signal names and identifiers
- User flows and multi-step sequences
- ECU state management
- Verification logic in domain language

**Correct example:**
```python
# BUSINESS LOGIC LAYER
from core_libraries.can_signal_monitor import CANSignalMonitor
from core_libraries.test_logger import TestLogger

class ABSSignalFlows:
    # Signal names live HERE - not in test scripts
    ABS_STATUS_SIGNAL   = "ABSActivationStatus"
    WHEEL_SPEED_FL      = "WheelSpeedFrontLeft"
    DEGRADED_MODE_VALUE = 0x02

    def verify_degraded_mode_activated(self):
        actual = self.monitor.read_signal(self.ABS_STATUS_SIGNAL)
        assert actual == self.DEGRADED_MODE_VALUE
```

---

## Layer 3 — Core Libraries

**Contains:**
- CAN signal monitoring utilities
- XCP connection handling
- Test logging framework
- Report generation
- Data file readers

**Critical property:** Zero SUT knowledge.
Works for ABS, ESP, braking, infotainment —
any project on the same technology stack.

**Correct example:**
```python
# CORE LIBRARIES LAYER - SUT independent
class CANSignalMonitor:
    """No ABS, ESP, or project-specific logic here"""

    def read_signal(self, signal_name: str) -> float:
        pass

    def wait_for_signal(self, signal_name: str,
                        expected_value: float,
                        timeout_ms: int) -> bool:
        pass
```

---

## Scaling Across Projects

Core libraries become shared foundation for all projects.

| Project | Uses Its Own | Shares With All |
|---------|-------------|----------------|
| ABS Project | ABS Scripts + ABS Logic | Core Libraries |
| ESP Project | ESP Scripts + ESP Logic | Core Libraries |
| Braking ECU | Braking Scripts + Braking Logic | Core Libraries |

> ⭐ Core libraries = internal product.
> Version them. Release independently.
> Write changelogs. Notify dependent teams.

---

## Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| Signal names in test scripts | 500 files per ARXML change | Signals belong in business logic |
| Scripts calling core directly | Business logic scattered | Code review enforcement |
| Business logic in core | Core becomes SUT-specific | Core must have zero SUT knowledge |
| One giant "utils" layer | Nobody knows where things belong | Define layer boundaries in writing |
| No layer enforcement | Violations accumulate silently | Add layer check to PR template |

---

## Architect Insights

> **Layer boundaries are architecture contracts.**
> Write them in README.
> Enforce in every code review.
> One violation allowed = ten more follow.

> **For automotive:**
> Business logic layer is where ARXML knowledge lives.
> Signal names, CAN IDs, DTC codes — all here.
> This single discipline reduces maintenance
> cost by 60-80% in large ECU projects.

> **Keep layers to minimum.**
> Syllabus recommends low number of layers.
> Three covers almost every use case.

---

## Reflection Questions

1. 600 test scripts use hardcoded signal names.
   Firmware update renames all signals.
   What is your refactoring strategy?

2. New TAE argues one flat layer is simpler.
   How do you demonstrate layering value
   with a concrete automotive example?

3. Core signal monitor method signature changes.
   Three projects depend on it.
   What is your migration strategy as architect?

4. Pull request directly calls XCPHandler from
   test script, bypassing business logic.
   How do you respond in code review?

5. Draw your current ABS project as three layers.
   What needs refactoring?

---

## See Also

- `taf-layers/core_libraries/can_signal_monitor.py`
- `taf-layers/business_logic/abs_signal_flows.py`
- `taf-layers/test_scripts/test_abs_wheel_speed.py`

---

*Next: Sub-Chapter 3.1.4 — Approaches for Automating Test Cases*