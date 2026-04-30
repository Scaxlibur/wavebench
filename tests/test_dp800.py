import unittest

from wavebench.drivers.dp800 import DP800Power, parse_apply_response, parse_measure_all_response


class FakeTransport:
    def __init__(self):
        self.queries = []
        self.writes = []

    def write(self, command: str) -> None:
        self.writes.append(command)

    def query(self, command: str) -> str:
        self.queries.append(command)
        mapping = {
            "*IDN?": "RIGOL TECHNOLOGIES,DP832A,SN,FW",
            ":APPL? CH1": "CH1:30V/3A,5.000,0.100",
            ":MEAS:ALL? CH1": "5.0114,0.0000,0.000",
            ":OUTP? CH1": "ON",
            ":OUTP:MODE? CH1": "CV",
            "SYST:ERR?": '0,"No error"',
        }
        return mapping[command]

    def close(self) -> None:
        pass


class DP800Tests(unittest.TestCase):
    def test_parse_apply_response(self):
        rating, voltage, current = parse_apply_response("CH1:30V/3A,5.000,0.100")
        self.assertEqual(rating, "30V/3A")
        self.assertEqual(voltage, 5.0)
        self.assertEqual(current, 0.1)

    def test_parse_measure_all_response(self):
        voltage, current, power = parse_measure_all_response("5.0114,0.0000,0.000")
        self.assertEqual(voltage, 5.0114)
        self.assertEqual(current, 0.0)
        self.assertEqual(power, 0.0)

    def test_get_status_reads_read_only_fields(self):
        transport = FakeTransport()
        driver = DP800Power(transport=transport)
        status = driver.get_status(1)
        self.assertEqual(status.channel, 1)
        self.assertEqual(status.output, "ON")
        self.assertEqual(status.mode, "CV")
        self.assertEqual(status.rating, "30V/3A")
        self.assertEqual(status.set_voltage_v, 5.0)
        self.assertEqual(status.set_current_a, 0.1)
        self.assertEqual(status.measured_voltage_v, 5.0114)
        self.assertEqual(status.measured_current_a, 0.0)
        self.assertEqual(status.measured_power_w, 0.0)
        self.assertEqual(transport.queries, [
            ":APPL? CH1",
            ":MEAS:ALL? CH1",
            ":OUTP? CH1",
            ":OUTP:MODE? CH1",
        ])

    def test_set_voltage_current_limit_writes_apply_only(self):
        transport = FakeTransport()
        driver = DP800Power(transport=transport)
        status = driver.set_voltage_current_limit(1, 3.3, 0.2, check_errors=True)
        self.assertEqual(transport.writes, [":APPL CH1,3.3,0.2"])
        self.assertEqual(status.output, "ON")
        self.assertNotIn(":OUTP CH1,ON", transport.writes)
        self.assertNotIn(":OUTP CH1,OFF", transport.writes)

    def test_set_voltage_current_limit_rejects_invalid_values(self):
        driver = DP800Power(transport=FakeTransport())
        with self.assertRaisesRegex(Exception, "voltage must be >= 0"):
            driver.set_voltage_current_limit(1, -1.0, 0.1)
        with self.assertRaisesRegex(Exception, "current limit must be > 0"):
            driver.set_voltage_current_limit(1, 1.0, 0.0)


if __name__ == "__main__":
    unittest.main()
