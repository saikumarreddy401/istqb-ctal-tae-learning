# Sub-Chapter 8.1.2 — Technical Analysis of the TAF

> **Syllabus Reference:** TAE-8.1.2
> **Cognitive Level:** K4 — Analyze
> **Chapter:** 8 — Continuous Improvement of Test Automation
> **Status:** ✅ Complete

---

## 1. Concept Explanation

### What Technical Analysis Means

Technical analysis is the systematic examination
of the TAF's internal health — its code quality,
architecture, dependency structure, and runtime
behaviour — to identify where improvement effort
will have the highest impact.

> ⭐ **Technical analysis answers: "Where is the
> TAF accumulating risk?"**
> Not where it is failing today, but where it
> will fail tomorrow if nothing changes.
> This is the distinction between reactive
> maintenance and proactive improvement.

### Why Technical Analysis Is K4

K4 requires evaluation and recommendation —
not just identification. The exam will present
a TAF health scenario and ask you to:
- Evaluate which findings are most critical
- Recommend a prioritised improvement plan
- Justify your recommendations with evidence

---

## 2. Technical Debt in Test Automation

> ⭐ **Technical debt** is the accumulated cost
> of shortcuts, deferred refactoring, and
> architectural compromises in the TAF codebase.
> Like financial debt, it accrues interest —
> every new feature added to a high-debt TAF
> costs more than it would in a clean TAF.

### Sources of Technical Debt in TAF

| Source | Example | Accumulated Cost |
|--------|---------|-----------------|
| Hardcoded values | Expected values not from ARXML | Every signal definition change requires manual test update |
| Duplicated test logic | 40 near-identical tests | 40 places to update per requirement change |
| No abstraction layers | Test scripts call CAN bus directly | CAN library change breaks all test scripts |
| Magic numbers | `assert response.data[3] == 127` | Meaning lost — unmaintainable |
| Missing fixtures | Manual setup code in every test | Setup defects propagate everywhere |
| No version control discipline | Untagged test releases | Cannot reproduce past results |

### Measuring Technical Debt
```python
def analyse_taf_technical_debt(src_directory: str) -> dict:
    """
    Analyse TAF codebase for technical debt indicators.
    Returns metrics per file for prioritisation.
    """
    import ast
    import os
    from pathlib import Path

    debt_report = {}

    for py_file in Path(src_directory).rglob("*.py"):
        with open(py_file) as f:
            source = f.read()
            tree = ast.parse(source)

        # Count magic numbers (numeric literals not in assignments)
        magic_numbers = sum(
            1 for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, (int, float))
            and node.value not in (0, 1, -1, True, False)
        )

        # Count hardcoded strings that look like paths or IPs
        hardcoded_strings = sum(
            1 for node in ast.walk(tree)
            if isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and (
                node.value.startswith("192.168") or
                node.value.startswith("C:\\") or
                node.value.endswith(".arxml") or
                node.value.endswith(".csv")
            )
        )

        # Count TODO/FIXME comments
        todo_count = source.upper().count("TODO") + \
                     source.upper().count("FIXME")

        debt_report[str(py_file)] = {
            "magic_numbers": magic_numbers,
            "hardcoded_strings": hardcoded_strings,
            "todo_fixme_count": todo_count
        }

    return debt_report
```

---

## 3. Dependency Analysis

### Why Dependencies Are a Health Risk

Every external dependency the TAF relies on
is a potential breaking change. When a dependency
updates its API, the TAF breaks.

> ⭐ Dependency analysis identifies:
> - Outdated packages with known vulnerabilities
> - Unused dependencies adding attack surface
> - Tightly coupled components that cannot
>   be updated independently
```python
def analyse_import_dependencies(src_directory: str) -> dict:
    """
    Map which TAF modules depend on which external packages.
    Identifies coupling and unused imports.
    """
    import ast
    from pathlib import Path
    from collections import defaultdict

    dependency_map = defaultdict(set)

    for py_file in Path(src_directory).rglob("*.py"):
        module_name = py_file.stem
        with open(py_file) as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    dependency_map[module_name].add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    dependency_map[module_name].add(node.module)

    return dict(dependency_map)
```

**Automotive example — dependency coupling risk:**

| Module | Depends On | Risk |
|--------|-----------|------|
| `test_abs_wheel_speed.py` | `ecutest_api` directly | ECUTest version change breaks test scripts |
| `test_abs_wheel_speed.py` | `core.can_signal_monitor` | Correct — abstracted via TAF layer |
| `abs_signal_flows.py` | `can` (python-can) directly | Library change breaks business logic |
| `abs_signal_flows.py` | `core.can_signal_monitor` | Correct — single abstraction point |

> ⭐ Test scripts must depend on TAF abstraction
> layers — never on external libraries directly.
> This is the architectural principle from Chapter 3
> (TAF layers) applied to dependency health analysis.

---

## 4. Code Coverage of the TAF Itself

