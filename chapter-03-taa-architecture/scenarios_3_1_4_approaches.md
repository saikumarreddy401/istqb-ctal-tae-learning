# Sub-Chapter 3.1.4 — Exam Scenarios Practice (Automation Approaches)

> **Syllabus Reference:** TAE-3.1.4
> **Cognitive Level:** K3 — Apply
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Approach Selection for Non-Technical Team

**Situation:**
A vehicle OEM has a team of 8 systems engineers
who write ECU requirements in DOORS. They have
no programming experience. The project manager
wants them to be able to specify automated
acceptance tests directly without depending
on TAEs for every test case.

The SUT is an ESP ECU with a stable CAN interface.
The TAE team has strong Python skills.

**Question:**
Which automation approach best fits this situation?

- A) Capture/Playback — systems engineers can
  record interactions without programming
- B) TDD — systems engineers write tests before
  features are implemented
- C) Keyword-Driven Testing — TAEs build the keyword
  library and systems engineers write test cases
  using domain-specific keywords
- D) Linear Scripting — systems engineers write
  simple scripts without custom libraries

---

**✅ Correct Answer: C**

**Reasoning:**
KDT is specifically designed for situations where:
- Non-technical stakeholders need to specify tests
- TAEs build and maintain the keyword implementation
- Test cases are expressed in domain language

The TAE team builds keywords like:
`INJECT_FAULT`, `VERIFY_SIGNAL`, `SET_VEHICLE_SPEED`

Systems engineers then write test cases as tables:
```
| SET_VEHICLE_SPEED | 80        | km/h        |
| INJECT_FAULT      | SteerAngle| OPEN_CIRCUIT|
| VERIFY_SIGNAL     | ESPStatus | ACTIVE      |
```

No programming required from systems engineers.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Capture/playback requires SUT availability, produces unmaintainable scripts, no analyst involvement in specification |
| B | TDD requires programming — systems engineers have none. Also TDD is for developers at component level |
| D | Linear scripting requires basic programming — systems engineers have none |

**Key rule:** KDT separates keyword IMPLEMENTATION
(TAE responsibility) from keyword USAGE
(analyst responsibility). This is its core value.

---

## Scenario 2 — DDT Justification

**Situation:**
An ABS ECU project must validate behavior across:
- 12 calibration variants
- 6 sensor fault modes
- 4 vehicle speed ranges

Total combinations: 12 × 6 × 4 = 288 test scenarios.

A junior TAE proposes writing 288 individual
test scripts, one per combination.

**Question:**
Which approach should the architect recommend
instead and what is the primary benefit?

- A) BDD — because 288 scenarios can be written
  in Gherkin format for better readability
- B) DDT — one test script runs 288 times with
  different data combinations from a CSV file
- C) Capture/Playback — record one scenario and
  the tool generates the 288 variants
- D) Linear scripting — 288 scripts are acceptable
  for a project this size

---

**✅ Correct Answer: B**

**Reasoning:**
DDT is precisely designed for this situation.

| Approach | Scripts Needed | Maintenance When Variant Added |
|----------|---------------|-------------------------------|
| 288 individual scripts | 288 | Update 288 scripts |
| DDT with CSV | 1 | Add 1 row to CSV |

**CSV structure:**
```
variant_id, fault_mode,    speed_range, expected_status
V01_S1_80,  OPEN_CIRCUIT, 80-120 km/h, DEGRADED
V01_S1_60,  OPEN_CIRCUIT, 60-80 km/h,  DEGRADED
V01_S2_80,  SHORT_CIRCUIT,80-120 km/h, DEGRADED
... 288 rows total
```

When a 13th calibration variant is added:
- Without DDT: write 24 new scripts
- With DDT: add 24 rows to the CSV file

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | BDD improves collaboration and readability but does not solve the variant multiplication problem |
| C | Capture/playback cannot parameterize across combinations — it records one fixed sequence |
| D | 288 scripts means 288x maintenance effort — unsustainable |

---

## Scenario 3 — BDD Misuse Identification

**Situation:**
A TAE team has adopted BDD for their braking ECU
project. They write all test cases in Gherkin format:
```gherkin
Scenario: Brake pressure validation
  Given the brake pressure sensor is connected
  When brake pedal is pressed to 80% travel
  Then brake pressure signal shall be 120 bar
  And response time shall be under 50ms
```

The Gherkin scenarios are written entirely by TAEs.
Systems engineers and business stakeholders have
never reviewed or contributed to the scenarios.
The scenarios are not linked to DOORS requirements.

**Question:**
What is the PRIMARY problem with this BDD implementation?

- A) The Gherkin syntax is incorrect —
  And statements are not allowed
- B) BDD is being used as a test writing style only —
  the collaboration intent of BDD is completely missing
- C) The scenarios are too detailed —
  BDD should only describe high-level behavior
- D) TAEs should not write BDD scenarios —
  only business analysts should write them

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus explicitly warns that the most common
BDD misuse is treating it as a writing style without
involving business representatives and developers
in the whole approach.

BDD's primary value is:
- Business, dev, and test defining behavior TOGETHER
- Scenarios serving as living specification documents
- Requirements and tests staying synchronized

When TAEs write Gherkin alone:
- Scenarios may not reflect actual business intent
- Stakeholders get no value from the format
- The team has the overhead of BDD with none of the benefit

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | `And` is valid Gherkin syntax |
| C | BDD scenarios can be detailed — detail level is not the issue |
| D | TAEs CAN write BDD scenarios — but not ALONE. All roles collaborate |

**Key rule:** BDD is a COLLABORATION methodology.
If only one role is writing scenarios, it is
being misused regardless of how good the Gherkin looks.

---

## Scenario 4 — TDD Application Level

