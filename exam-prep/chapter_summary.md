# ISTQB CTAL-TAE v2.0 — Complex Scenario Bank

> **Purpose:** Multi-chapter scenarios combining concepts
> **Difficulty:** Higher than standard exam questions
> **Usage:** Final preparation — tests integrated thinking
> **Time:** Allow 3-4 minutes per scenario

---

## How to Use This File

These scenarios combine concepts from multiple chapters.
Real exam questions often test cross-chapter application.
Work through each scenario before reading the answer.

---

## Scenario 1 — Architecture Failure Analysis (Ch 2 + Ch 3 + Ch 4)

**Situation:**
An ABS ECU automation project has been running for
8 months. The team reports:

- 600 test scripts all import CANSignalMonitor directly
- Signal name "ABSActivationStatus" hardcoded in 480 scripts
- ARXML updated every 3 weeks with SW releases
- 2 TAEs spend 65% of time on maintenance
- Test execution order matters — tests 50-100 fail
  when run before tests 1-49
- No feature branches — all commits go directly to main
- No static analysis in CI/CD pipeline

**Question:**
Identify the THREE most critical architectural problems
and map each to its syllabus chapter and concept.

---

**✅ Answer:**

**Problem 1 — TAF Layer Violation (Chapter 3)**

Scripts calling core libraries directly violates the
fundamental TAF layering rule. Signal names hardcoded
in 480 scripts means every ARXML update requires
touching hundreds of files.

Root cause: No business logic layer. No POM equivalent.
Fix: Introduce signal object class (POM pattern).
Move all signal names to one class.
Impact: Reduces ARXML update effort from days to minutes.

**Problem 2 — Missing Test Fixtures (Chapter 4)**

Tests 50-100 failing when run before tests 1-49 is
the classic sign of non-atomic tests.
Tests depend on execution order — missing setup/teardown.

Root cause: No test fixture defining preconditions.
Fix: Add `setup_method()` and `teardown_method()`.
Impact: Tests become atomic — any order produces
same results.

**Problem 3 — No Static Analysis or Branching (Chapter 4)**

No static analysis means layer violations accumulate
undetected. No feature branches means one broken commit
affects the entire team simultaneously.

Root cause: Missing maintainability practices.
Fix: Add pylint to CI/CD pipeline. Implement
feature/ release/ bugfix/ branching strategy.
Impact: Code quality enforced automatically.
Team isolation prevents cascade failures.

---

## Scenario 2 — Pilot Failure Investigation (Ch 4 + Ch 5)

**Situation:**
A TAE runs a 4-week ABS HIL automation pilot.

Week 1-3: 12 test cases written, all passing locally.
Week 4: TAE attempts CI/CD integration.
Discovers Jenkins agent on office network cannot
reach HIL rack on lab network (firewall).
IT ticket raised — 6 weeks for firewall approval.

Pilot declared "successful" and full deployment
of 300 test cases begins while firewall is pending.

Month 2: Team has 300 test cases written.
Firewall still pending. No CI/CD execution.
Nightly runs triggered manually only.

**Question:**
What pilot guideline was violated, what should
have happened, and what is the correct recovery plan?

---

**✅ Answer:**

**Guideline violated (Chapter 4 — Section 4.1.1):**
CI/CD integration is mandatory DURING the pilot —
not after. The syllabus explicitly states:
*"During the pilot, it is also recommended to try
to integrate the solution into the CI/CD."*

CI/CD integration was treated as post-pilot work.
The firewall issue — a HIGH probability, HIGH impact
infrastructure risk — was discovered at the worst
possible time: when 300 tests depend on it.

**What should have happened:**
- Week 1: Attempt CI/CD integration immediately
- Week 1: Firewall issue discovered with only 12 tests
- Week 1: IT ticket raised — 6 weeks starts earlier
- Pilot continues — full deployment begins AFTER
  firewall is resolved and CI/CD confirmed working
- Full deployment on solid infrastructure

