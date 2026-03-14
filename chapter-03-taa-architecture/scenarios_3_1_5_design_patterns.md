# Sub-Chapter 3.1.5 — Exam Scenarios Practice (Design Patterns)

> **Syllabus Reference:** TAE-3.1.5
> **Cognitive Level:** K3 — Apply
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Facade Pattern Identification

**Situation:**
A TAE is reviewing test scripts for an ESP ECU project.
She finds the following code in a test case file:
```python
import can
import struct

class TestESPActivation:
    def test_esp_activates_on_oversteer(self):
        bus = can.Bus(channel='PCAN_USBBUS1',
                      bustype='pcan',
                      bitrate=500000)
        raw_msg = struct.pack('>HH', 0x0320, 0x0000)
        msg = can.Message(arbitration_id=0x2B0,
                          data=raw_msg)
        bus.send(msg)
        response = bus.recv(timeout=2.0)
        value = struct.unpack('>H', response.data[0:2])[0]
        assert value == 0x0002
        bus.shutdown()
```

**Question:**
Which design pattern would most improve this code
and what is the primary benefit?

- A) Singleton pattern — ensure only one CAN bus
  instance exists across the test suite
- B) Facade pattern — hide CAN tool complexity
  and raw byte encoding behind a simple
  domain-language interface
- C) Flow model pattern — wrap this test into
  a reusable user journey
- D) Page object model — move the CAN IDs into
  a separate signal object class

---

**✅ Correct Answer: B**

**Reasoning:**
The test script contains multiple layers of
tool-specific complexity that belong hidden
behind a facade:

| Problem in Current Code | Facade Solution |
|------------------------|----------------|
| `import can` in test script | Hidden inside facade |
| `struct.pack('>HH', ...)` raw encoding | Hidden inside facade |
| `arbitration_id=0x2B0` raw CAN ID | Hidden inside facade |
| `struct.unpack('>H', ...)` raw decoding | Hidden inside facade |
| `bus.shutdown()` lifecycle management | Hidden inside facade |

**After applying facade pattern:**
```python
class TestESPActivation:
    def test_esp_activates_on_oversteer(self):
        esp_flows = ESPSignalFlows()
        esp_flows.simulate_oversteer_condition()
        esp_flows.verify_esp_intervention_active()
```

Zero tool imports. Zero raw bytes. Pure domain language.

**Why other options are secondary:**

| Option | Why Secondary |
|--------|--------------|
| A | Singleton helps but does not solve the raw byte exposure problem |
| C | Flow model is the next step AFTER facade is applied |
| D | POM helps with signal names but does not hide tool complexity |

**Key rule:** Facade is the FIRST pattern to apply
when tool-specific code appears in test scripts.

---

## Scenario 2 — Singleton Appropriate Use

**Situation:**
A test suite runs 200 ABS test cases sequentially.
Each test case contains this setup code:
```python
def setup_method(self):
    self.bus = can.Bus(channel='PCAN_USBBUS1',
                       bustype='pcan',
                       bitrate=500000)
    self.session = UDSSession.open("192.168.1.100")
    self.xcp = XCPConnection.connect("192.168.1.101")
```

And this teardown code:
```python
def teardown_method(self):
    self.bus.shutdown()
    self.session.close()
    self.xcp.disconnect()
```

The test suite takes 4 hours to run.
Profiling shows 18 minutes spent on connection
setup and teardown across 200 test cases.

**Question:**
Which pattern addresses this performance problem
and what is the additional safety benefit?

- A) Facade pattern — wrapping connections in
  a facade makes them faster to initialize
- B) Singleton pattern — one shared connection
  created once, reused by all test cases,
  preventing both performance waste and
  conflicting simultaneous connections
- C) Page object model — storing connection
  parameters in one class reduces setup time
- D) Flow model pattern — combining setup steps
  into a single flow method reduces overhead

---

**✅ Correct Answer: B**

**Reasoning:**
Singleton solves two problems simultaneously:

**Problem 1 — Performance:**

