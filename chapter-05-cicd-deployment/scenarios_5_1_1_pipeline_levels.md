# Sub-Chapter 5.1.1 — Exam Scenarios Practice (Pipeline Levels)

> **Syllabus Reference:** TAE-5.1.1
> **Cognitive Level:** K3 — Apply
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Test Level Assignment

**Situation:**
An ESP ECU project has the following automated tests:

| Test | Description |
|------|-------------|
| A | SIL unit tests for ESP SW components |
| B | HIL system tests verifying ESP activation |
| C | TAF configuration tests checking ARXML exists |
| D | CAN signal validation across all variants |
| E | OEM acceptance tests on preproduction HIL rack |

**Question:**
Which tests belong in the BUILD phase pipeline?

- A) Tests B, D, and E — they verify the complete system
- B) Tests A and C only — SIL unit tests and TAF
  configuration tests belong in the build phase
- C) All five tests — everything should run on every commit
- D) Only Test A — configuration tests run separately

---

**✅ Correct Answer: B**

**Reasoning:**
Build phase contains tests that:
- Do not require hardware deployment
- Run fast enough for developer feedback
- Act as quality gates before artifact creation

| Test | Phase | Reason |
|------|-------|--------|
| A — SIL unit tests | BUILD ✅ | No hardware needed, fast |
| B — HIL system tests | DEPLOYMENT | Requires flashed ECU on HIL rack |
| C — TAF config tests | BUILD ✅ | Verify TAF files — no SUT needed |
| D — CAN validation | DEPLOYMENT | Requires running ECU on CAN bus |
| E — OEM acceptance | DEPLOYMENT | Requires preproduction environment |

**Why C is wrong:**
Running HIL system tests on every commit would
make the build phase take hours — blocking
developer feedback loops completely.

**Key rule:**
Build phase = fast, no hardware.
Deployment phase = hardware required, slower.

---

## Scenario 2 — Approach 1 vs Approach 2

**Situation:**
A safety-critical ABS ECU project is setting up
CI/CD pipelines for system test integration.

The test manager asks:
*"If the system tests fail after deployment,
can we automatically roll back the firmware
to the previous version?"*

**Question:**
Which pipeline approach satisfies this requirement
and what is the tradeoff?

- A) Approach 2 — separate test pipeline can
  trigger automatic rollback after failure
- B) Approach 1 — tests run as part of deployment
  phase so deployment fails and rolls back
  automatically on test failure. Tradeoff:
  if tests need rerun, redeployment is required
- C) Neither approach supports automatic rollback —
  rollback is always a manual operation
- D) Approach 2 with manual rollback scripts
  satisfies this requirement equally

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus states for Approach 1:

> *"This can be beneficial, as based on the test
> results, the deployment can fail and also be
> rolled back."*

**Approach comparison for safety-critical ABS:**

| Property | Approach 1 | Approach 2 |
|----------|-----------|-----------|
| Tests as quality gate | ✅ Yes | ❌ No |
| Automatic rollback on failure | ✅ Yes | ❌ Manual only |
| Rerun without redeployment | ❌ No | ✅ Yes |
| Best for safety-critical | ✅ Yes | ❌ No |

**The tradeoff explicitly stated in syllabus:**
Approach 1 rollback benefit comes at the cost of
requiring redeployment if tests simply need rerun
(not because of a real defect).

For safety-critical automotive systems where
incorrect firmware must never remain deployed,
Approach 1 is the correct choice.

**Why A is wrong:**
Approach 2 is explicitly a SEPARATE pipeline
that does NOT act as a deployment quality gate
and cannot trigger automatic rollback.

---

## Scenario 3 — Configuration Tests Value

**Situation:**
A nightly ABS regression pipeline runs 300 test cases.
Every Wednesday morning all 300 tests fail with:
```
FileNotFoundError: abs_signals.arxml not found
at path: config/abs_signals.arxml
```

