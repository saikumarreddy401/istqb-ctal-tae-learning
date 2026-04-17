# ISTQB CTAL-TAE v2.0 — Keyword Glossary

> **Purpose:** Every examinable term defined in one place
> **Usage:** Read before exam — terms appear in questions
> **Source:** CTAL-TAE v2.0 Syllabus + ISTQB Glossary

---

## How to Use This File

- Read through once per week during study
- Cover the Definition column and test recall
- Pay special attention to terms marked ⭐
- Terms often confused with each other are grouped

---

## A

| Term | Definition | Exam Trap |
|------|-----------|----------|
| **Acceptance testing** | Testing to determine if a system satisfies acceptance criteria for release | Belongs in deployment phase — not build phase |
| **Accessibility identifier** | Stable unique ID assigned to UI or interface element enabling reliable automation targeting | Generated automatically by framework or set manually by developers |
| **API testing** | Testing interfaces that allow communication between software components | Can be automated at integration level — before UI exists |
| **Architecture transparency** | Documentation clarity about what interfaces exist at each test level | Stale ARXML = architecture transparency failure |
| **Assertion** | Statement in a test that compares actual result to expected result | Missing assertion = false negative — test always passes |
| **Atomic test** | Test case that passes or fails independently of execution order | Enabled by test fixtures — setup and teardown |

---

## B

| Term | Definition | Exam Trap |
|------|-----------|----------|
| **BDD (Behavior-Driven Development)** | Development methodology using Given/When/Then natural language to define behavior collaboratively | Not just a writing style — requires business + dev + test collaboration |
| **Branching strategy** | Agreed use of version control branches for features, releases, and defect fixes | Syllabus specifically recommends separate branches for each purpose |

---

## C

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **Capture/playback** | Records manual SUT interactions and replays them automatically | High maintenance — SUT must be available during capture — no reuse |
| ⭐ **Configuration management** | Process of identifying, controlling, and tracking testware versions across environments | Includes environment config, test data, AND test suites |
| ⭐ **Contract testing** | Integration testing verifying that two services can communicate consistently over time | Goes BEYOND schema validation — requires both parties agree on interactions |
| **Consumer-driven contract** | Contract where the consumer defines expectations for how the provider responds | Consumer sets expectations — provider must satisfy them |
| **Controllability** | Degree to which the SUT can be driven into specific states by the automation | No controllability = can only test normal operation — no fault testing |
| **Core libraries** | TAF layer containing SUT-independent reusable utilities | Must have ZERO SUT knowledge — works for any project on same stack |

---

## D

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **DDT (Data-Driven Testing)** | Test scripts run multiple times with different data sets from external files | Built on structured scripting — data in CSV/XLSX/JSON/database |
| **Deployment variable** | Configuration value set before deployment starts | Similar to environment variable but set earlier in startup chain |
| **Design pattern** | Reusable solution to a commonly occurring design problem | Syllabus covers four: facade, singleton, POM, flow model |

---

## E

| Term | Definition | Exam Trap |
|------|-----------|----------|
| **Encapsulation** | OOP principle hiding internal implementation behind public interface | CAN tool API hidden inside CANSignalMonitor class |

---

## F

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **Facade pattern** | Hides implementation complexity behind a simple interface exposing only what testers need | Used on every tool API — CAN, XCP, UDS, HIL rack |
| ⭐ **False negative** | Test passes when the SUT has a real defect — most dangerous TAF failure | Caused by missing assertions, wrong expected values, unused variables |
| **False positive** | Test fails when the SUT is actually correct | Less dangerous than false negative but erodes trust |
| **Feature toggle** | Configuration flag that controls which test suites execute per release or environment | Alternative to versioned release — both are valid approaches |
| **Flaky test** | Test that produces inconsistent results without any SUT changes | More dangerous than stable failing test — erodes confidence |
| ⭐ **Flow model pattern** | Extension of POM adding a facade layer above signal objects storing reusable user action sequences | Provides double facade — POM stores identifiers, flow model stores sequences |

