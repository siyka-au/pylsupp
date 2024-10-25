import datetime
from enum import Enum

class UppCommand(Enum):
    READ_TEMPERATURE = b'ms'
    READ_TEMPERATURES_MONO_AND_RATIO = b'ek'
    READ_TEMPERATURE_VALUE_REPEATED = b'ms'
    EDM_SINGLE_FAST = 3
    EDM_SINGLE_LRANGE = 4   # Long range single measurement
    EDM_SINGLE_SRANGE = 5   # Short range single measurement
    EDM_CONT_STANDARD = 6   # Standard repeated measurement
    EDM_CONT_DYNAMIC = 7    # Dynamic repeated measurement
    EDM_CONT_REFLESS = 8    # Reflectorless repeated measurement
    EDM_CONT_FAST = 9       # Fast repeated measurement
    EDM_AVERAGE_IR = 10     # Standard average measurement
    EDM_AVERAGE_SR = 11     # Short range average measurement
    EDM_AVERAGE_LR = 12     # Long range average measurement

class LumasensePyrometer:
    """Lumasense pyrometer, e.g. IGA-6-23 or IGAR-6-adv."""

    def __init__(self, stream):
        """Setup serial interface, configure device.

        Args:
            config (dict): device configuration (as defined in
                config.yml in the devices-section).
            name (str, optional): Device name.
        """
        self.serial = stream

    def _get_ok(self):
        """Check if command was accepted."""
        assert self.serial.stream().decode().strip() == "ok"

    def _get_float(self):
        """Read floatingpoint value."""
        string_val = self.serial.readline().decode().strip()
        return float(f"{string_val[:-1]}.{string_val[-1:]}")

    @property
    def focus(self):
        """Get focuspoint."""
        cmd = f"{self.device_id}df\r"
        self.serial.write(cmd.encode())
        return self.serial.readline().decode().strip()

    @property
    def intrument_id(self):
        """Get the instrument id."""
        cmd = f"{self.device_id}na\r"
        self.serial.write(cmd.encode())
        return self.serial.readline().decode().strip()

    @property
    def emissivity(self):
        """Read the current emissivity."""
        cmd = f"{self.device_id}em\r"
        self.serial.write(cmd.encode())
        return self._get_float()

    @property
    def transmissivity(self):
        """Read the current transmissivity."""
        cmd = f"{self.device_id}et\r"
        self.serial.write(cmd.encode())
        return self._get_float()

    @property
    def t90(self):
        """Reat the current t90 value."""
        cmd = f"{self.device_id}ez\r"
        self.serial.write(cmd.encode())
        idx = int(self.serial.readline().decode().strip())
        t90_dict_inverted = {v: k for k, v in self.t90_dict.items()}
        return t90_dict_inverted[idx]

    def set_emissivity(self, emissivity):
        """Set emissivity and check if it was accepted."""
        cmd = f"{self.device_id}em{emissivity*100:05.1f}\r".replace(".", "")
        self.serial.write(cmd.encode())
        self._get_ok()
        assert self.emissivity == emissivity * 100

    def set_transmissivity(self, transmissivity):
        """Set transmissivity and check if it was accepted."""
        cmd = f"{self.device_id}et{transmissivity*100:05.1f}\r".replace(".", "")
        self.serial.write(cmd.encode())
        self._get_ok()
        assert self.transmissivity == transmissivity * 100

    def set_t90(self, t90):
        """Set t90 and check if it was accepted."""
        cmd = f"{self.device_id}ez{self.t90_dict[t90]}\r"
        self.serial.write(cmd.encode())
        self._get_ok()
        assert self.t90 == t90

    def read_temperature(self):
        """Read temperature form device.

        Returns:
            float: temperature reading.
        """
        cmd = f"{self.device_id}ms\r"
        self.serial.write(cmd.encode())
        return self._get_float()

