from pathlib import Path

from wavebench.config import (
    AutoscaleConfig,
    ConnectionConfig,
    OutputConfig,
    ScopeConfig,
    SourceConfig,
    WaveBenchConfig,
    WaveformConfig,
)
from wavebench.discovery import DiscoveryResult
from wavebench.doctor import doctor_records, has_doctor_errors


def make_config(*, source_resource="TCPIP::192.168.1.127::INSTR"):
    return WaveBenchConfig(
        connection=ConnectionConfig(
            backend="lan",
            resource="TCPIP::192.168.1.115::INSTR",
            timeout_ms=1000,
            opc_timeout_ms=30000,
        ),
        scope=ScopeConfig(
            driver="rtm2032",
            model_hint="RTM2032",
            default_channel=1,
            reset_before_run=False,
            check_errors=True,
        ),
        autoscale=AutoscaleConfig(wait_opc=True, check_errors=True),
        waveform=WaveformConfig(format="real", byte_order="lsbf", points="DEF"),
        output=OutputConfig(
            directory=Path("data/raw"),
            package_naming="timestamp_label",
            save_csv=True,
            save_npy=True,
            save_json=True,
            save_commands_log=True,
            save_screenshot=False,
        ),
        source_path=Path("wavebench.toml"),
        source=SourceConfig(
            driver="dg4202",
            resource=source_resource,
            default_channel=1,
            check_errors=True,
            ensure_fix_mode_on_set_frequency=True,
            settle_ms_after_set_frequency=0,
        ),
    )


def test_doctor_reports_configured_instruments_ok():
    idns = {
        "TCPIP::192.168.1.115::INSTR": "Rohde&Schwarz,RTM2032,123,06.010",
        "TCPIP::192.168.1.127::INSTR": "Rigol Technologies,DG4202,DG4E,00.01.14",
    }

    records = doctor_records(make_config(), idn_probe=lambda resource, timeout_ms: idns.get(resource))

    assert [record.severity for record in records] == ["ok", "ok"]
    assert not has_doctor_errors(records)


def test_doctor_reports_missing_resource_as_warning():
    records = doctor_records(make_config(source_resource=None), idn_probe=lambda resource, timeout_ms: "unused")

    source = next(record for record in records if record.target == "source")
    assert source.severity == "warning"
    assert "未配置" in source.message
    assert not has_doctor_errors(records)


def test_doctor_reports_unreachable_resource_as_error():
    records = doctor_records(make_config(), idn_probe=lambda resource, timeout_ms: None)

    assert has_doctor_errors(records)
    assert all(record.severity == "error" for record in records)


def test_doctor_reports_idn_mismatch_as_warning():
    records = doctor_records(make_config(), idn_probe=lambda resource, timeout_ms: "UNKNOWN,MODEL,0")

    assert [record.severity for record in records] == ["warning", "warning"]
    assert not has_doctor_errors(records)


def test_doctor_appends_candidate_for_unreachable_matching_idn():
    def discoverer(**kwargs):
        assert kwargs["subnet"] == "192.168.1.0/24"
        return [
            DiscoveryResult(
                address="192.168.1.225",
                port=None,
                protocol="visa",
                resource="TCPIP::192.168.1.225::INSTR",
                source="network",
                status="idn",
                idn="Rigol Technologies,DG4202,DG4E,00.01.14",
            ),
            DiscoveryResult(
                address="192.168.1.226",
                port=None,
                protocol="visa",
                resource="TCPIP::192.168.1.226::INSTR",
                source="network",
                status="idn",
                idn="Rohde&Schwarz,RTM2032,123,06.010",
            ),
        ]

    records = doctor_records(
        make_config(),
        idn_probe=lambda resource, timeout_ms: None,
        discover_subnet="192.168.1.0/24",
        discoverer=discoverer,
    )

    candidates = [record for record in records if record.severity == "candidate"]
    assert [(record.target, record.resource) for record in candidates] == [
        ("scope", "TCPIP::192.168.1.226::INSTR"),
        ("source", "TCPIP::192.168.1.225::INSTR"),
    ]


def test_doctor_does_not_suggest_candidate_for_healthy_target():
    records = doctor_records(
        make_config(),
        idn_probe=lambda resource, timeout_ms: "Rigol Technologies,DG4202,DG4E,00.01.14",
        discover_subnet="192.168.1.0/24",
        discoverer=lambda **kwargs: [
            DiscoveryResult(
                address="192.168.1.225",
                port=None,
                protocol="visa",
                resource="TCPIP::192.168.1.225::INSTR",
                source="network",
                status="idn",
                idn="Rigol Technologies,DG4202,DG4E,00.01.14",
            )
        ],
    )

    assert not [record for record in records if record.severity == "candidate"]
