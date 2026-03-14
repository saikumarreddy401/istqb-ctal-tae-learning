# Sub-Chapter 4.2.1 — Exam Scenarios Practice (Deployment Risks)

> **Syllabus Reference:** TAE-4.2.1
> **Cognitive Level:** K4 — Analyze
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Logging Level Identification

**Situation:**
An ABS ECU automated test suite produces the
following log entries during a test run:
```
[14:23:01] ABS_TEST_001 started
[14:23:02] Monitoring signals: ABSStatus, WheelSpeedFL
[14:23:03] Injecting open circuit on CH_01
[14:23:04] ABSStatus read: 0x02 — expected 0x02
[14:23:05] ABS_TEST_001 PASSED
[14:23:06] ABS_TEST_002 started
[14:23:07] CAN message received 15ms late — within tolerance
[14:23:08] ABSStatus read: 0x01 — expected 0x02 — ASSERTION FAILED
[14:23:09] ABS_TEST_002 FAILED
[14:23:10] HIL rack connection lost — cannot continue
[14:23:10] Aborting test execution
```

**Question:**
Map the last four significant log entries to
their correct logging levels:

- A) Late CAN = Error, Assertion failed = Fatal,
  Connection lost = Warn, Abort = Error
- B) Late CAN = Warn, Assertion failed = Error,
  Connection lost = Fatal, Abort = Fatal
- C) Late CAN = Info, Assertion failed = Warn,
  Connection lost = Error, Abort = Fatal
- D) Late CAN = Debug, Assertion failed = Info,
  Connection lost = Warn, Abort = Error

---

**✅ Correct Answer: B**

**Reasoning:**

| Log Entry | Level | Reason |
|-----------|-------|--------|
| CAN message 15ms late — within tolerance | **Warn** | Unexpected condition but test continues — does not fail |
| Assertion failed — wrong signal value | **Error** | Condition fails and fails this test case |
| HIL rack connection lost | **Fatal** | Error event that may abort entire execution |
| Aborting test execution | **Fatal** | Execution cannot continue |

**The key distinctions:**

| Level | Test Continues? | Test Fails? |
|-------|----------------|------------|
| Fatal | ❌ May abort | ✅ Yes |
| Error | ✅ Next test runs | ✅ Yes — this test |
| Warn | ✅ Yes | ❌ No |
| Info | ✅ Yes | ❌ No |

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Connection lost is Fatal not Error — it aborts execution |
| C | Assertion failure is Error not Warn — it fails the test |
| D | Late CAN message is Warn not Debug — it is unexpected but handled |

> ⭐ Fatal = abort execution.
> Error = fail this test, continue to next.
> Warn = flag unexpected condition, continue test.

---

## Scenario 2 — Test Fixture Missing

**Situation:**
An ABS test suite has 20 test cases.
Test cases run in this order:
1-5: normal operation tests
6-10: fault injection tests (inject faults, verify response)
11-20: recovery tests (verify ECU recovers after fault)

The team notices that tests 11-20 pass when run
after tests 6-10 but fail when run in isolation
or in a different order.

**Question:**
Which deployment risk explains this behavior
and what is the solution?

- A) Packaging risk — the test scripts are
  not correctly versioned
- B) Test structuring risk — missing test fixtures
  mean tests are not atomic and depend on
  execution order
- C) Logging risk — insufficient logging prevents
  diagnosis of the failures
- D) Updating risk — a tool update has introduced
  order-dependent behavior

---

**✅ Correct Answer: B**

**Reasoning:**
Tests 11-20 failing when run in isolation but
passing after tests 6-10 is the classic sign
of non-atomic tests with missing fixtures.

Tests 6-10 inject faults and leave the ECU
in a faulted state. Tests 11-20 expect the
ECU to be in that faulted state as their
starting condition — but nobody put the ECU
into that state explicitly.

**What is missing:**
```python
# Tests 11-20 need this setup fixture
def setup_method(self):
    # Explicitly create the precondition
    # that tests 11-20 depend on
    self.fault.inject_reference_fault()
    self.abs.verify_fault_state_active()
```

**The syllabus states:**
Test fixtures provide freedom in controlling
test environment and test data.
They enable tests that are REPEATABLE and ATOMIC.

**Without fixture:**
- Test 11 passes if test 10 ran before it ✅
- Test 11 fails if run in isolation ❌
- Test 11 fails if test suite starts from test 11 ❌

**With fixture:**
- Test 11 always passes regardless of order ✅

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Packaging affects version consistency — not execution order |
| C | Logging helps diagnosis but does not cause the order dependency |
| D | Tool updates cause API failures — not execution order dependency |

---

## Scenario 3 — Packaging Risk

