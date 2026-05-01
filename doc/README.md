# WaveBench 文档总览

WaveBench 是面向电赛调试场景的轻量 Python 自动测量台。当前阶段支持 R&S RTM2032 示波器采集、RIGOL DG4202 信号源控制、RIGOL DP800 系列电源控制，并坚持显式命令与可验证的小步实验流程。

## 当前阶段

```text
阶段 1：LAN 仪器显式控制 + 可复现实验采集
```

目标：

```text
可靠地远程读取示波器波形、显式控制信号源和电源，并保存 CSV / NPY / metadata / commands.log。
```

当前已经支持单次/多通道采集、失败采集包、数据质量摘要、采集窗口控制、DG4202 离散扫频与占空比控制、DP800 电源显式控制，以及多仪器 run plan 执行。run plan 的 `scope.capture` 可选择质量检查，并在质量警告时按 `[quality].auto_recover_attempts` 触发多次显式 autoscale 重采；若多次采集指标稳定，可标记为 `ok_by_consistency`。`[steps.expect]` 可对采集指标设置 min/max 断言，断言失败会把实验标记为 failed。GUI 和隐式实验流程仍不属于当前阶段；v0.2 已开始加入离线包读取、`capture inspect` 和静态 `run report`；报告会汇总每次采集的频率、Vpp、RMS、均值、duty、rise/fall 等信号分析指标。这些命令只读已有文件，不连接仪器。

## 文档索引

### 项目设计

- [WaveBench_项目边界.md](./project/WaveBench_项目边界.md)
  - 定义项目定位、阶段划分、当前不做什么。
- [WaveBench_CLI形态.md](./project/WaveBench_CLI形态.md)
  - 定义交互式 / 非交互式 CLI、LAN-only 约束、第一阶段命令。
- [WaveBench_设备抽象层.md](./project/WaveBench_设备抽象层.md)
  - 定义 transport、device、service、data/export 分层，以及后续接入信号发生器的边界。
- [WaveBench_数据输出格式.md](./project/WaveBench_数据输出格式.md)
  - 定义采集包目录、CSV / NPY / JSON / commands.log 输出格式。
- [WaveBench_配置文件格式.md](./project/WaveBench_配置文件格式.md)
  - 定义 TOML 本机配置、查找顺序、参数优先级和 example 配置。
- [WaveBench_错误处理和日志策略.md](./project/WaveBench_错误处理和日志策略.md)
  - 定义错误分类、退出码、终端日志、commands.log 和 failed 采集包策略。
- [RTM2032_MVP命令确认表.md](./instruments/RTM2032_MVP命令确认表.md)
  - 整理 MVP-1 要使用的 SCPI 命令、用途、注意事项和推荐命令序列。
- [WaveBench_示波器采集模块设计草案.md](./project/WaveBench_示波器采集模块设计草案.md)
  - 早期开发思路草案，包含资料检索、模块设想、风险分析。

### 设备资料

- [WaveBench_DP800电源只读接入设计.md](./project/WaveBench_DP800电源只读接入设计.md)
  - DP800 系列电源第一阶段只读接入设计：`power idn/status`，不写输出。
- [WaveBench_DP800电源显式设置设计.md](./project/WaveBench_DP800电源显式设置设计.md)
  - DP800 电压/电流限值显式设置设计：`power set`，不控制 output。
- [WaveBench_DP800电源输出控制设计.md](./project/WaveBench_DP800电源输出控制设计.md)
  - DP800 输出开关显式控制设计：`power output on|off`，不设置电压/电流。
- [WaveBench_多仪器协同流程设计.md](./project/WaveBench_多仪器协同流程设计.md)
  - 多仪器实验流程层设计：显式组合 power/source/scope 动作，先设计 plan/check，再执行。
- [WaveBench_run_plan_使用指南.md](./project/WaveBench_run_plan_使用指南.md)
  - 面向 plan 作者的实用说明：`run schema`、`run check` 常见报错、`run.json` / `summary.csv` 输出字段。
