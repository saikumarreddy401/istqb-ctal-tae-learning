# Chapter 1 — Introduction and Objectives for Test Automation

**Syllabus ref:** TAE-1.1.1, TAE-1.2.1, TAE-1.2.2
**Cognitive level:** K2 (Understand)
**Status:** In Progress

---

## Why Test Automation Exists

To decouple verification cost from system size and change
frequency. Manual regression cost grows linearly with system
size. Automation breaks that relationship.

---

## Advantages (know these with context, not just as a list)

- More tests per build
- Tests impossible to run manually (real-time, parallel)
- Faster execution than manual
- Less subject to human error
- More efficient use of test resources
- Quicker quality feedback
- Improves system reliability
- Improves consistency across test cycles

## Disadvantages (these are equally examinable)

- Additional cost (TAE hire, hardware, training)
- Initial investment to set up TAS
- Time to develop AND maintain
- Requires clear objectives to succeed
- Rigidity — less adaptable to SUT changes
- Automation itself can introduce defects

## Limitations (critical for exam traps)

- Not all manual tests can be automated
- Only verifies what it is programmed to check
- Only checks machine-interpretable results
- Only checks results verifiable by a test oracle

---

## The Three-Question Rule for Exam Scenarios

1. How frequently does this test run?
2. How stable is the SUT?
3. Does the team have the skills to maintain it?

Frequent + Stable + Capable = automation justified
Infrequent OR unstable OR low skill = disadvantages dominate

---

## SDLC Models Summary

### Waterfall
- Automation after implementation phase
- Tests run only during verification phase
- Late feedback = expensive defect fixing

### V-model (key for automotive)
- TAF recommended at EACH test level
- Component > Integration > System > Acceptance
- Direct mapping to ECU development phases

### Agile
- Goal = in-sprint automation
- Eliminates silos between dev/test/business
- Best practices: code reviews, pair programming,
  frequent automated execution

---

## Tool Selection Key Factors

1. SUT architecture (UI / API / embedded / network)
2. Team programming experience level
3. Tool language vs SUT language match
4. Commercial vs open-source tradeoffs
5. CI/CD integration capability
6. Scalability and maintainability

---

## Automotive Context Notes

- ECU SUT interface = hardware (CAN adapter, HIL rack)
- Automation advantages apply strongly (288 ABS variants)
- Hardware availability constraint = unique risk
- Some safety behaviors need physical validation always
- ECUTest strengths: CAN/LIN support, ARXML import, HIL integration

---

## Exam Scenarios Practiced

See exam_scenarios.md in this folder