**Situation:**
An ABS ECU defect is reported by the OEM.
The defect was detected by automated regression
testing two weeks ago during SW release 2.3 testing.

The test manager asks the TAE to re-run the
exact test that found the defect to confirm
the fix in release 2.4.

The TAE cannot reproduce the exact test execution
because:
- Test scripts were modified after 2.3 testing
- The ARXML file used for 2.3 is unknown
- The calibration data CSV used is unknown
- ECUTest version may have been updated

**Question:**
Which deployment risk category caused this
situation and what specific practices would
have prevented it?

- A) Infrastructure risk — the HIL rack
  configuration was not documented
- B) Updating risk — ECUTest auto-update
  changed the test behavior
- C) Packaging risk — testware was not
  version-controlled and tagged to SW release,
  making it impossible to reproduce the
  exact test environment from two weeks ago
- D) Logging risk — insufficient logs mean
  the test result cannot be verified

---

**✅ Correct Answer: C**

**Reasoning:**
This is the classic packaging risk scenario.
All four missing items are testware that
should have been version-controlled:

| Testware | Should Have Been |
|----------|----------------|
| Test scripts | Tagged in Git as `v2.3-test-scripts` |
| ARXML file | Tagged in Git as `v2.3-arxml` |
| Calibration CSV | Tagged in Git alongside scripts |
| ECUTest version | Pinned in `requirements.txt` or config |

**With correct packaging:**
```
Git tag: abs-testware-v2.3
├── test_scripts/          ← exact scripts used
├── calibration_data/      ← exact data used
├── arxml/abs_v2.3.arxml   ← exact ARXML used
└── requirements.txt       ← ECUTest==2.4.1
```

Re-running would be:
```bash
git checkout abs-testware-v2.3
# Run exact same environment as 2.3 testing
```

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | HIL rack config matters but the problem is testware reproducibility |
| B | ECUTest update is one component — the overall problem is packaging strategy |
| D | Logs show results but cannot recreate the test environment |

> ⭐ **Key rule:**
> If you cannot reproduce a test failure,
> your packaging strategy has failed.

---

## Scenario 4 — Infrastructure Risk Analysis

**Situation:**
A TAE deploys ABS automation to a Jenkins CI/CD
pipeline for nightly execution. The setup:

- Jenkins agent: 192.168.1.50 (office network)
- HIL rack: 192.168.100.10 (lab network)
- ECU diagnostic server: 192.168.100.20 (lab network)
- Firewall between office and lab networks

Day 1 of deployment: All 150 tests fail with
connection timeout errors. No test executes.

**Question:**
Analyze the situation and identify the PRIMARY
infrastructure risk that was not mitigated.

- A) Resource utilization — the Jenkins agent
  does not have enough CPU for 150 tests
- B) Network reliability — the lab network
  is unstable causing connection drops
- C) Firewall blocking — no firewall rules
  exist to allow traffic from office network
  Jenkins agent to lab network HIL rack
  and ECU diagnostic server
- D) Hardware availability — the HIL rack
  was not powered on before the tests ran

---

**✅ Correct Answer: C**

**Reasoning:**
All 150 tests failing immediately with connection
timeouts on day 1 indicates the connection
never established at all — not that it dropped.

This is the signature of a firewall blocking
all traffic between network segments.

**Evidence analysis:**

| Observation | Indicates |
|-------------|----------|
| All 150 tests fail | Not a specific test issue |
| All fail with TIMEOUT | Connection never established |
| Happens immediately | Not intermittent — consistent |
| Day 1 of deployment | Infrastructure not validated |

**Required firewall rules:**
- Jenkins agent (192.168.1.50) → HIL rack (192.168.100.10)
- Jenkins agent (192.168.1.50) → ECU server (192.168.100.20)
- Specific ports for CAN-over-IP, XCP, UDS protocols

**Prevention:** This should have been discovered
and resolved during the pilot CI/CD integration.
The pilot guideline of integrating CI/CD during
pilot phase exists precisely to catch this.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | CPU resource issues cause slow execution or timeouts during execution — not immediate failure of all tests |
| B | Unstable network causes intermittent failures — not 100% failure on day 1 |
| D | Hardware availability causes specific test failures — not connection timeouts on all 150 |

---

## Scenario 5 — Updating Risk Mitigation

**Situation:**
Every Monday morning the ABS automation pipeline
fails. By Tuesday it works again without any
changes. Investigation reveals:

- Jenkins agents auto-update on Sunday nights
- ECUTest plugin for Jenkins updated last Sunday
- The new plugin version has a different API
  for launching ECUTest test suites
- The TAE manually rolls back the plugin
  each Monday morning

This has happened three Mondays in a row.

**Question:**
What is the correct long-term mitigation strategy?

