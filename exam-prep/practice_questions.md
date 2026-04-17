# ISTQB CTAL-TAE v2.0 — Practice Questions Bank

> **Coverage:** All 8 chapters
> **Mix:** K2 / K3 / K4 cognitive levels
> **Format:** Same as real exam — scenario-based MCQ
> **Usage:** Time yourself — 1.5 minutes per question

---

## How to Use This File

1. Work through questions without looking at answers
2. Mark your answer
3. Check answer section at the bottom
4. Track your score per chapter
5. Repeat weak areas until consistent

---

## Score Tracker

| Chapter | Questions | Your Score | Target |
|---------|-----------|-----------|--------|
| Ch 1 — Introduction | Q1-Q5 | — / 5 | 4 / 5 |
| Ch 2 — Preparing | Q6-Q10 | — / 5 | 4 / 5 |
| Ch 3 — Architecture | Q11-Q20 | — / 10 | 8 / 10 |
| Ch 4 — Implementing | Q21-Q28 | — / 8 | 7 / 8 |
| Ch 5 — CI/CD | Q29-Q34 | — / 6 | 5 / 6 |
| Ch 6 — Reporting | Q35-Q40 | — / 6 | 5 / 6 |
| Ch 7 — Verifying | Q41-Q46 | — / 6 | 5 / 6 |
| Ch 8 — Improvement | Q47-Q52 | — / 6 | 5 / 6 |
| **Total** | **52** | **— / 52** | **44 / 52** |

---

## Chapter 1 — Introduction and Objectives (K2)

### Q1
A team has been manually testing an ABS ECU for
14 months. Regression cycles take 2 weeks.
The team is considering automation.

Which factor MOST justifies the automation investment?

- A) Automation eliminates all human error from testing
- B) The high regression frequency means the time saved
  per cycle will recover the investment over time
- C) Automation allows permanent reassignment of all
  test engineers to development work
- D) Automated tests are more thorough than manual tests

---

### Q2
After a major firmware update, 90% of the automated
ABS test suite passes. The test manager declares
the release quality is good.

What is the MOST accurate critique of this conclusion?

- A) 90% pass rate is too low — 100% is required
- B) Automation only verifies what it is programmed
  to check — new firmware behavior outside existing
  test scope may not be detected
- C) The pass rate would be higher with more test cases
- D) The test manager should wait for manual testing
  to confirm the result

---

### Q3
A new infotainment system changes its UI every sprint.
A TAE proposes full UI test automation from day one.

Which disadvantage is MOST relevant to evaluate?

- A) Automation requires hiring a TAE
- B) Automated tests are rigid and less adaptable
  to SUT changes — high maintenance cost in a
  rapidly evolving UI
- C) Automation executes slower than manual testing
  for UI systems
- D) Automation cannot check UI test results

---

### Q4
In an Agile project, what is the goal called when
automated tests are delivered within the same sprint
as the feature they verify?

- A) Shift-right testing
- B) In-sprint automation
- C) Test-first development
- D) Continuous delivery

---

### Q5
Which statement about test automation limitations
is CORRECT according to CTAL-TAE v2.0?

- A) All manual tests can be automated given
  sufficient time and budget
- B) Automation can verify any quality characteristic
  if the right tool is selected
- C) Automation can only check results that can
  be verified by an automated test oracle
- D) Automation is equally effective for exploratory
  and regression testing

---

## Chapter 2 — Preparing for Test Automation (K4)

### Q6
A TAE is evaluating an ABS ECU for test automation.
The ECU outputs CAN signals but has no mechanism
for the TAF to inject fault conditions.

Which testability pillar is missing?

- A) Observability
- B) Architecture transparency
- C) Controllability
- D) Accessibility

---

### Q7
Which environment is the FIRST one where monitoring
must be present according to CTAL-TAE v2.0?

- A) Local development environment
- B) Build environment
- C) Integration environment
- D) Preproduction environment

---

### Q8
A tool evaluation comparison table shows:

