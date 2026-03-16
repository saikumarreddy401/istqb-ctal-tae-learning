# Scenarios — Sub-Chapter 5.1.3 — Test Automation Dependencies for API Infrastructure

> **Syllabus Reference:** TAE-5.1.3
> **Cognitive Level:** K2 — Understand
> **File:** scenarios_5_1_3_api_dependencies.md
> **Status:** ✅ Complete

---

## Scenario 1 — Schema Validation vs Contract Testing (K2)

### Situation

A Bosch TAE is validating CAN signal communication for
the ABS system. He writes a test that loads the ARXML
file and checks that all signal definitions have a
valid name, start bit, length, and scaling factor.
If the ARXML is structurally correct, the test passes.

A colleague reviews the test and says:
"This is schema validation — not contract testing.
We still have no contract test."

### Question

Explain the difference between what the TAE implemented
and what a contract test would verify. Use the ABS
CAN signal context.

### Answer

> ⭐ The TAE implemented **schema validation**.
> It confirms the ARXML file is well-formed and
> contains required fields — but it does not verify
> that the ECU's actual runtime behavior matches
> what the ARXML defines.

| Aspect | Schema Validation (what TAE built) | Contract Test (what is missing) |
|--------|-----------------------------------|---------------------------------|
| What it checks | ARXML structure is valid | ECU signal values match ARXML contract at runtime |
| When it runs | File parsing time | Test execution against running ECU |
| What it catches | Missing fields, wrong data types | ECU sending wrong scaling, wrong range, wrong byte order |
| Failure example | ARXML missing scaling factor field | ECU sends wheel speed in km/h but ARXML defines 0.01 km/h |

**What the contract test would look like:**
```python
def test_wheel_speed_signal_contract():
    """
    Contract: WheelSpeedFL on CAN ID 0x1A0
    Bytes 0-1, scaling 0.01 km/h, range 0-250 km/h
    """
    signal = can_monitor.read_signal("WheelSpeedFL")

    assert signal.can_id == 0x1A0
    assert signal.byte_position == (0, 1)
    assert 0 <= signal.value_kmh <= 250
```

> Schema validation answers: *"Is the ARXML well-formed?"*
> Contract testing answers: *"Does the ECU behave as
> the ARXML contract specifies?"*

---

## Scenario 2 — Where Contract Tests Belong in the Pipeline (K2)

### Situation

Your team currently runs UDS contract tests as part of
the integration test stage. This means the tests only
run after the ECU firmware has been deployed to the
HIL rack. A firmware change that violates the UDS
contract is not discovered until the HIL integration
run — typically 4–6 hours after the firmware was built.

A test architect proposes moving the contract tests
to the build pipeline stage, running them against a
UDS service stub rather than the real ECU.

### Question

Explain why the architect's proposal is correct and
what the TAE must change to enable it.

### Answer

> ⭐ Contract tests belong in the **build stage** because
> their purpose is to detect API incompatibilities
> before deployment — not after.

**Current flow (wrong):**
```
Firmware built → deployed to HIL → integration tests run
→ contract violation found → 4-6 hours delay
```

**Proposed flow (correct):**
```
Firmware built → contract tests run against UDS stub
→ contract violation found immediately
→ merge blocked before HIL deployment
```

**What the TAE must change:**

| Change | Detail |
|--------|--------|
| Replace real ECU with UDS stub | Stub returns pre-defined responses per DID |
| Contract tests run in build pipeline | No HIL rack required |
| Real ECU tests remain in integration stage | Full runtime behavior tested separately |

> The contract test does not test the ECU's real behavior —
> it tests that the interface contract is still honoured.
> A stub is sufficient and correct for this purpose.

---

## Scenario 3 — Consumer-Driven vs Provider-Driven (K2)

### Situation

The Bosch ESP team owns the ESP diagnostic service.
Five consumer teams depend on this service:

- ABS integration team (reads ESP stability status)
- Dashboard team (reads ESP warning flag)
- Calibration team (reads calibration variant ID)
- HIL test automation team (reads multiple DIDs)
- End-of-line test team (reads production test results)