**Recovery plan:**
1. Pause new test case development at 300 cases
2. Escalate firewall ticket with business impact data
3. As interim: set up VPN or jump host as workaround
4. Document infrastructure requirements formally
5. Resume full deployment only when CI/CD confirmed
6. Lesson learned: infrastructure validation = week 1
   of every future pilot

---

## Scenario 3 — Silent Failure Investigation (Ch 2 + Ch 6 + Ch 7)

**Situation:**
The ABS nightly regression suite reports 96% pass rate
consistently for 6 weeks. The team is confident.

A systems engineer manually verifies one ABS scenario
and finds the ECU behavior changed 4 weeks ago
when a new firmware was released. The automated
suite never detected it.

Investigation reveals:
- ARXML was updated 4 weeks ago with new signal names
- TAF was NOT updated — still uses old signal names
- Old signal names no longer exist on CAN bus
- Tests monitor signals that are never transmitted
- "No fault detected" matches expected result — passes

**Question:**
Identify the failure chain from architecture to reporting
and what multi-layer defense would have prevented it.

---

**✅ Answer:**

**Failure chain:**

| Layer | What Failed |
|-------|------------|
| Architecture transparency (Ch 2) | ARXML version not locked to SW release |
| Configuration management (Ch 5) | Testware not tagged to SW release version |
| Test execution (Ch 7) | No environment verification before suite start |
| Reporting (Ch 6) | 96% pass rate reported as quality indicator without defect detection trend analysis |

**The silent false pass mechanism:**
Old signal name → not on CAN bus → no value received
→ timeout → default value → matches "no fault" expectation
→ PASS → repeated 6 weeks → 96% reported confidently

**Multi-layer defense:**

**Layer 1 — Config management (Ch 5):**
Lock ARXML version to SW release tag in Git.
TAF build fails if ARXML version does not match
current SW release.

**Layer 2 — Environment verification (Ch 7):**
Pre-suite smoke test verifies expected signals
are actively transmitting on CAN bus.
If ABSActivationStatus not seen in 2 seconds →
smoke test fails → suite does not run.

**Layer 3 — Metric analysis (Ch 6):**
Track defect detection rate alongside pass rate.
Rising pass rate + zero defects for 6 weeks =
alert for test suite alignment review.

**Layer 4 — Architecture (Ch 3):**
Signal names in POM class.
POM class validated against ARXML on TAF build.
Build fails if ARXML and POM disagree.

---

## Scenario 4 — Tool Selection Under Constraints (Ch 2 + Ch 8)

**Situation:**
An ESP ECU project must select a test automation tool.
Requirements gathered from stakeholders:

| Requirement | Priority |
|-------------|---------|
| CAN/LIN signal monitoring | Must-have |
| ARXML import | Must-have |
| Python scripting | Must-have |
| CI/CD integration | Should-have |
| Low license cost | Nice-to-have |
| AI-assisted test generation | Nice-to-have |

Tool evaluation results:

| Criterion | Tool A | Tool B | Tool C |
|-----------|--------|--------|--------|
| CAN/LIN support | ✅ Native | ⚠️ Plugin | ❌ None |
| ARXML import | ✅ | ❌ | ❌ |
| Python scripting | ✅ | ✅ | ✅ |
| CI/CD integration | ✅ | ✅ | ⚠️ Manual |
| License cost | 💰💰💰 | 💰💰 | 🆓 Free |
| AI test generation | ❌ | ✅ | ✅ |

The test manager prefers Tool C because it is free
and has AI test generation. A junior TAE prefers
Tool B because it balances cost and features.

**Question:**
Which tool should be recommended, what is the
justification, and how do you respond to the
test manager and junior TAE?

---

**✅ Answer:**

**Recommended: Tool A**

**Justification (Chapter 2 — Section 2.2.2):**
Must-have requirements are non-negotiable.
Must-haves are evaluated first — cost is nice-to-have.