| Criterion | Tool A | Tool B |
|-----------|--------|--------|
| CAN support | ✅ Native | ❌ None |
| Python scripting | ✅ | ✅ |
| CI/CD integration | ✅ | ✅ |
| License cost | 💰💰💰 | 🆓 Free |

The project requires CAN support as a MUST-HAVE.

Which tool should be recommended?

- A) Tool B — free licensing saves project budget
- B) Tool A — satisfies the must-have CAN requirement
  regardless of higher cost
- C) Neither — no tool satisfies all requirements
- D) Both — use Tool B for non-CAN tests and
  Tool A only when needed

---

### Q9
The ARXML file defines all CAN signal names,
IDs, and scaling for an ABS ECU project.
The ARXML is updated but the TAF is not.

Which testability pillar has been compromised
and what is the likely consequence?

- A) Controllability — the TAF can no longer
  inject signals into the ECU
- B) Architecture transparency — test automation
  may monitor wrong signal IDs causing silent
  false passes
- C) Observability — the ECU cannot provide
  outputs to the TAF
- D) All three pillars — ARXML affects everything

---

### Q10
Which type of testing is NOT performed in the
integration environment according to the syllabus?

- A) System integration testing
- B) API testing
- C) White-box testing
- D) Acceptance testing

---

## Chapter 3 — Test Automation Architecture (K3)

### Q11
In the Generic Test Automation Architecture (gTAA),
which capability is OPTIONAL?

- A) Test Definition
- B) Test Execution
- C) Test Adaptation
- D) Test Generation

---

### Q12
A TAE builds a test script that imports the
`CANSignalMonitor` class directly from core libraries
and uses it to read `"ABSActivationStatus"` with
the hardcoded value `0x02` in the assertion.

Which TAF layering rules are violated?

- A) Only one rule — the signal name is hardcoded
- B) Two rules — test script calls core library directly
  and contains SUT-specific signal names and values
- C) No rules — test scripts are allowed to use
  any available library
- D) One rule — assertions belong in business logic

---

### Q13
An ABS project has 12 calibration variants and
6 sensor fault modes — 72 test combinations.

Which automation approach produces 72 test
executions from ONE test script?

- A) Keyword-driven testing
- B) Behavior-driven development
- C) Data-driven testing
- D) Capture/playback

---

### Q14
Which design pattern ensures only ONE CAN bus
connection exists during the entire test suite
execution?

- A) Facade pattern
- B) Flow model pattern
- C) Page object model
- D) Singleton pattern

---

### Q15
When the ARXML renames a signal from
`"ABSActivationStatus"` to `"ABS_ActivationState"`,
which design pattern limits the update to ONE file?

- A) Singleton pattern
- B) Facade pattern
- C) Page object model
- D) Flow model pattern

---

### Q16
A test manager asks why the team adopted BDD
but testers are writing all Gherkin scenarios
without any involvement from systems engineers
or business representatives.

What is the PRIMARY problem?

- A) Gherkin syntax is being used incorrectly
- B) BDD is being used as a writing style only —
  the collaboration intent is missing entirely
- C) TAEs should not write BDD scenarios at all
- D) The scenarios are too technical for BDD

---

### Q17
The flow model pattern differs from the page
object model in which specific way?

- A) Flow model stores signal identifiers —
  POM stores user action sequences
- B) Flow model adds a facade layer above POM
  storing reusable multi-step user action sequences —
  POM stores identifiers and expected values only
- C) Flow model is used for mobile testing —
  POM is used for ECU testing
- D) Flow model and POM are the same pattern
  with different names

---

### Q18
Which automation approach requires tests to be
written BEFORE the feature is implemented?

- A) Data-driven testing
- B) Keyword-driven testing
- C) Test-driven development
- D) Behavior-driven development

---

### Q19
A TAF has three layers: test scripts, business
logic, and core libraries. The core libraries
are described as SUT-independent.

What does SUT-independent mean for core libraries?

- A) Core libraries do not need to be tested
- B) Core libraries contain no ABS, ESP, or
  project-specific knowledge — they work for
  any project on the same technology stack
- C) Core libraries are automatically generated
  by the CI/CD pipeline