Investigation reveals the ARXML file path was
changed from `config/` to `arxml/` during
Tuesday's refactoring commit.

The entire nightly run — 300 tests — produced
no useful results. The HIL rack ran for 4 hours
producing only FileNotFoundErrors.

**Question:**
Which test type would have caught this problem
immediately in the build phase before the
nightly run was triggered?

- A) Additional system tests checking file access
- B) TAF configuration tests that verify all
  required file paths exist during the TAF build —
  catching the missing ARXML in seconds not hours
- C) Static analysis would have detected
  the wrong file path
- D) The ARXML path should be hardcoded to
  prevent accidental changes

---

**✅ Correct Answer: B**

**Reasoning:**
Configuration tests are a subspecies of component
tests that run during the TAF BUILD step.

**What the configuration test would look like:**
```python
def test_arxml_file_at_expected_path():
    """
    Verify ARXML file exists at configured path.
    Catches path changes before nightly run.
    """
    arxml_path = Path(config.ARXML_PATH)
    assert arxml_path.exists(), (
        f"ARXML not found at {arxml_path}. "
        f"Check ARXML_PATH in config."
    )
```

**Timeline comparison:**

| Scenario | When Discovered | Impact |
|----------|----------------|--------|
| No config tests | Wednesday 06:00 after 4hr run | 300 tests = zero results |
| With config tests | Tuesday during build (seconds) | Build fails immediately, dev fixes path |

**Why C is wrong:**
Static analysis checks code quality and syntax —
it does not verify runtime file path existence.

**Key exam rule:**
Configuration tests catch environment problems
BEFORE tests execute — saving entire runs
from producing false or zero results.

---

## Scenario 4 — Nightly Regression Purpose

**Situation:**
A TAE proposes running the full 400-case ABS
regression suite on every commit to main.
Each commit triggers the full suite.
The suite takes 3.5 hours on the HIL rack.

After one week developers complain:
- They cannot get feedback for 3.5+ hours
- Multiple commits queue behind each other
- The HIL rack is booked solid
- Hotfix commits wait hours behind regular commits

**Question:**
Which pipeline architecture change solves this
while maintaining regression coverage?

- A) Remove test cases until the suite runs
  in under 30 minutes
- B) Split tests — run a fast smoke suite
  on every commit in the deployment phase,
  run the full regression suite as a separate
  nightly pipeline at 02:00 daily
- C) Buy more HIL racks to run tests in parallel
  on every commit
- D) Only run regression testing weekly
  to reduce HIL rack usage

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus specifically addresses this:

> *"A regression test suite can be run every night
> (i.e., the nightly regression), especially for
> longer running test suites, so the team will
> have a clear picture of the quality of the SUT
> in the morning."*

**Correct architecture:**

| Pipeline | Trigger | Tests | Duration |
|----------|---------|-------|---------|
| Commit pipeline | Every commit | 20 smoke tests | 15 min |
| Nightly pipeline | 02:00 daily | 400 full regression | 3.5 hours |

**Benefits:**
- Developers get 15-minute feedback on commits
- Full regression results ready at 06:00
- HIL rack used efficiently
- Coverage maintained — just at different frequency

**Why C is wrong:**
More hardware solves capacity but not the
developer feedback loop problem.
Even with 10 racks, 3.5 hours on every commit
means 3.5 hours wait for developers.

---

## Scenario 5 — Pipeline Stage Identification

**Situation:**
A TAE is designing a pipeline for an ESP ECU project.
She must assign the following activities to stages:

| Activity | Description |
|----------|-------------|
| 1 | Run pylint on test automation code |
| 2 | Run SIL tests for ESP SW components |
| 3 | Flash ESP firmware to HIL rack |
| 4 | Run ESP CAN signal validation suite |
| 5 | Run nightly performance degradation test |
| 6 | Verify ECU diagnostic server reachable |
| 7 | Run OEM acceptance test scenarios |

**Question:**
Which assignment correctly maps all activities
to their pipeline stages?

