# Sub-Chapter 4.1.1 — Exam Scenarios Practice (Pilot Guidelines)

> **Syllabus Reference:** TAE-4.1.1
> **Cognitive Level:** K3 — Apply
> **Purpose:** Exam-style scenario practice with answers

---

## How to Use This File

1. Read the situation carefully
2. Cover the answer section
3. Pick your answer and reason why
4. Reveal and compare

---

## Scenario 1 — Pilot Scope Definition

**Situation:**
A TAE is asked to run an automation pilot for
a new ESP ECU project. The project has:
- 400 test cases defined in TestRail
- 6 calibration variants
- Team of 2 TAEs with Python skills
- ECUTest available but never used by the team
- Jenkins CI/CD pipeline already running for SW builds

The TAE plans to automate all 400 test cases
during the pilot to prove the approach works.

**Question:**
What is the PRIMARY mistake in this pilot plan?

- A) The team should use a different tool
  since they have no ECUTest experience
- B) The pilot scope is too large — 400 test cases
  is full deployment not a pilot, defeating the
  purpose of the pilot as a time-boxed experiment
- C) Python is the wrong language choice for
  ECUTest automation
- D) The CI/CD pipeline should not be involved
  in the pilot phase

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus defines a pilot as a small,
time-boxed experiment to validate the approach
before full deployment.

Automating 400 test cases IS the full deployment.
The pilot should select a REPRESENTATIVE SAMPLE —
typically 5-15 test cases that cover different
test types, complexity levels, and scenarios.

**Correct pilot scope for this project:**

| Item | Pilot Scope |
|------|------------|
| Test cases | 5-8 representative cases covering different fault types |
| Calibration variants | 2 of 6 — prove DDT approach works |
| Duration | 2-3 weeks maximum |
| Success criteria | Cases run reliably, CI/CD connected, approach proven |

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | No ECUTest experience is a non-technical factor to evaluate — not a blocker. Training is the solution |
| C | Python is fully supported by ECUTest — correct choice |
| D | CI/CD integration DURING pilot is explicitly recommended by the syllabus |

---

## Scenario 2 — CI/CD Integration During Pilot

**Situation:**
A TAE completes a 3-week automation pilot for
ABS ECU testing. The pilot produces:
- 8 working test scripts in ECUTest
- All 8 tests pass reliably on the TAE's workstation
- Good documentation of the approach
- Clear tradeoff comparison of two tools

However, the CI/CD integration was planned
for "after the pilot is done."

On the first day of full deployment, the team
discovers the Jenkins CI/CD agent cannot
communicate with the HIL rack due to a
firewall restriction between network segments.
Resolving this takes 3 weeks of IT approvals.

**Question:**
Which pilot guideline was not followed and
what was the consequence?

- A) The pilot should have evaluated more test cases
  to discover the network issue earlier
- B) The pilot should have integrated the solution
  into CI/CD during the pilot phase — this would
  have exposed the firewall issue in week 1
  instead of week 1 of full deployment
- C) The TAE should have chosen a different CI/CD
  tool that does not require network access
- D) The firewall issue is an IT infrastructure
  problem unrelated to the automation pilot

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus explicitly states:

> *"During the pilot, it is also recommended to
> try to integrate the solution and the already
> implemented code into the CI/CD. This may expose
> issues early, either in the SUT, the TAS, or in
> the overall integration of different tools
> within the organization."*

**Cost comparison:**

| When Discovered | Who is Affected | Time to Fix |
|----------------|----------------|------------|
| Pilot week 1 | 1 TAE | Hours — escalate IT ticket |
| Deployment week 1 | Entire team blocked | 3 weeks IT approval process |

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | More test cases do not reveal network issues |
| C | The CI/CD tool is not the problem — network access is |
| D | It IS related to automation pilot — infrastructure validation is part of pilot scope |

**Key rule:**
CI/CD integration is NOT post-pilot activity.
It is a mandatory pilot activity.

---

## Scenario 3 — Multiple Prototype Evaluation

**Situation:**
A TAE presents the pilot results to stakeholders.
She has built ONE prototype using ECUTest with
Python structured scripting and DDT.
The prototype works well for the 8 test cases.

