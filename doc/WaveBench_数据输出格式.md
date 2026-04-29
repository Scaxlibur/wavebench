# WaveBench 数据输出格式

## 设计目标

第一阶段的数据输出围绕三件事设计：

1. 人能快速看懂；
2. Python 能直接分析；
3. 以后能追溯当时怎么测的。

当前阶段只支持：

```text
CSV + NPY + JSON + commands.log
```

暂不考虑 MATLAB 兼容、Parquet、数据库和自动报告。

## 当前实现状态（2026-04-29）

`9c9cc32 feat: fetch and capture RTM2032 waveforms` 已实现单通道采集包输出：

```text
data/raw/20260429_162450_square_1khz/
├─ ch1.csv
├─ ch1.npy
├─ metadata.json
└─ commands.log
```

实机样例来自 RTM2032 自带约 1 kHz 方波：

```text
samples = 10000
time    = -1.000000e-03 .. 9.998000e-04 s
dt      = 2.000000e-07 s
voltage = about -0.5 .. 0.62 V
```

当前 `capture` 已推进为 `SINGle + *OPC?` 单次采集后再读取波形并打包。


## 采集包

每次采集生成一个独立目录，称为“采集包”。

单通道示例：

```text
data/raw/20260429_011530_ch1/
├─ ch1.csv
├─ ch1.npy
├─ metadata.json
└─ commands.log
```

以后如果支持多通道：

```text
data/raw/20260429_011530_ch1_ch2/
├─ ch1.csv
├─ ch1.npy
├─ ch2.csv
├─ ch2.npy
├─ metadata.json
└─ commands.log
```

如果以后支持截图，可增加：

```text
screenshot.png
```

## 目录命名规则

默认规则：

```text
YYYYMMDD_HHMMSS_<label>
```

单通道：

```text
20260429_011530_ch1
```

多通道：

```text
20260429_011530_ch1_ch2
```

如果用户传入 `--basename`：

```bash
wavebench scope capture --channel 1 --basename opamp_gain_test
```

则目录名：

```text
20260429_011530_opamp_gain_test_ch1
```

## 默认输出目录

默认输出目录：

```text
data/raw/
```

`data/` 不进入 git。

未来 `.gitignore` 应加入：

```gitignore
data/
```

如果用户传参：

```bash
wavebench scope capture --out D:\WaveBenchData
```

则采集包放入指定目录下：

```text
D:\WaveBenchData\20260429_011530_ch1\
```

## CSV 文件

CSV 用来给人看，也方便 Excel、Origin、Python 快速读取。

单通道 CSV：

```csv
index,time_s,voltage_v
0,-4.998e-7,0.0012
1,-4.996e-7,0.0011
2,-4.994e-7,0.0010
```

列定义：

| 列名 | 含义 |
|---|---|
| `index` | 样本序号 |
| `time_s` | 时间，单位秒 |
| `voltage_v` | 电压，单位伏 |

不保存“只有电压”的 CSV。没有时间轴的数据后续很难追溯。

第一阶段每通道一个 CSV：

```text
ch1.csv
ch2.csv
```

以后如果多通道时间轴一致，可再考虑合并 CSV：

```csv
index,time_s,ch1_voltage_v,ch2_voltage_v
```

## NPY 文件

NPY 用于 Python 快速读取。

第一阶段保存二维数组：

```python
array.shape == (N, 2)
```

列定义：

```text
[:, 0] = time_s
[:, 1] = voltage_v
```

读取示例：

```python
import numpy as np

data = np.load("ch1.npy")
t = data[:, 0]
v = data[:, 1]
```

每通道一个 NPY：

```text
ch1.npy
ch2.npy
```

## metadata.json

JSON 只保存元信息，不保存大数组。

示例结构：

