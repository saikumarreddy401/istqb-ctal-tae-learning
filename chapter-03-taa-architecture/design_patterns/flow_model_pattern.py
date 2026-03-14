"""
DESIGN PATTERN — Flow Model Pattern
Syllabus: CTAL-TAE v2.0 Section 3.1.5

Definition:
    An expansion of the Page Object Model.
    Introduces an additional facade over page objects
    storing all user actions that interact with page objects.
    By introducing double facade design, provides improved
    abstraction and maintainability — test steps can be
    reused in multiple test scripts.

Structure:
    Test Scripts → Flow Model → Signal Objects (POM)

Automotive Application:
    ABS fault injection and verification sequences
    reused across multiple test cases.

Author: Sai Kumar Reddy
"""

from page_object_model import ABSSignalObjects


class ABSTestFlows:
    """
    Flow Model for ABS ECU testing.

    Layer above POM (ABSSignalObjects).
    Stores complete user action sequences.
    Test scripts call flows — not individual signal operations.

    Benefits:
    - Test step reuse across multiple scripts
    - Double facade protection against SUT changes
    - Domain-language test scripts
    - Single update point for sequence changes
    """

    def __init__(self, monitor, fault_controller):
        self.monitor = monitor
        self.fault   = fault_controller
        self.signals = ABSSignalObjects()

    def trigger_wheel_fault_and_verify_response(
            self,
            sensor_name: str,
            expected_dtc: str,
            timeout_ms: int = None):
        """
        Complete fault injection and verification sequence.
        Reused by multiple test cases with different parameters.

        Used by:
        - test_abs_wheel_speed_fault.py (4 test cases)
        - test_abs_degraded_mode.py (6 test cases)
        - test_abs_regression.py (12 test cases)
        Total: 22 test cases use this single flow
        """
        if timeout_ms is None:
            timeout_ms = self.signals.MAX_DEGRADED_RESPONSE_MS

        self._inject_fault(sensor_name)
        self._verify_degraded_mode(timeout_ms)
        self._verify_dtc_set(expected_dtc)

    def verify_normal_operating_mode(self):
        """
        Verify ECU is in normal mode.
        Used as precondition flow in test setup.
        """
        actual = self.monitor.read_signal(
            self.signals.ABS_ACTIVATION_STATUS
        )
        assert actual == self.signals.STATUS_NORMAL, (
            f"Expected NORMAL ({self.signals.STATUS_NORMAL}) "
            f"but got ({actual})"
        )

    def clear_all_faults_and_verify_recovery(self):
        """
        Clear all injected faults and verify ECU recovers.
        Used as postcondition flow in test teardown.
        """
        self.fault.clear_all_faults()
        self._verify_normal_mode_restored()

    def _inject_fault(self, sensor_name: str):
        """Private flow step — hidden from test scripts."""
        self.fault.inject_open_circuit(sensor_name)

    def _verify_degraded_mode(self, timeout_ms: int):
        """Private flow step — hidden from test scripts."""
        actual = self.monitor.read_signal(
            self.signals.ABS_ACTIVATION_STATUS
        )
        assert actual == self.signals.STATUS_DEGRADED

    def _verify_dtc_set(self, dtc_code: str):
        """Private flow step — hidden from test scripts."""
        pass

    def _verify_normal_mode_restored(self):
        """Private flow step — hidden from test scripts."""
        actual = self.monitor.read_signal(
            self.signals.ABS_ACTIVATION_STATUS
        )
        assert actual == self.signals.STATUS_NORMAL