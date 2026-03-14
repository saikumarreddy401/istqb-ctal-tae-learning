# Chapter 2 — Exam Scenarios Practice

> **Syllabus Reference:** TAE-2.1.1 · TAE-2.1.2 · TAE-2.2.1 · TAE-2.2.2
> **Cognitive Level:** K4 — Analyze
> **Purpose:** Exam-style scenario practice with answers and traps explained

---

## How to Use This File

1. Read the scenario carefully
2. Cover the answer section
3. Pick your answer and reason
4. Then reveal and compare

---

## Scenario 1 — Testability Gap Discovery

**Situation:**
A TAE joins a project where an ABS ECU has already been
developed and delivered. The TAE is asked to build
automated tests for fault handling behavior.
After analysis, the TAE discovers:

- CAN signal outputs are readable via monitoring tools ✅
- No fault injection capability exists on the test bench ❌
- The ARXML file is 6 months old and not updated ❌

**Question:**
Which combination of testability pillars is missing?

- A) Observability and controllability
- B) Controllability and architecture transparency
- C) Observability and architecture transparency
- D) All three pillars are missing

---

**✅ Correct Answer: B**

**Reasoning:**
- Observability ✅ — CAN signals are readable
- Controllability ❌ — No fault injection = cannot drive
  the ECU into the states needed for fault testing
- Architecture transparency ❌ — Stale ARXML means
  the interface documentation cannot be trusted

**Why other options are wrong:**
- A: Observability EXISTS (signals are readable)
- C: Controllability is the more critical missing piece here
- D: Observability is confirmed as present

**Automotive insight:**
Stale ARXML is one of the most dangerous gaps —
tests can run and pass while verifying nothing,
because signal IDs have changed silently.

---

## Scenario 2 — Wrong Environment Choice

**Situation:**
A test team runs their full automated regression suite
including performance load tests and UAT scenarios
directly in the build environment after every code commit.
The build pipeline takes 4 hours to complete.
Developers complain that feedback is too slow.

**Question:**
What is the PRIMARY architectural mistake here?

- A) The team is running too many test cases
- B) Performance and UAT tests are being run in the
     wrong environment
- C) The build environment should not have any automation
- D) Developers should not receive test feedback

---

**✅ Correct Answer: B**

**Reasoning:**
The build environment is designed for component tests,
component integration tests, and static analysis only.
It must be fast to give developers immediate feedback.

Performance tests belong in **preproduction.**
UAT belongs in **preproduction** (business stakeholders).

Running them in the build environment violates the
shift-left principle — these tests are too heavy
for the early pipeline stage.

**Why other options are wrong:**
- A: The number of tests is not the stated problem
- C: Build environment SHOULD have automation — just
     the right type (component + static analysis)
- D: Developer feedback is exactly what build automation
     is designed to provide

**Key rule to remember:**

| Environment | What belongs there |
|-------------|-------------------|
| Build | Component + integration + static analysis |
| Integration | System + API + UI (black box) |
| Preproduction | Performance + UAT + full regression |

---

## Scenario 3 — Monitoring Placement

**Situation:**
A team has five environments set up: local development,
build, integration, preproduction, and production.
They currently have monitoring tools active only in
preproduction and production.

After a system integration test failure in the
integration environment, they cannot determine whether
the failure was caused by a SUT defect or a test
environment issue.

**Question:**
According to the CTAL-TAE syllabus, what is the
root cause of their diagnostic problem?

- A) They need better test logging in their TAF
- B) Monitoring should have been present from the
     integration environment onwards
- C) Integration environment should only run
     component tests which don't need monitoring
- D) Production monitoring is sufficient for
     diagnosing integration failures

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus explicitly states that the integration
environment is the **first environment where monitoring
must be present.**

Without monitoring in the integration environment,
there is no visibility into what the SUT was doing
when the test failed — making root cause analysis
nearly impossible.

**Why other options are wrong:**
- A: TAF logging helps but cannot replace environment
     monitoring for infrastructure-level failures
- C: Integration environment runs system/API/UI tests —
     not just component tests
- D: Production monitoring cannot retroactively diagnose
     what happened in a different environment

**Exam trap:** The question is about WHERE monitoring
starts — not whether monitoring exists at all.
Always: integration environment = first monitoring point.

---

## Scenario 4 — Tool Selection Analysis (K4)

**Situation:**
A team is selecting a test automation tool for a new
ESP ECU project. Their requirements are:

| Requirement | Priority |
|-------------|----------|
| CAN bus signal monitoring | Must have |
| ARXML import support | Must have |
| Python scripting capability | Must have |
| CI/CD pipeline integration | Should have |
| Low license cost | Nice to have |

They evaluate three tools:

| Criterion | Tool A | Tool B | Tool C |
|-----------|--------|--------|--------|
| CAN support | ✅ Native | ⚠️ Plugin | ❌ None |
| ARXML import | ✅ | ❌ | ❌ |
| Python scripting | ✅ | ✅ | ✅ |
| CI/CD integration | ✅ | ✅ | ⚠️ Manual |
| License cost | 💰💰💰 | 💰💰 | 🆓 Free |

