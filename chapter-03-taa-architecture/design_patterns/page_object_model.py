"""
DESIGN PATTERN — Page Object Model (POM)
Syllabus: CTAL-TAE v2.0 Section 3.1.5

Definition:
    A class file created as a page model.
    When SUT structure changes, TAE updates ONE place only —
    the identifier inside the page model — instead of
    updating every test case that uses that identifier.

Automotive Application:
    ECU Signal Object — automotive equivalent of web POM.
    All CAN signal names, expected values, and DTC codes
    in one class. When ARXML changes, update here only.

Author: Sai Kumar Reddy
"""


class ABSSignalObjects:
    """
    ABS ECU Signal Object — Page Object Model for CAN signals.

    All signal names sourced from ARXML.
    All expected values sourced from requirements.
    All DTC codes sourced from diagnostic specification.

    When ARXML is updated:
        → Update signal names HERE
        → All 600 test scripts automatically use new names
        → Zero test script modifications required
    """

    # ─── CAN Signal Names (from ARXML) ───────────────────
    ABS_ACTIVATION_STATUS  = "ABSActivationStatus"
    WHEEL_SPEED_FL         = "WheelSpeedFrontLeft"
    WHEEL_SPEED_FR         = "WheelSpeedFrontRight"
    WHEEL_SPEED_RL         = "WheelSpeedRearLeft"
    WHEEL_SPEED_RR         = "WheelSpeedRearRight"
    DIAGNOSTIC_FAULT_CODE  = "DiagnosticFaultCode"
    BRAKE_PRESSURE_FRONT   = "BrakePressureFront"
    BRAKE_PRESSURE_REAR    = "BrakePressureRear"

    # ─── Expected State Values (from requirements) ────────
    STATUS_INACTIVE        = 0x00
    STATUS_NORMAL          = 0x01
    STATUS_DEGRADED        = 0x02
    STATUS_FAULT           = 0x03

    # ─── DTC Fault Codes (from diagnostic spec) ──────────
    DTC_WHEEL_FL_OPEN      = "C0035"
    DTC_WHEEL_FR_OPEN      = "C0045"
    DTC_WHEEL_RL_OPEN      = "C0055"
    DTC_WHEEL_RR_OPEN      = "C0065"
    DTC_BRAKE_PRESSURE     = "C0121"

    # ─── Timing Requirements (from requirements) ─────────
    MAX_DEGRADED_RESPONSE_MS = 500
    MAX_DTC_SET_MS           = 1000
    MAX_WARNING_LAMP_MS      = 500


class ESPSignalObjects:
    """
    ESP ECU Signal Object — separate POM for ESP signals.
    Completely independent from ABS signal objects.
    """

    ESP_CONTROL_STATUS     = "ESPControlStatus"
    YAW_RATE_SIGNAL        = "YawRateSensor"
    LATERAL_ACCELERATION   = "LateralAcceleration"
    STEERING_ANGLE         = "SteeringAngleSensor"

    STATUS_INACTIVE        = 0x00
    STATUS_ACTIVE          = 0x01
    STATUS_INTERVENING     = 0x02

    DTC_YAW_RATE_FAULT     = "C0455"
    DTC_STEERING_FAULT     = "C0475"