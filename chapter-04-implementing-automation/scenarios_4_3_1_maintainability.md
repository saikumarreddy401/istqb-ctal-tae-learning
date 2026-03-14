# Sub-Chapter 4.3.1 — Exam Scenarios Practice (Maintainability)

> **Syllabus Reference:** TAE-4.3.1
> **Cognitive Level:** K2 — Understand
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Clean Code Principle Identification

**Situation:**
A TAE reviews this ABS test automation code:
```python
def t1(s, v, t):
    x = mon.rd(s)
    if x == v:
        return True
    else:
        time.sleep(t/1000)
        x = mon.rd(s)
        return x == v
```

**Question:**
Which clean code principles are violated?

- A) Only logging is missing
- B) Naming conventions and avoid long methods
  are both violated
- C) Naming conventions violated — method name,
  parameters, and variable names are all meaningless.
  Logging is also missing
- D) Only the method structure needs improvement —
  names are acceptable abbreviations

---

**✅ Correct Answer: C**

**Reasoning:**
This code violates multiple clean code principles:

| Violation | Principle # | Detail |
|-----------|------------|--------|
| `t1` — meaningless method name | 1 — Naming | What does t1 do? |
| `s, v, t` — single letter params | 1 — Naming | What are s, v, t? |
| `x` — meaningless variable | 1 — Naming | What does x hold? |
| `mon.rd()` — cryptic API call | 1 — Naming | rd = read? |
| No logging at all | 6 — Use logging | Cannot diagnose failures |

**Clean version:**
```python
def verify_signal_reaches_expected_value(
        signal_name: str,
        expected_value: float,
        timeout_ms: int
) -> bool:
    """Verify CAN signal equals expected within timeout."""
    logger.info(f"Verifying {signal_name} == {expected_value}")
    actual = self.monitor.read_signal(signal_name)
    if actual == expected_value:
        logger.info(f"Signal verified: {actual}")
        return True
    logger.debug(f"Retrying after {timeout_ms}ms wait")
    time.sleep(timeout_ms / 1000)
    actual = self.monitor.read_signal(signal_name)
    logger.debug(f"Final read: {actual}")
    return actual == expected_value
```

**Why option D is wrong:**
Single letter parameter names are never acceptable
in professional automation code — they are not
abbreviations, they are meaningless identifiers.

---

## Scenario 2 — Hardcoding Impact Analysis

**Situation:**
An ABS project has 600 test scripts.
The timing requirement for degraded mode
activation changes from 500ms to 300ms
across all fault injection tests.

**Team A** has hardcoded `500` directly in scripts:
```python
# Appears in 480 test files
assert monitor.wait_for("ABSStatus", 0x02, 500)
```

**Team B** uses a constant:
```python
# ABSSignalObjects.py — one file
MAX_DEGRADED_RESPONSE_MS = 500  # change here only

# In all 480 test files:
assert monitor.wait_for(
    ABS.ABS_STATUS,
    ABS.STATUS_DEGRADED,
    ABS.MAX_DEGRADED_RESPONSE_MS
)
```

**Question:**
What is the exact difference in effort and
what additional risk does Team A face?

- A) Same effort — find and replace works equally
  for both approaches
- B) Team A: update 480 files with risk of missing
  some occurrences causing silent wrong timeouts.
  Team B: update 1 constant in 1 file —
  all 480 tests automatically use 300ms
- C) Team B has more effort because they must
  update both the constant and the import
  in all 480 files
- D) Team A has less effort because their code
  is simpler without the constant class

---

**✅ Correct Answer: B**

**Reasoning:**

| Team | Files to Change | Miss Risk | Silent Failure Risk |
|------|---------------|-----------|-------------------|
| Team A | 480 files | High — some occurrences missed | Tests use 500ms when requirement is 300ms |
| Team B | 1 file | Zero — one constant updated | None — all tests use new value |

**The silent failure risk for Team A:**
If even ONE file still has `500` after the change:
- Test waits 500ms for something that should happen in 300ms
- Test passes — ECU meets the 500ms tolerance
- But ECU FAILS the actual 300ms requirement
- This defect is not detected by automation

**This is a quality assurance failure, not just
a maintenance inconvenience.**