**Situation:**
A software architect proposes using TDD for all
testing on a new ESP ECU project including:
- Software component unit tests
- CAN network integration tests
- HIL system tests
- OEM acceptance tests

**Question:**
For which test level is TDD most appropriate
and where should other approaches be used instead?

- A) TDD is appropriate for all four levels —
  writing tests first always improves quality
- B) TDD is most appropriate for software component
  tests — integration, system, and acceptance tests
  should use structured scripting, DDT, or BDD
- C) TDD is only appropriate for acceptance tests
  because requirements are defined first
- D) TDD should not be used for ECU testing —
  it is only suitable for web application development

---

**✅ Correct Answer: B**

**Reasoning:**
TDD is primarily a component-level development
practice used by developers writing software
component tests before implementing features.

| Test Level | TDD Suitable? | Better Approach |
|-----------|--------------|----------------|
| SW component (SWC) | ✅ Yes | TDD |
| CAN integration | ❌ No | Structured scripting |
| HIL system | ❌ No | DDT — multiple variants |
| OEM acceptance | ❌ No | BDD — business readable |

TDD at system/integration level requires the
complete system to exist before tests can be
written — which contradicts TDD's test-first principle.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | TDD is impractical at system level — you cannot write a HIL test before the ECU exists |
| C | TDD tests are written before features, not before requirements |
| D | TDD works for any software including ECU SW components |

---

## Scenario 5 — Approach Evolution

**Situation:**
An ABS project started 18 months ago with
capture/playback automation.

Current state:
- 150 recorded test scripts
- Each script averages 800 lines of generated code
- Every firmware update breaks 40-60 scripts
- Two TAEs spend 60% of their time on maintenance
- Test coverage has not grown in 6 months

The project manager asks the automation architect
for a recommendation.

**Question:**
What is the recommended migration strategy
and which approach should replace capture/playback?

- A) Add more TAEs to handle the maintenance load
  and continue with capture/playback
- B) Migrate to structured scripting with DDT —
  refactor scripts progressively starting with
  the highest-maintenance test cases first
- C) Switch to BDD immediately — Gherkin scenarios
  are easier to maintain than generated scripts
- D) Delete all 150 scripts and restart from scratch
  with a new tool

---

**✅ Correct Answer: B**

**Reasoning:**
This is the classic capture/playback failure pattern:
- High maintenance cost growing with every release
- No reuse between test cases
- Coverage stagnating due to maintenance consuming all capacity

**Migration strategy:**

| Step | Action |
|------|--------|
| 1 | Build three-layer TAF with structured scripting |
| 2 | Identify top 20% of scripts causing 80% of maintenance |
| 3 | Refactor those first — highest ROI |
| 4 | Add DDT for calibration variant coverage |
| 5 | Progressively migrate remaining scripts |
| 6 | Do not attempt big-bang migration — too risky |

DDT is added because the root cause of many
repeated scripts is variant multiplication —
the same test logic repeated for different
calibration parameters.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Adding people to a broken architecture scales the problem, not the solution |
| C | BDD solves collaboration problems — not maintenance problems caused by missing layers |
| D | Deleting all scripts means losing 18 months of test coverage investment |

---

## Scenario 6 — Approach Combination

**Situation:**
A new vehicle braking ECU project is being scoped.
The team consists of:
- 3 SW developers (Python, C)
- 2 TAEs (Python, ECUTest)
- 2 systems engineers (DOORS, no programming)
- 1 product owner (reviews requirements)

Test scope:
- 8 software components needing component tests
- 50 CAN signal validation scenarios
- 200 system integration scenarios across
  6 calibration variants
- 30 acceptance scenarios reviewed by product owner

**Question:**
Which combination of approaches covers all
test scope requirements most effectively?

- A) BDD for everything — one approach for all levels
- B) DDT for everything — parameterize all test cases
- C) TDD for component tests, DDT for CAN validation
  and system integration, BDD for acceptance scenarios
- D) Structured scripting only — one consistent
  approach across all levels

---

**✅ Correct Answer: C**

**Reasoning:**

| Scope | Team | Best Approach | Reason |
|-------|------|--------------|--------|
| 8 SW components | 3 developers | TDD | Developers write component tests before implementing features |
| 50 CAN signal scenarios | 2 TAEs | DDT | Signal validation parameterized across configurations |
| 200 system × 6 variants | 2 TAEs | DDT | 200 × 6 = 1200 executions from 200 scripts + data file |
| 30 acceptance scenarios | Product owner + TAEs | BDD | Product owner readable, reviews and approves scenarios |

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | BDD at component level is impractical — developers need fast unit test cycles not Gherkin |
| B | DDT alone does not serve the collaboration need of acceptance testing |
| D | Structured scripting alone does not leverage TDD benefits for component development or BDD benefits for stakeholder acceptance |

**Key insight:** Professional automation projects
almost always use multiple approaches — one per
test level based on who writes the tests and
what the tests verify.

---

## Quick Reference — Approach Selection Exam Rules

| Situation | Answer |
|-----------|--------|
| Non-technical analysts write tests | KDT |
| Many data combinations or variants | DDT |
| Component-level development | TDD |
| Cross-team acceptance criteria | BDD |
| Standard professional project | Structured scripting |
| Quick proof of concept only | Capture/playback |
| BDD without business involvement | Misuse — not real BDD |
| KDT built on top of | DDT |
| Structured scripting is | Foundation for DDT and KDT |
| TDD cycle | Red → Green → Refactor |
| DDT data sources | CSV, XLSX, JSON, database |
| Capture/playback main limitation | SUT must be available during capture |
| Capture/playback main failure | Hard to maintain, scale, and evolve |

---

*Next: Sub-Chapter 3.1.5 — Design Principles and Design Patterns*