| Approach | Connection Operations | Time |
|----------|----------------------|------|
| New connection per test | 200 × open + 200 × close = 400 ops | 18 minutes |
| Singleton shared connection | 1 × open + 1 × close = 2 ops | ~5 seconds |

**Problem 2 — Safety:**
Without Singleton, if two test cases ever run
concurrently, both try to open a UDS session.
ECU rejects the second session request.
This causes intermittent failures that are
very difficult to diagnose.

Singleton guarantees only ONE UDS session exists
at any time — regardless of test execution order.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Facade wraps interfaces but does not reduce the number of connection operations |
| C | POM stores identifiers — not connection objects |
| D | Flow model organizes test steps — not connection lifecycle |

**Automotive insight:**
ECU diagnostic sessions (UDS) are hardware-limited.
Most ECUs support only ONE active diagnostic session.
Singleton is not optional here — it is a hardware constraint.

---

## Scenario 3 — POM Maintenance Benefit

**Situation:**
Two teams are building ABS test automation.

**Team A** uses Page Object Model:
```python
# abs_signal_objects.py
class ABSSignalObjects:
    ABS_STATUS = "ABSActivationStatus"
    WHEEL_SPEED_FL = "WheelSpeedFrontLeft"
    STATUS_DEGRADED = 0x02
```

**Team B** uses hardcoded strings directly:
```python
# test_abs_fault_1.py
assert monitor.read("ABSActivationStatus") == 0x02

# test_abs_fault_2.py
assert monitor.read("ABSActivationStatus") == 0x02

# ... repeated across 400 test files
```

A new ARXML release renames:
- `"ABSActivationStatus"` → `"ABS_ActivationState_01"`
- `"WheelSpeedFrontLeft"` → `"WheelSpeed_FL_v2"`

**Question:**
What is the exact difference in maintenance
effort between the two teams?

- A) Both teams have the same effort —
  find and replace works for both approaches
- B) Team A updates 2 lines in one file.
  Team B updates every file containing
  the signal name — potentially 400+ files
- C) Team B has less effort because their
  code is simpler without the extra class
- D) Team A has more effort because they
  must update both the POM class and
  all files that use it

---

**✅ Correct Answer: B**

**Reasoning:**

| Team | Files to Update | Risk |
|------|---------------|------|
| Team A (POM) | 1 file — `abs_signal_objects.py` | Zero — single source of truth |
| Team B (hardcoded) | Up to 400 files | High — easy to miss occurrences |

**Team A update:**
```python
# abs_signal_objects.py — update 2 lines only
ABS_STATUS     = "ABS_ActivationState_01"   # was "ABSActivationStatus"
WHEEL_SPEED_FL = "WheelSpeed_FL_v2"         # was "WheelSpeedFrontLeft"
# All 400 test files automatically use new names
```

**Team B update:**
- Search across 400 test files
- Replace every occurrence manually
- Risk missing some occurrences
- Tests using old name silently monitor wrong signal
- Silent false passes until someone notices

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Find and replace across 400 files has high miss risk and takes hours |
| C | Simplicity in test files comes at the cost of unmaintainability |
| D | Team A does NOT update files that use the POM — they all reference the constant which is already updated |

**Key exam rule:**
POM benefit = when SUT changes, update ONE place.
All consumers automatically get the updated value.
This is the single source of truth principle.

---

## Scenario 4 — Flow Model vs POM Distinction

**Situation:**
A TAE has built an ABS signal object class (POM):
```python
class ABSSignalObjects:
    ABS_STATUS = "ABSActivationStatus"
    STATUS_DEGRADED = 0x02
    DTC_WHEEL_FL = "C0035"
```

She now has 15 test cases that all perform
this same three-step sequence:
```python
# Repeated in 15 test cases
fault.inject_open_circuit(sensor)
time.sleep(0.5)
assert monitor.read(ABSSignalObjects.ABS_STATUS) == ABSSignalObjects.STATUS_DEGRADED
assert diagnostics.read_dtc() == ABSSignalObjects.DTC_WHEEL_FL
```

The timing requirement changes from 500ms to 300ms.
She must update all 15 test cases.