- D) Core libraries can only be maintained by
  senior TAEs

---

### Q20
Which SOLID principle enables hardware-free
unit testing of business logic by allowing
a mock CAN monitor to replace the real one?

- A) Single Responsibility
- B) Open-Closed
- C) Dependency Inversion
- D) Liskov Substitution

---

## Chapter 4 — Implementing Test Automation (K4)

### Q21
A test automation pilot is defined.
Which activity should happen DURING the pilot
according to CTAL-TAE v2.0?

- A) Writing all 400 test cases for the full suite
- B) Integrating the pilot solution into CI/CD to
  expose infrastructure issues early
- C) Completing the full TAF architecture before
  any scripts are written
- D) Replacing all existing manual tests

---

### Q22
A CI/CD pipeline runs the ABS regression suite.
A log entry shows:

`[FATAL] HIL rack connection lost — aborting`

What is the correct behavior after this log entry?

- A) The failing test case is marked as failed
  and the next test case runs
- B) A warning is logged and execution continues
  with reduced functionality
- C) Test execution may be aborted — Fatal level
  indicates an error that may stop the entire run
- D) The pipeline retries the connection three times

---

### Q23
Test cases 11-20 in a suite always pass when
run after tests 1-10 but fail when run in isolation.

Which deployment risk explains this?

- A) Packaging risk — testware not versioned
- B) Test structuring risk — missing test fixtures
  mean tests are not atomic and depend on
  execution order
- C) Updating risk — tool version changed behavior
- D) Logging risk — insufficient logs prevent diagnosis

---

### Q24
Which logging level is used when an unexpected
condition occurs but the test case CONTINUES
without failing?

- A) Error
- B) Fatal
- C) Warn
- D) Info

---

### Q25
A TAE submits code with a method containing
12 input parameters and 80 lines of logic
doing connection, signal reading, fault injection,
verification, and cleanup.

Which TWO clean code principles are violated?

- A) Use logging and avoid hardcoding
- B) Avoid too many input parameters AND
  avoid long complex methods
- C) Use design patterns and focus on testability
- D) Common naming conventions and logical structure

---

### Q26
Which branching strategy does the CTAL-TAE
syllabus specifically recommend for testware?

- A) Single main branch with all commits
- B) Separate branches for features, releases,
  and defect fixes
- C) One branch per test engineer
- D) Separate repository per ECU project

---

### Q27
A deployed testware package cannot reproduce
a test failure from 3 weeks ago because:
- Scripts were modified after the failure
- ARXML file version is unknown
- Calibration CSV version is unknown

Which deployment risk caused this?

- A) Logging risk
- B) Test structuring risk
- C) Packaging risk — testware components were
  not version-controlled and tagged to the
  SW release at time of testing
- D) Infrastructure risk

---

### Q28
The syllabus reference for clean code principles
in test automation is:

- A) ISTQB Foundation Level Syllabus
- B) ISO/IEC 25010 quality characteristics
- C) Robert C. Martin "Clean Code" 2008
- D) IEEE 1671 test automation standards

---

## Chapter 5 — CI/CD Deployment Strategies (K3)

### Q29
Which test level belongs in the BUILD phase
of a CI/CD pipeline?

- A) System integration tests
- B) OEM acceptance tests
- C) Component tests and static analysis
- D) Performance efficiency tests

---

### Q30
In CI/CD pipeline Approach 1 for system test
integration, what happens when tests fail?

- A) Tests are skipped and deployment continues
- B) The pipeline reports failure but deployment
  remains live — manual rollback required
- C) The deployment fails and can be automatically
  rolled back based on test results
- D) The test suite reruns automatically three times

---

### Q31
Three components of configuration management
for testware are defined in the syllabus. Which
correctly lists all three?

- A) Test tools, test reports, test environments
- B) Test environment configuration, test data,
  test suites and test cases
- C) Test scripts, test logs, test metrics
- D) CI/CD pipeline, version control, test management

---

### Q32
Contract testing verifies that two services
can communicate with each other. How does it
differ from schema validation?

