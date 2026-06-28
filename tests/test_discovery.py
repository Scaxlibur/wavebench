import unittest

from wavebench.discovery import PortProbe, discover_network, parse_discovery_ports
from wavebench.errors import ConfigError


class DiscoveryTests(unittest.TestCase):
    def test_parse_discovery_ports_deduplicates_and_validates(self):
        self.assertEqual(parse_discovery_ports("5025, 5555,5025"), (5025, 5555))
        with self.assertRaisesRegex(ConfigError, "发现端口无效"):
            parse_discovery_ports("5025,nope")
        with self.assertRaisesRegex(ConfigError, "1..65535"):
            parse_discovery_ports("0")

    def test_discover_network_reports_scpi_idn_and_vxi11_candidate(self):
        def tcp_probe(address, port, timeout_s):
            return address == "192.168.1.11" and port == 111

        def scpi_probe(address, port, timeout_s):
            if address == "192.168.1.10" and port == 5025:
                return PortProbe(open=True, idn="RIGOL TECHNOLOGIES,DG4202,DG4E000000000,00.01.18")
            return PortProbe(open=False)

        results = discover_network(
            "192.168.1.8/29",
            ports=(5025, 111),
            timeout_ms=1,
            workers=2,
            query_idn=True,
            tcp_probe=tcp_probe,
            scpi_probe=scpi_probe,
        )

        resources = [item.resource for item in results]
        self.assertIn("TCPIP::192.168.1.10::5025::SOCKET", resources)
        self.assertIn("TCPIP::192.168.1.11::INSTR", resources)
        idn_result = next(item for item in results if item.address == "192.168.1.10")
        self.assertEqual(idn_result.status, "idn")
        self.assertIn("DG4202", idn_result.idn)

    def test_discover_network_idn_only_hides_open_only_ports(self):
        def scpi_probe(address, port, timeout_s):
            return PortProbe(open=True, idn=None, note="idn timeout")

        results = discover_network(
            "192.168.1.10/32",
            ports=(5025,),
            timeout_ms=1,
            query_idn=True,
            include_open=False,
            scpi_probe=scpi_probe,
        )
        self.assertEqual(results, [])

    def test_discover_network_refuses_large_subnet_by_default(self):
        with self.assertRaisesRegex(ConfigError, "raise --max-hosts"):
            discover_network("192.168.0.0/16", timeout_ms=1)


if __name__ == "__main__":
    unittest.main()