> ⭐ Coverage of the TAF means: what percentage
> of the TAF's own code is executed by TAF
> unit tests — not by product tests.
```bash
# Measure TAF unit test coverage
pytest tests/taf_unit_tests/ \
  --cov=framework-prototype \
  --cov-report=html:coverage_report \
  --cov-report=term-missing
```

**Coverage targets for TAF components:**

| TAF Component | Minimum Coverage | Reason |
|--------------|-----------------|--------|
| Core libraries (signal monitor, UDS handler) | 90% | High-impact, failure causes false negatives |
| Business logic (ABS flows, fault injection) | 85% | Safety-critical logic |
| Test scripts | Not measured by unit coverage | Verified by product tests |
| Report generator | 90% | Incorrect counts affect release decisions |
| Configuration loader | 95% | Failure aborts entire suite |

---

## 5. Architecture Health Analysis

### Coupling and Cohesion Assessment

> ⭐ **Low coupling + high cohesion = healthy TAF.**
> High coupling = changes propagate unexpectedly.
> Low cohesion = modules do too many things.

**Coupling analysis — count inter-module dependencies:**

| Finding | Healthy | Unhealthy |
|---------|---------|----------|
| Test scripts → core libraries | 0 direct imports | Any direct import |
| Business logic → test scripts | 0 (one-way dependency) | Any reverse dependency |
| Core libraries → business logic | 0 (no upward dependency) | Any upward dependency |
| Configuration → any module | 0 (loaded by runner) | Hardcoded in modules |

**Cohesion analysis — does each module do one thing?**
```python
# LOW COHESION — one module does too many things
class AbsTestHelper:
    def read_wheel_speed(self): ...      # Signal reading
    def inject_fault(self): ...          # Fault injection
    def generate_report(self): ...       # Reporting
    def load_config(self): ...           # Configuration
    def connect_to_ecu(self): ...        # Connection management

# HIGH COHESION — each class does one thing
class CanSignalMonitor:
    def read_signal(self): ...
    def wait_for_signal(self): ...
    def assert_signal_value(self): ...

class FaultInjector:
    def inject_sensor_fault(self): ...
    def inject_network_fault(self): ...
    def clear_all_faults(self): ...
```

### Layer Violation Detection
```python
def detect_layer_violations(test_dir: str, core_dir: str) -> list:
    """
    Detect test scripts importing directly from
    external libraries — bypassing TAF core layer.
    These are architectural violations.
    """
    import ast
    from pathlib import Path

    # External libraries that should only be used in core
    protected_imports = {"can", "ecutest_api", "xcp", "udsoncan"}
    violations = []

    for test_file in Path(test_dir).rglob("test_*.py"):
        with open(test_file) as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                module = (
                    node.names[0].name if isinstance(node, ast.Import)
                    else node.module or ""
                )
                if module.split(".")[0] in protected_imports:
                    violations.append({
                        "file": str(test_file),
                        "import": module,
                        "violation": (
                            f"Test script imports {module} directly. "
                            f"Use core abstraction layer instead."
                        )
                    })

    return violations
```

---

## 6. Runtime Health Metrics

Beyond static analysis, runtime behaviour
reveals health problems that code inspection
cannot find.

| Runtime Metric | Healthy Value | Warning | Action Threshold |
|---------------|--------------|---------|-----------------|
| Average test setup time | < 2 seconds | 2–5 seconds | > 5 seconds |
| Average test teardown time | < 1 second | 1–3 seconds | > 3 seconds |
| CAN bus timeout rate | < 1% | 1–3% | > 3% |
| UDS connection retry rate | < 1% | 1–5% | > 5% |
| Memory usage growth per test | 0 MB | < 1 MB | > 1 MB (memory leak) |
| Flaky test rate | < 2% | 2–5% | > 5% |
```python
def collect_runtime_metrics(junit_xml_path: str) -> dict:
    """
    Extract runtime health metrics from JUnit XML.
    Returns summary statistics for dashboard.
    """
    import xml.etree.ElementTree as ET
    import statistics

    tree = ET.parse(junit_xml_path)
    durations = []
    setup_times = []

    for testcase in tree.iter("testcase"):
        duration = float(testcase.get("time", 0))
        durations.append(duration)

    if not durations:
        return {}

    return {
        "total_tests": len(durations),
        "mean_duration_seconds": statistics.mean(durations),
        "median_duration_seconds": statistics.median(durations),
        "p95_duration_seconds": sorted(durations)[
            int(len(durations) * 0.95)
        ],
        "max_duration_seconds": max(durations),
        "tests_over_30s": sum(1 for d in durations if d > 30),
        "total_execution_seconds": sum(durations)
    }
```

---

## 7. Technical Analysis Report

> ⭐ Technical analysis produces a structured
> findings report — not just a list of problems.
> Each finding has: severity, evidence, impact,
> and recommended action.

**Technical analysis report template:**