- A) Contract testing is automated —
  schema validation is manual
- B) Contract testing goes beyond schema validation
  by requiring both parties to agree on the
  allowed set of interactions over time
- C) Schema validation is more comprehensive
  than contract testing
- D) They are the same technique with different names

---

### Q33
In consumer-driven contract testing,
who defines the contract?

- A) The provider — showing how its service operates
- B) The consumer — setting expectations for how
  the provider should respond to its requests
- C) The TAE — independently of both parties
- D) The test manager — based on requirements

---

### Q34
A full ABS regression suite takes 3.5 hours.
Running it on every commit blocks developer feedback.

What is the recommended pipeline architecture?

- A) Reduce test cases until suite runs in 30 minutes
- B) Run fast smoke tests on every commit and full
  regression as a nightly pipeline
- C) Only run regression before releases
- D) Run tests in parallel to reduce to 30 minutes

---

## Chapter 6 — Reporting and Metrics (K4)

### Q35
Which metric is the MOST dangerous if
misinterpreted according to CTAL-TAE principles?

- A) Test execution time increasing
- B) Pass rate rising while defect detection rate
  is simultaneously declining — may indicate
  suite losing alignment with product
- C) Flaky rate below 5%
- D) Code coverage at 80%

---

### Q36
A test report shows a test case status as
"Blocked." What does this mean and how should
it be reported?

- A) Blocked is the same as Failed — report together
- B) Blocked means the test could not execute due
  to a precondition failure — report separately
  from Failed to distinguish SUT defects from
  infrastructure problems
- C) Blocked means the test passed with warnings
- D) Blocked tests should be excluded from reports

---

### Q37
The correct formula for pass rate is:

- A) Passed / Total test cases including skipped
- B) Passed / (Passed + Failed + Blocked + Error)
- C) Passed / (Passed + Failed) only
- D) (Passed + Warned) / Total

---

### Q38
An ABS automation report for an ISO 26262
safety-critical project must include which
additional fields NOT required for standard reports?

- A) Test execution time and pass rate
- B) ECU serial number, firmware version,
  requirements traceability, tester identification,
  and retention period
- C) CI/CD pipeline name and GitHub commit hash
- D) Number of test cases and defect count

---

### Q39
Which data collection timing captures baseline
values before stimulation in an ECU test?

- A) During execution only
- B) After execution — for comparison
- C) Before execution — to verify preconditions
  and capture baseline signal values
- D) At random intervals throughout execution

---

### Q40
A test suite has 200 tests. After analyzing results:
- 60 tests fail on component A only
- 40 tests fail on component B only
- 5 tests fail on components A and B together

This pattern indicates:

- A) Random failures — no pattern exists
- B) Failure cluster in components A and B —
  likely a defect in each component causing
  localized failures
- C) The entire test suite needs to be rewritten
- D) The TAF has a systematic defect

---

## Chapter 7 — Verifying the Test Automation Solution (K3)

### Q41
Before running a test suite, an environment
smoke test should complete within:

- A) 30 minutes — to be thorough
- B) 2 minutes — fast enough to not delay pipeline
  while still verifying critical preconditions
- C) The same time as one test case
- D) There is no time requirement for smoke tests

---

### Q42
A test case always passes even when the ECU
has a known defect. Investigation reveals:

```python
def test_abs_status():
    expected = 0x02
    actual = monitor.read_signal("ABSStatus")
    result = (actual == expected)
    # result is never asserted
```

What type of TAF defect is this?

- A) A flaky test — result varies per run
- B) A false negative — test always passes
  regardless of SUT behavior because the
  assertion result is never evaluated
- C) A false positive — test always fails
  regardless of SUT behavior
- D) An intermittent failure caused by timing

---

### Q43
Mutation testing is used to verify test automation
quality. What does it involve?

- A) Running tests on multiple hardware configurations
- B) Introducing deliberate small code changes to
  the SUT and verifying the TAF detects them —
  if mutants survive, the test suite has gaps
- C) Automatically generating new test cases
- D) Testing the TAF on a simulated SUT

