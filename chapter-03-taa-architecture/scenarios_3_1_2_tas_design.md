# Sub-Chapter 3.1.2 — Exam Scenarios Practice (TAS Design)

> **Syllabus Reference:** TAE-3.1.2
> **Cognitive Level:** K2 — Understand
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Missing Design Decision

**Situation:**
A TAE builds a complete TAF for an ABS ECU project.
Test scripts run successfully on the HIL rack.
Results are stored as XML files in a shared network folder.

Three months later a new test analyst joins the team.
She cannot find which test cases cover which requirements,
cannot see historical pass/fail trends, and spends
two days every week manually copying results into
a spreadsheet for the weekly quality report.

**Question:**
Which TAS design decision was not made during
the architecture phase?

- A) Tool and library selection
- B) Connectivity requirements identification
- C) Test management tool integration
- D) Version control and repositories

---

**✅ Correct Answer: C**

**Reasoning:**
The test management integration decision ensures
that automated results flow directly into the
test management tool — linking results to
requirements, showing coverage, and enabling
trend analysis.

Without this decision being made during TAS design,
results exist only as raw XML files requiring
manual processing — exactly the situation described.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Tool selection was made — ECUTest runs successfully |
| B | Connectivity works — tests execute on HIL rack |
| D | Version control may exist — the problem is result visibility |

**Key rule:**
Test management integration must be designed
as part of the TAS — not added as an afterthought
when stakeholders complain about missing visibility.

---

## Scenario 2 — Connectivity Gap

**Situation:**
A TAF is built and tested successfully on a
developer's local machine connected directly
to the HIL rack via USB CAN adapter.

When the same TAF is deployed to the CI/CD
Jenkins agent to run automatically overnight,
80% of tests fail with connection timeout errors.
The HIL rack is on a separate network segment
from the Jenkins agent server.

**Question:**
Which TAS design decision would have prevented
this situation?

- A) Plugin and component development
- B) Connectivity requirements identification
- C) Defect management integration
- D) Test management integration

---

**✅ Correct Answer: B**

**Reasoning:**
The connectivity requirements decision involves
mapping ALL connections the TAF needs before
any scripts are written — including firewalls,
network segments, protocols, and endpoints.

Had this mapping been done during TAS design,
the team would have identified that:
- Jenkins agent is on network segment A
- HIL rack is on network segment B
- Firewall rules needed before CI/CD deployment

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | No custom plugin is needed — network access is the issue |
| C | Defect management is about raising defects, not connectivity |
| D | Test management is about results reporting, not connectivity |

**Automotive insight:**
In automotive organizations, HIL racks are often
on isolated network segments for security reasons.
This must be identified and resolved during TAS
design — never discovered during deployment.

---

## Scenario 3 — Version Control Synchronization

**Situation:**
An ABS ECU project has the following version control setup:

- Test scripts: stored in Git ✅
- Test data CSV files: stored on shared drive ❌
- ARXML signal definitions: stored on systems
  engineering SharePoint ❌
- HIL rack configuration: documented in Word file ❌

A new firmware release changes 15 signal names
in the ARXML. Tests run against the new firmware
and 60% pass.

**Question:**
What is the PRIMARY risk created by this
version control setup?

- A) Test scripts may have syntax errors
  that Git does not detect
- B) Test data, ARXML, and rack configuration
  are not synchronized with the test script
  version — creating silent mismatches
- C) The shared drive may run out of storage
  space for test data files
- D) SharePoint does not support binary files
  like ARXML

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus states that testware version control
must cover all testware components and they must
be synchronized to the same release.

When ARXML lives on SharePoint and test scripts
live in Git, there is no mechanism to ensure
the ARXML version used during a test run matches
the test script version. The 60% pass rate after
15 signal name changes is exactly the consequence
of this mismatch — some tests still reference
old signal names and pass incorrectly or fail
for the wrong reason.

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Git detects syntax errors during commit hooks |
| C | Storage space is an infrastructure concern, not a version control risk |
| D | SharePoint supports any file type — this is not the issue |

**Key rule:**
ARXML must be version-controlled in Git and
tagged to the same SW release as the test scripts.
This is non-negotiable in automotive automation.

---

## Scenario 4 — Custom Component Documentation

**Situation:**
Eighteen months ago a senior TAE built a custom
Python component that handles CAN signal timing
tolerance comparison for the ABS test suite.
The component is used by 340 test cases.

The senior TAE has left the company.
A new firmware update changes the timing tolerance
requirements from ±2ms to ±5ms.

