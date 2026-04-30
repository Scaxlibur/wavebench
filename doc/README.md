# WaveBench 文档总览

WaveBench 是面向电赛调试场景的轻量 Python 自动测量台。当前阶段聚焦 R&S RTM2032 示波器的 LAN 远程采集；后续再扩展到普源信号发生器和自动测量流程。

## 当前阶段

```text
阶段 1：示波器只读采集 + 显式 Autoscale
```

目标：

```text
可靠地远程执行 Auto，读取 RTM2032 当前波形，并保存 CSV / NPY / metadata / commands.log。
```

当前已经支持单次采集、失败采集包、数据质量摘要、采集窗口控制和基础输出控制。正式扫频流程、信号发生器控制、GUI 和自动报告仍不属于 MVP-1。

## 文档索引

### 项目设计

- [WaveBench_项目边界.md](./WaveBench_项目边界.md)
  - 定义项目定位、阶段划分、当前不做什么。
- [WaveBench_CLI形态.md](./WaveBench_CLI形态.md)
  - 定义交互式 / 非交互式 CLI、LAN-only 约束、第一阶段命令。
- [WaveBench_设备抽象层.md](./WaveBench_设备抽象层.md)
  - 定义 transport、device、service、data/export 分层，以及后续接入信号发生器的边界。
- [WaveBench_数据输出格式.md](./WaveBench_数据输出格式.md)
  - 定义采集包目录、CSV / NPY / JSON / commands.log 输出格式。
- [WaveBench_配置文件格式.md](./WaveBench_配置文件格式.md)
  - 定义 TOML 本机配置、查找顺序、参数优先级和 example 配置。
- [WaveBench_错误处理和日志策略.md](./WaveBench_错误处理和日志策略.md)
  - 定义错误分类、退出码、终端日志、commands.log 和 failed 采集包策略。
- [RTM2032_MVP命令确认表.md](./RTM2032_MVP命令确认表.md)
  - 整理 MVP-1 要使用的 SCPI 命令、用途、注意事项和推荐命令序列。
- [WaveBench_示波器采集模块设计草案.md](./WaveBench_示波器采集模块设计草案.md)
  - 早期开发思路草案，包含资料检索、模块设想、风险分析。

### 设备资料

- [WaveBench_DP800电源只读接入设计.md](./WaveBench_DP800电源只读接入设计.md)
  - DP800 系列电源第一阶段只读接入设计：`power idn/status`，不写输出。

- [RTM2000_VISA_SCPI_手册摘录.md](./RTM2000_VISA_SCPI_手册摘录.md)
  - RTM2000 用户手册中 VISA / SCPI 相关摘录，作为命令确认依据。

## 进度速览

### 已完成

- [x] 初始化 Python 项目骨架与本机 TOML 配置。
- [x] 通过 LAN VISA 接通 RTM2032：`TCPIP::192.168.123.2::INSTR`。
- [x] 实机打通 `scope idn`、`scope errors`、`scope autoscale`。
- [x] 实机打通 `scope fetch --channel 1`。
- [x] 实机打通 `scope capture --channel 1 --label <label>`。
- [x] 实机打通 `scope capture --channel 2 --label <label>`。
- [x] 支持 `scope capture --channel 1 --channel 2` 逐通道采集。
- [x] `scope capture` 默认执行 `SINGle + *OPC?` 后读取波形。
- [x] 采集包输出：CSV、NPY、`metadata.json`、`commands.log`。
- [x] 失败采集包：`metadata.partial.json`、`error.txt`、`commands.log`。
- [x] 数据质量摘要：Vpp、均值、RMS、频率估计、周期数估计、质量提示。
- [x] 输出控制：`--no-csv`、`--no-npy`。
- [x] 点数范围控制：`--points def|max|dmax`。
- [x] 采集时窗控制：`--time-range <seconds>`。
- [x] 自动窗口：`--window-frequency <Hz> --target-cycles <N>`。
- [x] 预期频率校验：`--expect-frequency <Hz> --frequency-tolerance <ratio>`。

### 当前实机状态

2026-04-29 已在 RTM2032 上完成采集闭环：

```text
Windows Ethernet -> RTM2032 192.168.123.2 -> VISA/SCPI
*IDN? -> AUToscale -> fetch/capture -> acquisition package
```

已验证数据样例：

```text
1 kHz square: 10000 samples, dt=200 ns, voltage≈-0.5..0.64 V
1 kHz sine  : 10000000 samples with DMAX, Vpp≈5.12 V, freq≈999.997 Hz
5 kHz sine  : Vpp≈5.12 V, freq≈5001.36 Hz
sweep smoke : 1k→10k linear sweep, auto 10 ms window, no low-cycle warning
formal source->scope loop: source set-freq 1 kHz, scope verified ≈1 kHz
real square-wave metrics: 100 kHz square, duty≈0.5, rise/fall≈32 ns
private point-sweep flow validated on 1 kHz / 2 kHz / 5 kHz / 10 kHz
```

已确认下一阶段信号源目标设备：