---

## G

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **gTAA (Generic Test Automation Architecture)** | High-level blueprint defining four capabilities and four external interfaces for automation | Test Generation is the ONLY optional capability |
| **Gherkin** | Natural language format (Given/When/Then) used in BDD for writing scenarios | Format used by BDD tools to execute scenarios as tests |

---

## H

| Term | Definition | Exam Trap |
|------|-----------|----------|
| **Hardcoding** | Embedding values directly in code without ability to change them easily | Solution: constants class + DDT — not acceptable in professional automation |

---

## I

| Term | Definition | Exam Trap |
|------|-----------|----------|
| **In-sprint automation** | Automated tests delivered within the same sprint as the feature being tested | Agile automation goal — eliminates test debt |
| **Inheritance** | OOP principle where child class inherits behavior from parent class | Base ECU test class provides setup/teardown to all child test classes |

---

## K

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **KDT (Keyword-Driven Testing)** | Test cases expressed as tables of keywords and data — keywords defined from user perspective | Often built on top of DDT — complex to implement but simple to use |

---

## L

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **Logging levels** | Six levels: Fatal, Error, Warn, Info, Debug, Trace | Fatal MAY ABORT execution — Error FAILS test — Warn CONTINUES test |
| **Linear scripting** | Manually written scripts without custom libraries | No reuse between tests — maintenance intensive at scale |

---

## M

| Term | Definition | Exam Trap |
|------|-----------|----------|
| **Maintainability** | Degree to which automation can be modified, extended, and understood over time | Affected by naming, hardcoding, method length, logging, patterns |
| **Mutation testing** | Introducing deliberate small code changes to SUT to verify TAF detects them | Surviving mutant = gap in test suite — does not test TAF code itself |
| **MTTD (Mean Time to Detect)** | Average time between defect introduction and detection by automation | Key metric for measuring automation effectiveness |

---

## O

| Term | Definition | Exam Trap |
|------|-----------|----------|
| **Observability** | Degree to which the SUT exposes internal state for verification | No observability = cannot verify actual vs expected results |

---

## P

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **Page Object Model (POM)** | Design pattern where one class contains all identifiers for one SUT interface | When SUT changes — update ONE class — all tests automatically updated |
| **Pilot project** | Time-boxed automation experiment run before full deployment to validate assumptions | Should integrate CI/CD DURING pilot — not after |
| **Polymorphism** | OOP principle where same interface works for different implementations | Same test verification method works for ABS and ESP ECUs |
| **Provider-driven contract** | Contract where the provider defines how its service operates | Provider creates contract — consumer must conform |

---

## R

| Term | Definition | Exam Trap |
|------|-----------|----------|
| **Repeatability** | Test produces same result on every execution | Enabled by test fixtures — depends on known preconditions |

---

## S

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **Schema validation** | Verifying that API response structure matches defined schema | Schema validation ≠ contract testing — contract testing goes further |
| ⭐ **Singleton pattern** | Ensures only ONE instance of a resource exists throughout execution | Used for CAN connection, UDS session, logger — prevents duplicate connections |
| **SOLID principles** | S: Single Responsibility, O: Open-Closed, L: Liskov, I: Interface Segregation, D: Dependency Inversion | Dependency Inversion most exam-relevant — enables mock/stub replacement |
| **Static analysis** | Analysis of code without execution to find defects and quality issues | Must run on TAF code — same discipline as SUT production code |
| **Structured scripting** | Test automation using reusable libraries, test steps, and user journeys | Foundation for DDT and KDT |
| **SUT (System Under Test)** | The software or hardware being tested by the automation | In automotive = ECU on HIL rack |

---

## T