| Must-Have | Tool A | Tool B | Tool C |
|-----------|--------|--------|--------|
| CAN/LIN native | ✅ | ⚠️ Plugin only | ❌ |
| ARXML import | ✅ | ❌ | ❌ |
| Python | ✅ | ✅ | ✅ |

Only Tool A satisfies ALL three must-haves.
Tool B fails ARXML import — a must-have.
Tool C fails CAN/LIN AND ARXML — two must-haves.

**Response to test manager:**
"Tool C cannot import ARXML — which means it cannot
read signal definitions for CAN validation. This is
our core requirement. A free tool that cannot do the
core job costs more in workarounds and custom
development than the Tool A license. AI test
generation is attractive but it is a nice-to-have
that cannot override two missing must-haves."

**Response to junior TAE:**
"Tool B's CAN support is a plugin — not native.
Plugins create dependency risk: if the plugin is
not maintained, CAN support breaks. More critically,
Tool B has no ARXML import. Every signal would need
to be manually defined — immediately negating any
cost saving from the license. Tool A is the only
technically sound choice."

**Chapter 8 note:**
If the team later needs AI test generation,
this can be evaluated as an additional tool
complementing Tool A — not replacing it.
Must-haves first. Enhancement tools second.

---

## Scenario 5 — Metrics Misinterpretation (Ch 6 + Ch 8)

**Situation:**
An ABS automation suite dashboard shows after
12 months of continuous improvement:

| Metric | Month 1 | Month 6 | Month 12 |
|--------|---------|---------|---------|
| Pass rate | 72% | 88% | 97% |
| Defect detection | 18/sprint | 9/sprint | 2/sprint |
| Flaky rate | 12% | 6% | 3% |
| Test count | 200 | 350 | 500 |
| Assertion density | 3.2 | 2.8 | 1.6 |

The project manager presents this to the OEM
as evidence of excellent quality improvement.

**Question:**
Analyze each metric trend. Which trends are
genuinely positive, which are concerning, and
what do the combined trends actually indicate?

---

**✅ Answer:**

**Metric by metric analysis:**

| Metric | Trend | Assessment |
|--------|-------|-----------|
| Pass rate 72%→97% | Rising | ⚠️ Concerning without context |
| Defect detection 18→2/sprint | Falling sharply | ❌ RED FLAG |
| Flaky rate 12%→3% | Falling | ✅ Positive improvement |
| Test count 200→500 | Rising | ✅ Coverage growing |
| Assertion density 3.2→1.6 | Falling | ❌ RED FLAG |

**The combined picture (Chapter 6 + Chapter 8):**

Rising pass rate + falling defect detection
= classic suite stagnation pattern.
500 tests running, 97% passing, finding 2 defects
per sprint is far WORSE than 200 tests finding 18.

The suite has grown in quantity while declining in
quality — tests are being added that pass easily
without challenging real product behavior.

Assertion density dropping from 3.2 to 1.6 per test
confirms this — tests have fewer meaningful checks.
Below 2.0 is the threshold for false negative risk.

Flaky rate improvement IS genuine — this is the one
real improvement in the dataset.

**What to tell the project manager:**
"Pass rate rising while defect detection falls is not
evidence of quality improvement — it is evidence
that our test suite is losing alignment with the product.
We need to audit assertion quality, add tests that
challenge new features, and establish a defect
injection exercise to verify the suite can still
find defects it should find."

---

## Scenario 6 — Multi-System TAF Architecture (Ch 3 + Ch 4 + Ch 5)

**Situation:**
A Bosch department has three ECU projects:

| Project | ECU | Team | Status |
|---------|-----|------|--------|
| Project A | ABS | 3 TAEs | Running 18 months |
| Project B | ESP | 2 TAEs | Starting now |
| Project C | Braking ECU | 1 TAE | Starting in 3 months |

Project A has a working core CAN library.
Project B needs to start automation immediately.
Project C is resource-constrained — 1 TAE only.

