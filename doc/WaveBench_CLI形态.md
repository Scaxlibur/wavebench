# WaveBench CLI 形态

## 设计目标

WaveBench 从第一阶段开始就支持两种使用方式：

- **非交互式命令行**：适合脚本调用、批处理、电赛现场快速执行。
- **交互式 shell / 菜单**：适合调试、不想记参数、第一次配置仪器时使用。

两种模式必须共用同一套底层逻辑，不能各写一套采集流程。

当前阶段只考虑 **LAN 连接**，暂不考虑 USB / GPIB / Serial。

## 命令入口

主命令：

```bash
wavebench
```

一级子命令按设备或功能划分：

```bash
wavebench scope ...
wavebench gen ...
wavebench run ...
wavebench config ...
```

第一阶段只实现：

```bash
wavebench scope ...
```

`gen`、`run`、`config` 暂时作为后续扩展方向，不急着实现。

## 非交互式模式

### 查询仪器身份

```bash
wavebench scope idn --resource TCPIP::192.0.2.10::INSTR
```

如果没有传入 `--resource`，则从配置文件读取。

### 查看状态

```bash
wavebench scope status
```

执行：

```text
*IDN?
SYST:ERR?
```

期望输出：

```text
Instrument: Rohde&Schwarz,RTM2032,...
Error: 0,"No error"
```

### Auto / Autoscale

```bash
wavebench scope auto
```

等价命令：

```bash
wavebench scope autoscale
```

该命令对应 RTM2000 手册中的：

```text
AUToscale
```

作用：分析已启用通道信号，自动设置水平、垂直和触发参数，使波形稳定显示。

执行流程：

```text
连接仪器
  ↓
查询 *IDN?
  ↓
*CLS
  ↓
AUToscale
  ↓
*OPC?
  ↓
SYST:ERR?
```

注意：`AUToscale` 是异步命令，必须等待完成后再继续读取波形。

该命令会改变示波器前面板设置，因此只能作为显式命令执行；`fetch` 和 `capture` 默认不自动调用 autoscale。

### 读取当前波形

```bash
wavebench scope fetch --channel 1
```

`fetch` 不触发新采集，只读取当前波形。适合示波器已经停在某个状态时使用。

### 单次采集并读取波形

```bash
wavebench scope capture --channel 1
```

完整参数示例：

```bash
wavebench scope capture \
  --resource TCPIP::192.0.2.10::INSTR \
  --channel 1 \
  --format real \
  --points dmax \
  --out data/raw \
  --basename test_wave
```

`capture` 执行一次单次采集，再读取波形。

流程：

```text
连接仪器
  ↓
查询 *IDN?
  ↓
不 reset
  ↓
设置波形传输格式
  ↓
SINGle
  ↓
*OPC?
  ↓
读取 header
  ↓
读取 data
  ↓
保存 csv / npy / json / commands.log
```

### 读取错误队列

```bash
wavebench scope errors
```

循环读取：

```text
SYST:ERR?
```

直到：

```text
0,"No error"
```

## 交互式模式

推荐命令：

```bash
wavebench scope shell
```

第一版使用轻量菜单，不做复杂 TUI。

示例：

```text
WaveBench Scope Shell
Resource: TCPIP::192.0.2.10::INSTR

1. IDN
2. Status
3. Auto / Autoscale
4. Fetch CH1
5. Capture CH1
6. Fetch CH2
7. Capture CH2
8. Errors
0. Exit

>
```

交互模式也必须调用底层 service 函数，不直接实现采集逻辑。

## fetch、capture 与 auto 的区别

```text
auto    = 自动调整水平、垂直和触发设置，让波形稳定显示
fetch   = 不触发采集，直接读取当前波形
capture = 触发一次采集，等待完成，再读取波形
```

电赛现场的典型用法：

```bash
wavebench scope auto
wavebench scope fetch --channel 1
```

或者：

```bash
wavebench scope auto
wavebench scope capture --channel 1
```

`auto` 是显式操作；`fetch` / `capture` 默认保持保守，不偷偷修改前面板主要设置。

## LAN-only 约束

当前阶段只支持 LAN VISA 资源：

```text
TCPIP::<instrument-ip>::INSTR
```

暂不支持：

- USBTMC；
- GPIB；
- Serial；
- VXI-11 之外的特殊资源写法。

## 配置文件示例

```yaml
connection:
  backend: lan
  resource: "TCPIP::192.0.2.10::INSTR"
  timeout_ms: 10000
  opc_timeout_ms: 30000

scope:
  model_hint: "RTM2032"
  reset_before_run: false
  check_errors: true

capture:
  default_channel: 1
  waveform_format: "real"
  byte_order: "lsbf"
  points: "dmax"

autoscale:
  wait_opc: true
  check_errors: true

output:
  directory: "data/raw"
  save_csv: true
  save_npy: true
  save_json: true
  save_commands_log: true
```

## 参数优先级

```text
命令行参数 > config.yaml > 默认值
```

例如配置文件默认 CH1，但命令行传入：

```bash
wavebench scope capture --channel 2
```

则按 CH2 执行。

## 第一阶段命令清单

第一阶段实现：

```bash
wavebench scope idn
wavebench scope status
wavebench scope auto
wavebench scope autoscale
wavebench scope errors
wavebench scope fetch --channel 1
wavebench scope capture --channel 1
wavebench scope shell
```

暂不实现：

```bash
wavebench scope set-timebase
wavebench scope set-trigger
wavebench scope set-channel
wavebench gen ...
wavebench run ...
```

## 当前 CLI 边界

```text
LAN only
RTM2032 only
scope only
支持交互式 shell
支持命令行传参
支持显式 auto / autoscale
默认不 reset
fetch / capture 默认不接管前面板设置
优先完成 auto、fetch、capture 三条高频路径
```


## 第二阶段补充：信号源 CLI 最小骨架

当前新增最小信号源命令：

```bash
wavebench source idn
wavebench source status --channel 1
wavebench source status --channel 2
wavebench source set-freq --channel 2 1000
wavebench source output --channel 2 on
```

信号源当前目标设备为 RIGOL DG4202，底层走 PyVISA / NI-VISA，不与示波器共用 R&S 专用库。
