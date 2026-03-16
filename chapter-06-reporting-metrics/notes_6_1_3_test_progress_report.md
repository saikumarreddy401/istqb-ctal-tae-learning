# Sub-Chapter 6.1.3 — Test Progress Report Construction

> **Syllabus Reference:** TAE-6.1.3
> **Cognitive Level:** K2 — Understand
> **Chapter:** 6 — Test Automation Reporting and Metrics
> **Status:** ✅ Complete

---

## 1. Concept Explanation

### Purpose of the Test Progress Report

The test progress report is the formal communication
artifact that conveys the current state of testing
to stakeholders who make project decisions.

> ⭐ The report does not exist to prove that testing
> happened. It exists to support decisions:
> - Can we release?
> - Do we need more testing?
> - Is the product quality acceptable?
> - Are we on schedule?

Without a structured report, each stakeholder
interprets raw data differently. With a structured
report, the same facts reach all stakeholders in
a consistent, comparable format.

### Automated Report vs Manual Report

| Property | Manual Report | Automated Report |
|----------|--------------|-----------------|
| Frequency | Weekly or milestone-based | Per pipeline run or nightly |
| Effort | High — TAE writes narrative | Low — generated from collected data |
| Consistency | Variable — depends on author | Consistent — same template every run |
| Latency | Hours after test completion | Minutes after test completion |
| Scalability | Does not scale with test volume | Scales with pipeline |

> ⭐ Test automation enables automated report
> generation. The TAE's role shifts from writing
> reports to designing report templates and
> ensuring data collection supports them.

---

## 2. Mandatory Content of a Test Progress Report

> ⭐ The syllabus defines mandatory content.
> Know all items — they are directly examinable.

### Mandatory Section 1 — Test Period and Scope

| Element | What It Contains |
|---------|-----------------|
| Reporting period | Date range or sprint covered |
| SUT version(s) tested | Exact firmware or software version |
| Test environment | HIL rack, pipeline stage, configuration |
| Test suite scope | Which test suites were executed |
| Planned vs actual scope | What was planned vs what actually ran |

> If scope changed — tests skipped, environment
> unavailable, suite subset run — this must be
> explicitly stated. Silent scope reduction is
> a reporting failure.

### Mandatory Section 2 — Test Results Summary

| Element | What It Contains |
|---------|-----------------|
| Total tests executed | Count of test cases run |
| Pass count and percentage | Absolute and relative pass rate |
| Fail count and percentage | Absolute and relative fail rate |
| Blocked / skipped count | Tests that could not run and why |
| Error count | Tests that failed due to infrastructure, not product |

**Automotive example table:**

| Result | Count | Percentage |
|--------|-------|-----------|
| Passed | 387 | 94.6% |
| Failed | 18 | 4.4% |
| Blocked | 4 | 1.0% |
| Error | 0 | 0.0% |
| **Total** | **409** | **100%** |

> ⭐ **Blocked and Error are not failures.**
> Blocked = test could not run (dependency missing,
> environment not ready). Error = infrastructure
> problem during execution. Both must be reported
> separately from product-caused failures.

### Mandatory Section 3 — Defects Found

| Element | What It Contains |
|---------|-----------------|
| New defects raised | Defects created from this test cycle |
| Defect severity distribution | Critical / major / minor counts |
| Defects linked to requirements | Traceability to failing requirement |
| Open defects from prior cycles | Defects not yet fixed affecting results |
| Defects fixed and retested | Verification of resolved items |

> The defect section connects test results to
> product quality decisions. A report with 18
> failures but no defects raised is incomplete —
> either defects were not raised or failures
> were not investigated.

### Mandatory Section 4 — Test Coverage

| Element | What It Contains |
|---------|-----------------|
| Requirements coverage | Percentage of requirements with automated tests |
| Risk coverage | High-risk areas tested vs total |
| New functionality coverage | Coverage of features added this release |
| Coverage gaps | Requirements with no automated test coverage |

> ⭐ Coverage must appear in the report even when
> pass rate is high. A 97% pass rate on 60%
> coverage does not support a release decision
> for a safety-critical product.

### Mandatory Section 5 — Trend Information

| Element | What It Contains |
|---------|-----------------|
| Pass rate over last N runs | Trend direction — improving or degrading |
| Execution time trend | Is the suite getting slower? |
| Defect detection trend | Are we finding more or fewer defects? |
| Flaky test count trend | Is suite stability improving? |

