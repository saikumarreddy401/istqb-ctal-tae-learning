# Sub-Chapter 5.1.2 — Configuration Management for Testware

> **Syllabus Reference:** TAE-5.1.2
> **Cognitive Level:** K2 — Understand
> **Chapter:** 5 — Implementation and Deployment Strategies
> **Status:** ✅ Complete

---

## Why Configuration Management Matters

Automation runs on multiple environments and
multiple SUT versions. Without config management:
- Wrong testware version runs against wrong SUT
- Environment settings mixed between pipelines
- Cannot reproduce failures from previous releases

> ⭐ *"Configuration management is an integral
> part of test automation, as automation will
> often be executed on multiple test environments
> and versions of the SUT."*
> — CTAL-TAE v2.0 Syllabus

---

## The Three Components

> ⭐ All three are explicitly listed in syllabus.
> Know all three by name — they are examinable.

| Component | What It Manages |
|-----------|----------------|
| **Test environment configuration** | URLs, credentials, connection settings per environment |
| **Test data** | Input values and expected results per release |
| **Test suites and test cases** | Which tests run for which release or feature |

---

## Component 1 — Test Environment Configuration

Different settings per pipeline environment:

| Setting | Local Dev | Integration | Preproduction |
|---------|-----------|-------------|---------------|
| ECU IP address | 192.168.1.10 | 192.168.100.10 | 192.168.200.10 |
| CAN interface | PCAN_USB1 | VECTOR_CH1 | VECTOR_CH2 |
| Log level | DEBUG | INFO | INFO |

**Storage options:**

| Scenario | Where Config Lives |
|----------|-------------------|
| Single project | Stored with testware in repo |
| Multiple projects sharing core libraries | Common core library or shared repo |

**Automotive YAML example:**
```yaml
# config/integration_environment.yaml
hil_rack:
  ip_address: "192.168.100.10"
  can_interface: "VECTOR_CH1"
ecu:
  firmware_version: "ABS_v2.4.0"
testware:
  arxml_path: "config/abs_v2.4.arxml"
  log_level: "INFO"
```

---

## Component 2 — Test Data

Can be specific to environment or SUT release.

| Project Size | Storage |
|-------------|---------|
| Small TAF | With testware in Git |
| Large TAF | Test data management system |

**Automotive versioned data structure:**
```
data/
├── calibration_v2.3/
│   └── abs_calibration_variants.csv
└── calibration_v2.4/
    └── abs_calibration_variants.csv
```

> ⭐ Test data versioned alongside test scripts.
> Old release data stays available for reproduction.

---

## Component 3 — Test Suites and Test Cases

Two approaches — both examinable:

### Approach A — Feature Toggle

Config flag per release controls which suites run.
```python
FEATURE_CONFIG = {
    "ABS_v2.3": {"run_performance": False},
    "ABS_v2.4": {"run_performance": True}
}
```

| Property | Detail |
|----------|--------|
| Mechanism | Config flag per release or environment |
| Best when | Gradual feature rollout |
| Benefit | One suite covers all releases |

---

### Approach B — Versioned Testware Release

Testware tagged with same version as SUT.
```
Git tags:
abs-testware-v2.3  ← exact match to ABS SW v2.3
abs-testware-v2.4  ← exact match to ABS SW v2.4
```

| Property | Detail |
|----------|--------|
| Mechanism | Git tag matching SW release version |
| Best when | Strict traceability required |
| Benefit | Exact match between SUT and testware |

> ⭐ **Approach comparison:**
>
> | Approach | Mechanism | Best For |
> |----------|----------|---------|
> | Feature toggle | Config flag per release | Gradual rollout |
> | Versioned release | Git tag matching SW | Strict traceability |

---

## Automotive Config Management Architecture
```
Git Repository
├── main          → latest stable
├── Tags
│   ├── abs-testware-v2.3
│   │   ├── test_scripts/
│   │   ├── data/calibration_v2.3/
│   │   └── config/abs_v2.3.arxml
│   └── abs-testware-v2.4
│       ├── test_scripts/
│       ├── data/calibration_v2.4/
│       └── config/abs_v2.4.arxml
└── Environment configs (not in releases)
    ├── config/integration.yaml
    └── config/preproduction.yaml
```

---

## Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| No environment config management | Wrong credentials in wrong environment | Config files per environment in Git |
| Test data not versioned | Cannot reproduce old release failures | Version data alongside scripts |
| No feature toggle | New tests run against old releases | Feature toggle config per release |
| Testware not tagged | Cannot match testware to SW release | Tag on every SW release |

---

## Architect Insights

> ⭐ **Testware config management =
> same discipline as SUT config management.**
> Treat testware releases same as software releases.

> **For automotive:**
> ARXML must be tagged to SW release.
> ABS SW v2.4 tagged → ARXML v2.4 tagged same commit.
> Most critical config management requirement.

> **Environment config belongs in Git.**
> New TAE should run tests in any environment
> by checking out repo and selecting config.
> Never in someone's head or on their laptop.

---

## Reflection Questions

1. Your ABS CI/CD pipeline accidentally runs
   testware v2.3 against SW release v2.4.
   Which config management component failed
   and which approach would prevent this?

2. A new HIL rack is added for the integration
   environment. It has a different IP address
   and CAN interface name. How do you update
   the configuration without affecting local
   development or preproduction environments?

3. ABS v2.4 introduces a new performance test suite.
   These tests must NOT run against v2.3.
   Which approach — feature toggle or versioned
   release — do you implement and why?

4. A TAE on holiday reports that tests passed
   last week using calibration data that has
   since been updated. You need to reproduce
   the exact test run from last week.
   What config management practice enables this?

5. Three teams share the same core CAN signal
   library. Each team has different environment
   configs. Where should environment configs
   be stored and how should they be managed?

---

## Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Create environment config YAML for your current HIL rack | `automotive-domain/hil_rack_config.md` |
| 2 | Check if your current test data is version controlled alongside scripts | `framework-prototype/tests/` |
| 3 | Identify whether your project needs feature toggles or versioned releases | `chapter-05/notes_5_1_2_config_management.md` |

---

*Next: Sub-Chapter 5.1.3 — Test Automation Dependencies for API Infrastructure*