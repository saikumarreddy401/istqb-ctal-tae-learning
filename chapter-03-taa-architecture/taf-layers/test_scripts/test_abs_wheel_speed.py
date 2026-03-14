"""
TEST SCRIPTS LAYER
ABS Wheel Speed Fault Test Cases

Purpose : ABS ECU wheel speed sensor fault validation
Project : ABS ECU validation project
Author  : Sai Kumar Reddy
Syllabus: CTAL-TAE v2.0 — TAF Layering (3.1.3)

Rules:
- NO signal names here — use business logic methods
- NO CAN IDs, DTC codes, or tool API calls here
- NO direct calls to core libraries
- Test cases describe WHAT is tested in plain language
- All SUT interaction goes through business logic layer
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from taf_layers.business_logic.abs_signal_flows import ABSSignalFlows
from taf_layers.business_logic.fault_injection_sequences import FaultInjection


class TestABSWheelSpeedFault:
    """
    Test suite: ABS wheel speed sensor fault handling.
    All tests use business logic layer exclusively.
    Signal names and expected values are NOT in this file.
    """

    def setup_method(self):
        """Run before each test — establish normal operating mode."""
        self.abs = ABSSignalFlows()
        self.fault = FaultInjection()
        self.abs.set_normal_operating_mode()

    def test_front_left_sensor_open_circuit(self):
        """
        Verify ABS responds correctly to front left
        wheel speed sensor open circuit fault.

        Requirement: REQ-ABS-042
        Expected: Degraded mode + DTC C0035 within 500ms
        """
        # Arrange — already in normal mode from setup
        # Act
        self.fault.inject_open_circuit("front_left_wheel_speed")
        # Assert
        self.abs.verify_degraded_mode_activated(timeout_ms=500)
        self.abs.verify_dtc_set("C0035")

    def test_front_right_sensor_open_circuit(self):
        """
        Verify ABS responds correctly to front right
        wheel speed sensor open circuit fault.

        Requirement: REQ-ABS-043
        Expected: Degraded mode + DTC C0045 within 500ms
        """
        self.fault.inject_open_circuit("front_right_wheel_speed")
        self.abs.verify_degraded_mode_activated(timeout_ms=500)
        self.abs.verify_dtc_set("C0045")

    def test_all_wheel_speeds_normal_at_startup(self):
        """
        Verify all four wheel speed signals are
        readable and within expected range at startup.

        Requirement: REQ-ABS-010
        """
        speeds = self.abs.read_all_wheel_speeds()
        for wheel, speed in speeds.items():
            assert speed >= 0, f"Wheel {wheel} speed is negative: {speed}"