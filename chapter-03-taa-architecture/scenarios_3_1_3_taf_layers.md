# Sub-Chapter 3.1.3 — Exam Scenarios Practice (TAF Layering)

> **Syllabus Reference:** TAE-3.1.3
> **Cognitive Level:** K3 — Apply
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Layer Violation Detection

**Situation:**
A TAE is reviewing a pull request for a new ABS
test case. The code looks like this:
```python
from core_libraries.can_signal_monitor import CANSignalMonitor

class TestABSActivation:
    def test_abs_activates_on_wheel_slip(self):
        monitor = CANSignalMonitor()
        monitor.connect("PCAN_USBBUS1", 500000)
        monitor.start_monitoring(["ABSActivationStatus"])
        # inject wheel slip via HIL
        result = monitor.read_signal("ABSActivationStatus")
        assert result == 0x01
```

**Question:**
Which TAF layering rule does this test script violate?

- A) The test script is too long and should be split
  into smaller test cases
- B) The test script directly calls core libraries
  and contains SUT-specific signal names —
  bypassing the business logic layer
- C) The test script should not use assert statements —
  these belong in the business logic layer
- D) The CAN monitor connection should be established
  in a separate configuration file

---

**✅ Correct Answer: B**

**Reasoning:**
This test script violates two TAF layering rules:

| Violation | Rule Broken |
|-----------|------------|
| `from core_libraries.can_signal_monitor import CANSignalMonitor` | Scripts must NEVER call core libraries directly |
| `"ABSActivationStatus"` hardcoded in test script | Signal names belong in business logic layer |
| `assert result == 0x01` with hardcoded value | Expected values belong in business logic layer |

**Correct version should be:**
```python
from business_logic.abs_signal_flows import ABSSignalFlows

class TestABSActivation:
    def test_abs_activates_on_wheel_slip(self):
        abs_flows = ABSSignalFlows()
        abs_flows.verify_abs_activated_on_wheel_slip()
```

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Length is not the issue — architecture is |
| C | Assert statements are correct in test scripts when using business logic results |
| D | Connection configuration is valid to externalize but not the primary violation |

---

## Scenario 2 — Maintenance Impact Analysis

**Situation:**
A project has 800 test scripts structured as follows:

- All 800 scripts import `CANSignalMonitor` directly
- Signal name `"WheelSpeedFrontLeft"` appears
  in 340 test scripts as a hardcoded string
- Signal name `"ABSActivationStatus"` appears
  in 520 test scripts as a hardcoded string

A new ARXML release renames:
- `"WheelSpeedFrontLeft"` → `"WheelSpeed_FL_kmh"`
- `"ABSActivationStatus"` → `"ABS_ActivationState"`

**Question:**
How many files need to be modified and what is
the PRIMARY architectural cause of this situation?

- A) 2 files — only the ARXML and one config file
- B) Up to 860 files — all scripts containing
  either signal name plus the core library,
  caused by missing business logic layer
- C) 800 files — all test scripts must be updated
  because the core library changed
- D) 0 files — ARXML changes do not affect
  test scripts

---

**✅ Correct Answer: B**

**Reasoning:**
Without a business logic layer containing signal names:

| Signal | Files Containing It | Files to Update |
|--------|-------------------|----------------|
| WheelSpeedFrontLeft | 340 test scripts | 340 files |
| ABSActivationStatus | 520 test scripts | 520 files |
| Total | | Up to 860 files |

**With correct layering:**

| Signal | Lives In | Files to Update |
|--------|---------|----------------|
| WheelSpeedFrontLeft | `ABSSignalFlows` class | 1 file |
| ABSActivationStatus | `ABSSignalFlows` class | 1 file |
| Total | | 2 files |

**Root cause:** Signal names belong in the business
logic layer — not scattered across 860 test scripts.
This is the most concrete demonstration of why
TAF layering exists.

**Key calculation for exam scenarios:**
When signal names are in test scripts =
number of files to update = number of test scripts
using that signal.
When signal names are in business logic =
number of files to update = 1 per signal class.

---

