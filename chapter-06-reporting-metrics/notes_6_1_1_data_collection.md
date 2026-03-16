# Sub-Chapter 6.1.1 — Data Collection Methods in Test Automation

> **Syllabus Reference:** TAE-6.1.1
> **Cognitive Level:** K3 — Apply
> **Chapter:** 6 — Test Automation Reporting and Metrics
> **Status:** ✅ Complete

---

## 1. Concept Explanation

### Why Data Collection Is the Foundation of Reporting

Test automation generates large volumes of raw data.
Without deliberate collection strategy, that data is
lost, inaccessible, or unusable for decision-making.

> ⭐ **Data collection is not automatic.**
> The TAE must design what data is collected,
> when it is collected, where it is stored, and
> in what format — before a single test runs.

Poor data collection produces:
- Reports that cannot answer stakeholder questions
- Inability to diagnose flaky test root causes
- No trend data for process improvement
- Compliance failures in safety-critical projects

---

## 2. Categories of Data to Collect

The syllabus identifies data collection across
three categories. All three are examinable.

### Category 1 — Test Execution Data

Data produced during test execution:

| Data Item | What It Captures |
|-----------|-----------------|
| Test case result (pass/fail/error/skip) | Outcome per test |
| Test execution duration | Time per test case and suite |
| Timestamp (start and end) | When the test ran |
| Test environment identifier | Which rack, which pipeline stage |
| SUT version under test | Which firmware/software was tested |
| Test case identifier | Unique ID linking result to specification |
| Failure message and stack trace | Root cause information for failures |
| Screenshots or signal logs on failure | Evidence for diagnosis |

### Category 2 — Test Environment Data

Data about the environment in which tests ran:

| Data Item | What It Captures |
|-----------|-----------------|
| Hardware configuration | HIL rack ID, ECU serial number |
| Software versions | OS, TAF version, tool versions |
| Network / bus configuration | CAN baud rate, interface used |
| Resource utilization | CPU, memory during test execution |
| Environment stability indicators | Connection errors, timeouts |

### Category 3 — Process and Coverage Data

Data about what was tested and how well:

| Data Item | What It Captures |
|-----------|-----------------|
| Requirements coverage | Which requirements have automated tests |
| Code coverage (where applicable) | Lines/branches executed by tests |
| Defect density per component | Failures clustered by module |
| Test suite execution frequency | How often each suite runs |
| Automation ratio | Automated vs manual test count |

> ⭐ **Exam point:** Categories 1, 2, and 3 serve
> different audiences. Developers need Category 1.
> Infrastructure teams need Category 2.
> Management and process improvement need Category 3.

---

## 3. Data Collection Methods

### Method 1 — Built-in Framework Logging

Most test frameworks provide native result collection:

| Framework | Native Collection |
|-----------|-----------------|
| pytest | JUnit XML via `--junit-xml` flag |
| Robot Framework | output.xml generated automatically |
| ECUTest | HTML and XML test reports natively |
| TestNG | XML results with suite and test breakdown |

> This is the minimum baseline. Every TAF must use
> native framework result collection as the starting
> point. Additional collection layers build on top.

**Automotive example — ECUTest:**
ECUTest generates an execution report per test run.
The report contains pass/fail per test case, execution
time, and signal log references. This XML output feeds
into CI/CD pipeline dashboards automatically.

### Method 2 — Custom Logging Within Test Code

Framework logging captures results but not context.
Custom logging captures the reasoning behind results:
```python
import logging
import json
from datetime import datetime

class TestDataCollector:
    """Collects structured test execution data for reporting."""

    def __init__(self, test_id: str, sut_version: str, env_id: str):
        self.test_id = test_id
        self.sut_version = sut_version
        self.env_id = env_id
        self.start_time = datetime.utcnow()
        self.data_points = []

    def record_signal_reading(
        self, signal_name: str, value: float, expected: float
    ) -> None:
        """Record a CAN signal measurement during test execution."""
        self.data_points.append({
            "timestamp": datetime.utcnow().isoformat(),
            "signal": signal_name,
            "actual": value,
            "expected": expected,
            "delta": abs(value - expected),
            "within_tolerance": abs(value - expected) < 0.5
        })

    def finalize(self, result: str, failure_reason: str = None) -> dict:
        """Produce structured test execution record."""
        return {
            "test_id": self.test_id,
            "sut_version": self.sut_version,
            "environment": self.env_id,
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.utcnow().isoformat(),
            "result": result,
            "failure_reason": failure_reason,
            "signal_readings": self.data_points
        }
```