**Question:**
Which pattern should she apply to prevent
this maintenance problem and what does it add
that POM alone does not provide?

- A) Singleton — ensure only one instance of
  ABSSignalObjects exists
- B) Facade — hide the assert statements
  behind a simpler interface
- C) Flow Model — add a layer above POM that
  stores the reusable multi-step sequence,
  so timing changes require updating one method
- D) Inheritance — create a base test class
  containing the repeated sequence

---

**✅ Correct Answer: C**

**Reasoning:**
POM stores IDENTIFIERS (signal names, expected values).
Flow Model stores SEQUENCES (multi-step user actions).

These are different responsibilities requiring
different patterns.

**What POM provides:**
- Single location for signal names and constants
- Update signal name in one place ✅

**What POM does NOT provide:**
- Reuse of multi-step action sequences ❌
- Single location for timing requirements ❌

**What Flow Model adds:**
```python
class ABSTestFlows:
    FAULT_RESPONSE_TIMEOUT_MS = 300  # changed from 500 → update here only

    def inject_fault_and_verify_response(self, sensor, dtc):
        fault.inject_open_circuit(sensor)
        time.sleep(self.FAULT_RESPONSE_TIMEOUT_MS / 1000)
        assert monitor.read(ABSSignalObjects.ABS_STATUS) == \
               ABSSignalObjects.STATUS_DEGRADED
        assert diagnostics.read_dtc() == dtc

# All 15 test cases now:
def test_fl_sensor_fault(self):
    flows.inject_fault_and_verify_response(
        "front_left", ABSSignalObjects.DTC_WHEEL_FL
    )
```

Timing change: update ONE constant in flow class.
15 test cases automatically use new timing.

**Structure after applying both patterns:**
```
Test Scripts → Flow Model → Signal Objects (POM)
```

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Singleton manages instance lifecycle — not sequences |
| B | Facade hides tool complexity — not test sequences |
| D | Inheritance can work but creates tight coupling — Flow Model is the recommended pattern |

---

## Scenario 5 — SOLID Principle Violation

**Situation:**
A TAE builds the following class for ABS testing:
```python
class ABSTestManager:
    def connect_to_ecu(self): pass
    def read_can_signal(self, name): pass
    def inject_fault(self, sensor): pass
    def generate_html_report(self): pass
    def send_email_notification(self): pass
    def load_calibration_csv(self): pass
    def write_to_database(self): pass
    def compare_signal_tolerance(self): pass
```

After three months the class has grown to
1,400 lines. Every change anywhere in the class
risks breaking unrelated functionality.
Two TAEs cannot work on it simultaneously
without constant merge conflicts.

**Question:**
Which SOLID principle is being violated and
what is the correct refactoring approach?

- A) Open-Closed principle — the class needs
  more abstract base classes
- B) Single Responsibility principle — one class
  is doing eight different jobs and should be
  split into focused single-purpose classes
- C) Dependency Inversion principle — the class
  should depend on abstractions not implementations
- D) Liskov Substitution principle — subclasses
  cannot safely replace this class

---

**✅ Correct Answer: B**

**Reasoning:**
The Single Responsibility Principle states that
a class should have ONE reason to change.

`ABSTestManager` has EIGHT reasons to change:
- ECU connection protocol changes → affects `connect_to_ecu`
- Signal monitoring tool changes → affects `read_can_signal`
- HIL rack API changes → affects `inject_fault`
- Report format changes → affects `generate_html_report`
- Email server changes → affects `send_email_notification`
- CSV format changes → affects `load_calibration_csv`
- Database schema changes → affects `write_to_database`
- Tolerance algorithm changes → affects `compare_signal_tolerance`

**Correct refactoring:**

| Responsibility | New Class |
|---------------|----------|
| ECU connection | `ECUConnectionManager` |
| CAN signal monitoring | `CANSignalMonitor` |
| Fault injection | `FaultInjectionController` |
| HTML reporting | `HTMLReportGenerator` |
| Email notification | `EmailNotificationService` |
| CSV data loading | `CalibrationDataLoader` |
| Database writing | `TestResultRepository` |
| Signal comparison | `SignalToleranceComparator` |