**Why C is wrong:**
Team B updates ONE file only — the constants file.
The import in 480 files does not change.
The constant name `MAX_DEGRADED_RESPONSE_MS` stays the same.
Only the VALUE changes — in one place.

---

## Scenario 3 — Branching Strategy

**Situation:**
An ABS ECU project has the following activities
happening simultaneously:

- TAE 1 adding 15 new test cases for a new feature
- TAE 2 fixing a broken test from yesterday's run
- TAE 3 preparing testware for the v2.4 release
- All three are committing directly to `main`

On Tuesday morning the nightly pipeline fails.
Nobody knows which commit caused it because
three TAEs made 28 commits to main since Monday.

**Question:**
Which clean code / maintainability practice
was not followed and what is the solution?

- A) Logging was insufficient to diagnose
  the pipeline failure
- B) No branching strategy was in place —
  all three activities should have been on
  separate branches so each can be isolated,
  tested, and merged independently
- C) Too many commits were made — commits
  should be batched weekly
- D) TAEs should not work simultaneously
  on the same repository

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus states that using different branches
for features, releases, and defect fixes is
helpful in understanding branch contents.

**Correct branching for this scenario:**

| Activity | Branch | Purpose |
|----------|--------|---------|
| New feature tests | `feature/abs-new-feature-tests` | Isolated development |
| Broken test fix | `bugfix/fix-broken-regression-test` | Targeted fix |
| Release preparation | `release/abs-testware-v2.4` | Stable release candidate |

**When pipeline fails:**
- Revert `main` to last known good state
- Each branch can be tested independently
- Root cause identified by merging branches one at a time
- Fix found without affecting other work

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Logging helps diagnose but does not prevent the root cause confusion |
| C | Commit frequency is not the issue — isolation is |
| D | Parallel work is expected and correct — branching manages it |

---

## Scenario 4 — Static Analysis Value

**Situation:**
A test manager questions why the TAE wants to
add pylint static analysis to the CI/CD pipeline
for test automation code:

*"Our test scripts are not shipped to customers.
They are internal tools only. Static analysis
is overkill for test code — it is only necessary
for production ECU software."*

**Question:**
Which argument best justifies static analysis
for test automation code?

- A) Static analysis is required by ISTQB
  certification and must be applied to all code
- B) Static analysis for TAF code catches naming
  violations, security issues like plaintext
  passwords, and code quality problems that
  directly affect test result reliability —
  poor automation code produces unreliable
  results even when the ECU is correct
- C) Static analysis is free to add so there
  is no reason not to include it
- D) Static analysis makes the code easier to read
  but has no impact on test results

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus states:

> *"To ensure high quality of the test automation
> code, it is recommended to make use of static
> analyzers. Code formatters will improve the
> readability of the test automation code."*

**Business case for TAF static analysis:**

| Issue Found by Static Analysis | Impact on Test Results |
|-------------------------------|----------------------|
| Plaintext password in test script | Security vulnerability — test credentials exposed |
| Hardcoded timeout of wrong value | Tests pass when ECU fails real requirement |
| Unused variable holding expected value | Assertion never executes — false pass |
| Wrong comparison operator | `=` instead of `==` — always passes |
| Dead code path | Test steps never execute |

**Key argument:**
Test code quality directly determines whether
test RESULTS can be trusted.
Unreliable test code = unreliable quality gate.
Unreliable quality gate = defects shipped to OEM.

**Why D is wrong:**
Static analysis does impact test results —
it catches logic errors that cause false passes
and false failures.

---

## Scenario 5 — Multiple Principles Violated

**Situation:**
A TAE submits this code for review:
```python
def process_abs_data(d, flg, tm, md, vl, ex, ct, rp):
    r = False
    if flg:
        x = d.read(vl)
        if x == ex:
            r = True
            ct += 1
    if md == 2:
        time.sleep(tm)
        x2 = d.read(vl)
        if x2 == ex:
            r = True
    if rp:
        print(str(r) + " " + str(ct))
    return r
```

**Question:**
How many clean code principles from the syllabus
are violated in this method?

- A) One — only naming conventions
- B) Three — naming, method length, and logging
- C) Five — naming, hardcoding style, too many
  parameters, long complex method, and logging