- [WaveBench_v0.1_收口清单.md](./project/WaveBench_v0.1_收口清单.md)
  - 第一个 release 前的能力边界、暂缓事项、门禁和发布步骤。
- [WaveBench_v0.2_路线图.md](./project/WaveBench_v0.2_路线图.md)
  - v0.2 的解耦优先路线：包读取 API、离线报告、capture inspect 与截图保存边界。
- [WaveBench_v0.2_收口清单.md](./project/WaveBench_v0.2_收口清单.md)
  - v0.2 release 前的能力边界、门禁、实机 smoke 和 release notes 入口。
- [WaveBench_v0.3_路线图.md](./project/WaveBench_v0.3_路线图.md)
  - v0.3 的报告可视化路线：summary card、expected vs measured、波形预览、report manifest 和离线 FFT inspect。
- [WaveBench_v0.3_收口清单.md](./project/WaveBench_v0.3_收口清单.md)
  - v0.3 release 前的完成情况、门禁、暂缓事项和 release notes 入口。
- [WaveBench_v0.4_路线图.md](./project/WaveBench_v0.4_路线图.md)
  - v0.4 的 DG4202 任意波形输出 MVP 路线：先确认 SCPI，再做离线 builder、driver upload 和示波器闭环。
- [WaveBench_v0.4_收口清单.md](./project/WaveBench_v0.4_收口清单.md)
  - v0.4 release 前的能力边界、门禁、实机闭环证据和 release notes 入口。
- [WaveBench_v0.4_闭环验证记录.md](./project/WaveBench_v0.4_闭环验证记录.md)
  - DG4202 CH1 到 RTM2032 CH1 的基础波形与任意波闭环验证记录；FFT 验收优先于当前时域频率估计。
- [DG4202_任意波形命令确认表.md](./instruments/DG4202_任意波形命令确认表.md)
  - v0.4 前置命令确认表；`DATA:DAC VOLATILE` 上传与 little-endian DAC block 已经实机确认。

- [RTM2000_VISA_SCPI_手册摘录.md](./instruments/RTM2000_VISA_SCPI_手册摘录.md)
  - RTM2000 用户手册中 VISA / SCPI 相关摘录，作为命令确认依据。

- [DG4000_ProgrammingGuide_CN.md](./instruments/DG4000_ProgrammingGuide_CN.md)
  - RIGOL DG4000 系列编程手册 Markdown 版，作为 DG4202 任意波形 SCPI 的主要依据。
- [普源DP800系列电源_编程手册.md](./instruments/普源DP800系列电源_编程手册.md)
  - RIGOL DP800 系列编程手册 Markdown 版，作为电源 SCPI 的主要依据。

## 进度速览

### 已完成

- [x] 初始化 Python 项目骨架与本机 TOML 配置。
- [x] 通过 LAN VISA 接通 RTM2032：`TCPIP::<rtm2032-ip>::INSTR`。
- [x] 实机打通 `scope idn`、`scope errors`、`scope autoscale`。
- [x] 实机打通 `scope fetch --channel 1`。
- [x] 实机打通 `scope capture --channel 1 --label <label>`。
- [x] 实机打通 `scope capture --channel 2 --label <label>`。
- [x] 支持 `scope capture --channel 1 --channel 2` 逐通道采集。
- [x] `scope capture` 默认执行 `SINGle + *OPC?` 后读取波形。
- [x] 采集包输出：CSV、NPY、`metadata.json`、`commands.log`。
- [x] 失败采集包：`metadata.partial.json`、`error.txt`、`commands.log`。
- [x] 数据质量摘要：Vpp、均值、RMS、频率估计、周期数估计、每周期点数、质量提示。
- [x] 输出控制：`--no-csv`、`--no-npy`。
- [x] 点数范围控制：`--points def|max|dmax`。
- [x] 采集时窗控制：`--time-range <seconds>`。
- [x] 自动窗口：`--window-frequency <Hz> --target-cycles <N>`。
- [x] 预期频率校验：`--expect-frequency <Hz> --frequency-tolerance <ratio>`。

