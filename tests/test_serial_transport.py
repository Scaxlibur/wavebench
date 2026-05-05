import unittest

from wavebench.logging import CommandLogger
from wavebench.transport.serial_transport import SerialTransport


class FakeSerialSession:
    def __init__(self):
        self.writes = []
        self.closed = False

    def write(self, payload: bytes):
        self.writes.append(payload)

    def flush(self):
        pass

    def readline(self) -> bytes:
        return b"1.23e+00\n"

    def close(self):
        self.closed = True


class SerialTransportTests(unittest.TestCase):
    def test_write_appends_newline(self):
        session = FakeSerialSession()
        transport = SerialTransport("/dev/ttyUSB0", session, CommandLogger())
        transport.write("*IDN?")
        self.assertEqual(session.writes, [b"*IDN?\n"])

    def test_query_reads_one_ascii_line(self):
        session = FakeSerialSession()
        transport = SerialTransport("/dev/ttyUSB0", session, CommandLogger())
        self.assertEqual(transport.query("MEAS?"), "1.23e+00")
        self.assertEqual(session.writes, [b"MEAS?\n"])

    def test_query_float_list_uses_ascii_parser(self):
        session = FakeSerialSession()
        transport = SerialTransport("/dev/ttyUSB0", session, CommandLogger())
        self.assertEqual(transport.query_float_list("MEAS?"), [1.23])


if __name__ == "__main__":
    unittest.main()