## Scenario 3 — Core Library Reuse

**Situation:**
A company has three ECU projects:
- Project A: ABS ECU validation (started 2 years ago)
- Project B: ESP ECU validation (started 6 months ago)
- Project C: New braking ECU (starting now)

Project A built a `CANSignalMonitor` core library
that is well-tested and documented.

The Project B team built their own `SignalReader`
class because they were not aware of Project A's library.

The Project C team is starting now and must decide
which approach to follow.

**Question:**
What is the recommended TAF architecture decision
for Project C and what organizational practice
would have prevented the duplication in Project B?

- A) Project C should build its own library from
  scratch to ensure it meets their exact requirements
- B) Project C should reuse Project A's core library
  and the company should maintain shared core
  libraries as an internal product with a discovery
  mechanism for new teams
- C) Project C should use Project B's library since
  it is more recent and likely more modern
- D) All three projects should merge their libraries
  into one giant utility class immediately

---

**✅ Correct Answer: B**

**Reasoning:**
The TAF layering principle states that core libraries
are SUT-independent and reusable across any project
on the same technology stack.

Project A's `CANSignalMonitor` works for any CAN-based
ECU project — ABS, ESP, braking, or any other.
Project C should reuse it directly.

**What would have prevented Project B duplication:**

| Practice | Description |
|----------|-------------|
| Shared core library repository | Discoverable by all teams |
| Internal release process | Teams notified of available libraries |
| Architecture review for new projects | Reuse assessed before building new |
| Core library README | Clear documentation of capabilities |

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Building from scratch wastes effort and creates inconsistency |
| C | Recency does not determine quality — Project A is well-tested |
| D | Merging immediately risks breaking all three projects simultaneously |

**Architect insight:**
Core libraries should be treated as an internal
open-source product. New projects discover and
reuse them. Teams contribute improvements back.
This compounds value across the organization.

---

## Scenario 4 — Layer Assignment

**Situation:**
A TAE is building a TAF for ESP ECU testing.
She has written the following components and
needs to assign each to the correct layer.

| Component | Description |
|-----------|-------------|
| `ESPStatusChecker.verify_stability_control_active()` | Checks ESP status signal matches expected value |
| `CANFrameParser.decode_message(raw_bytes)` | Decodes raw CAN bytes into signal values |
| `test_esp_activates_on_oversteer.py` | Test case verifying ESP activates during oversteer |
| `ESPSignalNames.STABILITY_CONTROL_STATUS` | Constant containing the ESP status signal name |
| `TestReportGenerator.create_html_report()` | Creates HTML report from test results |

**Question:**
Which assignment is CORRECT?

- A) All five belong in core libraries since they
  are all reusable utilities
- B) `CANFrameParser` and `TestReportGenerator`
  in core libraries, `ESPStatusChecker` and
  `ESPSignalNames` in business logic,
  test case in test scripts
- C) Everything belongs in business logic to keep
  the architecture simple
- D) The test case belongs in core libraries since
  it is reused across multiple suites

---

**✅ Correct Answer: B**

**Reasoning:**

| Component | Layer | Reason |
|-----------|-------|--------|
| `CANFrameParser` | Core libraries | SUT-independent — works for any CAN project |
| `TestReportGenerator` | Core libraries | SUT-independent — works for any project |
| `ESPStatusChecker` | Business logic | Contains ESP-specific verification logic |
| `ESPSignalNames` | Business logic | Contains ESP-specific signal name constants |
| Test case file | Test scripts | Contains test case definition and assertions |

**The key question for assigning each component:**
*"Does this contain any ESP-specific, ABS-specific,
or project-specific knowledge?"*

- Yes → Business logic layer
- No, it is generic → Core libraries layer
- It is a test case → Test scripts layer

---

## Scenario 5 — Breaking Change Management

**Situation:**
The shared core `CANSignalMonitor` library used by
3 projects needs a change. The current method is:
```python
def read_signal(self, signal_name: str) -> float:
```

The new version adds a required parameter:
```python
def read_signal(self, signal_name: str,
                timeout_ms: int) -> float:
```