The new TAE opens the component source code
and finds no comments, no README, no input/output
documentation, and no unit tests.
It takes three weeks to understand and modify
the component safely.

**Question:**
Which TAS design decision was poorly executed
and what specific practice was violated?

- A) Tool selection — the wrong language was chosen
  for the custom component
- B) Plugin and component development — the component
  was built without documentation or tests
- C) Version control — the component was not
  stored in Git
- D) Connectivity requirements — the component
  lacks error handling for connection failures

---

**✅ Correct Answer: B**

**Reasoning:**
The plugin and component development decision
includes not just building the component but
ensuring it is properly documented, tested,
and maintainable by anyone on the team.

A custom component used by 340 test cases with
no documentation, no README, and no unit tests
creates a single point of failure — exactly
what happened when the original author left.

**Best practices violated:**

| Practice | Violation |
|----------|----------|
| README for every component | No documentation existed |
| Input/output specification | No interface contract |
| Unit tests for custom components | No tests to verify changes |
| Clean code principles | No comments, unclear logic |

**Key rule:**
Every custom TAF component must be documented
and tested as if it will be maintained by
someone who has never seen it before.
Because eventually it will be.

---

## Scenario 5 — TAS Design Decision Sequence

**Situation:**
A test manager asks a new TAE to start building
automated tests for an ESP ECU project immediately.
The TAE has access to the ECU, a HIL rack,
ECUTest licenses, and a list of 200 test cases.

The TAE starts writing test scripts on day one.

**Question:**
Which TAS design decisions should the TAE have
made BEFORE writing any test scripts?

- A) Only version control setup is needed first
- B) All six TAS design decisions should be
  made before scripting begins
- C) Tool selection and connectivity requirements
  are sufficient to begin scripting
- D) No design decisions are needed — scripting
  can begin immediately with available tools

---

**✅ Correct Answer: B**

**Reasoning:**
The TAA defines the complete technical design
for the TAS before implementation begins.
Skipping design decisions creates problems
that are expensive to fix later:

| Skipped Decision | Problem Discovered Late |
|-----------------|------------------------|
| Connectivity mapping | CI/CD pipeline cannot reach HIL rack |
| Test management integration | Results invisible for 6 months |
| Defect management integration | Failures tracked manually in spreadsheets |
| Version control setup | Cannot reproduce failures from 2 weeks ago |
| Plugin identification | Custom components built inconsistently |

Starting to script without these decisions
means rebuilding the architecture while
simultaneously trying to deliver test cases —
the most expensive and stressful way to work.

**Key rule:**
TAA is designed upfront. TAS is built after.
Scripts come last — not first.

---

## Scenario 6 — Defect Management Integration

**Situation:**
An automated overnight test run finds 12 failures
in the ABS ECU regression suite.
The test engineer arrives in the morning and
manually creates 12 Jira tickets, copying
test case names, failure messages, log file paths,
and environment details from the XML result files
into each ticket. This takes 2.5 hours every morning
failures are found.

**Question:**
Which TAS design decision, if properly implemented,
would eliminate or significantly reduce this
manual effort?

- A) Test management integration
- B) Defect management integration
- C) Version control and repositories
- D) Plugin and component development

---

**✅ Correct Answer: B**

**Reasoning:**
The defect management integration decision
ensures that when a test fails, defect creation
is automated or semi-automated with all
context pre-populated:

| Field | Automated Source |
|-------|----------------|
| Test case ID and name | TAF execution log |
| Failure evidence | Screenshot or signal trace |
| Environment details | TAF configuration |
| Expected vs actual | TAF assertion result |
| Log file path | TAF output directory |

With proper defect management integration,
the engineer reviews and approves pre-populated
tickets rather than creating them from scratch.

**Why A is wrong:**
Test management integration handles result
visibility and requirement coverage — not
defect creation. Both are needed but they
serve different purposes.

---

## Quick Reference — TAS Design Exam Rules

| Rule | Remember This |
|------|--------------|
| Six design decisions | Tools, Plugins, Connectivity, Test Mgmt, Defect Mgmt, Version Control |
| Design before scripting | TAA designed upfront — scripts come last |
| ARXML in version control | Tagged to SW release — non-negotiable in automotive |
| Custom components | Must have README, interface spec, and unit tests |
| Connectivity mapping | Done during design — never discovered during deployment |
| Test vs defect management | Test mgmt = results and coverage, Defect mgmt = failure tickets |
| Missing test mgmt integration | Results invisible to stakeholders |
| Missing connectivity mapping | Intermittent failures in CI/CD |

---

*Next: Sub-Chapter 3.1.3 — TAF Layering*