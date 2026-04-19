**Benefits:**
- Gateway can be tested with ABS mock satisfying contract
- ABS can verify contract without gateway present
- Defects in interface detected in build phase
- Full system tests reserved for behavioral verification

**Pipeline stage assignment (Chapter 5 — Section 5.1.1):**

| Test Type | Stage | Reason |
|-----------|-------|--------|
| Contract verification | Build phase | No hardware needed — fast |
| Schema validation | Build phase | JSON/ARXML structure check |
| Full system integration | Deployment phase | All ECUs needed |

Contract testing runs in the BUILD phase —
catching interface defects in seconds instead of
after 45 minutes of hardware setup.
Full system tests still needed — but triggered
only after contracts pass.

---

## Cross-Chapter Rules Summary

| Concept | Chapter | The Rule |
|---------|---------|---------|
| Test Generation | 3 | Only optional gTAA capability |
| Scripts and core | 3 | Scripts NEVER call core directly |
| Pilot CI/CD | 4 | Mandatory DURING pilot — not after |
| Fatal vs Error | 4 | Fatal aborts — Error fails single test |
| Test fixtures | 4 | Enable atomic and repeatable tests |
| Integration monitoring | 2 | First environment with monitoring |
| Stale ARXML | 2+5 | Silent false passes — most dangerous |
| Must-haves | 2+8 | Always override cost |
| Pass rate formula | 6 | Passed / (Passed + Failed) only |
| Blocked reporting | 6 | Separate from Failed — always |
| False negative | 7 | Most dangerous TAF defect |
| Flaky threshold | 8 | > 5% = mandatory investigation |
| Baseline before restructure | 8 | Always — measure before changing |
| Contract vs schema | 5 | Contract = interaction agreement over time |
| Consumer-driven | 5 | Consumer sets expectations |

---

*All exam-prep files complete*
*Use practice_questions.md for timed exam practice*
*Use keyword_glossary.md for term definitions*
*Use chapter_summary.md on exam day morning*
*Use this file for final integrated thinking practice*