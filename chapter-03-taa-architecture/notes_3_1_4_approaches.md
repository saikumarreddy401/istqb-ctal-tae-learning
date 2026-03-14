# Sub-Chapter 3.1.4 — Approaches for Automating Test Cases

> **Syllabus Reference:** TAE-3.1.4
> **Cognitive Level:** K3 — Apply
> **Chapter:** 3 — Test Automation Architecture
> **Status:** ✅ Complete

---

## Why Multiple Approaches Exist

No single approach fits every project.
Choice depends on team skills, SUT stability,
who writes tests, number of variants, and
collaboration needs.

> ⭐ The exam tests whether you can SELECT the right
> approach for a given scenario — not just define them.

---

## Master Overview

| Approach | Skill | Maintenance | Best For | Avoid When |
|----------|-------|-------------|---------|-----------|
| Capture/Playback | None | Very High | Quick demo only | Any long-term project |
| Linear Scripting | Basic | High | Small stable SUT | SUT changes frequently |
| Structured Scripting | Medium | Low | Most projects | Zero coding skill |
| TDD | High | Low | Component level | System/integration |
| DDT | Medium | Low | Multi-variant | Single variant only |
| KDT | High to build | Medium | Business analyst involvement | Small systems |
| BDD | Medium | Medium | Cross-team collaboration | Technical-only teams |

---

## Capture / Playback

Records manual interactions and replays them.

| ✅ Pros | ❌ Cons |
|--------|--------|
| No programming needed | Breaks on any SUT change |
| Fast to start | No reuse between tests |
| | SUT must be available during capture |
| | Only feasible for small stable SUTs |

> ❌ Automotive: Never for ECU projects.
> ECU interfaces change with every firmware release.
> Use only for stakeholder demonstrations.

---

## Linear Scripting

Manually written scripts without custom libraries.

| ✅ Pros | ❌ Cons |
|--------|--------|
| Easy to start | No reuse |
| Modifiable unlike capture/playback | Hard to maintain at scale |
| | SUT must be available while writing |

---

## Structured Scripting ⭐ Foundation

Reusable libraries, test steps, user journeys.
Foundation for DDT and KDT.

| ✅ Pros | ❌ Cons |
|--------|--------|
| Easy to maintain and scale | Initial TAF investment |
| Business logic separated from scripts | Requires programming knowledge |
| Reuse across test cases | |

> ⭐ Minimum recommended approach for any
> professional automation project.

---

## TDD — Test-Driven Development

Tests written BEFORE features are implemented.

### The Cycle

| Step | Color | Action |
|------|-------|--------|
| 1 | 🔴 Red | Write one failing test |
| 2 | 🟢 Green | Write minimum code to pass |
| 3 | 🔵 Refactor | Clean code, keep tests passing |

| ✅ Pros | ❌ Cons |
|--------|--------|
| Improves code quality | Takes time to adopt |
| Improves testability | False confidence if done wrong |
| Reduces defect propagation | |
| Better code coverage | |

**Automotive use:** ECU SW component development.
Developers write component tests before
implementing each software requirement.

---

## DDT — Data-Driven Testing ⭐ Critical for Automotive

Same script runs multiple times with different data.
```
1 test script × 12 calibration variants
= 12 test executions automatically
```

| ✅ Pros | ❌ Cons |
|--------|--------|
| Test expansion by adding data rows | Test data management required |
| Test analysts specify tests via data files | |
| Massive reduction in script count | |

**Automotive ROI:**
12 calibration variants × 6 fault modes
= 72 tests from ONE script + ONE CSV file.
Without DDT = 72 separate scripts = 72x maintenance.

> ⭐ DDT is non-negotiable for automotive ECU projects
> with calibration variants or hardware configurations.

---

## KDT — Keyword-Driven Testing

Test cases as tables of keywords and data.
Keywords defined from USER perspective.
Built on top of DDT.
```
| INJECT_FAULT  | WheelSpeedFL | OPEN_CIRCUIT |
| VERIFY_SIGNAL | ABSStatus    | DEGRADED     |
| VERIFY_DTC    | C0035        | SET          |
```

| ✅ Pros | ❌ Cons |
|--------|--------|
| Non-technical analysts write tests | Complex to build and maintain |
| Can be used for manual testing too | Overkill for small systems |

> ⭐ KDT is often built on top of DDT.
> Keywords are defined from USER perspective.

---

## BDD — Behavior-Driven Development

Natural language tests using Given-When-Then.
A collaboration methodology — not just syntax.
```gherkin
Given the ABS ECU is in normal operating mode
When a wheel speed sensor open circuit occurs
Then the fault code C0035 shall be set
And ABS status shall be DEGRADED within 500ms
```

| ✅ Pros | ❌ Cons |
|--------|--------|
| Bridges business, dev, and test | Misused as just a writing style |
| Living documentation | Negative tests still need TAE input |
| Works across test levels | Requires consistent business involvement |

> ⭐ Most common BDD misuse: TAEs write Gherkin
> alone without business involvement.
> BDD is a COLLABORATION tool — not just syntax.

---

## Approach Selection — Decision Framework

| Situation | Recommended Approach |
|-----------|---------------------|
| No programming skills in team | Capture/Playback or KDT |
| Component-level development | TDD |
| Many calibration variants | DDT |
| Business analysts writing tests | KDT or BDD |
| Standard professional project | Structured Scripting |
| Cross-team acceptance criteria | BDD |

### Automotive Recommendation by Test Level

| Test Level | Approach | Reason |
|-----------|---------|--------|
| ECU component (SWC) | TDD | Developers own component tests |
| CAN signal validation | DDT | 72 combinations from one script |
| System integration | Structured + BDD | Requirements traceability |
| HIL regression | DDT | Multiple configurations |
| Acceptance testing | BDD | Business readable scenarios |

---

## Common Failures

| Failure | Prevention |
|---------|-----------|
| Capture/playback long-term | Use structured scripting minimum |
| DDT without data governance | Version control data files with scripts |
| BDD without business involvement | Involve business reps from sprint 0 |
| KDT for 50-test project | Only justified for large non-technical teams |
| TDD skipped for component SW | Mandatory for ECU SW development |

---

## Key Exam Rules

| Rule | Remember |
|------|---------|
| Structured scripting | Foundation for DDT and KDT |
| DDT data sources | CSV, XLSX, JSON, database |
| KDT built on | DDT |
| BDD format | Given / When / Then (Gherkin) |
| TDD cycle | Red → Green → Refactor |
| BDD biggest misuse | Used as writing style without collaboration |
| Capture/playback limitation | SUT must be available during capture |

---

*Next: Sub-Chapter 3.1.5 — Design Principles and Patterns*