The test manager asks:
*"How do we know this is the best approach?
Did you consider any alternatives?"*

The TAE has no comparison to show.

**Question:**
Which pilot guideline was not followed and
what should the TAE have done differently?

- A) The TAE should have tested more tools
  regardless of time constraints
- B) The syllabus recommends creating several
  different initial prototypes showing pros
  and cons of different approaches so
  stakeholders can see objective tradeoffs
- C) The test manager's question is unreasonable —
  one working prototype is sufficient evidence
- D) Alternative approaches are only needed
  when the first approach fails

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus states:

> *"Based on the requirements, several different
> initial prototypes can be created to show the
> pros and cons of the different approaches.
> From there the TAEs can decide which path
> to move forward with."*

**What multiple prototypes provide:**

| Benefit | Example |
|---------|---------|
| Objective comparison | Structured scripting vs BDD vs KDT |
| Stakeholder confidence | Decision based on evidence not opinion |
| Risk reduction | Weaknesses of chosen approach known upfront |
| Faster approval | No need to repeat the pilot after questions |

**Practical approach for ABS pilot:**

| Prototype | Approach | Time to build |
|-----------|---------|--------------|
| Prototype A | Structured scripting + DDT | 3 days |
| Prototype B | BDD with Gherkin | 2 days |
| Comparison table | Pros/cons/cost/skill matrix | 1 day |

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Time-boxing prevents unlimited comparison — 2-3 prototypes is sufficient |
| C | The test manager's question is valid — stakeholder approval requires evidence |
| D | Alternatives are explored to CHOOSE the best approach, not as fallback |

---

## Scenario 4 — Non-Technical Aspects Evaluation

**Situation:**
A TAE runs a technically successful automation
pilot. The 10 test cases work perfectly.
CI/CD is integrated. The approach is proven.

The TAE recommends proceeding to full deployment
with ECUTest for the entire department of
12 projects.

Two months into deployment, the project manager
discovers that the department has budget for only
2 ECUTest licenses but needs 8 licenses for
12 simultaneous projects. Procurement takes
4 months. Half the projects are blocked.

**Question:**
Which pilot evaluation category was completely
missed and what specific aspect should have
been checked?

- A) Technical aspects — more test cases should
  have been run to discover the license issue
- B) Non-technical aspects — specifically licensing
  and organization rules should have been evaluated
  before recommending department-wide deployment
- C) Test level selection — the wrong test levels
  were covered in the pilot
- D) CI/CD integration — the pipeline was not
  properly set up for multiple projects

---

**✅ Correct Answer: B**

**Reasoning:**
The syllabus explicitly lists non-technical
aspects to evaluate during the pilot:

| Non-Technical Aspect | This Scenario |
|---------------------|--------------|
| Team knowledge and experience | Checked ✅ |
| Team structure | Checked ✅ |
| **Licensing and organization rules** | **NOT checked ❌** |
| Type of planned testing | Checked ✅ |
| Target test levels | Checked ✅ |

Licensing is a non-technical aspect that can
block an entire deployment if not evaluated
during the pilot phase.

**What should have happened:**
Before recommending department-wide deployment:
1. Count required concurrent licenses
2. Check current license availability
3. Check procurement lead time
4. Include license cost in ROI calculation
5. Present license plan alongside technical recommendation

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | License issues are not discovered by running more test cases |
| C | Test level selection is technical — licensing is non-technical |
| D | CI/CD is working — this is a procurement issue |

---

## Scenario 5 — Pilot Evaluation and Decision

**Situation:**
After a 3-week ABS automation pilot the results are:

| Metric | Result |
|--------|--------|
| Test cases automated | 8 of 8 targeted ✅ |
| CI/CD integration | Working ✅ |
| Test execution time | 45 minutes per run ✅ |
| Tool — ECUTest | Working ✅ |
| Team able to maintain scripts | Only the pilot TAE understands the framework ❌ |
| Documentation | No README, no comments ❌ |

The pilot TAE declares the pilot a success
and recommends immediate full deployment.

**Question:**
Is the pilot a complete success and should
full deployment proceed immediately?

