# Sub-Chapter 4.1.1 — Pilot and Deployment Guidelines

> **Syllabus Reference:** TAE-4.1.1
> **Cognitive Level:** K3 — Apply
> **Chapter:** 4 — Implementing Test Automation
> **Status:** ✅ Complete

---

## What Is a Test Automation Pilot?

A time-boxed automation experiment run BEFORE
full deployment to validate assumptions and
discover risks early.

> ⭐ *"A pilot does not take long to conduct
> but its outcome may have significant impact
> on the direction the project takes."*
> — CTAL-TAE v2.0 Syllabus

---

## Six Items to Evaluate During Pilot Setup

> ⭐ All six are explicitly listed in syllabus.
> Know all six by name — they are examinable.

| # | Item | Question Answered |
|---|------|------------------|
| 1 | Programming language | Which language fits SUT and team? |
| 2 | Commercial or open-source tool | Which tool works for this SUT? |
| 3 | Test levels to cover | Component? System? Integration? |
| 4 | Test cases selected | Which cases best prove the approach? |
| 5 | Test case development approach | DDT? BDD? Structured? |
| 6 | Non-technical aspects | Team skills, licensing, org rules |

---

## Non-Technical Aspects — Equally Examinable

| Aspect | Why It Matters |
|--------|---------------|
| Team knowledge and experience | Determines realistic approach |
| Team structure | Who owns, reviews, fixes automation? |
| Licensing and organization rules | Tool may need procurement approval |
| Type of planned testing | Smoke, regression, acceptance? |
| Target test levels to cover | Drives scope and tool selection |

---

## Pilot Workflow

| Step | Action |
|------|--------|
| 1 | Define pilot scope in writing |
| 2 | Create 2-3 initial prototypes |
| 3 | Evaluate prototypes against requirements |
| 4 | Select one approach |
| 5 | Define timelines and check-in points |
| 6 | **Integrate into CI/CD during pilot** |
| 7 | Evaluate success or failure formally |
| 8 | Make go/no-go decision |

> ⭐ CI/CD integration DURING pilot is mandatory.
> Infrastructure issues found in pilot week 1
> cost hours. Found in deployment month 2
> cost days and block the whole team.

---

## After the Pilot — Decision Point

| Outcome | Decision |
|---------|---------|
| Approach works, ROI clear | Proceed to full deployment |
| Approach works, ROI unclear | Extend pilot, gather more data |
| Approach does not work | Pivot to different approach or tool |
| Infrastructure issues found | Resolve before deployment |

Evaluated by: TAEs AND test managers together.

---

## Automotive Pilot Example — ABS HIL Automation

| Item | Pilot Choice | Reason |
|------|-------------|--------|
| Language | Python | Team has Python skills |
| Tool | ECUTest | Native CAN/LIN/XCP support |
| Test level | System test | ECU integrated on HIL rack |
| Test cases | 5 fault injection scenarios | Representative sample |
| Approach | DDT + Structured scripting | 12 calibration variants |

**Non-technical findings:**

| Aspect | Finding |
|--------|---------|
| Team skills | 2 TAEs know ECUTest, 1 needs training |
| Licensing | ECUTest available, Jenkins CI/CD free |
| Org rules | HIL rack booking required 24h in advance |

**CI/CD integration finding:**
HIL rack on separate network segment from Jenkins.
Firewall rule needed — found in week 1 and fixed.
Without pilot CI/CD integration this would have
been found in deployment month 2.

---

## Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| No defined scope | Pilot runs indefinitely | Scope document before starting |
| Only one prototype | Cannot compare tradeoffs | Minimum 2-3 prototypes |
| No CI/CD in pilot | Infrastructure issues found late | Integrate CI/CD in week 1 |
| Non-technical ignored | Licensing blockers found months later | Evaluate upfront |
| No formal evaluation | Bad approach continues without decision | Mandatory go/no-go meeting |
| Scope too large | Pilot becomes the project | Keep to 2-4 weeks maximum |

---

## Architect Insights

> **The pilot is a risk management tool.**
> Every architecture assumption should be
> tested during the pilot. Wrong assumptions
> found in week 2 cost hours. Found in
> month 6 cost weeks.

> **For automotive:**
> HIL rack availability is the highest pilot risk.
> Shared racks need booking policy resolved
> during pilot — not after 200 tests are written.

> **Multiple prototypes = evidence for decisions.**
> Three prototypes with clear tradeoffs get
> faster stakeholder approval than "trust me."

---

## Reflection Questions

1. You are running an ABS HIL automation pilot.
   At the end of week 2 the CI/CD integration
   fails because the Jenkins agent cannot reach
   the HIL rack. What does this tell you about
   the pilot and how do you respond?

2. Your pilot creates one prototype using ECUTest.
   The test manager asks why you did not compare
   with an alternative tool. How do you justify
   or defend your approach?

3. The pilot scope was defined as 5 test cases
   but the team has written 50 by week 3.
   What has gone wrong and how do you reset?

4. Non-technical evaluation reveals the ECUTest
   license is not approved for your department
   and procurement takes 6 weeks. How does
   this change your pilot outcome?

5. The pilot succeeds technically but the TAE
   who ran it is the only person who understands
   the framework. Is the pilot a success?
   What was missed?

---

## Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Write a one-page pilot scope for your current ABS automation — define what success looks like | `chapter-04/notes_4_1_1_pilot.md` |
| 2 | List the non-technical aspects that would block automation in your current project | `automotive-domain/hil_rack_config.md` |
| 3 | Check if your CI/CD pipeline is connected to your HIL rack — if not, this is your first pilot task | `automotive-domain/hil_automation_architecture.md` |

---

*Next: Sub-Chapter 4.2.1 — Deployment Risks and Mitigation*