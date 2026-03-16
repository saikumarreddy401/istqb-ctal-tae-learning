# Scenarios — Sub-Chapter 5.1.2 — Configuration Management for Testware

> **Syllabus Reference:** TAE-5.1.2
> **Cognitive Level:** K2 — Understand
> **File:** scenarios_5_1_2_config_management.md
> **Status:** ✅ Complete

---

## Scenario 1 — Identify the Failed Component (K2)

### Situation

A Bosch ABS team runs their CI/CD pipeline on Monday morning.
The pipeline executes the full regression suite and reports
100% pass rate. On Tuesday, the calibration engineer notices
that the test results reference calibration data from
release v2.3, but the SUT deployed to the HIL rack is v2.4.

The v2.4 firmware introduced updated wheel speed thresholds.
The v2.3 calibration data contains the old threshold values.
All tests passed because the old thresholds were never violated.

### Question

Which of the three configuration management components failed,
and what is the most likely root cause?

### Answer

> ⭐ The failed component is **test data**.
>
> Root cause: calibration data was not versioned alongside
> the test scripts. The pipeline picked up the most recent
> data file (v2.3) rather than the data matching the SUT
> version (v2.4). Tests passed silently against incorrect
> expected values — a false pass scenario.

### Exam Insight

| Component Failure | Symptom |
|------------------|---------|
| Test environment config | Wrong IP, wrong CAN interface, connection errors |
| Test data | Incorrect expected values, false passes, cannot reproduce |
| Test suites / test cases | Wrong tests run, new features not tested |

> The dangerous failures are **test data failures** because
> they produce false passes — not test errors.
> Environment config failures are usually visible immediately.

---

## Scenario 2 — Feature Toggle vs Versioned Release (K2)

### Situation

Your team is developing ABS v2.5. The new release includes
two changes:

1. An updated brake pressure control algorithm (ready for testing)
2. A new predictive slip detection feature (still in development,
   not ready for testing)

The CI pipeline must test both v2.4 and v2.5 SUT builds.
Tests for the new slip detection feature must NOT run against v2.4.
Tests for the brake pressure algorithm must run against v2.5 only.

### Question A

Which approach — feature toggle or versioned release — is
more appropriate here, and why?

### Answer A

> ⭐ **Feature toggle** is the correct approach.
>
> Reason: The team needs granular control over which
> test suites run per SUT version, and the features are
> in different states of readiness. A versioned release
> approach would require maintaining separate testware
> branches per version, increasing complexity.
>
> A feature toggle config allows one codebase to serve
> both v2.4 and v2.5 with per-release flags:

| Config Key | ABS v2.4 | ABS v2.5 |
|-----------|---------|---------|
| run_brake_pressure_tests | True | True |
| run_predictive_slip_tests | False | False (not ready) |
| run_updated_algorithm_tests | False | True |

### Question B

When would versioned release be the correct choice instead?

### Answer B

> **Versioned release** is correct when:
> - Strict regulatory traceability is required (e.g. ISO 26262)
> - Exact reproducibility of a past test run is required
> - Each SUT release must be certified with a specific
>   testware version — no ambiguity allowed
>
> In safety-critical automotive projects, versioned release
> is often mandatory for functional safety releases.

---

## Scenario 3 — New HIL Rack Added (K2)

### Situation

Bosch adds a second HIL rack for the ESP integration
environment. The new rack has:

- IP address: 192.168.101.10 (original rack: 192.168.100.10)
- CAN interface: VECTOR_CH3 (original: VECTOR_CH1)
- Same UDS port, same firmware version

The test scripts must run on either HIL rack without modification.

### Question

How should environment configuration be structured to support
both racks without changing test scripts?

### Answer

> ⭐ Create a separate environment config file per rack.
> Test scripts load config by environment name — never
> by hardcoded values.

**Correct structure:**
```
config/
├── integration_rack_1.yaml
│     ip_address: "192.168.100.10"
│     can_interface: "VECTOR_CH1"
│
├── integration_rack_2.yaml
│     ip_address: "192.168.101.10"
│     can_interface: "VECTOR_CH3"
│
└── preproduction.yaml
      ip_address: "192.168.200.10"
      can_interface: "VECTOR_CH2"
```

**Pipeline call:**
```bash
pytest --env=integration_rack_2
```

> The test scripts never contain IP addresses or interface names.
> All environment-specific values are in config files only.
> This is the core principle of environment config management.

---

## Scenario 4 — Reproducing a Past Failure (K2)

### Situation

An ABS regression failure occurred during the release v2.3
certification run six weeks ago. The defect was closed as
"cannot reproduce" because the tester's environment had
already been updated to v2.4 testware and calibration data.

The certification audit now requires exact reproduction of
the v2.3 failure using the same testware and data that ran
during the original certification.