The ESP team wants to refactor the service response
format. They ask: "How do we know which consumers
will break if we change field X?"

### Question

Which contract testing approach answers the ESP team's
question, and how does it work in practice?

### Answer

> ⭐ **Consumer-driven contract testing** answers this question.
>
> Each consumer team publishes a contract describing
> exactly which fields and behaviors they depend on.
> The ESP team runs provider verification against all
> five published contracts before any change is merged.

**Workflow:**

| Step | Who | Action |
|------|-----|--------|
| 1 | Each consumer team | Defines interactions they depend on |
| 2 | Each consumer team | Publishes contract to contract broker |
| 3 | ESP team | Runs provider verification against all contracts |
| 4 | Contract broker | Reports which contracts pass or fail |
| 5 | ESP team | Knows exactly which consumers the change breaks |

> If the ESP team removes field X and the HIL automation
> team's contract depends on field X, the provider
> verification fails — before any code is merged.
> The ESP team knows immediately which team to contact.

**Why provider-driven is insufficient here:**

> If the ESP team publishes their own contract (provider-driven),
> they control what is guaranteed. Consumers may depend on
> fields the provider did not explicitly include in their contract.
> Provider-driven does not reveal hidden consumer dependencies.

---

## Scenario 4 — API Documentation as Baseline (K2)

### Situation

A new TAE joins the ABS team. To get up to speed quickly,
she writes CAN signal test assertions by reading last
month's integration test logs rather than reading the
ARXML specification. The assertions pass because the
current ECU behavior matches the logs.

Three weeks later the ABS firmware team updates the
wheel speed signal scaling from 0.01 km/h to 0.005 km/h
for higher precision. The ARXML is updated. The tests
still pass — because the assertions were written from
old log values, not from the ARXML contract.

### Question A

What architectural risk did the TAE introduce by using
logs instead of documentation as the baseline?

### Answer A

> ⭐ The TAE coupled test assertions to **observed
> past behavior** rather than to the **documented contract**.
>
> Risk: When the contract changes correctly (ARXML updated,
> firmware updated), the tests still pass — against the
> wrong values. This is a silent false pass.

| Baseline Source | Coupling | Risk |
|----------------|----------|------|
| Integration logs (used) | Coupled to past implementation | Tests pass silently after contract change |
| ARXML specification (correct) | Coupled to contract | Tests fail when contract changes — defect detected |

### Question B

How does using documentation as the baseline prevent
this failure?

### Answer B

> When assertions are derived from the ARXML contract,
> the test framework loads expected values from ARXML
> at runtime. When ARXML is updated to 0.005 km/h scaling,
> the expected values update automatically. If the ECU
> firmware has not yet been updated, the test fails —
> correctly identifying the mismatch between spec and
> implementation.
```python
# WRONG — hardcoded from log observation
assert wheel_speed_fl == 1250  # where did 1250 come from?

# CORRECT — derived from ARXML contract
expected = arxml_loader.get_signal_raw_value(
    signal_name="WheelSpeedFL",
    physical_value_kmh=12.50
)
assert wheel_speed_fl == expected
```

---

## Scenario 5 — Business Logic Understanding (K2)

### Situation

A TAE writes a UDS test for ABS fault memory reading.
The test sends a ReadDTCInformation request (service 0x19)
and asserts that the response code is 0x59 (positive
response). The test passes.

During a safety audit, the auditor asks: "Does your test
verify that the DTC content is correct — not just that
the ECU responded?"

The TAE has no answer. The test only checks the response
code, not the DTC bytes.

### Question

What business logic knowledge was missing, and what
should the contract test assert beyond the response code?

### Answer

> ⭐ The TAE understood the **API interface** (send 0x19,
> expect 0x59) but not the **business logic** (what the
> response bytes represent and what values are correct).

**Business logic the TAE should have understood:**

| Response Element | Business Logic Meaning |
|-----------------|----------------------|
| Bytes 0-1 | DTC code (e.g. 0xC0051 = wheel speed sensor fault) |
| Byte 2 | DTC status byte (bit 3 = confirmed fault) |
| Byte 3 | Occurrence counter (how many times fault triggered) |