| Finding | Severity | Evidence | Impact | Recommendation |
|---------|----------|---------|--------|---------------|
| 23 test scripts import `can` directly | High | Layer violation scan | ECU library change breaks 23 tests | Refactor to use `core.can_signal_monitor` |
| 6 functions with complexity > 15 | High | radon output | Unmaintainable, high defect risk | Refactor before next release |
| 47 duplicate test functions (speed variants) | Medium | Code duplication scan | Requirement change requires 47 updates | Parameterise into DDT suite |
| `python-can` dependency unpinned | High | requirements.txt review | Silent version upgrades may break CAN layer | Pin to `python-can==4.2.0` |
| TAF unit test coverage at 61% | Medium | pytest-cov report | 39% of TAF untested — false negative risk | Target 85% this quarter |
| 134 magic numbers in test assertions | Medium | AST analysis | Values meaningless, break on spec change | Replace with named constants from ARXML |

---

## 8. Automotive Domain — TAF Health Dashboard

### Monthly Technical Analysis Metrics — ABS TAF

| Metric | Target | Current | Trend | Action |
|--------|--------|---------|-------|--------|
| Layer violations | 0 | 3 | ↑ New | Assign to sprint |
| Functions complexity > 10 | 0 | 6 | → Stable | Schedule refactor |
| TAF unit test coverage | 85% | 71% | ↑ Improving | Continue |
| Unpinned dependencies | 0 | 2 | → Stable | Pin this sprint |
| Magic numbers in assertions | 0 | 134 | ↓ Reducing | Continue |
| TODO/FIXME comments | < 10 | 28 | → Stable | Schedule cleanup |
| Flaky test rate | < 2% | 3.1% | ↓ Improving | 3 remaining to fix |
| Mean test duration | < 15s | 18.4s | ↑ Growing | Profile top 10 slow |

---

## 9. Common Failures

| Failure | Consequence | Prevention |
|---------|------------|-----------|
| Technical analysis done once at project start | Debt accumulates undetected | Monthly analysis cycle |
| Findings documented but not actioned | Report exists, quality degrades | Findings go to sprint backlog with owner |
| Coverage measured for product — not TAF | TAF defects undetected | Separate coverage target for TAF unit tests |
| Layer violations accepted over time | Architecture degrades — high coupling | Zero tolerance for new layer violations |
| Runtime metrics not collected | Memory leaks and slowdowns invisible | Collect and trend runtime metrics per release |

---

## 10. Architect Insights

> ⭐ **Technical debt in a TAF is compounding.**
> A TAF with 134 hardcoded magic numbers today
> will have 200 next year if nothing changes.
> Each new test written by someone who sees
> existing hardcoded values will follow the
> same pattern. Debt sets the standard for
> future contributions.

> **Coverage of the TAF is not vanity.**
> 61% TAF coverage means 39% of the TAF's logic
> has never been verified to be correct.
> In a 400-test suite, 39% × 400 = 156 tests
> whose underlying logic has not been unit tested.
> The false negative risk from those 156 tests
> is unknown.

> **For automotive:**
> Layer violations are architecture violations.
> A test script that imports `udsoncan` directly
> instead of using the TAF UDS handler is an
> architectural defect — not a style issue.
> It must be treated as a High severity finding
> and fixed before the next release.

---

## 11. Reflection Questions

1. Your ABS TAF technical analysis reveals:
   TAF unit test coverage at 58%, 12 layer
   violations, 6 high-complexity functions,
   and 3 unpinned dependencies. Prioritise
   these four findings and justify your order
   using risk impact analysis.

2. A layer violation scan finds that 8 test
   scripts import `python-can` directly instead
   of using `core.can_signal_monitor`. The
   technical debt report rates this as High.
   A TAE argues: "The tests work — why fix
   something that isn't broken?" Construct
   the counter-argument using the concept of
   coupling and future maintenance cost.

3. Runtime metrics show mean test duration has
   grown from 12 seconds to 19 seconds over
   six months without new tests being added.
   List three hypotheses for root cause and
   specify what data you would examine to
   confirm each.

4. Your TAF has 134 magic numbers in assertions.
   A complete replacement would take two sprints.
   Design an incremental strategy that reduces
   risk immediately while spreading the full
   refactoring over three months.

5. The TAF technical analysis report has been
   produced monthly for six months. Findings
   are documented but no actions have been
   taken because "there is always higher priority
   work." The flaky rate is now 7%, coverage
   is at 58%, and layer violations have grown
   from 3 to 11. Construct the business case
   for dedicating 20% of each sprint to TAF
   technical debt reduction.

---

## 12. Practical Takeaways

| # | Action | Where |
|---|--------|-------|
| 1 | Run `detect_layer_violations` on your test suite and fix any direct external imports in test scripts | `framework-prototype/tests/` |
| 2 | Run `collect_runtime_metrics` on your latest JUnit XML and identify the top 3 slowest tests | `framework-prototype/core/report_generator.py` |
| 3 | Produce a technical analysis report for your current ABS TAF using the report template above | `chapter-08-continuous-improvement/` |

---

*Next: Sub-Chapter 8.1.3 — Restructuring Testware*