- A) Run the pipeline on Monday afternoons instead
  of Monday mornings to avoid the update window
- B) Pin the ECUTest Jenkins plugin version in
  the Jenkins configuration and disable
  automatic updates for automation-critical plugins.
  Test new versions in a separate environment
  before upgrading production
- C) Switch to a different CI/CD tool that does
  not auto-update
- D) Accept the Monday morning failures as
  a known issue and document the rollback procedure

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus identifies automatic updates as
a technical deployment risk and states they
can be mitigated by:
- Having adequate configuration plans
- Proper version pinning

**Correct mitigation strategy:**

| Action | Purpose |
|--------|---------|
| Pin plugin version in config | Prevents auto-update breaking production |
| Disable auto-updates for critical plugins | Automation team controls when updates happen |
| Test updates in separate environment | Validate before affecting production pipeline |
| Subscribe to plugin release notes | Know about updates before they arrive |

**Process for future updates:**
1. New ECUTest plugin version released
2. Test in isolated environment first
3. Validate all test scripts work with new version
4. Schedule controlled update during low-risk window
5. Monitor first run after update

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Timing change does not prevent the underlying update problem |
| C | Changing CI/CD tool is excessive — the update management process is the issue |
| D | Accepting a known recurring failure is never acceptable for production automation |

---

## Scenario 6 — K4 Risk Analysis

**Situation:**
You are the automation architect for a new
ESP ECU project. The deployment environment is:

- Jenkins CI/CD on office server
- HIL rack in separate lab (different network)
- ESP ECU flashed manually before test runs
- ECUTest v3.1 with python-can v4.0.0
- Test suite: 300 cases, nightly execution
- Team: 3 TAEs, all with ECUTest experience
- ARXML updated every 2 weeks with SW releases

**Question:**
Analyze this deployment and identify the THREE
highest-priority risks in order of impact.

- A) Resource utilization, updating risk,
  logging configuration
- B) Firewall/network access, ARXML version
  synchronization, ECU flash state verification
  in test fixtures
- C) Team skill gaps, licensing issues,
  test case count
- D) Logging verbosity, Python version,
  Jenkins agent CPU

---

**✅ Correct Answer: B**

**Reasoning:**
Analyzing each risk category against the scenario:

**Risk 1 — Firewall/Network Access (Infrastructure)**

| Factor | Analysis |
|--------|---------|
| Jenkins on office server | Network segment A |
| HIL rack in separate lab | Network segment B |
| Different network = firewall | High probability of blocking |
| Impact if not mitigated | Zero tests can execute |
| Priority | HIGHEST — must resolve before any test runs |

**Risk 2 — ARXML Version Synchronization (Packaging)**

| Factor | Analysis |
|--------|---------|
| ARXML updated every 2 weeks | Very frequent changes |
| Test suite has 300 cases | Large blast radius if ARXML mismatches |
| Nightly execution | Mismatch causes silent false passes overnight |
| Impact | 300 tests may pass but verify nothing |
| Priority | HIGH — systematic silent failure risk |

**Risk 3 — ECU Flash State in Fixtures (Test Structuring)**

| Factor | Analysis |
|--------|---------|
| ECU flashed manually before runs | No automated verification |
| If wrong firmware flashed | All 300 tests run against wrong SW version |
| No fixture to verify flash state | Tests start without confirming precondition |
| Impact | All results invalid — firmware mismatch undetected |
| Priority | HIGH — invalidates entire nightly run silently |

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Resource and logging are real risks but lower priority than the three that invalidate all test results |
| C | Team skills are not a risk — 3 TAEs all have ECUTest experience |
| D | Python version and CPU are operational concerns — not deployment architecture risks |

---

## Quick Reference — Deployment Risks Exam Rules

| Rule | Remember This |
|------|--------------|
| Two risk categories | Infrastructure + Technical deployment |
| Infrastructure risks | Firewall, CPU/RAM, network, hardware availability |
| Four technical risks | Packaging, Logging, Test structuring, Updating |
| Fatal level | May abort entire test execution |
| Error level | Fails this test case, next test continues |
| Warn level | Unexpected but test continues — no failure |
| Fatal vs Error | Fatal aborts suite, Error fails individual test |
| Test fixture purpose | Enables repeatable and atomic tests |
| Atomic test | Passes or fails independently of execution order |
| Non-atomic sign | Results differ based on test execution order |
| Packaging best practice | Tag testware version to SW release in Git |
| Update mitigation | Pin versions + test updates before production |
| Firewall risk sign | All tests fail with timeout on day 1 |
| ARXML version risk | Silent false passes — most dangerous |

---

*Next: Sub-Chapter 4.3.1 — Test Automation Solution Maintainability*