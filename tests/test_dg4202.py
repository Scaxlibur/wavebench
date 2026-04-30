import unittest

from wavebench.drivers.dg4202 import DG4202Source


class FakeTransport:
    def __init__(self):
        self.writes = []
        self.error_queue = ['0,"No error"']
        self.state = {
            "out": "ON",
            "func": "SIN",
            "freq": 5000.0,
            "volt": 5.0,
            "unit": "VPP",
            "offs": 0.0,
            "phas": 0.0,
            "mode": "SWE",
            "swe": "ON",
            "apply": '"SIN,5.000000E+03,5.000000E+00,0.000000E+00,0.000000E+00"',
            "duty": 50.0,
        }

    def write(self, command: str) -> None:
        self.writes.append(command)
        if command.startswith(":SOUR2:FREQ:MODE "):
            self.state["mode"] = command.split()[-1]
            self.state["swe"] = "OFF" if self.state["mode"] == "FIX" else "ON"
        elif command.startswith(":SOUR2:FREQ "):
            self.state["freq"] = float(command.split()[-1])
        elif command.startswith(":OUTP2 "):
            self.state["out"] = command.split()[-1]
        elif command.startswith(":SOUR2:FUNC "):
            self.state["func"] = command.split()[-1]
        elif command.startswith(":SOUR2:VOLT:UNIT "):
            self.state["unit"] = command.split()[-1]
        elif command.startswith(":SOUR2:VOLT "):
            self.state["volt"] = float(command.split()[-1])
        elif command.startswith(":SOUR2:FUNC:SQU:DCYC "):
            self.state["duty"] = float(command.split()[-1])

    def query(self, command: str) -> str:
        if command == "SYST:ERR?":
            if self.error_queue:
                return self.error_queue.pop(0)
            return '0,"No error"'
        mapping = {
            "*IDN?": "Rigol Technologies,DG4202,SN,FW",
            ":OUTP2?": self.state["out"],
            ":SOUR2:FUNC?": self.state["func"],
            ":SOUR2:FREQ?": str(self.state["freq"]),
            ":SOUR2:VOLT?": str(self.state["volt"]),
            ":SOUR2:VOLT:UNIT?": self.state["unit"],
            ":SOUR2:VOLT:OFFS?": str(self.state["offs"]),
            ":SOUR2:PHAS?": str(self.state["phas"]),
            ":SOUR2:FREQ:MODE?": self.state["mode"],
            ":SOUR2:SWE:STAT?": self.state["swe"],
            ":SOUR2:APPL?": self.state["apply"],
            ":SOUR2:FUNC:SQU:DCYC?": str(self.state["duty"]),
            ":SOUR2:FUNC:USER?": '"USER1"',
            ":SOUR2:ARB:SRAT?": "1000000",
        }
        if command not in mapping:
            self.error_queue.append('-113,"Undefined header"')
            return ""
        return mapping[command]

    def close(self) -> None:
        pass


class DG4202Tests(unittest.TestCase):
    def test_get_status_reads_basic_fields(self):
        driver = DG4202Source(transport=FakeTransport(), check_errors_after_ops=True)
        status = driver.get_status(2)
        self.assertEqual(status.channel, 2)
        self.assertEqual(status.output, "ON")
        self.assertEqual(status.frequency_mode, "SWE")
        self.assertEqual(status.frequency_hz, 5000.0)
        self.assertEqual(status.square_duty_cycle_percent, 50.0)

    def test_set_frequency_switches_to_fix_mode(self):
        transport = FakeTransport()
        driver = DG4202Source(transport=transport, check_errors_after_ops=True)
        status = driver.set_frequency(2, 1000.0, ensure_fix_mode=True, check_errors=True)
        self.assertEqual(transport.writes[0], ":SOUR2:FREQ:MODE FIX")
        self.assertEqual(transport.writes[1], ":SOUR2:FREQ 1000")
        self.assertEqual(status.frequency_mode, "FIX")
        self.assertEqual(status.frequency_hz, 1000.0)
        self.assertEqual(status.sweep_enabled, "OFF")

    def test_set_output_writes_requested_state(self):
        transport = FakeTransport()
        driver = DG4202Source(transport=transport, check_errors_after_ops=True)
        status = driver.set_output(2, False, check_errors=True)
        self.assertEqual(transport.writes[0], ":OUTP2 OFF")
        self.assertEqual(status.output, "OFF")

    def test_set_function_writes_normalized_function(self):
        transport = FakeTransport()
        driver = DG4202Source(transport=transport, check_errors_after_ops=True)
        status = driver.set_function(2, "square", check_errors=True)
        self.assertEqual(transport.writes[0], ":SOUR2:FUNC SQU")
        self.assertEqual(status.function, "SQU")

    def test_set_amplitude_vpp_writes_unit_and_value(self):
        transport = FakeTransport()
        driver = DG4202Source(transport=transport, check_errors_after_ops=True)
        status = driver.set_amplitude_vpp(2, 3.3, check_errors=True)
        self.assertEqual(transport.writes[0], ":SOUR2:VOLT:UNIT VPP")
        self.assertEqual(transport.writes[1], ":SOUR2:VOLT 3.3")
        self.assertEqual(status.amplitude, 3.3)
        self.assertEqual(status.amplitude_unit, "VPP")

    def test_set_square_duty_cycle_writes_percent(self):
        transport = FakeTransport()
        driver = DG4202Source(transport=transport, check_errors_after_ops=True)
        status = driver.set_square_duty_cycle(2, 25.0, check_errors=True)
        self.assertEqual(transport.writes[0], ":SOUR2:FUNC:SQU:DCYC 25")
        self.assertEqual(status.square_duty_cycle_percent, 25.0)


    def test_probe_arbitrary_queries_uses_query_only_candidates_and_reads_errors(self):
        transport = FakeTransport()
        driver = DG4202Source(transport=transport, check_errors_after_ops=True)

        results = driver.probe_arbitrary_queries(2)

        commands = [item.command for item in results]
        self.assertIn(":SOUR2:FUNC:USER?", commands)
        self.assertIn(":SOUR2:ARB:SRAT?", commands)
        self.assertTrue(all(command.endswith("?") for command in commands))
        accepted = {item.label: item.accepted for item in results}
        self.assertTrue(accepted["user_function"])
        self.assertTrue(accepted["arb_sample_rate"])
        self.assertFalse(accepted["source_data_catalog"])

    def test_probe_arbitrary_queries_rejects_non_query_candidate(self):
        driver = DG4202Source(transport=FakeTransport(), check_errors_after_ops=True)
        with self.assertRaises(Exception):
            driver.probe_arbitrary_queries(2, candidates=(("bad", ":SOUR{channel}:FUNC ARB"),))

    def test_set_square_duty_cycle_rejects_out_of_range_values(self):
        driver = DG4202Source(transport=FakeTransport(), check_errors_after_ops=True)
        with self.assertRaises(Exception):
            driver.set_square_duty_cycle(2, 100.0)


if __name__ == "__main__":
    unittest.main()