---

### Q44
A pylint static analysis report shows:

| Issue | Severity |
|-------|---------|
| W0612 unused variable `expected_value` in assertion | Critical |
| W0702 bare except clause | Critical |
| C0301 line too long | Low |

Which issues MUST be fixed before the pipeline proceeds?

- A) All three — all issues block the pipeline
- B) Only C0301 — style issues are highest priority
- C) W0612 and W0702 — Critical severity blocks
  the pipeline, C0301 Low severity does not
- D) None — static analysis is advisory only

---

### Q45
Three root cause categories exist for test failures.
A test fails because the ECU firmware has a defect.
Which category applies?

- A) Test defect — the assertion is wrong
- B) Environment issue — infrastructure problem
- C) Product defect — the SUT behavior does not
  meet requirements
- D) TAF defect — the framework has a bug

---

### Q46
Which wait mechanism is MOST reliable for
CAN signal-based test automation?

- A) Hardcoded `time.sleep(0.5)` — simple and predictable
- B) Polling with dynamic wait — checks condition
  repeatedly until true or timeout
- C) Event subscription from SUT — most reliable
  but requires SUT to expose events to TAF
- D) No wait — read signal immediately after stimulation

---

## Chapter 8 — Continuous Improvement (K4)

### Q47
A test suite has 500 tests. Over 6 months:
- Pass rate rises from 80% to 97%
- Defect detection rate falls from 15 per sprint
  to 3 per sprint
- No major product changes were made

What does this data pattern indicate?

- A) Product quality has significantly improved
- B) The test suite is losing alignment with product
  behavior — rising pass rate with falling defect
  detection suggests tests no longer challenge
  the product effectively
- C) The team should reduce the test suite size
- D) This is expected normal behavior for mature products

---

### Q48
A test case tests ABS activation status,
DTC setting, warning lamp activation, and
CAN bus response timing — all in one test.

What improvement should be made?

- A) Add more assertions to make it more thorough
- B) Split into four single-behavior test cases —
  one behavior per test enables precise failure
  diagnosis and independent maintenance
- C) Remove the test — it is too complex to maintain
- D) Convert to BDD format for better readability

---

### Q49
Which metric threshold indicates a mandatory
investigation of flaky tests is required?

- A) Flaky rate > 1%
- B) Flaky rate > 5%
- C) Flaky rate > 10%
- D) Flaky rate > 20%

---

### Q50
A team wants to migrate from ECUTest to a new
tool. Which practice is mandatory during migration?

- A) Delete all ECUTest scripts before starting
- B) Run new tool and old tool in parallel —
  compare results before decommissioning old tool
- C) Migrate all scripts in one weekend to minimize
  transition period
- D) Stop running tests during migration

---

### Q51
The TAF core library has 200 functions.
Unit test coverage is currently 45%.
What is the target coverage for production-quality
core libraries?

- A) 100% — every function must be tested
- B) 60% — adequate for internal tools
- C) 85% or higher for core libraries
- D) Coverage is not relevant for TAF code

---

### Q52
When restructuring automated testware after
SUT updates, what is the FIRST action?

- A) Delete all existing tests and rewrite from scratch
- B) Migrate all tests to the new architecture simultaneously
- C) Establish a baseline pass rate before any
  restructuring begins — to measure impact of changes
- D) Update all signal names across all test files first

---

## Answer Key