> Single-run snapshots are insufficient for
> release decisions. Trend data provides context.
> A 94% pass rate improving from 88% last week
> is a different signal than 94% declining from 98%.

### Mandatory Section 6 — Outstanding Risks and Issues

| Element | What It Contains |
|---------|-----------------|
| Untested areas | Functionality not yet covered |
| Blocked tests and reason | Why tests could not run |
| Environment issues | Infrastructure problems affecting results |
| Open critical defects | Known product defects not yet resolved |
| Recommendations | TAE recommendation on release readiness |

> ⭐ The risk section is where the TAE exercises
> professional judgment. Listing known gaps and
> recommending whether to release is a core
> TAE responsibility — not just data reporting.

---

## 3. Report Audiences and Content Customization

> ⭐ One dataset — multiple report views.
> The underlying data is the same. The presentation
> is tailored per audience.

| Audience | Focus | Detail Level |
|----------|-------|-------------|
| Development team | Failing tests, failure messages, signal traces | High technical detail |
| Test manager | Pass rate trend, coverage, defect count | Summary with drill-down |
| Project / release manager | Go/no-go recommendation, risk summary | Executive summary only |
| Safety auditor | Requirement coverage, traceability, retention proof | Compliance-focused |

**Automotive example — same data, different reports:**

Development team report includes:
- List of 18 failing test cases with full failure messages
- CAN signal trace links for each failure
- Root cause hypothesis per failure cluster

Release manager report includes:
- Pass rate: 94.6% (target: 95% — 0.4% below threshold)
- Coverage: 91% of safety requirements covered
- Recommendation: conditional release pending 4 blocked tests

Safety auditor report includes:
- Traceability matrix: requirement ID → test case ID → result
- Test environment configuration at time of execution
- Artifact retention confirmation: results stored 5 years

---

## 4. Automated Report Generation in CI/CD

### Pipeline-Integrated Report Generation
```yaml
# GitHub Actions — generate and publish test report
- name: Run ABS regression suite
  run: pytest tests/ --junit-xml=results/junit.xml

- name: Generate HTML report
  run: python scripts/generate_report.py
    --junit results/junit.xml
    --sut-version ${{ env.ECU_VERSION }}
    --environment integration
    --output results/abs_test_report.html

- name: Publish report to GitHub Pages
  uses: peaceiris/actions-gh-pages@v3
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./results
```

### Report Generator Structure
```python
from dataclasses import dataclass
from datetime import datetime
from typing import List
import xml.etree.ElementTree as ET

@dataclass
class TestRunSummary:
    """Structured test run data for report generation."""
    sut_version: str
    environment: str
    execution_date: datetime
    total_tests: int
    passed: int
    failed: int
    blocked: int
    errors: int
    execution_duration_seconds: float
    failed_test_ids: List[str]

    @property
    def pass_rate(self) -> float:
        """Calculate pass rate as percentage."""
        if self.total_tests == 0:
            return 0.0
        return (self.passed / self.total_tests) * 100

    @property
    def meets_quality_gate(self) -> bool:
        """Check if results meet release threshold."""
        return self.pass_rate >= 95.0

def parse_junit_xml(xml_path: str, sut_version: str,
                    environment: str) -> TestRunSummary:
    """Parse JUnit XML into structured report data."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    passed = int(root.get("tests", 0)) - int(root.get("failures", 0))
    failed = int(root.get("failures", 0))
    errors = int(root.get("errors", 0))
    duration = float(root.get("time", 0))

    failed_ids = [
        tc.get("name")
        for tc in root.iter("testcase")
        if tc.find("failure") is not None
    ]

    return TestRunSummary(
        sut_version=sut_version,
        environment=environment,
        execution_date=datetime.utcnow(),
        total_tests=int(root.get("tests", 0)),
        passed=passed,
        failed=failed,
        blocked=0,
        errors=errors,
        execution_duration_seconds=duration,
        failed_test_ids=failed_ids
    )
```

---

## 5. Report Frequency and Triggers

| Report Type | Trigger | Audience |
|------------|---------|---------|
| Per-commit report | Every pipeline run | Development team |
| Daily summary | Nightly regression completion | Test manager |
| Release report | Before every release | All stakeholders |
| Trend report | Weekly or sprint-based | Management |
| Compliance report | Milestone or audit request | Safety auditor |

> ⭐ Per-commit reports must be lightweight and
> fast to read. Release reports must be comprehensive.
> Do not use the same template for both — information
> overload kills adoption.

