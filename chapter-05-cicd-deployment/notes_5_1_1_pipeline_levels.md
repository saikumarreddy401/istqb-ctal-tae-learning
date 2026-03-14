# Sub-Chapter 5.1.1 — Test Automation at Different Test Levels Within Pipelines

> **Syllabus Reference:** TAE-5.1.1
> **Cognitive Level:** K3 — Apply
> **Chapter:** 5 — Implementation and Deployment Strategies
> **Status:** ✅ Complete

---

## Why CI/CD Integration Is the Goal

> ⭐ *"One of the main benefits of test automation
> is that implemented tests can run unattended —
> making them ideal candidates to run within pipelines."*
> — CTAL-TAE v2.0 Syllabus

Without CI/CD: automation runs when someone triggers it.
With CI/CD: automation runs automatically on every change.

---

## Test Levels Mapped to Pipeline Stages

> ⭐ Know exactly which test level belongs in which stage.
> This is directly examinable at K3 level.

| Test Level | Pipeline Stage | Acts as Quality Gate? |
|-----------|---------------|----------------------|
| Configuration tests (TAF) | Build step | ✅ Yes |
| Component tests | Build step | ✅ Yes — crucial |
| Component integration tests | Build step | ✅ Yes |
| System tests | Deployment pipeline | ✅ Last quality gate |
| System integration tests | Delivery pipeline | ✅ Yes |
| Acceptance tests | Deployment phase | ✅ Yes |

---

## The Two Pipeline Phases

| Phase | Contains | Outcome |
|-------|---------|---------|
| **Build** | Compile + Component tests + Static analysis | SW artifact created |
| **Deployment** | Deploy + System tests + Integration tests | Release candidate confirmed |

> ⭐ Component and integration tests = BUILD phase.
> System and acceptance tests = DEPLOYMENT phase.

---

## Configuration Tests for TAF/TAS

A subspecies of component tests.
Run during TAF BUILD — not SUT test execution.

**What they verify:**

| Check | Prevents |
|-------|---------|
| All file paths exist | Runtime FileNotFoundError |
| ARXML at expected path | Missing signal definitions |
| CSV data files present | Missing test data |
| Environment variables set | Missing configuration |
| HIL rack reachable | Connection failures at runtime |
```python
def test_arxml_file_exists():
    assert Path("config/abs_signals.arxml").exists()

def test_calibration_data_present():
    assert Path("data/calibration_variants.csv").exists()
```

> ⭐ Configuration tests run during TAF BUILD.
> They are the TAF's own quality gate.

---

## Two Approaches for Higher-Level Tests

### Approach 1 — Tests as Part of Deployment
```
Deploy → System tests → PASS: deployment confirmed
                      → FAIL: deployment rolled back
```

| Property | Value |
|----------|-------|
| Quality gate | ✅ Yes |
| Automatic rollback | ✅ Yes |
| Rerun requires | Redeployment |
| Best for | Safety-critical systems |

---

### Approach 2 — Tests as Separate Pipeline
```
Deploy → Trigger separate test pipeline
       → Results reported only
       → Rollback = manual action
```

| Property | Value |
|----------|-------|
| Quality gate | ❌ No |
| Flexible test suites | ✅ Yes |
| Rollback | ❌ Manual |
| Best for | Multiple test variants per release |

> ⭐ In Approach 2, lightweight deployment checks
> verify SUT is running but do NOT verify
> full functional suitability.

---

## Additional Pipeline Uses

| Use | Description | When |
|-----|------------|------|
| **Nightly regression** | Full regression suite runs overnight | Long suites that cannot run on every commit |
| **Non-functional tests** | Performance and load tests | Periodically — not on every commit |

> ⭐ Nightly regression especially valuable for
> LONGER running test suites.

---

## Automotive Pipeline Architecture

| Stage | What Runs | Hardware Needed |
|-------|----------|----------------|
| Build | Compile + SIL tests + MISRA | None |
| Deployment | Flash ECU + HIL system tests | HIL rack |
| Nightly | Full ABS/ESP regression | HIL rack |
| Periodic | Performance testing | HIL rack |

---

## Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| System tests in build phase | Hours to build — developer feedback blocked | Move to deployment phase |
| No configuration tests | Runtime failures on missing files | Add config tests to TAF build |
| No nightly regression | Long suite never runs | Schedule nightly pipeline |
| Approach 2 without smoke tests | SUT deployed but not verified | Add lightweight deployment checks |

---

## Architect Insights

> **Pipeline stage assignment is architecture.**
> Wrong assignment = developer feedback blocked
> or deployment risk undetected.

> **For automotive:**
> SIL = build phase (no hardware needed, fast).
> HIL = deployment phase (hardware required, slower).
> This matches syllabus model exactly.

> **Configuration tests are often most valuable.**
> They catch environment problems before any
> test executes — saving entire run from false results.

---

## Reflection Questions

1. Your ABS HIL tests currently run in the build
   phase taking 4 hours. Developers cannot get
   feedback for hours after committing.
   What is the architectural fix?

2. A new ESP feature is deployed. System tests
   run as Approach 2 separate pipeline.
   Tests fail. The pipeline reports failure but
   the deployment is already live.
   What is the risk and how does Approach 1
   address it?

3. The nightly ABS regression suite starts failing
   every Tuesday morning. No code was committed
   Monday night. What do you investigate first?

4. A TAE adds configuration tests that check
   ARXML file existence. The build phase now
   fails when ARXML is missing rather than
   failing 200 tests at runtime.
   Explain why this is an improvement.

5. Design a complete pipeline architecture for
   an ESP ECU project with SIL tests, HIL tests,
   nightly regression, and monthly performance tests.

---

## Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Map your current ECUTest tests to pipeline stages — which belong in build vs deployment | `automotive-domain/hil_automation_architecture.md` |
| 2 | Write 3 configuration test cases for your current TAF | `framework-prototype/tests/` |
| 3 | Identify which of your tests should run nightly vs on every commit | `chapter-05/notes_5_1_1_pipeline_levels.md` |

---

## See Also

- `pipeline_examples/github_actions_workflow.yml`
- `pipeline_examples/pipeline_strategy.md`

---

*Next: Sub-Chapter 5.1.2 — Configuration Management for Testware*