> Custom logging captures signal values, tolerances,
> and intermediate states — not just pass/fail.
> This data is essential for diagnosing intermittent
> failures in HIL environments.

### Method 3 — CI/CD Pipeline Artifact Collection

The pipeline collects and stores test artifacts:
```yaml
# GitHub Actions — collect test artifacts
- name: Run ABS regression suite
  run: pytest tests/ --junit-xml=results/abs_results.xml

- name: Upload test results
  uses: actions/upload-artifact@v3
  with:
    name: abs-test-results-${{ github.run_id }}
    path: |
      results/abs_results.xml
      logs/can_signal_trace.log
      logs/ecu_test_report.html
    retention-days: 90
```

> Pipeline artifact collection ensures results are
> preserved and accessible even after the test
> environment is torn down. Retention period must
> match compliance requirements — in automotive,
> often years, not days.

### Method 4 — Test Management System Integration

For traceability to requirements:

| Integration | What It Enables |
|------------|----------------|
| JIRA Xray | Link automated results to JIRA requirements |
| ALM / qTest | Map test cases to safety requirements |
| TestRail | Centralized result storage with history |
| Polarion | ASPICE-compliant requirement-test traceability |

> ⭐ **For automotive safety (ISO 26262 / ASPICE):**
> Test results must be traceable to requirements.
> Automated results written to a test management
> system provide the audit trail. Pipeline-only
> storage is insufficient for certification projects.

### Method 5 — Time-Series Data Collection

For trend analysis and dashboards:

| Tool | Use Case |
|------|---------|
| InfluxDB | Store test execution metrics as time-series |
| Prometheus | Scrape pipeline metrics, alert on thresholds |
| Grafana | Visualize pass rate trends over time |
| Elasticsearch | Store and search large test log volumes |

**Automotive example — HIL rack utilization:**
```python
# Push execution metrics to InfluxDB after each run
from influxdb_client import InfluxDBClient, Point

def publish_test_metrics(
    test_suite: str,
    pass_count: int,
    fail_count: int,
    duration_seconds: float,
    sut_version: str
) -> None:
    """Publish test run metrics to time-series database."""
    client = InfluxDBClient(url="http://metrics-server:8086")
    write_api = client.write_api()

    point = (
        Point("test_execution")
        .tag("suite", test_suite)
        .tag("sut_version", sut_version)
        .field("pass_count", pass_count)
        .field("fail_count", fail_count)
        .field("pass_rate", pass_count / (pass_count + fail_count))
        .field("duration_seconds", duration_seconds)
    )
    write_api.write(bucket="test-metrics", record=point)
```

---

## 4. Data Collection Timing

> ⭐ **When** data is collected matters as much as
> **what** is collected. Three collection points exist:

| Timing | What Is Collected | Example |
|--------|-----------------|---------|
| Before test execution | Environment state, SUT version, config | HIL rack IP, ECU firmware version |
| During test execution | Signal readings, intermediate states, timestamps | CAN signal values per test step |
| After test execution | Result, duration, artifacts, coverage | Pass/fail, log files, JUnit XML |

> Failing to collect before-execution data means
> you cannot reproduce the environment that produced
> a specific result. This is a common gap in HIL
> automation — the ECU firmware version is not
> recorded with the test result.

---

## 5. Automotive Domain — Data Collection Architecture

### HIL Test Data Collection Stack