- A) All in build phase — faster feedback
- B) 1,2 in build; 3,4,6 in deployment;
  5 in nightly; 7 in separate acceptance pipeline
- C) 1,2,6 in build; 3,4,7 in deployment; 5 in nightly
- D) 1,2,3,6 in build; 4,5,7 in deployment

---

**✅ Correct Answer: B**

**Reasoning:**

| Activity | Stage | Reason |
|----------|-------|--------|
| 1 — pylint | Build | Static analysis runs before any tests |
| 2 — SIL tests | Build | No hardware needed, fast |
| 3 — Flash firmware | Deployment | Requires HIL rack hardware |
| 4 — CAN validation | Deployment | Requires flashed ECU on CAN bus |
| 5 — Performance test | Nightly | Long-running, periodic not per-commit |
| 6 — Diagnostic server check | Deployment | Verifies infrastructure before tests run |
| 7 — OEM acceptance | Separate pipeline | Different stakeholders, different trigger |

**Why C is wrong:**
Activity 6 — verifying the diagnostic server
is reachable — belongs in the DEPLOYMENT phase
because it verifies runtime infrastructure
AFTER deployment, not during TAF build.

**Why D is wrong:**
Flashing firmware (activity 3) requires hardware —
it cannot run in the build phase on a standard
build agent without HIL rack access.

---

## Scenario 6 — Non-Functional Tests in Pipeline

**Situation:**
A test manager asks:
*"Should we add ABS ECU response time tests
to our nightly regression pipeline?"*

Current nightly pipeline: 300 functional tests,
runs in 3.5 hours.
Response time tests: 45 minutes additional.

The team has monthly performance review meetings.

**Question:**
What is the recommended pipeline integration
strategy for the performance tests?

- A) Add to nightly pipeline — the extra 45 minutes
  is acceptable for nightly execution
- B) Add to the build phase — performance must
  be verified on every commit
- C) Create a separate periodic pipeline triggered
  monthly to align with performance review meetings —
  or triggered on-demand before release
- D) Performance tests should not be automated —
  they require human analysis

---

**✅ Correct Answer: C**

**Reasoning:**
The syllabus states:

> *"Running non-functional tests: Either part of
> a continuous deployment pipeline, or separately,
> to periodically monitor certain non-functional
> quality characteristics of the system such as
> performance efficiency."*

**Analysis:**

| Option | Issue |
|--------|-------|
| Add to nightly | Adds 45 min every night — 270 min/week overhead for monthly meeting value |
| Build phase | Performance tests require full deployed system — cannot run in build |
| Monthly pipeline | Matches review cadence, manageable overhead ✅ |
| Not automated | Contradicts automation benefit of consistency |

**Recommended strategy:**
- Monthly scheduled pipeline aligned with review meetings
- Also triggerable on-demand before major releases
- Results published to dashboard for trend analysis

**Key principle:**
Pipeline scheduling should match the VALUE
delivered by the test results.
Monthly performance review = monthly pipeline.
Daily quality gate = nightly pipeline.
Per-commit safety check = build pipeline.

---

## Quick Reference — Pipeline Levels Exam Rules

| Rule | Remember This |
|------|--------------|
| Build phase tests | Component + SIL + TAF config + static analysis |
| Deployment phase tests | System + system integration + acceptance |
| Configuration tests | Run during TAF build — verify paths and files |
| Nightly regression | For long suites that cannot run per-commit |
| Approach 1 benefit | Automatic rollback on test failure |
| Approach 1 tradeoff | Rerun requires redeployment |
| Approach 2 benefit | Flexible test suites per deployment |
| Approach 2 risk | No automatic rollback — manual only |
| Non-functional tests | Periodic pipeline — not per-commit |
| Config test value | Catches missing files before 300 tests run |
| Automotive build | SIL tests — no hardware |
| Automotive deployment | HIL tests — hardware required |

---

*Next: Sub-Chapter 5.1.2 — Configuration Management for Testware*