| Q | A | Chapter | K-Level |
|---|---|---------|---------|
| 1 | B | Ch 1 | K2 |
| 2 | B | Ch 1 | K2 |
| 3 | B | Ch 1 | K2 |
| 4 | B | Ch 1 | K2 |
| 5 | C | Ch 1 | K2 |
| 6 | C | Ch 2 | K2 |
| 7 | C | Ch 2 | K2 |
| 8 | B | Ch 2 | K4 |
| 9 | B | Ch 2 | K4 |
| 10 | C | Ch 2 | K2 |
| 11 | D | Ch 3 | K2 |
| 12 | B | Ch 3 | K3 |
| 13 | C | Ch 3 | K3 |
| 14 | D | Ch 3 | K3 |
| 15 | C | Ch 3 | K3 |
| 16 | B | Ch 3 | K2 |
| 17 | B | Ch 3 | K2 |
| 18 | C | Ch 3 | K2 |
| 19 | B | Ch 3 | K2 |
| 20 | C | Ch 3 | K3 |
| 21 | B | Ch 4 | K3 |
| 22 | C | Ch 4 | K2 |
| 23 | B | Ch 4 | K4 |
| 24 | C | Ch 4 | K2 |
| 25 | B | Ch 4 | K2 |
| 26 | B | Ch 4 | K2 |
| 27 | C | Ch 4 | K4 |
| 28 | C | Ch 4 | K2 |
| 29 | C | Ch 5 | K3 |
| 30 | C | Ch 5 | K3 |
| 31 | B | Ch 5 | K2 |
| 32 | B | Ch 5 | K2 |
| 33 | B | Ch 5 | K2 |
| 34 | B | Ch 5 | K3 |
| 35 | B | Ch 6 | K4 |
| 36 | B | Ch 6 | K2 |
| 37 | C | Ch 6 | K2 |
| 38 | B | Ch 6 | K4 |
| 39 | C | Ch 6 | K3 |
| 40 | B | Ch 6 | K4 |
| 41 | B | Ch 7 | K3 |
| 42 | B | Ch 7 | K3 |
| 43 | B | Ch 7 | K3 |
| 44 | C | Ch 7 | K3 |
| 45 | C | Ch 7 | K3 |
| 46 | C | Ch 7 | K3 |
| 47 | B | Ch 8 | K4 |
| 48 | B | Ch 8 | K4 |
| 49 | B | Ch 8 | K4 |
| 50 | B | Ch 8 | K4 |
| 51 | C | Ch 8 | K4 |
| 52 | C | Ch 8 | K4 |

---

## Answer Explanations — Selected Key Questions

### Q2 — Why B
Automation only verifies what programmed to check.
New firmware behavior outside existing test scope
goes undetected. 90% pass rate proves existing
behavior is maintained — not that new behavior is correct.

### Q9 — Why B
Architecture transparency is the documentation
of interfaces. Stale ARXML means the TAF monitors
wrong CAN IDs. Tests run and pass because no
signal activity detected at old ID — silent false pass.

### Q12 — Why B
Rule 1 violated: scripts call core libraries directly.
Rule 2 violated: signal name and expected value
belong in business logic — not test scripts.

### Q23 — Why B
Test results depending on execution order =
missing test fixtures. Fixtures establish
known preconditions so each test is atomic
and independent of what ran before.

### Q35 — Why B
Rising pass rate + falling defect detection =
tests passing without finding real issues.
Classic sign of test suite losing alignment
with product. Most dangerous metric combination.

### Q42 — Why B
Unused variable holding assertion result =
false negative. Test always passes because
`result` is calculated but never evaluated.
Most dangerous TAF defect type.

### Q47 — Why B
Rising pass rate + falling defect detection
with no product changes = suite stagnation.
Tests are passing because they no longer
challenge the product — not because product improved.

---

## Weak Area Drill — If Score Below 4/5 Per Chapter

| Chapter | Key Rules to Revise |
|---------|-------------------|
| Ch 1 | Three question rule, test oracle limitation |
| Ch 2 | Three testability pillars, five environments, must-haves first |
| Ch 3 | gTAA four capabilities, TAF layer rules, seven approaches, four patterns |
| Ch 4 | Six pilot items, six logging levels, eight clean code principles |
| Ch 5 | Build vs deployment phase, Approach 1 vs 2, three config components |
| Ch 6 | Pass rate formula, Blocked vs Failed, trend over snapshot |
| Ch 7 | False negative definition, mutation testing, critical vs low severity |
| Ch 8 | Flaky rate threshold, one behavior per test, 85% coverage target |

---

*Use scenario_bank.md for multi-chapter complex scenarios*
*Use keyword_glossary.md for term definitions*
*Use chapter_summary.md for rapid pre-exam revision*