- A) Yes — all technical metrics are met and
  CI/CD is working
- B) No — the pilot is technically successful
  but the knowledge transfer and documentation
  gaps mean full deployment will create a
  single point of failure
- C) Yes — documentation can be written after
  deployment when the framework is stable
- D) No — the test execution time of 45 minutes
  is too slow for production use

---

**✅ Correct Answer: B**

**Reasoning:**
The pilot must evaluate BOTH technical AND
non-technical aspects before recommending deployment.

**Technical evaluation:** ✅ Pass
**Non-technical evaluation:**

| Aspect | Status | Risk |
|--------|--------|------|
| Team knowledge | Only 1 person understands framework | Single point of failure |
| Documentation | None | New team members cannot contribute |
| Maintainability | Unknown | If pilot TAE leaves, framework is stranded |

**The syllabus states:**
TAEs AND test managers together evaluate the pilot
to assess success or failure.

A framework understood by only one person is
not a successful pilot — it is a prototype
that will become unmaintainable at scale.

**Correct decision:**
Before full deployment:
1. Write framework README and documentation
2. Have second TAE understand and extend one test
3. Conduct knowledge transfer session
4. Then proceed to deployment

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | Technical metrics alone do not define pilot success |
| C | Documentation written after deployment is rarely written at all |
| D | 45 minutes for full ECU regression is acceptable |

---

## Scenario 6 — Pilot Scope Growth

**Situation:**
A 2-week ABS pilot starts with 5 test cases.

End of week 1: 5 test cases complete ✅
The team decides to add 10 more test cases
because "we are making good progress."

End of week 2: 15 test cases complete but
CI/CD integration not started, non-technical
evaluation not done, no prototype comparison,
no formal evaluation meeting scheduled.

**Question:**
What has happened and what should the TAE do?

- A) The pilot is going well — more test cases
  means more confidence in the approach
- B) Scope creep has occurred — the pilot has
  become development work. The TAE should
  stop adding cases, complete the missing
  pilot activities, and hold the evaluation meeting
- C) The timeline should be extended by 2 more
  weeks to accommodate the additional test cases
- D) The CI/CD integration can be skipped since
  the test cases are already working

---

**✅ Correct Answer: B**

**Reasoning:**
This is classic scope creep — one of the most
common pilot failures.

**What was supposed to happen in 2 weeks:**

| Pilot Activity | Status |
|---------------|--------|
| 5 representative test cases | ✅ Done (plus 10 extra) |
| CI/CD integration | ❌ Not started |
| Non-technical evaluation | ❌ Not done |
| Prototype comparison | ❌ Not done |
| Formal evaluation meeting | ❌ Not scheduled |

The 10 extra test cases consumed the time
budgeted for the other pilot activities.

**Correct action:**
1. Stop adding test cases immediately
2. Complete CI/CD integration this week
3. Complete non-technical evaluation
4. Schedule evaluation meeting
5. Present 15 test cases as evidence (more than needed)
6. Make the go/no-go decision on time

**Why other options are wrong:**

| Option | Why Wrong |
|--------|----------|
| A | More test cases without completing pilot activities = incomplete pilot |
| C | Extending timeline rewards scope creep — sets bad precedent |
| D | CI/CD integration is mandatory pilot activity — cannot be skipped |

---

## Quick Reference — Pilot Exam Rules

| Rule | Remember This |
|------|--------------|
| Pilot purpose | Validate assumptions before full deployment |
| Six evaluation items | Language, tool, test levels, test cases, approach, non-technical |
| Non-technical aspects | Team skills, structure, licensing, test type, test levels |
| CI/CD integration | Mandatory DURING pilot — not after |
| Number of prototypes | Multiple — to show pros/cons of different approaches |
| Pilot evaluation | TAEs AND test managers together |
| Pilot failure signs | Scope creep, no CI/CD, single person understands framework |
| Pilot success criteria | Technical works + team can maintain + CI/CD connected |
| Licensing check | Non-technical aspect — must be done during pilot |
| Pilot timeline | Time-boxed — typically 2-4 weeks |

---

*Next: Sub-Chapter 4.2.1 — Deployment Risks and Mitigation*