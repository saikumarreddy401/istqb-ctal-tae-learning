# Sub-Chapter 4.2.1 — Deployment Risks and Mitigation

> **Syllabus Reference:** TAE-4.2.1
> **Cognitive Level:** K4 — Analyze
> **Chapter:** 4 — Implementing Test Automation
> **Status:** ✅ Complete

---

## Two Risk Categories

> ⭐ The syllabus distinguishes two categories.
> Know both — exam scenarios test each separately.

| Category | Examples |
|----------|---------|
| **Infrastructure risks** | Firewall, resources, network, hardware |
| **Technical deployment risks** | Packaging, logging, test structuring, updating |

---

## Infrastructure Risks

| Risk | Automotive Example | Mitigation |
|------|-------------------|-----------|
| Firewall openings | Jenkins cannot reach HIL rack | Request firewall rule in pilot |
| Resource utilization (CPU/RAM) | ECUTest consuming CPU during real-time test | Profile resource usage in pilot |
| Network connection | CAN-over-IP latency causing timing failures | Dedicated network segment for automation |
| Network reliability | XCP connection dropped mid-calibration | Connection watchdog + retry logic |
| Hardware availability | HIL rack powered off during CI run | Dedicated CI rack + health check precondition |
| Device configuration | ECU not flashed with correct firmware | Firmware verification in test fixture setup |

### HIL Rack = Mobile Device

| Mobile Device Risk | HIL Rack Equivalent |
|-------------------|-------------------|
| Device must be powered on | HIL rack powered on |
| Sufficient battery | UPS or reliable power |
| Connected to network | Jenkins agent reaches rack IP |
| Access to SUT | ECU flashed with correct firmware |

---

## Technical Risk 1 — Packaging

Version control of testware = same discipline
as version control of SUT source code.

| Packaging Risk | Consequence | Prevention |
|---------------|------------|-----------|
| Testware not versioned | Cannot reproduce past failures | Git for all testware from day one |
| No release tagging | Cannot match testware to SW release | Tag testware with SW release version |
| No central repository | Different engineers run different versions | Artifact repository — Nexus or similar |

---

## Technical Risk 2 — Logging Levels

> ⭐ All six logging levels are examinable.
> Know them in order with definitions.

| Level | When Used | Fails Test? |
|-------|----------|------------|
| **Fatal** | Error may abort entire test execution | Aborts |
| **Error** | Condition fails and fails the test case | Fails |
| **Warn** | Unexpected condition but test continues | No |
| **Info** | Basic execution information | No |
| **Debug** | Execution details for failure investigation | No |
| **Trace** | Most detailed — every operation logged | No |

**Configuration per environment:**

| Environment | Recommended Level |
|------------|-----------------|
| Local development | Debug or Trace |
| CI/CD build | Info (Debug on failure) |
| Integration | Info (Debug on failure) |
| Preproduction | Info |

> ⚠️ Logging too sparse = cannot diagnose failures.
> Logging too verbose = log files unmanageable.
> Solution: configurable level per environment.

---

## Technical Risk 3 — Test Structuring

| Term | Definition |
|------|-----------|
| **Test harness** | Test runner — executes test cases |
| **Test fixture** | Setup and teardown creating pre/postconditions |

**What fixtures enable:**

| Capability | Without Fixture | With Fixture |
|-----------|----------------|-------------|
| Test isolation | Tests depend on order | Each test starts from known state |
| Repeatability | Results vary per run | Same result every execution |
| Atomicity | Pass/fail depends on previous tests | Each test passes or fails independently |

> ⭐ Test fixtures enable REPEATABLE and ATOMIC tests.
> Non-atomic tests cannot be trusted for quality decisions.

**Automotive fixture pattern:**
```python
def setup_method(self):
    self.abs.verify_normal_operating_mode()
    self.fault.clear_all_faults()

def teardown_method(self):
    self.fault.clear_all_faults()
    self.monitor.stop_monitoring()
```

---

## Technical Risk 4 — Updating

| Update Risk | Automotive Example | Mitigation |
|------------|-------------------|-----------|
| Tool auto-update | ECUTest API change breaks scripts | Pin ECUTest version in config |
| Library update | python-can API change | Pin in requirements.txt |
| CI agent update | Plugin incompatibility | Test updates in pilot first |
| OS update | Path changes break execution | Use containers to freeze environment |

**Requirements.txt pinning example:**
```
ecutest==2.4.1
python-can==4.1.0
pytest==7.4.0
```

---

## Deployment Risk Register Template

| Risk | Probability | Impact | Mitigation | Owner | Status |
|------|------------|--------|-----------|-------|--------|
| Firewall blocks Jenkins→HIL | High | High | Request rule in pilot week 1 | TAE | Open |
| ECUTest auto-update | Medium | High | Pin version in config | TAE | Mitigated |
| HIL rack unavailable | Medium | High | Dedicated CI rack | Test Manager | Open |
| ARXML version mismatch | High | High | Lock ARXML to SW release tag | TAE | Mitigated |
| Fixture fails to reset ECU | Medium | Medium | Watchdog timer on teardown | TAE | Open |

---

## Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| No firewall check | CI/CD blocked for weeks | Check in pilot |
| Fatal vs Error confused | Tests abort when should only fail | Know all six levels |
| No test fixtures | Test order dependency | Always implement setup/teardown |
| Auto-updates unmanaged | Random Monday morning failures | Pin all versions |
| No packaging strategy | Cannot reproduce past failures | Version from day one |
| Logging too sparse | Cannot diagnose without re-run | Configure per environment |

---

## Architect Insights

> **Risk identification is an architectural activity.**
> Risk register created during TAS design —
> not discovered during deployment.

> **HIL rack = mobile device in automotive.**
> Power, network, firmware, configuration —
> all verified before every CI/CD test run.

> **Logging level is deployment configuration.**
> Never hardcode in scripts.
> Configurable per environment.
> Automatic Debug capture on test failure.

> **Fixtures are not optional.**
> No fixture = no atomicity = unreliable results
> that cannot be trusted for quality decisions.

---

## Reflection Questions

1. Your ABS nightly regression fails randomly
   on Monday mornings but passes if re-run manually.
   Which deployment risk categories do you
   investigate first and in what order?

2. A test case fails with a Fatal log entry.
   Another fails with an Error entry.
   What is the difference in behavior and
   what does each mean for test suite continuation?

3. Your ECUTest tool auto-updated over the weekend.
   Monday morning 30% of scripts fail with
   API errors. What is your immediate response
   and what long-term mitigation do you implement?

4. A new TAE joins and runs the regression suite.
   Results are different from the previous run
   even though no code changed. What test
   structuring problem likely exists?

5. Build a risk register with 5 entries for
   a new ESP ECU automation deployment on
   a shared HIL rack with Jenkins CI/CD.

---

## Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Create a `requirements.txt` with pinned versions for your current ECUTest project | `framework-prototype/requirements.txt` |
| 2 | Add setup_method and teardown_method to one existing test class | `framework-prototype/tests/` |
| 3 | Build a 5-row risk register for your current HIL automation deployment | `automotive-domain/hil_automation_architecture.md` |

---

*Next: Sub-Chapter 4.3.1 — Test Automation Solution Maintainability*