Project A has 340 business logic methods calling
`read_signal()`. Project B has 180. Project C has 90.

**Question:**
What is the correct architectural approach to
managing this breaking change?

- A) Update the method immediately and notify
  all teams to fix their code by end of week
- B) Create a new method `read_signal_with_timeout()`
  and deprecate the old one, giving teams a
  migration period before removing the old method
- C) Each project should fork the core library
  and maintain their own version going forward
- D) The change should be rejected — core libraries
  must never be modified once released

---

**✅ Correct Answer: B**

**Reasoning:**
Core libraries are an internal product. Breaking
changes follow the same discipline as external APIs:

| Step | Action |
|------|--------|
| 1 | Add new method alongside old one |
| 2 | Mark old method as deprecated with warning |
| 3 | Communicate change to all dependent teams |
| 4 | Give migration period (1-2 sprints minimum) |
| 5 | Remove old method only when all teams migrated |

This approach is called **backward-compatible evolution**
and prevents breaking three projects simultaneously.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Breaks all 610 calling locations simultaneously |
| C | Forking creates permanent divergence — defeats the purpose of shared libraries |
| D | Libraries must evolve — rejection is not sustainable |

---

## Scenario 6 — Identifying the Right Layer

**Situation:**
During a code review the following test code is found:
```python
# File: test_abs_regression.py

import can  # python-can library
import time

class TestABSRegression:
    def test_abs_fault_response(self):
        bus = can.interface.Bus(channel='PCAN_USBBUS1',
                                bustype='pcan',
                                bitrate=500000)
        msg = can.Message(arbitration_id=0x123,
                          data=[0x02, 0x00, 0x00, 0x00])
        bus.send(msg)
        time.sleep(0.5)
        response = bus.recv(timeout=1.0)
        assert response.data[0] == 0x02
        bus.shutdown()
```

**Question:**
How many layer violations does this test script contain
and what is the correct refactoring approach?

- A) One violation — the `time.sleep()` should use
  a dynamic wait instead
- B) Four violations — direct tool import, raw CAN
  message construction, hardcoded CAN ID, and
  hardcoded expected byte value all belong in
  lower layers
- C) No violations — test scripts are allowed to
  use any library they need
- D) Two violations — the CAN ID and expected value
  should be in a constants file

---

**✅ Correct Answer: B**

**Reasoning:**
This test script contains multiple layer violations:

| Violation | Belongs In |
|-----------|-----------|
| `import can` — direct tool library | Core libraries layer |
| `can.interface.Bus(...)` — tool API call | Core libraries layer |
| `arbitration_id=0x123` — raw CAN ID | Business logic (signal abstraction) |
| `data=[0x02, 0x00...]` — raw CAN bytes | Business logic (signal encoding) |
| `response.data[0] == 0x02` — raw byte assertion | Business logic (verification method) |

**Correct version:**
```python
from business_logic.abs_signal_flows import ABSSignalFlows
from business_logic.fault_injection_sequences import FaultInjection

class TestABSRegression:
    def test_abs_fault_response(self):
        abs_flows = ABSSignalFlows()
        fault = FaultInjection()
        fault.inject_abs_fault_condition()
        abs_flows.verify_degraded_mode_activated()
```

Zero tool imports. Zero hardcoded values.
Zero raw CAN bytes. Pure business domain language.

---

## Quick Reference — TAF Layering Exam Rules

| Rule | Remember This |
|------|--------------|
| Scripts call business logic ONLY | Never call core libraries from scripts |
| Signal names location | Business logic layer — never in scripts |
| Core library property | Zero SUT knowledge — reusable across all projects |
| Layer change trigger | Scripts change for new tests, BL changes for SUT changes, Core changes for tool changes |
| Violation symptom | Many files to update when SUT changes |
| Scaling benefit | Core libraries shared across all projects |
| Breaking change approach | Deprecate old, add new, give migration period |
| Layer count recommendation | Keep layers to minimum — three covers most cases |

---

*Next: Sub-Chapter 3.1.4 — Approaches for Automating Test Cases*