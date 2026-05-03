
import unittest

from wavebench.logging import CommandLogger
from wavebench.transport.pyvisa_transport import PyVisaTransport


class FakePyVisaSession:
    def __init__(self):
        self.queries = []
        self.raw_writes = []
        self.reads = []

    def query(self, command: str) -> str:
        self.queries.append(command)
        if command == "VALUES?":
            return "1, 2.5, 3"
        if command == "*OPC?":
            return "1"
        if command == "EMPTY_THEN_READ?":
            return ""
        return ""

    def read(self) -> str:
        self.reads.append("read")
        return "DELAYED"

    def write_raw(self, command: bytes) -> None:
        self.raw_writes.append(command)

    def query_binary_values(self, command: str, datatype: str = "B", container=list):
        self.queries.append(command)
        if datatype == "B":
            return container([1, 2, 3])
        raise RuntimeError("binary float path unavailable")

    def close(self) -> None:
        pass


class FakeResourceManager:
    def close(self) -> None:
        pass


class PyVisaTransportTests(unittest.TestCase):
    def test_query_float_list_falls_back_to_ascii_values(self):
        transport = PyVisaTransport("TCPIP::x::INSTR", FakeResourceManager(), FakePyVisaSession(), CommandLogger())

        self.assertEqual(transport.query_float_list("VALUES?"), [1.0, 2.5, 3.0])

    def test_query_reads_again_after_empty_socket_response(self):
        session = FakePyVisaSession()
        transport = PyVisaTransport("TCPIP::x::INSTR", FakeResourceManager(), session, CommandLogger())

        self.assertEqual(transport.query("EMPTY_THEN_READ?"), "DELAYED")
        self.assertEqual(session.reads, ["read"])

    def test_query_bin_block_and_opc(self):
        transport = PyVisaTransport("TCPIP::x::INSTR", FakeResourceManager(), FakePyVisaSession(), CommandLogger())

        self.assertEqual(transport.query_bin_block("DATA?"), b"\x01\x02\x03")
        self.assertEqual(transport.query_opc(), "1")


if __name__ == "__main__":
    unittest.main()