### 当前实机状态

2026-04-29 已在 RTM2032 上完成采集闭环：

```text
Windows Ethernet -> RTM2032 <rtm2032-ip> -> VISA/SCPI
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
RIGOL DG4202 @ <dg4202-ip>
PyVISA + NI-VISA verified
resource = TCPIP::<dg4202-ip>::INSTR
fixed-mode write/readback on DG4202 channel output verified
source set-frequency settle delay configurable via settle_ms_after_set_frequency
square duty-cycle command verified with :SOUR2:FUNC:SQU:DCYC
```

已确认电源目标设备：

```text
RIGOL DP832A @ <dp800-ip>
resource = TCPIP::<dp800-ip>::INSTR
power idn/status read-only smoke verified
CH1 output/set/status smoke verified
power set smoke: 5.0V -> 3.3V -> 5.0V verified with RTM2032 CH2
power output smoke: ON -> OFF -> ON verified with RTM2032 CH2
```

已验证多仪器 run plan：

```text
plan = plans/dp800_scope_probe_voltage_steps.toml
run  = data/runs/20260430_150454_dp800_scope_probe_voltage_capture
steps = 6, status = ok
sequence = scope guard -> 5 V capture -> 3.3 V set/capture -> 5 V restore/capture
scope CH2 mean ≈ 4.8826 V -> 3.1976 V -> 4.8842 V

plan = plans/dg4202_duty_10k_power_ch2_check.toml
run  = data/runs/20260430_154307_dg4202_duty_10k_power_ch2_check
steps = 18, status = ok, restore = ok
source CH2 duty request/readback = 25% / 50% / 75%
scope CH1 measured duty = 0.25 / 0.50 / 0.75 at 10 kHz
source snapshot restored = ON / SIN / 5000 Hz / 5 Vpp / duty 50%
scope CH2 power mean ≈ 4.8919 V -> 4.8876 V
```

### 推荐实机命令

信号发生器最小探测：

```bash
python -m wavebench source idn --config wavebench.toml
python -m wavebench source status --config wavebench.toml --channel 2
```

电源探测与显式控制：

```bash
python -m wavebench power idn --config wavebench.toml --resource TCPIP::<dp800-ip>::INSTR
python -m wavebench power status --config wavebench.toml --resource TCPIP::<dp800-ip>::INSTR --channel 1
python -m wavebench power set --config wavebench.toml --resource TCPIP::<dp800-ip>::INSTR --channel 1 --voltage 5.0 --current-limit 0.1
python -m wavebench power output --config wavebench.toml --resource TCPIP::<dp800-ip>::INSTR --channel 1 on
```

`power set` 不改变 output 状态；`power output` 不改变电压/电流限值。

多仪器流程检查、执行与离线报告：

```bash
python -m wavebench run schema
python -m wavebench run check --config wavebench.toml --plan plans/dp800_scope_probe_voltage_steps.toml
python -m wavebench run check --config wavebench.toml --plan plans/example_scope_expect_quality.toml
python -m wavebench run check --config wavebench.toml --plan plans/demo_dg4202_10k_screenshot_report.toml
python -m wavebench run plan --config wavebench.toml --plan plans/dp800_scope_probe_voltage_steps.toml
python -m wavebench run plan --config wavebench.toml --plan plans/demo_dg4202_10k_screenshot_report.toml
python -m wavebench run report data/runs/<run_dir>
```

离线查看采集包与截图采集：

```bash
python -m wavebench capture inspect data/raw/<capture_dir>
python -m wavebench capture inspect data/raw/<capture_dir> --fft
python -m wavebench scope capture --config wavebench.toml --channel 1 --label smoke_with_screen --points def --no-csv --screenshot
```