**Question:**
Which tool should be recommended and why?

- A) Tool C — because it is free and supports Python
- B) Tool B — because it balances cost and most features
- C) Tool A — because it satisfies all must-have
     requirements
- D) No tool should be selected — none satisfies
     all requirements

---

**✅ Correct Answer: C**

**Reasoning:**
The syllabus approach to tool evaluation is to assess
tools against requirements with priorities.

Must-have requirements are non-negotiable:
- CAN support → Tool A ✅ Tool B ⚠️ Tool C ❌
- ARXML import → Tool A ✅ Tool B ❌ Tool C ❌
- Python scripting → All three ✅

Only Tool A satisfies ALL must-have requirements.
High license cost is a "nice to have" concern —
important but not a disqualifier when must-haves
are at stake.

**Why other options are wrong:**
- A: Tool C fails two must-have requirements —
     cost cannot override mandatory needs
- B: Tool B fails ARXML import — a must-have
- D: Tool A satisfies all must-haves — selection
     is justified

**Exam pattern:** Always resolve must-haves first.
Nice-to-haves never override must-haves in tool
selection analysis.

---

## Scenario 5 — SUT Analysis Before Automation

**Situation:**
A TAE is asked to build automated tests for a new
vehicle network validation project. The project involves:

- 3 ECUs communicating over CAN
- 12 software calibration variants per ECU
- Test team has Python skills but no ECUTest experience
- Tests must run nightly in CI/CD pipeline
- Third-party sensor ECU is involved with no
  source code access

**Question:**
Which SUT analysis factor presents the HIGHEST risk
to the automation strategy?

- A) The 12 calibration variants per ECU
- B) The team's lack of ECUTest experience
- C) The third-party sensor ECU with no source access
- D) The requirement to run tests nightly in CI/CD

---

**✅ Correct Answer: C**

**Reasoning:**
The syllabus explicitly lists handling third-party
dependencies as a key SUT analysis factor.

A third-party ECU with no source code access means:
- No controllability over its internal behavior
- No observability into its internal state
- Cannot inject fault conditions into it
- Must use mocks, stubs, or simulators instead

This is the highest risk because it directly limits
what can be tested and how — requiring architectural
decisions (stub design, contract testing, simulation
models) before any scripting begins.

**Why other options are lower risk:**
- A: 12 variants is a data-driven testing challenge —
     solvable with parameterization
- B: Tool experience gap is a training/ramp-up issue —
     manageable with time
- D: CI/CD integration is a deployment concern —
     solvable with pipeline configuration

**Automotive insight:**
Third-party ECU dependency is extremely common in
vehicle projects. Always plan for simulation or
stub strategy before committing to automation scope.

---

## Scenario 6 — Stale Architecture Documentation

**Situation:**
An automation team has been running CAN signal
validation tests for 6 months. After a major ECU
software update, 85% of tests continue to pass.
However, during a manual review, an engineer notices
that several ECU behaviors have clearly changed
compared to the requirements document.

**Question:**
What is the most likely explanation for this situation
from a testability perspective?

- A) The test scripts have defects in their assertions
- B) The ARXML used by the TAF was not updated to
     match the new software release
- C) The ECU observability interfaces were removed
     in the new software version
- D) The CI/CD pipeline is running the wrong
     test suite version

---

**✅ Correct Answer: B**

**Reasoning:**
This is the classic stale ARXML silent failure pattern.

When ARXML is not updated after a software release:
- TAF monitors signals at old CAN IDs
- New software broadcasts on new or changed IDs
- Old IDs show no activity
- Tests that expect "no fault" pass incorrectly
- Behavioral changes go undetected

The 85% pass rate with known behavioral changes is
the signature of this problem — tests are not
actually verifying current behavior.

**Why other options are less likely:**
- A: Script assertion defects would cause consistent
     failures, not 85% pass with known behavior changes
- C: Removed observability interfaces would cause
     test execution errors, not silent passes
- D: Wrong test suite version would show version
     mismatch errors in CI/CD logs

**Key takeaway:**
ARXML version must be locked to SW release version
in version control. This is an architecture governance
requirement, not just a process suggestion.

---

## Quick Reference — Chapter 2 Exam Rules

| Rule | Remember This |
|------|--------------|
| Testability pillars | Observability + Controllability + Transparency |
| First monitoring environment | Integration environment |
| Build environment tests | Component + integration + static analysis only |
| Preproduction purpose | NFR testing + UAT + full regression |
| Tool selection order | Must-haves first, then should-haves, then nice-to-haves |
| Stale ARXML risk | Silent false passes — most dangerous failure mode |
| Third-party dependency | Always plan stub/mock/simulator strategy first |
| K4 exam approach | Analyze scenario → identify violated principle → eliminate traps |

---

## My Own Scenarios

> Add scenarios from your Day 1 training session here.
> Format: Situation → Question → Options → Answer → Reasoning

---

*Next: Chapter 3 — Test Automation Architecture exam scenarios*