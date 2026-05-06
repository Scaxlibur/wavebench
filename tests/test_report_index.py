from pathlib import Path
import csv
import json
import unittest
from tempfile import TemporaryDirectory

from wavebench.report.index import build_manifest_entry, write_report_index


class ReportIndexTests(unittest.TestCase):
    def _make_run(self, root: Path, name: str, *, status: str = 'ok') -> Path:
        run_dir = root / name
        run_dir.mkdir(parents=True)
        (run_dir / 'summary.csv').write_text('index,kind,status\n0,scope.capture,ok\n', encoding='utf-8')
        (run_dir / 'report.html').write_text('<html></html>', encoding='utf-8')
        run = {
            'status': status,
            'experiment': {'name': name, 'label': name},
            'plan': f'plans/{name}.toml',
            'steps': [
                {
                    'index': 0,
                    'kind': 'scope.capture',
                    'status': 'ok',
                    'artifact': {
                        'quality': {
                            'summary': {
                                'frequency_estimate_hz': 1000.5,
                                'voltage_vpp_v': 1.0,
                            }
                        },
                        'expect': {'status': 'ok'},
                        'expect_fft': {'status': 'ok'},
                    },
                },
                {
                    'index': 1,
                    'kind': 'dmm.read',
                    'status': 'ok',
                    'artifact': {
                        'dmm_reading': {'function': 'acv', 'value': 0.353, 'unit': 'V'},
                        'expect': {'status': 'ok'},
                    },
                },
            ],
            'restore': {'status': 'ok', 'source_channels': [1, 2]},
        }
        (run_dir / 'run.json').write_text(json.dumps(run, indent=2), encoding='utf-8')
        return run_dir

    def test_build_manifest_entry_extracts_primary_metrics(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = self._make_run(root, 'demo_run')
            entry = build_manifest_entry(run_dir)
            self.assertEqual(entry['status'], 'ok')
            self.assertEqual(entry['experiment_label'], 'demo_run')
            self.assertEqual(entry['restore_source_channels'], [1, 2])
            self.assertEqual(entry['primary_scope_frequency_hz'], 1000.5)
            self.assertEqual(entry['primary_scope_vpp_v'], 1.0)
            self.assertEqual(entry['primary_dmm_value'], 0.353)
            self.assertEqual(entry['primary_dmm_function'], 'acv')
            self.assertEqual(entry['expect_failures'], 0)
            self.assertEqual(entry['expect_fft_failures'], 0)


    def test_build_manifest_entry_falls_back_to_legacy_single_restore_channel(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_dir = self._make_run(root, 'legacy_restore')
            run = json.loads((run_dir / 'run.json').read_text(encoding='utf-8'))
            run['restore'] = {'status': 'ok', 'source_channel': 2}
            (run_dir / 'run.json').write_text(json.dumps(run, indent=2), encoding='utf-8')
            entry = build_manifest_entry(run_dir)
            self.assertEqual(entry['restore_source_channels'], [2])

    def test_write_report_index_writes_json_and_csv(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            run_a = self._make_run(root, 'run_a')
            run_b = self._make_run(root, 'run_b', status='failed')
            out = root / 'out'
            result = write_report_index([run_a, run_b], out)
            self.assertTrue(result.manifest_json_path.exists())
            self.assertTrue(result.manifest_csv_path.exists())
            self.assertTrue(result.index_html_path.exists())
            html = result.index_html_path.read_text(encoding='utf-8')
            self.assertIn('WaveBench report index', html)
            self.assertIn('run_a', html)
            manifest = json.loads(result.manifest_json_path.read_text(encoding='utf-8'))
            self.assertEqual(manifest['count'], 2)
            self.assertEqual(len(manifest['runs']), 2)
            with result.manifest_csv_path.open(newline='', encoding='utf-8') as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['restore_source_channels'], '1|2')


if __name__ == '__main__':
    unittest.main()