**Question:**
Design the TAF architecture strategy for all
three projects covering: layer structure, core
library sharing, CI/CD integration, and
configuration management.

---

**✅ Answer:**

**Architecture strategy:**

**Layer structure (Chapter 3 — Section 3.1.3):**

Core libraries built by Project A become the
foundation for all three projects.
Project C with 1 TAE gets immediate value
without rebuilding utilities from scratch.

**Core library governance (Chapter 3 + Chapter 8):**
- Core libraries versioned independently in Git
- Semantic versioning: major.minor.patch
- Breaking changes: deprecate old API, add new,
  give all teams 2 sprint migration window
- Each project pins core library version in
  requirements.txt

**CI/CD integration (Chapter 5 — Section 5.1.1):**

| Project | Build Phase | Deployment Phase |
|---------|------------|-----------------|
| Project A | SIL + TAF config + static analysis | HIL system tests |
| Project B | TAF config + pylint | HIL system tests (separate rack) |
| Project C | TAF config | HIL tests (shared rack — booking required) |

Project C risk: shared HIL rack availability.
Mitigation: dedicated CI time slot, rack health
check as pre-suite gate.

**Configuration management (Chapter 5 — Section 5.1.2):**

| Project | Testware Release Approach |
|---------|--------------------------|
| Project A (mature) | Versioned release — Git tags matching SW versions |
| Project B (new) | Feature toggles initially — migrate to versioned after 3 months |
| Project C (constrained) | Feature toggles — simpler to maintain with 1 TAE |

Environment configs: separate YAML per environment
per project. Stored in each project's repo.
Never shared between projects — environments differ.

**Pilot for Project B (Chapter 4 — Section 4.1.1):**
2-week pilot before full deployment.
Week 1: 5 test cases + CI/CD integration immediately.
Evaluate: ECUTest reuse from Project A, firewall
access to ESP HIL rack, team skill gaps.
Week 2: evaluate results, go/no-go decision.

---

## Scenario 7 — Verification Failure Root Cause (Ch 7 + Ch 4)

**Situation:**
A TAE investigates why two test cases produce
unexpected results:

**Test Case A:** Always passes — even when ECU
has a known DTC fault active.

```python
def test_no_active_dtcs():
    dtc_list = diagnostics.read_active_dtcs()
    expected_empty = []
    result = (dtc_list == expected_empty)
    # Function ends here — result not asserted
```

**Test Case B:** Fails intermittently — passes
roughly 60% of runs, fails 40%, no code changes.

```python
def test_abs_response_time():
    fault.inject_open_circuit("front_left")
    time.sleep(0.5)  # hardcoded wait
    status = monitor.read_signal("ABSStatus")
    assert status == ABS.STATUS_DEGRADED
```

**Question:**
Diagnose each test case, identify the defect type,
and provide the corrected implementation.

---

**✅ Answer:**

**Test Case A — False Negative (Chapter 7)**

Defect type: False negative — test always passes
regardless of SUT behavior.

Root cause: `result` is calculated but never
evaluated with an assert statement.
The comparison runs, stores True or False,
then the function returns without checking.

Impact: This test provides zero quality assurance.
DTCs can be active — test always passes.
This is the most dangerous TAF defect type.

**Corrected implementation:**
```python
def test_no_active_dtcs():
    """Verify no active DTCs present before test suite."""
    dtc_list = diagnostics.read_active_dtcs()
    assert dtc_list == [], (
        f"Expected no active DTCs but found: {dtc_list}"
    )
```

---

**Test Case B — Flaky Test (Chapter 7 + Chapter 4)**

Defect type: Flaky test caused by hardcoded sleep.

Root cause: `time.sleep(0.5)` hardcoded.
ECU response time varies with system load.
When ECU responds in 480ms — test passes.
When ECU responds in 520ms — test fails.
40% failure rate = timing margin is borderline.

