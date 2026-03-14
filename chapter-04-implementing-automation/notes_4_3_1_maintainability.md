"""
CLEAN CODE EXAMPLE — Logging Levels
Syllabus: CTAL-TAE v2.0 Section 4.3.1 and 4.2.1

Demonstrates all six logging levels as defined
in the CTAL-TAE syllabus with automotive examples.

All six levels are examinable — know them in order.

Author: Sai Kumar Reddy
"""

import logging
import sys


# ─────────────────────────────────────────────────────────────
# SIX LOGGING LEVELS — SYLLABUS DEFINITION
# ─────────────────────────────────────────────────────────────

# FATAL  — Error events that may ABORT test execution
# ERROR  — Condition fails and FAILS the test case
# WARN   — Unexpected condition but test CONTINUES
# INFO   — Basic information about test execution
# DEBUG  — Execution details for failure investigation
# TRACE  — Most detailed — every operation logged


# ─────────────────────────────────────────────────────────────
# LOGGING CONFIGURATION
# ─────────────────────────────────────────────────────────────

def configure_test_logger(
        log_level: str = "INFO",
        log_file: str = "test_execution.log"
) -> logging.Logger:
    """
    Configure logger for test automation.
    Log level is configurable per environment — never hardcoded.

    Args:
        log_level: Logging level string — INFO, DEBUG, etc.
        log_file : Output file path for log records

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("TAF")
    logger.setLevel(getattr(logging, log_level.upper()))

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# ─────────────────────────────────────────────────────────────
# AUTOMOTIVE LOGGING EXAMPLES — ALL SIX LEVELS
# ─────────────────────────────────────────────────────────────

logger = configure_test_logger(log_level="DEBUG")


class ABSTestWithLogging:
    """
    Demonstrates correct use of all six logging levels
    in an ABS ECU test automation context.
    """

    def test_abs_fault_response(self):

        # ── INFO ─────────────────────────────────────────────
        # Basic information about what is happening
        logger.info("ABS_TEST_042 started")
        logger.info("Monitoring signals: ABSStatus, WheelSpeedFL")

        # ── DEBUG ─────────────────────────────────────────────
        # Detailed execution information for investigation
        logger.debug("CAN adapter connected: PCAN_USBBUS1 @ 500kbps")
        logger.debug("Signal sampling rate: 10ms")
        logger.debug("XCP session opened: ECU 192.168.100.10")

        # Inject fault
        logger.info("Injecting open circuit on CH_01 (front left wheel speed)")
        logger.debug("HIL channel CH_01 set to OPEN_CIRCUIT state 0x01")

        # ── WARN ──────────────────────────────────────────────
        # Unexpected but test continues — no failure
        can_delay_ms = 15
        if can_delay_ms > 10:
            logger.warning(
                f"CAN message received {can_delay_ms}ms late "
                f"— within 20ms tolerance, test continues"
            )

        # ── TRACE ─────────────────────────────────────────────
        # Most detailed — every low-level operation
        logger.debug("TRACE: XCP DAQ frame received: [0x02, 0x00, 0x01, 0xFF]")
        logger.debug("TRACE: Signal decode: ABSStatus = 0x02 (raw: 0x0200)")

        # Read and verify signal
        actual_status = 0x02
        expected_status = 0x02

        if actual_status == expected_status:
            logger.info(
                f"ABSStatus = {hex(actual_status)} — MATCHES expected "
                f"{hex(expected_status)}"
            )
        else:
            # ── ERROR ─────────────────────────────────────────
            # Test FAILS — but next test will still run
            logger.error(
                f"ASSERTION FAILED: ABSStatus = {hex(actual_status)} "
                f"— expected {hex(expected_status)}"
            )
            logger.error("Saving signal trace for root cause analysis")
            raise AssertionError(
                f"ABSStatus mismatch: got {hex(actual_status)}, "
                f"expected {hex(expected_status)}"
            )

        logger.info("ABS_TEST_042 PASSED")

    def test_with_fatal_condition(self):

        try:
            # Attempt to connect to HIL rack
            self._connect_to_hil_rack()

        except ConnectionError as e:
            # ── FATAL ─────────────────────────────────────────
            # MAY ABORT entire test execution
            logger.critical(
                f"FATAL: HIL rack connection lost — "
                f"cannot execute remaining test cases. "
                f"Error: {e}"
            )
            # Stop entire test execution
            raise SystemExit(1)

    def _connect_to_hil_rack(self):
        """Simulated connection — raises error to demonstrate Fatal."""
        raise ConnectionError("HIL rack at 192.168.100.10 unreachable")


# ─────────────────────────────────────────────────────────────
# ENVIRONMENT CONFIGURATION EXAMPLES
# ─────────────────────────────────────────────────────────────

LOGGING_CONFIG = {
    "local_development": "DEBUG",   # Full detail for developer
    "build_environment": "INFO",    # Basic info for CI/CD logs
    "integration":       "INFO",    # Basic + auto-debug on failure
    "preproduction":     "INFO",    # Basic info
    "production":        "WARN",    # Only unexpected conditions
}

# ─────────────────────────────────────────────────────────────
# LEVEL SUMMARY TABLE (for exam reference)
# ─────────────────────────────────────────────────────────────

LOGGING_LEVEL_SUMMARY = """
Level   | Abbrev | Fails Test? | Aborts Suite? | When Used
--------|--------|-------------|---------------|----------
FATAL   | CRIT   | YES         | MAY ABORT     | Connection lost, unrecoverable error
ERROR   | ERR    | YES         | NO            | Assertion failed, test condition failed
WARN    | WARN   | NO          | NO            | Unexpected but handled condition
INFO    | INFO   | NO          | NO            | Normal execution milestones
DEBUG   | DEBUG  | NO          | NO            | Details for failure investigation
TRACE   | TRACE  | NO          | NO            | Every low-level operation
"""