**Benefits after refactoring:**
- Two TAEs can work on different classes simultaneously
- Changes to reporting never affect signal monitoring
- Each class is testable independently
- Each class is understandable in isolation

---

## Scenario 6 — Dependency Inversion in Automotive

**Situation:**
A TAE builds ABS business logic tightly coupled
to the ECUTest tool:
```python
class ABSSignalFlows:
    def __init__(self):
        # Direct dependency on ECUTest tool
        import ecutest
        self.tool = ecutest.CANMonitor()
        self.tool.connect("CAN1", baud=500000)

    def verify_degraded_mode(self):
        value = self.tool.read("ABSActivationStatus")
        assert value == 0x02
```

The team wants to run business logic unit tests
on a developer laptop without ECUTest installed
and without a HIL rack connected.

**Question:**
Which SOLID principle and which pattern together
solve this problem?

- A) Single Responsibility + Facade pattern
- B) Dependency Inversion + Dependency Injection
- C) Open-Closed + Inheritance
- D) Interface Segregation + Singleton

---

**✅ Correct Answer: B**

**Reasoning:**
**Dependency Inversion Principle** states that
high-level modules should depend on abstractions,
not on concrete implementations.

**Dependency Injection** is the technique that
implements this principle.

**Current problem:**
`ABSSignalFlows` (business logic) directly
imports and instantiates ECUTest tool.
No ECUTest = cannot instantiate = cannot test.

**Solution — inject the dependency:**
```python
# Abstract interface — no tool knowledge
class SignalMonitorInterface:
    def read(self, signal_name: str) -> float:
        raise NotImplementedError

# Real implementation — uses ECUTest
class ECUTestMonitor(SignalMonitorInterface):
    def read(self, signal_name: str) -> float:
        import ecutest
        return ecutest.read_signal(signal_name)

# Mock implementation — no hardware needed
class MockCANMonitor(SignalMonitorInterface):
    def __init__(self, responses: dict):
        self._responses = responses
    def read(self, signal_name: str) -> float:
        return self._responses.get(signal_name, 0.0)

# Business logic depends on ABSTRACTION only
class ABSSignalFlows:
    def __init__(self, monitor: SignalMonitorInterface):
        self.monitor = monitor  # injected — not hardcoded

    def verify_degraded_mode(self):
        value = self.monitor.read("ABSActivationStatus")
        assert value == 0x02

# On HIL rack — use real tool
flows = ABSSignalFlows(ECUTestMonitor())

# On developer laptop — use mock
flows = ABSSignalFlows(MockCANMonitor({
    "ABSActivationStatus": 0x02
}))
```

**Benefits:**
- Business logic unit tested without hardware
- Tool can be swapped without changing business logic
- Mock enables fast CI/CD pipeline validation

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Facade hides complexity but does not enable hardware-free testing |
| C | Inheritance alone does not solve the injection problem |
| D | Singleton and Interface Segregation address different concerns |

---

## Quick Reference — Design Patterns Exam Rules

| Rule | Remember This |
|------|--------------|
| Facade purpose | Hide tool complexity behind simple domain interface |
| Singleton purpose | One instance communicates with SUT — no duplicates |
| POM purpose | One update point when SUT interface changes |
| Flow model purpose | Reusable multi-step sequences above POM |
| POM vs Flow Model | POM = identifiers, Flow Model = sequences |
| Facade vs POM | Facade = hide tool, POM = hide signal names |
| SOLID S | One class, one responsibility |
| SOLID O | Extend by new class, never modify existing |
| SOLID D | Depend on abstractions, enables mock/stub |
| OOP Encapsulation | Hide internals, expose public interface only |
| OOP Inheritance | Child inherits base setup and teardown |
| OOP Polymorphism | Same method works for ABS and ESP |
| Dependency Injection | Pass interface in constructor — not hardcoded |
| Hardware-free testing | Dependency Inversion + mock implementation |

---

*Chapter 3 Complete — Next: Chapter 4 — Implementing Test Automation*