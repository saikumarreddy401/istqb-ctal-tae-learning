"""
DESIGN PATTERN — Facade Pattern
Syllabus: CTAL-TAE v2.0 Section 3.1.5

Definition:
    Hides implementation details to only expose
    what testers need to create test cases.

Automotive Application:
    HIL fault injection complexity hidden behind
    simple domain-language interface.

Author: Sai Kumar Reddy
"""


class FaultInjectionFacade:
    """
    Facade over HIL rack fault injection API.

    Test scripts see: fault.inject_open_circuit("front_left")
    Facade hides:     channel lookup, HIL API calls,
                      verification, timeout handling, logging
    """

    _CHANNEL_MAP = {
        "front_left_wheel_speed":  "CH_01",
        "front_right_wheel_speed": "CH_02",
        "rear_left_wheel_speed":   "CH_03",
        "rear_right_wheel_speed":  "CH_04",
        "brake_pressure_sensor":   "CH_05",
        "steering_angle_sensor":   "CH_06",
    }

    _FAULT_TYPES = {
        "OPEN_CIRCUIT":   0x01,
        "SHORT_TO_GND":   0x02,
        "SHORT_TO_BATT":  0x03,
        "NORMAL":         0x00,
    }

    def inject_open_circuit(self, sensor_name: str):
        """Simple interface — all complexity hidden below."""
        self._apply_fault(sensor_name, "OPEN_CIRCUIT")

    def inject_short_to_ground(self, sensor_name: str):
        """Simple interface — all complexity hidden below."""
        self._apply_fault(sensor_name, "SHORT_TO_GND")

    def clear_all_faults(self):
        """Restore all channels to normal state."""
        for channel in self._CHANNEL_MAP.values():
            self._set_channel_state(channel, "NORMAL")

    def _apply_fault(self, sensor_name: str, fault_type: str):
        """Private — hidden from test scripts."""
        channel = self._resolve_channel(sensor_name)
        self._set_channel_state(channel, fault_type)
        self._verify_fault_active(channel, fault_type)

    def _resolve_channel(self, sensor_name: str) -> str:
        """Private — channel mapping hidden here."""
        channel = self._CHANNEL_MAP.get(sensor_name)
        if not channel:
            raise ValueError(
                f"Unknown sensor '{sensor_name}'. "
                f"Valid: {list(self._CHANNEL_MAP.keys())}"
            )
        return channel

    def _set_channel_state(self, channel: str, fault_type: str):
        """Private — HIL rack API call hidden here."""
        fault_code = self._FAULT_TYPES.get(fault_type, 0x00)
        print(f"[HIL] Setting {channel} to {fault_type} (0x{fault_code:02X})")

    def _verify_fault_active(self, channel: str, fault_type: str):
        """Private — verification hidden here."""
        print(f"[HIL] Verified {channel} is {fault_type}")