```text
RIGOL DG4202 @ 192.168.123.3
PyVISA + NI-VISA verified
resource = TCPIP::192.168.123.3::INSTR
fixed-mode write/readback on DG4202 channel output verified
source set-frequency settle delay configurable via settle_ms_after_set_frequency
```

已确认电源目标设备：

```text
RIGOL DP832A @ 192.168.123.4
resource = TCPIP::192.168.123.4::INSTR
power idn/status read-only smoke verified
CH1 manual setup: output=ON, mode=CV, set=5.0V/0.1A, measured≈5.0115V
```

### 推荐实机命令

信号发生器最小探测：

```bash
python -m wavebench source idn --config wavebench.toml
python -m wavebench source status --config wavebench.toml --channel 2
```

电源只读探测：

```bash
python -m wavebench power idn --config wavebench.toml --resource TCPIP::192.168.123.4::INSTR
python -m wavebench power status --config wavebench.toml --resource TCPIP::192.168.123.4::INSTR --channel 1
```

最小可写控制：

```bash
python -m wavebench source set-freq --config wavebench.toml --channel 2 1000
python -m wavebench source output --config wavebench.toml --channel 2 on
```


快速单次采集（不写 CSV）：

```bash
python -m wavebench scope capture --config wavebench.toml --channel 1 `
  --label smoke `
  --points def `
  --no-csv
```

按最低频率自动设置窗口，例如扫频最低 1 kHz、目标 10 个周期：

```bash
python -m wavebench scope capture --config wavebench.toml --channel 1 `
  --label sweep_smoke `
  --points def `
  --window-frequency 1000 `
  --target-cycles 10 `
  --no-csv
```

固定频率校验，例如期望 500 Hz、容差 5%：

```bash
python -m wavebench scope capture --config wavebench.toml --channel 1 `
  --label sine_500hz_check `
  --points def `
  --window-frequency 500 `
  --target-cycles 10 `
  --expect-frequency 500 `
  --frequency-tolerance 0.05 `
  --no-csv
```



多通道逐通道采集，例如 CH1 + CH2：

```bash
python -m wavebench scope capture --config wavebench.toml   --channel 1 --channel 2   --label dual_smoke   --points def   --window-frequency 1000   --target-cycles 10   --no-csv
```

多通道模式会在同一个采集包中写入 `ch1.npy`、`ch2.npy` 和统一的 `metadata.json`。当前语义是 `sequential_per_channel`：每个通道各自执行一次单次采集，metadata 中分别记录各自的 header 和 summary，不判断两个通道是否应当一致。

### 下一步

- [x] 明确多通道策略：`--channel` 可重复，按通道逐个触发采集；每个通道独立质量摘要，不假设信号相同。
- [x] 将 DG4202 整理进正式 WaveBench 架构最小骨架：`source idn/status/set-freq/output`。
- [x] 为离散扫点流程增加 source-mode 防呆：在固定频点实验前明确检查 `FREQ:MODE`，必要时从 `SWE` 切到 `FIX`。
- [x] 正式最小闭环已验证：`source set-freq` -> `scope capture`。
- [ ] 后续将离散扫点测试封装成统一流程命令或脚本。私有验证层已跑通离散频点闭环。
- [x] 接入 DP800 电源只读命令：`power idn/status`。
- [ ] 后续实现电源电压/电流设置命令，但必须显式调用，不允许 capture/sweep 默认修改电源。
- [ ] 后续再考虑截图、YAML 实验流程。

## 当前关键约束

- 当前只支持 LAN 连接。
- VISA 资源格式暂定：`TCPIP::<instrument-ip>::INSTR`。
- 本机配置使用 `wavebench.toml`，示例配置使用 `wavebench.example.toml`。
- `wavebench.toml` 不进 git。
- 第一阶段默认不 `*RST`。
- `auto / autoscale` 是显式命令，会改变水平、垂直和触发设置。
- `fetch` / `capture` 默认不偷偷调用 autoscale。
- `fetch` 与 `capture` 需要分开：
  - `fetch`：读取当前波形；
  - `capture`：触发单次采集后读取波形。
- 交互式和非交互式入口必须共用底层逻辑。
- CLI / shell 不直接写 SCPI；SCPI 集中在设备驱动层。
- Service 层表达实验动作，不表达设备命令。
- 每次采集生成独立采集包。
- 第一阶段输出：每通道 CSV、每通道 NPY、metadata.json、commands.log；可用 `--no-csv` / `--no-npy` 关闭大文件输出。
- 连接成功后失败保留 `*_failed` 采集包。
- `--points` 只接受 RTM2032 支持的 `def|max|dmax`，不接受任意数字点数。
- `--time-range` 会设置 RTM2032 的 `TIMebase:RANGe`，改变水平时窗。
- `--window-frequency` 只用于自动计算窗口；`--expect-frequency` 才用于频率一致性校验。
- `WaveBench_sweep状态恢复设计.md`：离散扫点前后的信号源状态保存与恢复设计。