```json
{
  "wavebench": {
    "version": "0.1.0",
    "mode": "scope.capture",
    "timestamp": "2026-04-29T01:15:30+08:00"
  },
  "instrument": {
    "kind": "scope",
    "driver": "RTM2032Scope",
    "resource": "TCPIP::192.168.1.100::INSTR",
    "idn": "Rohde&Schwarz,RTM2032,..."
  },
  "acquisition": {
    "operation": "capture",
    "channel": 1,
    "triggered_single": true,
    "reset_before_run": false,
    "front_panel_control": false
  },
  "waveform": {
    "format": "REAL",
    "byte_order": "LSBF",
    "points_mode": "DMAX",
    "points": 5000,
    "x_start_s": -4.998e-7,
    "x_stop_s": 5.0e-7,
    "x_increment_s": 2.0e-10,
    "y_unit": "V"
  },
  "files": {
    "csv": "ch1.csv",
    "npy": "ch1.npy",
    "commands": "commands.log",
    "screenshot": null
  },
  "notes": ""
}
```

必须记录：

- `operation`：区分 `fetch` 和 `capture`；
- `reset_before_run`；
- `front_panel_control`；
- VISA `resource`；
- `idn`；
- `points`；
- `x_start_s`；
- `x_stop_s`；
- `x_increment_s`。

公开分享数据时，`resource` 可以脱敏。

## fetch 与 capture 的差异

`fetch`：不触发新采集，只读取当前波形。

```json
"acquisition": {
  "operation": "fetch",
  "triggered_single": false
}
```

`capture`：触发一次单次采集，等待完成，再读取波形。

```json
"acquisition": {
  "operation": "capture",
  "triggered_single": true
}
```

这两个必须区分，否则以后无法判断数据来源。

## commands.log

`commands.log` 记录关键 SCPI 命令和响应，用于排查仪器控制问题。

示例：

```text
2026-04-29T01:15:30.123 WRITE *CLS
2026-04-29T01:15:30.130 QUERY *IDN?
2026-04-29T01:15:30.145 RESP Rohde&Schwarz,RTM2032,...
2026-04-29T01:15:30.160 WRITE FORM REAL
2026-04-29T01:15:30.170 WRITE FORM:BORD LSBF
2026-04-29T01:15:30.180 WRITE CHAN1:DATA:POIN DMAX
2026-04-29T01:15:30.200 WRITE SING
2026-04-29T01:15:30.210 QUERY *OPC?
2026-04-29T01:15:31.532 RESP 1
2026-04-29T01:15:31.540 QUERY CHAN1:DATA:HEAD?
2026-04-29T01:15:31.550 RESP -4.998E-07,5.000E-07,5000,1
2026-04-29T01:15:31.570 QUERY_BINARY CHAN1:DATA?
```

第一阶段使用简单文本日志即可，不需要复杂日志框架。

commands.log 的目的不是做漂亮日志，而是回答一个问题：

> 脚本刚才到底对仪器说了什么？

## 截图预留

第一阶段可以不实现截图，但 metadata 预留字段：

```json
"files": {
  "screenshot": null
}
```

未来启用：

```bash
wavebench scope capture --channel 1 --screenshot
```

生成：

```text
screenshot.png
```

## 第一阶段结论

```text
一个采集包 = 一个目录
每通道一个 CSV
每通道一个 NPY
一个 metadata.json
一个 commands.log
```

单通道采集包：

```text
data/raw/20260429_011530_ch1/
├─ ch1.csv
├─ ch1.npy
├─ metadata.json
└─ commands.log
```

CSV：

```text
index,time_s,voltage_v
```

NPY：

```python
shape = (N, 2)
columns = [time_s, voltage_v]
```

JSON：只放元信息，不放大数组。

commands.log：记录关键 SCPI 命令与响应。


## 数据质量摘要字段补充

`metadata.json` 的 `waveform.summary` 中包含：

- `frequency_estimate_hz`: 估计频率。
- `frequency_method`: 频率估计方法，例如 `hysteresis_rising_crossing` 或 `fft_peak`。
- `estimated_cycles`: 当前采集窗口内估计包含的周期数。
- `quality_warnings`: 数据质量提示列表；例如少于 2 个周期时给出 `low_cycle_count`，提示频率估计可能不可靠。

- `expected_frequency_hz`: 用户通过 CLI/config 给出的预期频率。
- `frequency_error_ratio`: 估计频率相对预期频率的误差比例。
- `frequency_in_tolerance`: 是否落在给定频率容差内。
- `frequency_mismatch`: 估计频率偏离预期频率时的提示。