Impact: Flaky tests erode confidence.
Team stops trusting pipeline results.
Real failures masked by "probably flaky" assumption.

**Corrected implementation:**
```python
def test_abs_response_time():
    """
    Verify ABS transitions to degraded mode within
    MAX_DEGRADED_RESPONSE_MS after fault injection.
    Uses dynamic wait with timeout — never hardcoded sleep.
    """
    fault.inject_open_circuit("front_left")
    result = monitor.wait_for_signal(
        signal_name    = ABS.ABS_STATUS,
        expected_value = ABS.STATUS_DEGRADED,
        timeout_ms     = ABS.MAX_DEGRADED_RESPONSE_MS
    )
    assert result, (
        f"ABS did not reach DEGRADED state within "
        f"{ABS.MAX_DEGRADED_RESPONSE_MS}ms of fault injection"
    )
```

Signal-based wait with timeout is the most reliable
mechanism — waits exactly as long as needed,
fails clearly if timeout exceeded.

---

## Scenario 8 — Contract Testing Decision (Ch 5 + Ch 3)

**Situation:**
An automotive gateway ECU routes messages between
three ECUs: ABS, ESP, and the Body Control Module.
Each ECU exposes a UDS diagnostic service.

A TAE must design integration testing for the
gateway's routing behavior.

Current approach: full system integration tests
require all three ECUs to be flashed and running.
Test setup takes 45 minutes per run.
Any single ECU firmware change triggers full rerun.

**Question:**
How could contract testing reduce this dependency
and at which pipeline stage should it run?

---

**✅ Answer:**

**Current problem:**
Full system integration tests create tight coupling.
All three ECUs must be available simultaneously.
Single ECU change = 45-minute setup for all.
This violates shift-left principle.

**Contract testing solution (Chapter 5 — Section 5.1.3):**

Each ECU service has a defined UDS interaction
contract — what requests it accepts, what responses
it returns, what error codes it generates.

**Consumer-driven approach for gateway testing:**
**Benefits:**
- Gateway can be tested with ABS mock satisfying contract
- ABS can verify contract without gateway present
- Defects in interface detected in build phase
- Full system tests reserved for behavioral verification

**Pipeline stage assignment (Chapter 5 — Section 5.1.1):**

| Test Type | Stage | Reason |
|-----------|-------|--------|
| Contract verification | Build phase | No hardware needed — fast |
| Schema validation | Build phase | JSON/ARXML structure check |
| Full system integration | Deployment phase | All ECUs needed |

Contract testing runs in the BUILD phase —
catching interface defects in seconds instead of
after 45 minutes of hardware setup.
Full system tests still needed — but triggered
only after contracts pass.

---

## Cross-Chapter Rules Summary

| Concept | Chapter | The Rule |
|---------|---------|---------|
| Test Generation | 3 | Only optional gTAA capability |
| Scripts and core | 3 | Scripts NEVER call core directly |
| Pilot CI/CD | 4 | Mandatory DURING pilot — not after |
| Fatal vs Error | 4 | Fatal aborts — Error fails single test |
| Test fixtures | 4 | Enable atomic and repeatable tests |
| Integration monitoring | 2 | First environment with monitoring |
| Stale ARXML | 2+5 | Silent false passes — most dangerous |
| Must-haves | 2+8 | Always override cost |
| Pass rate formula | 6 | Passed / (Passed + Failed) only |
| Blocked reporting | 6 | Separate from Failed — always |
| False negative | 7 | Most dangerous TAF defect |
| Flaky threshold | 8 | > 5% = mandatory investigation |
| Baseline before restructure | 8 | Always — measure before changing |
| Contract vs schema | 5 | Contract = interaction agreement over time |
| Consumer-driven | 5 | Consumer sets expectations |

---

*All exam-prep files complete*
*Use practice_questions.md for timed exam practice*
*Use keyword_glossary.md for term definitions*
*Use chapter_summary.md on exam day morning*
*Use this file for final integrated thinking practice*