**Complete contract test:**
```python
def test_uds_dtc_fault_memory_contract():
    """
    Contract: After wheel speed sensor fault injection,
    DTC 0xC0051 must be present with status = confirmed,
    occurrence counter >= 1
    """
    # Inject fault
    fault_injector.set_wheel_speed_sensor_open_circuit()

    # Read DTC
    response = uds_client.read_dtc_information(
        sub_function=0x02,  # reportDTCByStatusMask
        status_mask=0x08    # confirmed DTC
    )

    assert response.positive_response_code == 0x59
    assert 0xC0051 in response.dtc_list
    assert response.get_dtc_status(0xC0051).confirmed == True
    assert response.get_dtc_status(0xC0051).occurrence_count >= 1
```

> Checking only the response code verifies the API is
> responding — not that the ECU's fault memory logic
> is correct. Business logic understanding is what
> separates a shallow test from a meaningful one.

---

## Scenario 6 — CAN Message Format as Contract (K2)

### Situation

The Bosch ABS team and the instrument cluster team
communicate via CAN bus. The ABS ECU sends wheel speed
signals. The instrument cluster reads them to display
vehicle speed.

The ABS firmware team is planning to change the CAN
message layout for wheel speed — specifically moving
WheelSpeedFL from bytes 0–1 to bytes 2–3 to accommodate
a new signal in the same CAN frame.

### Question

Without contract testing, how would this change be
discovered, and how does defining the CAN message
format as a contract change the discovery point?

### Answer

> ⭐ **Without contract testing:**
>
> The byte layout change is implemented in ABS firmware.
> The instrument cluster team is not notified.
> Both modules are integrated in the vehicle.
> The speedometer displays incorrect values — or zero.
> Discovery happens at vehicle integration test — late,
> expensive, requires hardware coordination.

**With CAN contract testing:**

| Step | Action |
|------|--------|
| 1 | Instrument cluster team publishes consumer contract: WheelSpeedFL at bytes 0-1 |
| 2 | ABS team runs provider verification before committing the byte layout change |
| 3 | Contract test fails: WheelSpeedFL moved from bytes 0-1 to bytes 2-3 |
| 4 | ABS team and cluster team coordinate before any code is merged |
| 5 | Discovery at build time — not vehicle integration time |

**The CAN contract definition:**
```python
CAN_CONTRACT = {
    "message_id": 0x1A0,
    "signals": {
        "WheelSpeedFL": {"start_byte": 0, "length_bytes": 2, "scaling": 0.01},
        "WheelSpeedFR": {"start_byte": 2, "length_bytes": 2, "scaling": 0.01},
    }
}
```

> ⭐ The DBC and ARXML files are the CAN contract.
> Any change to signal byte positions, scaling, or
> message IDs is a contract change — and must be
> verified against all consumers before deployment.

---

## Quick Reference — Core Exam Points

| Concept | Key Point |
|---------|----------|
| API documentation as baseline | Derive all assertions from spec, not from logs or assumptions |
| Business logic understanding | Test meaning of response, not just response code |
| Schema validation | Checks message structure — not runtime behavior |
| Contract testing | Checks runtime behavior matches agreed interface |
| Consumer-driven contract | Consumer defines what it needs from provider |
| Provider-driven contract | Provider defines and publishes what it guarantees |
| Pipeline placement | Contract tests in build stage — not integration stage |
| Automotive equivalent | UDS spec = API contract, ARXML/DBC = schema |

---

## Consumer-Driven vs Provider-Driven — Exam Summary

| Property | Consumer-Driven | Provider-Driven |
|----------|----------------|----------------|
| Contract owner | Consumer | Provider |
| Best for | Microservice ecosystems, many consumers | Published APIs, provider controls spec |
| Finds | Provider changes breaking consumers | Consumer misuse of API |
| Automotive use | ECU test automation defines UDS contract | AUTOSAR SWC interface spec |
| Tool example | Pact framework | OpenAPI / Swagger validation |

---

*Next: Chapter 6 — Test Automation Reporting and Metrics*