| Term | Definition | Exam Trap |
|------|-----------|----------|
| ⭐ **TAA (Test Automation Architecture)** | Technical design blueprint of the TAS | Different from TAF — TAA is the design, TAF is the built framework |
| ⭐ **TAF (Test Automation Framework)** | Structural foundation inside the TAS — includes test harness and libraries | TAF is INSIDE the TAS — not the same thing as TAS |
| ⭐ **TAS (Test Automation Solution)** | Complete automation system — tools, scripts, infrastructure | TAS contains TAF — TAA is the design of TAS |
| **TDD (Test-Driven Development)** | Tests written before features are implemented — Red/Green/Refactor cycle | Primarily for component level — not system or acceptance tests |
| **Test adaptation** | gTAA capability connecting automation to SUT interfaces via APIs, protocols, services | NOT optional — mandatory capability in every architecture |
| **Test definition** | gTAA capability for defining and implementing test cases and suites | NOT optional — mandatory capability |
| **Test execution** | gTAA capability for running tests automatically and logging results | NOT optional — mandatory capability |
| ⭐ **Test fixture** | Setup and teardown defining preconditions and postconditions for test execution | Enables atomic and repeatable tests — missing fixture = execution order dependency |
| **Test generation** | gTAA capability for automated design of test cases from a model | ⭐ ONLY OPTIONAL capability in gTAA |
| **Test harness** | Also called test runner — executes test cases | Contains test fixtures — most important TAS structural element |
| ⭐ **Test oracle** | Mechanism determining if actual result equals expected result | If oracle is wrong — test passes with real defects present |
| **Testability** | Degree to which SUT supports automated testing | Non-functional requirement — must be designed in from start |
| **Testware** | All artifacts produced during test automation — scripts, data, configs, reports | Must be version controlled with same discipline as SUT code |

---

## Frequently Confused Term Pairs

| Pair | Distinction |
|------|------------|
| TAF vs TAS | TAF is the framework foundation INSIDE the TAS. TAS is the complete solution. |
| TAF vs TAA | TAF is what you build. TAA is the design blueprint you follow before building. |
| False negative vs False positive | False negative = passes with real defect (dangerous). False positive = fails with no defect (annoying). |
| Contract testing vs Schema validation | Contract testing verifies interaction agreement over time. Schema validates structure only. |
| Facade vs POM | Facade hides tool complexity. POM hides signal names and identifiers. |
| POM vs Flow model | POM stores identifiers. Flow model stores multi-step sequences. |
| Flaky test vs Intermittent failure | Flaky test = inconsistent results from same code. Intermittent = timing or environment issue. |
| Build phase vs Deployment phase | Build = compile + component tests. Deployment = flash ECU + system tests. |
| Approach 1 vs Approach 2 | Approach 1 = quality gate with auto rollback. Approach 2 = separate pipeline, manual rollback. |
| Error vs Fatal | Error = fails this test, next runs. Fatal = may abort entire execution. |
| Error vs Warn | Error = test fails. Warn = unexpected condition but test continues. |

---

## Chapter Keywords — Quick Reference

| Chapter | Must-Know Keywords |
|---------|-------------------|
| Ch 1 | test automation, SUT, test automation engineer, test oracle |
| Ch 2 | testability, observability, controllability, architecture transparency, API testing, GUI testing |
| Ch 3 | gTAA, TAF, TAS, TAA, test harness, test script, testware, DDT, KDT, BDD, TDD, capture/playback, structured scripting, linear scripting, POM, flow model, facade, singleton |
| Ch 4 | risk, test fixture, pilot, logging levels (all six), clean code principles |
| Ch 5 | contract testing, configuration management, feature toggle, consumer-driven contract |
| Ch 6 | measurement, metric, test log, test progress report, test step, pass rate, MTTD, flaky rate |
| Ch 7 | static analysis, false negative, mutation testing, smoke test, verification |
| Ch 8 | schema validation, test histogram, continuous improvement, restructuring |

---

*Use practice_questions.md to test application of these terms*
*Use chapter_summary.md for rapid pre-exam revision*