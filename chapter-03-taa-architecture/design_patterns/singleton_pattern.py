"""
DESIGN PATTERN — Singleton Pattern
Syllabus: CTAL-TAE v2.0 Section 3.1.5

Definition:
    Ensures only ONE instance of a resource exists.
    Used for shared resources communicating with SUT.

Automotive Application:
    Single CAN connection shared across entire test suite.
    Prevents multiple conflicting connections to same ECU.

Author: Sai Kumar Reddy
"""


class CANConnectionSingleton:
    """
    Singleton CAN connection manager.

    First call:  get_instance() → creates connection
    All calls:   get_instance() → returns SAME connection
    Result:      Only ONE connection to ECU at all times
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Returns the single shared CAN connection.
        Creates it only on first call.
        """
        if cls._instance is None:
            print("[CANConnection] Creating single connection...")
            cls._instance = cls._create_connection()
        else:
            print("[CANConnection] Returning existing connection")
        return cls._instance

    @classmethod
    def _create_connection(cls) -> dict:
        """Called ONCE only. All subsequent calls get cached instance."""
        return {
            "interface": "PCAN_USBBUS1",
            "baudrate":  500000,
            "status":    "connected"
        }

    @classmethod
    def reset(cls):
        """
        Reset singleton — use in test teardown only.
        Required when running tests in isolation.
        """
        cls._instance = None
        print("[CANConnection] Connection reset")


class TestLoggerSingleton:
    """
    Singleton test logger.
    All test cases write to the same log file.
    """

    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._create_logger()
        return cls._instance

    @classmethod
    def _create_logger(cls):
        return {"log_file": "test_execution.log", "level": "INFO"}


# ─── Demonstration ───────────────────────────────────────────
if __name__ == "__main__":
    conn1 = CANConnectionSingleton.get_instance()
    conn2 = CANConnectionSingleton.get_instance()
    conn3 = CANConnectionSingleton.get_instance()

    print(f"\nAll same instance: {conn1 is conn2 is conn3}")
    print(f"Connection: {conn1}")