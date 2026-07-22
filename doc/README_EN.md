# WaveBench Documentation

[中文文档](README.md) | English

WaveBench is a lightweight Python measurement bench for explicit, reproducible control of laboratory instruments. It currently covers oscilloscope capture, signal-generator and power-supply control, digital-multimeter reads, multi-instrument run plans, offline reports, and trusted executable instrument plugins.

The WaveBench distribution includes built-in drivers for the RTM2000/RTM2032, DS1104Z/DS1000Z, DG4000/DG4202, DP800, and DM3000/DM3058 families. First use does not require an external plugin: copy the example configuration and set the real instrument resource. External plugins are explicitly selected optional upgrades or extensions and do not replace the built-in short names used by the example configuration.

> Warning: WaveBench communicates with real laboratory equipment. Review the active configuration, wiring, voltage/current limits, input impedance, and output state before running any command that can change an instrument.

## Start here

- [Project boundaries](project/WaveBench_项目边界.md)
- [Configuration format](project/WaveBench_配置文件格式.md)
- [Run-plan guide](project/WaveBench_run_plan_使用指南.md)
- [Data and artifact formats](project/WaveBench_数据输出格式.md)
- [Error handling and command logs](project/WaveBench_错误处理和日志策略.md)
- [Executable instrument plugin development](project/WaveBench_插件开发指南.md)
- [Sweep analyzer public contract](project/WaveBench_sweep_analyzer_contract_EN.md)
- [Installing and managing instrument plugins](project/WaveBench_可安装仪器插件.md)

## Managed local plugins

WaveBench treats executable Python plugins as trusted code, not as sandboxed extensions. The managed lifecycle accepts only an explicitly supplied local source directory or wheel, requires the current interpreter to be a virtual environment, does not download packages, installs with dependencies disabled, and never edits `wavebench.toml`.

```bash
python -m wavebench plugin package check <folder-or-wheel>
python -m wavebench plugin install <folder-or-wheel> --dry-run
python -m wavebench plugin install <folder-or-wheel>
python -m wavebench plugin installed
python -m wavebench plugin info <canonical-driver-id> --installed
python -m wavebench plugin upgrade <folder-or-wheel> --dry-run
python -m wavebench plugin downgrade <folder-or-wheel> --dry-run
python -m wavebench plugin remove <canonical-driver-id> --dry-run
python -m wavebench plugin recover
```

Source-directory inspection executes the package's declared build backend in a subprocess, including during dry-run. Wheel inspection is static. Installation, replacement, and removal use an environment lock, an atomic ledger, a write-ahead transaction journal, cached wheel hashes, post-install descriptor validation, and best-effort rollback. Automatic recovery is deliberately limited to states that can be proven to match the exact previous or target installation.

The local marketplace index remains read-only. It does not download or install plugins.

Executable plugins use canonical IDs and cannot define aliases. Built-in IDs are protected except for narrowly allowlisted migration slots that bind one canonical ID to one distribution. For the DG4000 migration slot, `wavebench-rigol-dg4000` may provide `rigol.dg4202`; the short `dg4202` alias always selects the built-in fallback, and uninstalling the external distribution restores the built-in canonical implementation. DG4000 source plugins may import the stable `DG4000DacBlock` and `DG4000ByteOrder` types from `wavebench.instruments`; waveform loading, normalization, DAC14 encoding, services, and safety policy remain core responsibilities.

## Safety defaults

- No implicit instrument reset.
- No hidden output enable/disable.
- No automatic change to oscilloscope input impedance.
- No raw SCPI surface in the HTTP MCP service.
- No third-party plugin import during ordinary metadata listing.
- No system-Python plugin installation, network dependency resolution, or unmanaged-distribution takeover.

Most detailed design documents are currently maintained in Chinese. Commands, identifiers, schemas, and examples are kept stable across languages.
