import unittest

from wavebench.drivers.rtm2032 import RTM2032Scope, parse_waveform_header
from wavebench.errors import DataError


class FakeTransport:
    def __init__(self, responses):
        self.responses = responses
        self.queries = []
        self.writes = []

    def write(self, command):
        self.writes.append(command)

    def query(self, command):
        self.queries.append(command)
        return self.responses[command]

    def query_bin_block(self, command):
        self.queries.append(command)
        return self.responses[command]

    def close(self):
        pass


class WaveformHeaderTests(unittest.TestCase):
    def test_parse_waveform_header_real_format(self):
        header = parse_waveform_header("-1.0000E-03,9.9980E-04,10000,1")
        self.assertAlmostEqual(header.x_start, -1.0e-3)
        self.assertAlmostEqual(header.x_stop, 9.9980e-4)
        self.assertEqual(header.points, 10000)
        self.assertEqual(header.segment, 1)
        self.assertAlmostEqual(header.x_increment, 2.0e-7)

    def test_parse_waveform_header_rejects_invalid_response(self):
        with self.assertRaises(DataError):
            parse_waveform_header("not,a,header")

    def test_scope_channel_coupling_queries_configured_channel(self):
        transport = FakeTransport({"CHAN1:COUP?": " dcl\n"})
        scope = RTM2032Scope(transport=transport)

        self.assertEqual(scope.channel_coupling(1), "DCL")
        self.assertEqual(transport.queries, ["CHAN1:COUP?"])

    def test_scope_channel_coupling_rejects_invalid_channel(self):
        scope = RTM2032Scope(transport=FakeTransport({}))
        with self.assertRaises(DataError):
            scope.channel_coupling(0)

    def test_scope_screenshot_png_queries_hardcopy_data(self):
        transport = FakeTransport({"HCOP:DATA?": b"\x89PNG\r\n\x1a\nrest"})
        scope = RTM2032Scope(transport=transport)

        data = scope.screenshot_png()

        self.assertEqual(data[:8], b"\x89PNG\r\n\x1a\n")
        self.assertEqual(
            transport.writes,
            ["HCOP:LANG PNG", "HCOP:COL:SCH COL", "HCOP:MENU OFF"],
        )
        self.assertEqual(transport.queries, ["HCOP:DATA?"])

    def test_scope_screenshot_png_rejects_non_png(self):
        scope = RTM2032Scope(transport=FakeTransport({"HCOP:DATA?": b"not png"}))
        with self.assertRaises(DataError):
            scope.screenshot_png()


if __name__ == "__main__":
    unittest.main()

class VerticalScaleTests(unittest.TestCase):
    def test_capture_sets_vertical_scale_before_single(self):
        class Transport(FakeTransport):
            def __init__(self):
                super().__init__({"CHAN1:DATA:HEAD?": "0,1,2,1"})
            def query_float_list(self, command):
                self.queries.append(command)
                return [0.0, 1.0]
            def query_opc(self):
                self.queries.append("*OPC?")
                return "1"
        transport = Transport()
        scope = RTM2032Scope(transport=transport)

        scope.capture_waveform(channel=1, points="DEF", check_errors=False, vertical_scale_v_per_div=0.2)

        self.assertIn("CHAN1:SCAL 0.2", transport.writes)
        self.assertIn("CHAN1:POS 0", transport.writes)
        self.assertLess(transport.writes.index("CHAN1:SCAL 0.2"), transport.writes.index("SINGle"))
