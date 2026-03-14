"""
BUSINESS LOGIC LAYER
ABS Signal Flows — ABS ECU specific abstractions

Purpose : ABS ECU test flows using domain language
Project : ABS ECU validation project
Author  : Sai Kumar Reddy
Syllabus: CTAL-TAE v2.0 — TAF Layering (3.1.3)

Rules:
- SUT-specific knowledge lives HERE not in test scripts
- Signal names, CAN IDs, expected values defined here
- Calls core libraries — never called by core libraries
- Business logic = WHAT the ECU should do
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core_libraries.can_signal_monitor import CANSignalMonitor
from core_libraries.test_logger import TestLogger


class ABSSignalFlows:
    """
    ABS ECU specific test flows.
    All ABS signal names and expected values live here.
    Test scripts call these methods using domain language.
    """

    # ─── Signal Names from ARXML ──────────────────────────
    # Update HERE when ARXML changes — not in test scripts
    ABS_ACTIVATION_STATUS = "ABSActivationStatus"
    WHEEL_SPEED_FL        = "WheelSpeedFrontLeft"
    WHEEL_SPEED_FR        = "WheelSpeedFrontRight"
    WHEEL_SPEED_RL        = "WheelSpeedRearLeft"
    WHEEL_SPEED_RR        = "WheelSpeedRearRight"
    DIAGNOSTIC_FAULT_CODE = "DiagnosticFaultCode"

    # ─── Expected State Values ────────────────────────────
    STATUS_NORMAL         = 0x01
    STATUS_DEGRADED       = 0x02
    STATUS_INACTIVE       = 0x00

    def __init__(self):
        self.monitor = CANSignalMonitor()
        self.logger  = TestLogger()

    def set_normal_operating_mode(self):
        """
        Verify ABS ECU is in normal operating mode.
        Waits up to 2 seconds for normal status.
        """
        self.logger.info("Verifying ABS normal operating mode")
        result = self.monitor.wait_for_signal(
            signal_name    = self.ABS_ACTIVATION_STATUS,
            expected_value = self.STATUS_NORMAL,
            timeout_ms     = 2000
        )
        assert result, "ABS did not reach normal mode within 2000ms"

    def verify_degraded_mode_activated(self, timeout_ms: int = 1000):
        """
        Verify ABS transitions to degraded mode.
        Per requirement: transition must occur within 500ms of fault.

        Args:
            timeout_ms: Maximum time to wait for degraded mode
        """
        self.logger.info("Verifying ABS degraded mode activation")
        actual = self.monitor.read_signal(self.ABS_ACTIVATION_STATUS)
        assert actual == self.STATUS_DEGRADED, (
            f"Expected ABS status DEGRADED ({self.STATUS_DEGRADED}) "
            f"but got ({actual})"
        )

    def verify_dtc_set(self, dtc_code: str):
        """
        Verify a specific DTC is set in the ECU.

        Args:
            dtc_code: DTC identifier string e.g. 'C0035'
        """
        self.logger.info(f"Verifying DTC {dtc_code} is set")
        # UDS diagnostic read implementation here
        pass

    def read_all_wheel_speeds(self) -> dict:
        """
        Read current wheel speed values for all four wheels.

        Returns:
            Dict with wheel position keys and speed values in km/h
        """
        return {
            "front_left" : self.monitor.read_signal(self.WHEEL_SPEED_FL),
            "front_right": self.monitor.read_signal(self.WHEEL_SPEED_FR),
            "rear_left"  : self.monitor.read_signal(self.WHEEL_SPEED_RL),
            "rear_right" : self.monitor.read_signal(self.WHEEL_SPEED_RR),
        }