import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from wavebench.config import (
    AutoscaleConfig,
    ConnectionConfig,
    OutputConfig,
    ScopeConfig,
    SourceConfig,
    WaveBenchConfig,
    WaveformConfig,
)
from wavebench.drivers.dg4202 import SourceStatus
from wavebench.errors import InstrumentError
from wavebench.logging import CommandLogger
from wavebench.services.sweep_service import SweepService


def make_config(tmp: str) -> WaveBenchConfig:
    return WaveBenchConfig(
        connection=ConnectionConfig(backend='lan', resource='TCPIP::scope::INSTR', timeout_ms=1000, opc_timeout_ms=1000),
        scope=ScopeConfig(driver='rtm2032', model_hint=None, default_channel=1, reset_before_run=False, check_errors=True),
        autoscale=AutoscaleConfig(wait_opc=True, check_errors=True),
        waveform=WaveformConfig(format='real', byte_order='lsbf', points='DEF'),
        output=OutputConfig(
            directory=Path(tmp) / 'data' / 'raw',
            package_naming='timestamp_label',
            save_csv=False,
            save_npy=True,
            save_json=True,
            save_commands_log=True,
            save_screenshot=False,
        ),
        source_path=Path(tmp) / 'wavebench.toml',
        source=SourceConfig(
            driver='dg4202',
            resource='TCPIP::source::INSTR',
            default_channel=2,
            check_errors=True,
            ensure_fix_mode_on_set_frequency=True,
            settle_ms_after_set_frequency=0,
        ),
    )


class SweepServiceTests(unittest.TestCase):
    def test_discrete_sweep_rejects_source_output_off(self):
        with TemporaryDirectory() as tmp:
            config = make_config(tmp)
            service = SweepService(config=config, logger=CommandLogger())
            off_status = SourceStatus(
                channel=2,
                output='OFF',
                function='SIN',
                frequency_hz=1000.0,
                amplitude=5.0,
                amplitude_unit='VPP',
                offset_v=0.0,
                phase_deg=0.0,
                frequency_mode='FIX',
                sweep_enabled='OFF',
                apply_raw=None,
            )
            with patch('wavebench.services.sweep_service.SourceService') as source_cls:
                source_cls.return_value.set_frequency.return_value = off_status
                with self.assertRaisesRegex(InstrumentError, 'output is OFF'):
                    service.run_discrete(
                        frequencies_hz=[1000.0],
                        source_channel=2,
                        scope_channel=1,
                        target_cycles=10.0,
                        frequency_tolerance=0.05,
                        label='test',
                        save_csv=False,
                        save_npy=True,
                    )


if __name__ == '__main__':
    unittest.main()
