"""
CORE LIBRARIES LAYER
CAN Signal Monitor — SUT independent utility

Purpose : Monitor and read CAN signal values
Project : Reusable across all ECU projects
Author  : Sai Kumar Reddy
Syllabus: CTAL-TAE v2.0 — TAF Layering (3.1.3)

Rules:
- Zero SUT-specific knowledge in this file
- No ABS, ESP, or project signal names here
- Used by business logic layer only
"""


class CANSignalMonitor:
    """
    SUT-independent CAN signal monitoring utility.
    Works for any ECU project using CAN bus.
    Signal names passed as parameters — never hardcoded.
    """

    def __init__(self):
        self._connection = None
        self._is_monitoring = False
        self._captured_samples = {}

    def connect(self, interface: str, baudrate: int = 500000):
        """
        Connect to CAN interface.

        Args:
            interface: CAN interface name e.g. 'PCAN_USBBUS1'
            baudrate: CAN bus speed in bps, default 500kbps
        """
        # Tool-specific connection code here
        # e.g. python-can, Vector CANalyzer API
        self._connection = f"Connected to {interface} @ {baudrate}"
        print(f"[CANSignalMonitor] {self._connection}")

    def disconnect(self):
        """Safely disconnect from CAN interface."""
        self._connection = None
        print("[CANSignalMonitor] Disconnected")

    def read_signal(self, signal_name: str) -> float:
        """
        Read current value of a named CAN signal.

        Args:
            signal_name: Signal name from ARXML definition
        Returns:
            Current physical value of the signal
        """
        # Tool-specific signal read code here
        # Returns physical value after scaling applied
        return 0.0

    def wait_for_signal(self,
                        signal_name: str,
                        expected_value: float,
                        timeout_ms: int = 5000) -> bool:
        """
        Wait until signal reaches expected value or timeout.

        Args:
            signal_name  : Signal name from ARXML definition
            expected_value: Value to wait for
            timeout_ms   : Maximum wait time in milliseconds
        Returns:
            True if value reached, False if timeout
        """
        # Polling implementation here
        return True

    def start_monitoring(self, signal_names: list):
        """
        Begin recording values for a list of signals.

        Args:
            signal_names: List of signal names to record
        """
        self._is_monitoring = True
        self._captured_samples = {name: [] for name in signal_names}
        print(f"[CANSignalMonitor] Monitoring: {signal_names}")

    def stop_monitoring(self) -> dict:
        """
        Stop recording and return all captured samples.

        Returns:
            Dict of signal_name -> list of (timestamp, value) tuples
        """
        self._is_monitoring = False
        return self._captured_samples