---

## 6. Automotive Domain — Certification Report Requirements

### ISO 26262 Test Report Minimum Content

For functional safety certification, the test report
must contain as a minimum:

| Requirement | Content |
|-------------|---------|
| Test specification reference | Which test plan was executed |
| Test environment description | HIL configuration, ECU serial, firmware version |
| Test case results with verdict | Pass/fail per test case with timestamp |
| Traceability | Test case → safety requirement mapping |
| Deviation report | Any deviation from planned test procedure |
| Tester identification | Who executed or approved the test |
| Retention | Results stored for product lifetime |

> ⭐ An automated test report for ISO 26262 is not
> just a convenience — it is a compliance artifact.
> Every field has a regulatory purpose. Missing
> the ECU serial number or firmware version means
> the report cannot be accepted by the auditor.

### ASPICE Work Product WP-08

Under ASPICE SWE.4 and SWE.5, test reports must
demonstrate:

| ASPICE Requirement | Report Element |
|-------------------|---------------|
| Test cases executed | Total count with IDs |
| Test results recorded | Pass/fail per case |
| Consistency with test specification | Planned vs actual scope |
| Defects identified | Defect list with severity |
| Coverage achieved | Requirements coverage percentage |

---

## 7. Common Failures in Test Reporting

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| Pass rate without coverage | Incomplete release decision basis | Always include coverage |
| Blocked tests not reported | Hidden scope gaps | Report blocked separately with reason |
| Errors counted as failures | Product blamed for infrastructure issue | Categorize error vs failure |
| No trend data | Cannot detect gradual degradation | Always include last N runs |
| Single report for all audiences | Technical detail overwhelms manager; summary insufficient for developer | Generate audience-specific views |
| No recommendation section | Data presented but decision not supported | TAE must state release readiness |
| Missing SUT version | Report cannot be linked to specific firmware | Always record version in pre-test |

---

## 8. Architect Insights

> ⭐ **Report design is architecture.**
> A report that cannot answer the stakeholder's
> decision question is a failed design — regardless
> of how complete the underlying data is.
> Design reports by starting with the decisions
> they must support.

> **Automate the report — not just the tests.**
> If the report requires manual effort after every
> test run, it will not be produced consistently.
> Pipeline-generated reports are produced every run,
> for every SUT version, with zero additional effort.

> **For automotive:**
> Design your report schema to satisfy the most
> demanding audience — the safety auditor — and
> then generate lighter views for other audiences
> from the same data. Do not maintain separate
> data collections per audience.

> **The recommendation is the most valuable part
> of the report.** Data is available to everyone.
> Interpretation and professional judgment about
> release readiness is the TAE's unique contribution.
> Never omit the recommendation.

---

## 9. Reflection Questions

1. Your ABS release report shows 94.6% pass rate,
   91% requirements coverage, 18 failures, and
   4 blocked tests. The release manager asks for
   a go/no-go recommendation. The quality gate
   threshold is 95%. Construct the recommendation
   section of the report, including what additional
   information you need before making the call.

2. A safety auditor rejects your test report because
   the ECU serial number and firmware version are
   not recorded per test case — only per test run.
   Why does this distinction matter for certification,
   and how do you modify your data collection
   to resolve it?

3. Your test manager receives a report every morning
   with 400 lines of test case detail. She says she
   cannot extract what she needs to make a decision.
   Redesign the report structure for a test manager
   audience, specifying exactly which sections and
   metrics to include.

4. Three tests are reported as "Error" in this week's
   run — they did not produce a pass or fail verdict
   because the CAN interface connection dropped during
   execution. Should these be included in the pass
   rate calculation? Justify your answer and explain
   how the report should present them.

5. Your team generates a report after every nightly
   regression run but not after per-commit pipeline
   runs. A developer asks why their code change that
   broke two tests was not reported until the following
   morning. Design a reporting frequency strategy
   that provides the right information to developers
   and managers at the right time.

---

## 10. Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Define the mandatory sections for your ABS release report and map each to a stakeholder decision | `chapter-06-reporting-metrics/` |
| 2 | Implement the `parse_junit_xml` function in your framework prototype | `framework-prototype/core/report_generator.py` |
| 3 | List what your current ABS test reports are missing relative to ISO 26262 minimum content | `automotive-domain/hil_automation_architecture.md` |

---

*Next: Chapter 6 Scenarios — then Chapter 7 — Verifying TAS*