### Question

Which configuration management practices, if implemented
correctly, would allow exact reproduction of the v2.3 run?

### Answer

> ⭐ Two practices enable exact reproduction:
>
> 1. **Versioned testware release** — `abs-testware-v2.3`
>    Git tag checked out to restore exact test scripts
>
> 2. **Versioned test data** — `data/calibration_v2.3/`
>    folder preserved in the same tagged commit
>
> Both must be present. Versioned scripts with updated
> data, or updated scripts with versioned data, will
> not reproduce the original run.

| What Was Tagged | Enables |
|----------------|---------|
| Test scripts at v2.3 | Same test logic as original run |
| Test data at v2.3 | Same expected values as original run |
| ARXML at v2.3 | Same signal definitions as original run |
| Environment config | Same connection settings (separate file) |

> ⭐ **Exam point:** Environment config is typically NOT
> included in the versioned release tag because it is
> environment-specific, not release-specific.
> Environment configs are managed separately.

---

## Scenario 5 — Shared Core Library (K2)

### Situation

Three Bosch teams share a common CAN signal monitoring
library stored in a central repository. Each team has
its own TAF built on top of this library.

- Team A: ABS testing, HIL rack in Stuttgart
- Team B: ESP testing, HIL rack in Abstatt
- Team C: EPS (steering) testing, HIL rack in Schwieberdingen

Each team has different IP addresses, CAN interface names,
and log path configurations.

### Question

Where should environment configurations for each team
be stored, and what is the risk if they are stored
in the shared core library repository?

### Answer

> ⭐ Environment configs must be stored **in each team's
> own TAF repository** — not in the shared core library.

**Correct structure:**

| Location | What It Contains |
|----------|-----------------|
| Shared core library repo | Generic CAN monitoring logic only |
| Team A TAF repo | ABS test scripts + Stuttgart HIL config |
| Team B TAF repo | ESP test scripts + Abstatt HIL config |
| Team C TAF repo | EPS test scripts + Schwieberdingen HIL config |

**Risk of storing in shared repo:**

| Risk | Consequence |
|------|------------|
| Team A commits Stuttgart config | Breaks Team B and C pipelines |
| Config merge conflict between teams | Pipeline instability |
| Shared repo becomes environment-specific | Defeats purpose of shared library |

> The shared repository should contain ONLY logic
> that is environment-independent. The moment an
> IP address or interface name appears in the shared
> repo, the architecture is broken.

---

## Scenario 6 — ARXML Version Mismatch (K2)

### Situation

The ABS development team releases SW v2.4 to the integration
HIL rack. The TAE team checks out the latest testware from
the main branch. Unknown to them, the main branch still
contains `abs_v2.3.arxml` because the ARXML update was
committed to a feature branch but not yet merged.

The pipeline runs. CAN signal tests pass. Two days later
the development team discovers that wheel speed signal
scaling changed between v2.3 and v2.4. The v2.3 ARXML
was applying incorrect scaling factors. Results were invalid.

### Question

Which configuration management failure occurred, and
what practice would have prevented it?

### Answer

> ⭐ The failure is in **test environment configuration** —
> specifically the testware ARXML file was not versioned
> and released with the SUT version.

**Root cause:** ARXML was not tagged with the SW release.
The main branch contained stale ARXML from v2.3.

**Prevention — two options:**

| Option | How It Works |
|--------|-------------|
| Versioned release | Tag `abs-testware-v2.4` includes `abs_v2.4.arxml` |
| CI validation check | Pipeline step verifies ARXML version matches SUT version before running tests |

> ⭐ **This is the most critical automotive config
> management scenario.** In CAN-based ECU testing,
> stale ARXML produces silent false passes —
> tests pass with wrong signal interpretations.
> ARXML version management is non-negotiable.

---

## Quick Reference — All Three Components

| Component | Manages | Failure Symptom | Prevention |
|-----------|---------|----------------|-----------|
| Test environment config | IPs, interfaces, credentials | Connection errors, wrong environment | YAML per environment in Git |
| Test data | Input values, expected results | False passes, cannot reproduce | Version with test scripts |
| Test suites / test cases | Which tests run per release | Wrong tests run, missing coverage | Feature toggle or versioned release |

---

## Approach Comparison — Exam Summary

| Property | Feature Toggle | Versioned Release |
|----------|--------------|-----------------|
| Mechanism | Config flag per release | Git tag matching SW version |
| Best for | Gradual rollout, active development | Safety certification, strict traceability |
| Complexity | Lower (one codebase) | Higher (separate tagged states) |
| Reproducibility | Depends on toggle history | Exact — checkout tag and run |
| Automotive use | Development phase | Certification phase |

---

*Next: Sub-Chapter 5.1.3 — Test Automation Dependencies for API Infrastructure*