`run report` 和 `capture inspect` 只读已有 `run.json` / `summary.csv` / `metadata.json` / `ch*.npy`，不会连接仪器，也不会改写原始采集数据。`capture inspect --fft` 只输出离线频谱摘要。`scope capture --screenshot` 会在采集包中额外写入 `screenshot.png`。

`plans/example_scope_expect_quality.toml` 是公开示例计划，包含 source restore、`quality_gate`、`auto_recover` 和 `[steps.expect]`，只用于展示写法。`plans/demo_dg4202_10k_screenshot_report.toml` 是 v0.2 实机 demo：DG4202 CH2 输出 10 kHz 方波，RTM2032 CH1 采集波形和截图，断言频率和可见信号幅度，随后用 `run report` 生成 HTML。

`run plan` 会真实连接仪器并执行计划；DP800 直连示波器探头的计划必须保留显式 scope coupling guard。

信号源最小可写控制：

```bash
python -m wavebench source set-freq --config wavebench.toml --channel 2 1000
python -m wavebench source output --config wavebench.toml --channel 2 on
python -m wavebench source set-duty --config wavebench.toml --channel 2 25
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
- [x] 正式离散扫点命令：`sweep discrete`。
- [x] 接入 DP800 电源命令：`power idn/status/set/output`。
- [x] 设计实验流程层，必须显式组合 power/source/scope 动作，不允许 capture/sweep 默认修改电源。
- [x] 实现 `run check`、可配置 scope coupling guard、最小 `run plan` 执行器。
- [x] DP800 电压阶跃 run plan 实机 smoke 通过：5 V -> 3.3 V -> 5 V，并写入 `data/runs/...`。
- [x] 把 source step 接入 `run plan`，并新增 `source.set_duty`。
- [x] 三仪器流程 smoke 通过：DG4202 CH2 动态 duty -> RTM2032 CH1 分析；DP800 CH1 -> RTM2032 CH2 对照。
- [x] `run plan` source restore 通过：`[restore] source_state = true` 会在成功/失败路径恢复 output/function/frequency/amplitude/duty。
- [x] 修复 run plan 中 `target_cycles/window_frequency_hz` 未换算为 `time_range_s` 的问题；100 kHz duty 75% 复验为 0.75。
- [x] run plan `scope.capture` 支持 `quality_gate = true` 和 `auto_recover = true`；质量警告时按配置执行多次 `scope.auto` 后重采，并支持重复结果一致性判定。
- [x] run plan `scope.capture` 支持 `[steps.expect]` 指标 min/max 断言；断言失败会保留采集证据，并将 step/run 标记为 failed。
- [x] 新增公开 example plan：`plans/example_scope_expect_quality.toml`，展示质量恢复与实验断言写法。
- [x] 新增 `run schema`，从代码打印 run plan step schema；`run check` 对未知 kind、未知字段、缺字段给出更具体提示。
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
- `power set` 和 `power output` 是两个独立命令：前者不改变 output，后者不改变电压/电流限值。
- DP800 读回等待通过 `power.settle_ms_after_set` 与 `power.settle_ms_after_output` 配置，不应隐藏为不可见常量。
- 使用示波器测电源输出时，不要自动切换输入阻抗；50 Ω 输入耐压较低，必须由操作者明确确认。
- `[steps.expect]` 只检查采集摘要指标，不扫描原始波形；需要更复杂的判定时应先新增明确的 summary 指标。


### 2026-04-30 scope.auto run-plan step

- [x] `run plan` supports explicit `scope.auto` steps.
- [x] The step calls RTM2032 `AUToscale` through `ScopeService.autoscale()` and waits for completion via the existing `*OPC?` path.
- [x] `scope.capture` still does not call autoscale implicitly; plans must insert `scope.auto` where wanted.
