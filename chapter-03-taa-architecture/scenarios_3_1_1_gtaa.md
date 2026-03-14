# Sub-Chapter 3.1.1 — Exam Scenarios Practice (gTAA)

> **Syllabus Reference:** TAE-3.1.1
> **Cognitive Level:** K2 — Understand
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Optional vs Mandatory Capabilities

**Situation:**
A TAE is designing a new automation architecture for
an ESP ECU project. The project has 800 test cases
already defined manually by test analysts in TestRail.
The project manager asks why the TAE has not included
test generation capability in the architecture.

**Question:**
Which response best justifies the TAE's decision?

- A) Test generation is too expensive to implement
  and should always be avoided
- B) Test generation is an optional capability in
  the gTAA and is not needed when test cases are
  already manually defined
- C) Test generation only works for web applications
  and cannot be used for ECU testing
- D) Test generation requires a separate tool that
  is incompatible with ECUTest

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus explicitly states that test generation
is the only OPTIONAL capability in the gTAA.
The other three — definition, execution, adaptation —
are mandatory.

When 800 test cases already exist and are manually
defined, adding test generation provides no value
and adds unnecessary complexity.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Test generation is not always avoided — it is valuable for state-based systems |
| C | Test generation works for any system including ECU — via model-based testing |
| D | Tool compatibility is a project-specific concern, not a gTAA rule |

**Key rule:** Optional means assess the need first.
Do not add it just because it exists.

---

## Scenario 2 — Missing Interface Identification

**Situation:**
An automotive test team has built a complete TAF for
ABS ECU validation. The TAF executes 500 test cases
automatically on the HIL rack every night.
Test results are stored as XML files on a network drive.

The test manager complains that she cannot see which
requirements have been verified, which tests passed,
and what the overall quality status is without
manually parsing XML files.

**Question:**
Which gTAA interface is missing from this architecture?

- A) SUT Interface — the TAF is not connecting to
  the ECU correctly
- B) Configuration Management Interface — the pipeline
  is not triggering tests automatically
- C) Test Management Interface — automated results are
  not linked to the test management system
- D) Project Management Interface — automation progress
  is not being reported to the project manager

---

**✅ Correct Answer: C**

**Reasoning:**
The test management interface maps test case definitions
to automated test cases and makes results visible in
the test management tool (TestRail, Jira, etc.).

Without it, results exist only as raw XML files that
require manual analysis. The test manager cannot see
requirement coverage, pass/fail status, or quality
trends without this interface.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | SUT interface works — 500 tests execute successfully |
| B | Config management interface works — tests run nightly automatically |
| D | Project management interface is about development progress reporting, not test results |

**Automotive insight:**
This is one of the most common gaps in ECU test
automation. Teams build excellent execution pipelines
but results remain invisible to stakeholders because
the test management interface was never designed.

---

## Scenario 3 — TAF vs TAS vs TAA Terminology

**Situation:**
During an architecture review, three team members
make the following statements:

- Engineer A: *"The TAF is the complete automation
  system we have built including all tools,
  infrastructure, and scripts."*
- Engineer B: *"The TAA is the structural foundation
  inside our automation system."*
- Engineer C: *"The TAS is the complete automation
  solution, and the TAF is the framework
  foundation inside it."*

**Question:**
Which engineer is using the correct terminology?

- A) Engineer A
- B) Engineer B
- C) Engineer C
- D) All three are correct

---

**✅ Correct Answer: C**

**Reasoning:**

| Term | Correct Definition |
|------|-------------------|
| TAS | Complete automation solution — tools, scripts, infrastructure |
| TAF | Structural foundation INSIDE the TAS |
| TAA | Technical design blueprint of the TAS |

Engineer A confused TAF with TAS.
Engineer B confused TAA with TAF.
Engineer C used both terms correctly.

> ⭐ This terminology distinction appears in exam
> questions regularly. Memorize all three definitions.

---

## Scenario 4 — Adaptation Layer Risk

**Situation:**
A team is migrating their ABS ECU test automation
from one HIL vendor platform to another.
The test scripts, test data, and test reporting
all remain unchanged.

The project manager estimates the migration will
take 2 weeks. The TAE estimates 8 weeks.

**Question:**
Which gTAA capability best explains the TAE's
higher effort estimate?

- A) Test Definition — all test cases need to be
  rewritten for the new platform
- B) Test Execution — the new platform runs tests
  differently requiring full rework
- C) Test Adaptation — the adaptors connecting
  the TAF to the SUT must be rebuilt for
  the new HIL platform interfaces
- D) Test Generation — the model needs to be
  regenerated for the new platform

---

**✅ Correct Answer: C**