- D) All eight principles are violated

---

**✅ Correct Answer: C**

**Reasoning:**

| Principle | Violation | Evidence |
|-----------|----------|---------|
| 1 — Naming | All names meaningless | `d, flg, tm, md, vl, ex, ct, rp, r, x, x2` |
| 4 — Too many parameters | 8 parameters | `(d, flg, tm, md, vl, ex, ct, rp)` |
| 5 — Avoid long complex methods | Multiple responsibilities | Connect + read + wait + verify + report + count |
| 6 — Use logging | `print()` instead of logger | No log levels, no timestamps, no context |
| 8 — Focus on testability | Untestable method | Cannot unit test with 8 opaque parameters |

**Principles NOT violated:**
- 2 — Project structure (not visible in this snippet)
- 3 — Hardcoding (no literal values embedded)
- 7 — Design patterns (not applicable at method level)

**Clean version would split into:**
```python
def read_and_verify_signal(signal_name, expected):
    pass

def wait_for_signal_with_retry(signal_name, expected, timeout_ms):
    pass

def log_verification_result(result, count):
    pass
```

Three focused methods, meaningful names,
2 parameters each, proper logging.

---

## Scenario 6 — Maintainability Cause and Effect

**Situation:**
18 months into an ABS ECU automation project:
- 700 test scripts
- 3 TAEs spend 70% of time on maintenance
- Only 30% capacity for new test development
- Every firmware update breaks 80-100 scripts
- Root cause analysis takes 2-3 days per failure

**Question:**
Which combination of missing maintainability
practices most likely caused this situation?

- A) Insufficient logging and missing version control
- B) No naming conventions and wrong tool selection
- C) Hardcoded signal names/values in scripts,
  no POM equivalent, and no agreed naming conventions —
  creating maximum blast radius for every SUT change
- D) Too many test cases and insufficient team size

---

**✅ Correct Answer: C**

**Reasoning:**
The symptoms point to specific root causes:

| Symptom | Root Cause |
|---------|-----------|
| 80-100 scripts break per firmware update | Signal names hardcoded in scripts — no POM |
| 2-3 days to diagnose each failure | Poor naming — cannot understand code without investigation |
| 70% time on maintenance | No abstraction — every SUT change requires manual updates across hundreds of files |
| New test development at 30% | Maintenance consumes available capacity |

**This is the compounding effect of missing basics:**
```
No POM → signal names in 700 files
    + No naming conventions → code hard to understand
    + No DDT → data hardcoded in scripts
    = Every SUT change is a crisis
    = Maintenance consumes all capacity
    = No new test development possible
    = Automation becomes a liability not an asset
```

**Recovery plan:**
1. Introduce POM — move all signal names to one class
2. Establish naming convention — enforce in code review
3. Introduce DDT — move calibration data to CSV files
4. Add static analysis — prevent regression of standards
5. Refactor highest-maintenance scripts first (80/20 rule)

**Why A is wrong:**
Logging and version control are important but
they do not cause 70% maintenance overhead.
The blast radius problem (hardcoded values) is
the primary driver of high maintenance cost.

---

## Quick Reference — Maintainability Exam Rules

| Rule | Remember This |
|------|--------------|
| Clean code reference | Robert C. Martin "Clean Code" 2008 |
| Eight principles | Naming, Structure, No hardcoding, Few params, Short methods, Logging, Patterns, Testability |
| Naming — booleans | Use is_ or has_ prefix |
| Naming — constants | UPPER_SNAKE_CASE |
| Naming — methods | verb + noun in snake_case |
| Hardcoding solution | Constants class + DDT for test data |
| Hardcoding automotive risk | Wrong tolerance causes false pass on real requirement |
| Branching strategy | feature/ release/ bugfix/ branches |
| Static analysis purpose | Find security issues + code quality problems |
| Static analysis placement | In CI/CD pipeline — runs before test suite |
| Maintenance symptom | High percentage of time on maintenance not development |
| Root cause of high maintenance | Hardcoded values + no abstraction layers |
| Version control for testware | Same discipline as SUT source code |

---

*Chapter 4 Complete — Next: Chapter 5 — CI/CD Deployment Strategies*