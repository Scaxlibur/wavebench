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

暂不做：

```text
信号发生器、GUI、复杂触发、扫频、自动报告。
```

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

- [RTM2000_VISA_SCPI_手册摘录.md](./RTM2000_VISA_SCPI_手册摘录.md)
  - RTM2000 用户手册中 VISA / SCPI 相关摘录，作为命令确认依据。

## 进度速览

### 已完成

- [x] 确定项目名：WaveBench
- [x] 建立三段式目录：`doc/`、`tool-of-rei/`、项目文件
- [x] 设置 `.gitignore` 排除 `tool-of-rei/`
- [x] 迁入示波器开发思路草案
- [x] 迁入 RTM2000 VISA/SCPI 手册摘录
- [x] 完成项目边界讨论
- [x] 完成第一版 CLI 形态讨论
- [x] 完成设备抽象层讨论
- [x] 完成数据输出格式讨论
- [x] 完成配置文件格式讨论
- [x] 完成错误处理和日志策略讨论
- [x] 整理 RTM2032 MVP 命令确认表
- [x] 确认 `AUToscale` 可作为远程 Auto 功能

- [x] 初始化 Python 项目骨架
- [x] 实机打通 `scope idn`
- [x] 实机打通 `scope autoscale`
- [x] 实机打通 `scope fetch --channel 1`
- [x] 实机生成 `scope capture --channel 1 --label square_1khz` 采集包
- [x] 保存 CH1 CSV / NPY / metadata.json / commands.log

### 当前实机状态

2026-04-29 已在 RTM2032 上完成最小闭环：

```text
Windows Ethernet -> RTM2032 192.168.123.2 -> VISA/SCPI
*IDN? -> AUToscale -> CH1 REAL waveform fetch -> capture package
```

已验证的 1 kHz 方波数据：

```text
samples = 10000
time    = -1.000 ms .. 0.9998 ms
dt      = 200 ns
voltage = about -0.5 V .. 0.62 V
```

### 下一步

- [x] 对齐 `scope capture` 语义：默认执行 `SINGle + *OPC?`。
- [x] 补完整触发超时后的 failed package 行为。
- [x] 给采集包增加数据质量检查：频率估计、Vpp、RMS、均值。
- [x] 补完整触发超时后的 failed package 行为。
- [ ] 明确多通道策略：先支持 `--channel 2` 单通道，还是直接支持 `--channel 1 --channel 2` 逐通道采集。

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
- 第一阶段输出：每通道 CSV、每通道 NPY、metadata.json、commands.log。
- 连接成功后失败保留 `*_failed` 采集包。