**Reasoning:**
The adaptation layer contains all platform-specific
connection logic — CAN adaptor interfaces, HIL API
calls, fault injection module connections, real-time
signal monitoring interfaces.

When the HIL vendor platform changes, the entire
adaptation layer must be rebuilt to match the new
platform's APIs, even though the test logic
(definition layer) remains unchanged.

This is exactly why the three-layer TAF architecture
exists — the migration only affects the adaptation
layer, not the test scripts. But rebuilding the
adaptation layer for a complex HIL system takes
significant effort.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Test definition unchanged — scripts stay the same |
| B | Test execution framework unchanged — runner logic stays |
| D | Test generation not used in this project |

**Architect insight:**
Well-designed adaptation layers use abstraction
interfaces so that platform changes require only
the adaptor implementation to change — not the
business logic or test scripts above it.

---

## Scenario 5 — Config Management Interface Failure

**Situation:**
An ECU firmware update is released on Friday evening.
The CI/CD pipeline automatically triggers the
nightly test suite at 2am Saturday.
On Monday morning, 95% of tests pass.

However, the software release manager notices that
the test suite that ran was version 2.3 but the
firmware was version 3.0. The test suite for
version 3.0 exists in Git but was not used.

**Question:**
Which gTAA interface failed and what is the
primary consequence?

- A) SUT Interface failed — the TAF connected to
  the wrong ECU
- B) Configuration Management Interface failed —
  the pipeline used the wrong testware version
  against the new firmware
- C) Test Management Interface failed — results
  were reported to the wrong test plan
- D) Project Management Interface failed — the
  release manager was not notified of the update

---

**✅ Correct Answer: B**

**Reasoning:**
The configuration management interface is responsible
for managing the relationship between CI/CD pipelines,
environments, and testware versions.

A correctly designed config management interface
ensures that when firmware version 3.0 is released,
the pipeline automatically uses testware version 3.0.

The 95% pass rate is meaningless — it reflects
how well version 3.0 firmware passes version 2.3
tests, not whether version 3.0 behavior is correct.
This is a silent false confidence situation.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | SUT interface worked — TAF connected and ran tests |
| C | Test management interface may work — wrong version reported |
| D | Notification is a process issue, not a gTAA interface failure |

**Key rule:**
Config management interface must enforce version
locking between testware and SUT release.
This is non-negotiable in safety-critical automotive.

---

## Scenario 6 — gTAA Capability Identification

**Situation:**
An ECUTest project performs the following activities:

1. Loads the ARXML file to identify signal definitions
2. Reads test case steps from an XML test definition file
3. Sends CAN messages to the ABS ECU via CAN adapter
4. Monitors WheelSpeedFL signal response at 10ms intervals
5. Compares actual signal value to expected value
6. Writes pass/fail result to an XML log file
7. Generates an HTML test report

**Question:**
Activities 3 and 4 together belong to which
gTAA capability?

- A) Test Definition
- B) Test Execution
- C) Test Adaptation
- D) Test Generation

---

**✅ Correct Answer: C**

**Reasoning:**
Test Adaptation provides the necessary functionality
to adapt automated tests for the various components
and interfaces of the SUT.

Sending CAN messages via a CAN adapter (activity 3)
and monitoring signal responses via the same adapter
(activity 4) are both adaptation activities —
they bridge the abstract test logic to the
physical ECU interface.

**Mapping all activities to gTAA capabilities:**

| Activity | gTAA Capability |
|----------|----------------|
| 1 — Load ARXML | Test Adaptation (interface definition) |
| 2 — Read test definition XML | Test Definition |
| 3 — Send CAN messages | Test Adaptation |
| 4 — Monitor signal response | Test Adaptation |
| 5 — Compare actual vs expected | Test Execution |
| 6 — Write XML log | Test Execution |
| 7 — Generate HTML report | Test Execution |

> ⭐ The boundary between Execution and Adaptation
> is a common exam question. Execution = run and log.
> Adaptation = connect to and interact with SUT.

---

## Quick Reference — gTAA Exam Rules

| Rule | Remember This |
|------|--------------|
| Only optional capability | Test Generation |
| Three mandatory capabilities | Definition + Execution + Adaptation |
| SUT interface purpose | TAF connects to and interacts with SUT |
| Test management interface purpose | Links automated results to test plan |
| Config management interface purpose | Version locks testware to SUT release |
| TAF vs TAS | TAF is inside TAS — not the same thing |
| Adaptation vs Execution | Adaptation connects to SUT, Execution runs and logs |
| Missing test mgmt interface | Results invisible to stakeholders |
| Missing config mgmt interface | Wrong version tested — silent false confidence |

---

*Next: Sub-Chapter 3.1.2 — How to Design a Test Automation Solution*