| Layer | Tool / Method | Data Collected |
|-------|--------------|---------------|
| CAN signal layer | Vector CANalyzer / ECUTest signal monitor | Raw CAN values per timestamp |
| Test execution layer | ECUTest / pytest JUnit XML | Pass/fail, duration, test ID |
| CI/CD layer | GitHub Actions artifacts | XML results, signal logs |
| Metrics layer | Grafana + InfluxDB | Pass rate trends, execution time trends |
| Traceability layer | Polarion / JIRA Xray | Requirement coverage, audit trail |

### Data Collected Per ABS Test Run

| Data Item | Source | Storage |
|-----------|--------|---------|
| WheelSpeedFL signal trace | CAN monitor | .blf or .csv log file |
| ABS activation timestamp | ECU output signal | Signal trace |
| Test case pass/fail | ECUTest report | XML artifact |
| ECU firmware version | Pre-test query via UDS | Test metadata |
| HIL rack identifier | Environment config | Test metadata |
| Execution duration | Framework timer | JUnit XML |

---

## 6. Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| Only pass/fail collected | Cannot diagnose intermittent failures | Collect signal traces on failure |
| SUT version not recorded | Cannot link results to specific firmware | Record version in pre-test setup |
| No retention policy | Old results deleted before audit | Define retention per compliance requirement |
| Data in pipeline only | Lost when pipeline history cleared | Push to persistent storage or TMS |
| No environment data | Cannot reproduce failure on different rack | Collect rack ID and config in pre-test |
| Manual result entry | Human error, missing data, not scalable | Automate all result collection |

---

## 7. Architect Insights

> ⭐ **Design your data collection schema before
> writing your first test.** Retrofitting collection
> into existing automation is expensive and produces
> inconsistent data across test suites.

> **Treat test results as first-class data.**
> Test execution produces data that has value beyond
> the immediate pass/fail decision. Trend data,
> coverage data, and signal traces have long-term
> diagnostic and compliance value.

> **For automotive compliance:**
> ISO 26262 and ASPICE require traceability from
> test results to requirements. This cannot be
> achieved with pipeline artifacts alone. Test
> management system integration is mandatory for
> certification projects, not optional.

> **Collect more than you think you need.**
> Storage is cheap. Re-running a test to collect
> missing data is expensive — especially when the
> failure was intermittent or environment-dependent.

---

## 8. Reflection Questions

1. Your ABS regression suite runs on three different
   HIL racks. Test results are collected as JUnit XML
   in the pipeline. A failure occurs on Rack 2 but
   not on Rack 1 or 3. What data collection gap
   prevented you from diagnosing this immediately,
   and what would you add?

2. An ISO 26262 audit requires proof that all
   safety requirements for ABS have automated test
   coverage. Your pipeline stores JUnit XML results.
   Why is this insufficient, and what additional
   data collection is required?

3. A TAE on your team argues that collecting CAN
   signal traces for every test run is wasteful —
   it generates large files and slows the pipeline.
   How do you defend selective collection strategy
   (collect traces only on failure) while ensuring
   no diagnostic data is lost?

4. Your Grafana dashboard shows that ABS pass rate
   dropped from 97% to 84% over the past two weeks
   but no individual test failure has been investigated.
   What time-series data collection enabled this
   trend to be visible, and what decision does
   it support?

5. A new TAE joins and sets up a test run that
   produces 100% pass rate. Three days later the
   calibration engineer identifies that the ECU
   firmware tested was three versions old.
   Which pre-execution data collection item was
   missing, and how do you prevent this in the TAF?

---

## 9. Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Add SUT firmware version query to your TAF pre-test setup | `framework-prototype/core/test_logger.py` |
| 2 | Configure your pipeline to upload JUnit XML and signal logs as artifacts with 90-day retention | `chapter-05-cicd-deployment/pipeline_examples/` |
| 3 | List all data items your current ABS test suite collects and identify the top three gaps | `automotive-domain/hil_automation_architecture.md` |

---

*Next: Sub-Chapter 6.1.2 — Data Analysis for Test Results*