# RTM2032 MVP 命令确认表

## 目的

本文档整理 WaveBench MVP-1 需要使用的 RTM2000 / RTM2032 SCPI 命令，作为后续实现依据。

当前 MVP-1 范围：

```text
LAN 连接
RTM2032 示波器
scope idn / status / auto / fetch / capture / errors
REAL 波形读取
CSV + NPY + metadata.json + commands.log 输出
```

## 使用约定

- 以 RTM2000 手册摘录为准。
- 命令实现优先使用手册中确认的长命令或清晰缩写。
- `AUToscale`、`SINGle`、`STOP` 等事件命令为异步命令，必须使用 `*OPC?` 或等价机制同步。
- `fetch` / `capture` 默认不执行 `*RST`。
- `auto / autoscale` 是显式操作，会改变水平、垂直和触发设置。

## MVP-1 命令总表

| 功能 | 实现命令 | 手册确认 | 用途 | 实现备注 |
|---|---|---|---|---|
| 查询身份 | `*IDN?` | 已确认 | 返回厂商、型号、序列号、固件版本 | `scope idn`、metadata 必用 |
| 清状态 | `*CLS` | 已确认 | 清状态寄存器与输出缓冲区 | 操作开始前执行 |
| 等待完成 | `*OPC?` | 已确认 | 等待前序命令完成并返回 `1` | 用于 `AUToscale`、`SINGle` 后同步 |
| 错误查询 | `SYSTem:ERRor:[NEXT]?` / `SYST:ERR?` | 已确认 | 查询并弹出最旧错误；空队列返回 `0,"No error"` | 实现可用短命令 `SYST:ERR?` |
| 全部错误 | `SYSTem:ERRor:ALL?` | 已确认 | 查询并弹出全部未读错误 | `scope errors` 可选使用 |
| Auto | `AUToscale` | 已确认 | 自动设置水平、垂直、触发以稳定显示波形 | 异步；必须 `*OPC?`；显式命令 |
| 单次采集 | `SINGle` | 已确认 | 启动指定数量的采集 | 异步；默认采集数量为 1 |
| 单次采集别名 | `RUNSingle` | 已确认 | 与 `SINGle` 相同 | 实现优先用 `SINGle` |
| 停止采集 | `STOP` | 已确认 | 停止运行中的采集 | 可用于需要改 `DATA:POINts` 前；MVP-1 谨慎使用 |
| 数据格式 | `FORMat[:DATA] REAL` / `FORM REAL` | 已确认 | 设置波形导出为 32-bit IEEE 754 float binary block | MVP-1 只支持 REAL |
| 字节序 | `FORMat:BORDer LSBFirst` / `FORM:BORD LSBF` | 已确认 | 设置二进制导出字节序为 little-endian | 手册 REAL 示例使用 LSBF |
| 数据范围 | `CHANnel<m>:DATA:POINts DMAXimum` / `CHAN1:DATA:POIN DMAX` | 已确认 | 设置返回 displayed time range 内的最大波形点数 | 仅停止后完整生效；运行时可能自动用 DEF |
| 波形头 | `CHANnel<m>:DATA:HEADer?` / `CHAN1:DATA:HEAD?` | 已确认 | 返回 `XStart,XStop,RecordLength,ValuesPerSampleInterval` | 构造时间轴必用 |
| 波形数据 | `CHANnel<m>:DATA?` / `CHAN1:DATA?` | 已确认 | 返回指定通道波形数据 | 受 `FORM` 和 `DATA:POINts` 影响 |

## 推荐命令序列

### `scope idn`

```text
*IDN?
```

输出用于确认仪器型号。

### `scope status`

```text
*IDN?
SYST:ERR?
```

用于快速检查连接和错误队列。

### `scope errors`

方案 A：循环查询单条错误。

```text
SYST:ERR?
SYST:ERR?
...
```

直到返回：

```text
0,"No error"
```

方案 B：一次性查询全部错误。

```text
SYST:ERR:ALL?
```

MVP-1 可先实现方案 A，行为更直观。

### `scope auto` / `scope autoscale`

```text
*CLS
AUToscale
*OPC?
SYST:ERR?
```

注意：

- `AUToscale` 是异步命令。
- 该命令会改变水平、垂直和触发设置。
- 只在用户显式执行 `scope auto` / `scope autoscale` 时调用。

### `scope fetch --channel 1`

`fetch` 不触发新采集，直接读取当前波形。

```text
*CLS
FORM REAL
FORM:BORD LSBF
CHAN1:DATA:POIN DMAX
CHAN1:DATA:HEAD?
CHAN1:DATA?
SYST:ERR?
```

注意：

- 如果采集正在运行，手册说明 sample range 可能自动使用 `DEF`。
- 如果需要稳定读取 DMAX，可在后续版本考虑显式 `STOP`，但 MVP-1 先不默认停止用户当前操作。

### `scope capture --channel 1`

`capture` 触发一次单次采集后读取波形。

```text
*CLS
FORM REAL
FORM:BORD LSBF
CHAN1:DATA:POIN DMAX
SINGle
*OPC?
CHAN1:DATA:HEAD?
CHAN1:DATA?
SYST:ERR?
```

注意：

- `SINGle` 是异步命令。
- 如果触发条件未满足，`*OPC?` 可能超时。
- 超时提示应建议用户检查触发设置，或改用 `fetch` 读取当前波形。

## 波形 Header 解析

`CHANnel<m>:DATA:HEADer?` 返回逗号分隔列表：

```text
XStart,XStop,RecordLength,ValuesPerSampleInterval
```

含义：

| 位置 | 字段 | 含义 |
|---:|---|---|
| 1 | `x_start_s` | 起始时间，单位 s |
| 2 | `x_stop_s` | 结束时间，单位 s |
| 3 | `points` | 波形记录长度，单位 samples |
| 4 | `values_per_sample_interval` | 每个采样间隔的值数量，普通波形通常为 1 |

时间轴构造：

```python
dt = (x_stop_s - x_start_s) / (points - 1)
time_s = x_start_s + np.arange(points) * dt
```

需要校验：

- `points >= 2`
- `x_stop_s > x_start_s`
- 实际波形点数与 header points 一致

## 数据格式确认

`FORM REAL` 对应：

```text
32-bit IEEE 754 Floating-Point-Format
Definite Length Block Data according to IEEE 488.2
```

MVP-1 通过 `RsInstrument` 读取为 float list，再转换为 `np.ndarray`。

MVP-1 不做：

```text
FORM ASC
FORM UINT,8
FORM UINT,16
FORM UINT,32
```

UINT 路线需要 `XORigin? / XINCrement? / YORigin? / YINCrement? / YRESolution?` 参与换算，留到后续版本。

## 实机验证状态（2026-04-29）

已在 RTM2032（以太网 `192.168.123.2`）上验证：

| 项目 | 结果 | 备注 |
|---|---|---|
| `*IDN?` | 通过 | `Rohde&Schwarz,RTM2032,5710.0999k32/101662,06.010` |
| `AUToscale` + `*OPC?` | 通过 | 接入示波器自带约 1 kHz 方波后，前面板显示恢复正常 |
| `FORM REAL` / `FORM:BORD LSBF` | 通过 | `RsInstrument.query_bin_or_ascii_float_list()` 可直接解析 REAL binary block |
| `CHAN1:DATA:HEAD?` | 通过 | 示例返回 `-1.0000E-03,9.9980E-04,10000,1` |
| `CHAN1:DATA?` | 通过 | 读取 10000 点，电压约 `-0.5..0.62 V` |
| `scope capture` 采集包 | 通过 | 当前实现会打包当前波形，已输出 CSV / NPY / metadata / commands.log |

当前实现注意：

- `scope fetch` 已符合本文定义：读取当前波形，不触发新采集。
- `scope capture` 当前版本（`9c9cc32`）已经能生成采集包；后续 `capture-single` 实现改为执行 `SINGle + *OPC?`。
- 下一步需要决定 `capture` 是否严格按本文定义触发单次采集；如果是，就要补触发超时提示和 failed package。

## `DATA:POINts` 注意事项

手册确认可选值：

```text
DEFault
MAXimum
DMAXimum
```

MVP-1 使用：

```text
DMAXimum
```

含义：当前 waveform record 中 displayed time range 内的最大点数。

注意：

- `DATA:POINts` 的 sample range 只能在 STOP 模式下改变。
- 如果 acquisition 正在运行，仪器可能自动使用 `DEF`。
- MVP-1 不默认发送 `STOP`，避免意外改变用户当前前面板操作；如上机测试发现读取范围不稳定，再讨论是否在 `capture` 中加入安全的停止策略。

## 缩写策略

文档中保留长命令用于理解；实现中可使用手册和示例支持的缩写：

| 长命令 | 代码中可用缩写 |
|---|---|
| `FORMat[:DATA] REAL` | `FORM REAL` |
| `FORMat:BORDer LSBFirst` | `FORM:BORD LSBF` |
| `CHANnel1:DATA:POINts DMAXimum` | `CHAN1:DATA:POIN DMAX` |
| `CHANnel1:DATA:HEADer?` | `CHAN1:DATA:HEAD?` |
| `CHANnel1:DATA?` | `CHAN1:DATA?` |
| `SYSTem:ERRor:[NEXT]?` | `SYST:ERR?` |

如某个缩写上机测试失败，优先改用长命令。

## 待上机验证项

虽然手册已确认命令存在，但仍需在 RTM2032 实机验证：

- `*IDN?` 实际返回是否包含 `RTM2032`；
- `AUToscale; *OPC?` 是否按预期等待完成；
- `CHAN1:DATA:POIN DMAX` 在当前运行/停止状态下的实际行为；
- `FORM REAL; FORM:BORD LSBF; CHAN1:DATA?` 与 RsInstrument 的 binary float 读取是否兼容；
- `CHAN1:DATA:HEAD?` points 与实际读取点数是否一致。

## MVP-1 实现顺序建议

1. `scope idn`：只测 `*IDN?`。
2. `scope errors`：实现错误队列读取。
3. `scope auto`：实现 `AUToscale + *OPC?`。
4. `scope fetch --channel 1`：不触发采集，只读当前波形。
5. `scope capture --channel 1`：加入 `SINGle + *OPC?`。


## 2026-04-29 实机同步：已验证命令序列

### `scope capture` 当前序列

```text
*IDN?
*CLS
[optional] TIMebase:RANGe <seconds>
CHAN<m>:STAT ON
FORM REAL
FORM:BORD LSBF
CHAN:DATA:POIN DEF|MAX|DMAX
SINGle
*OPC?
CHAN<m>:DATA:HEAD?
CHAN<m>:DATA?
SYST:ERR?
```

说明：

- `scope capture` 会触发新的单次采集，不是只读取屏幕上已有波形。
- 默认不发送 `*RST`。
- `TIMebase:RANGe` 只在用户传入 `--time-range`，或通过 `--window-frequency + --target-cycles` 自动计算出时窗时发送。
- `CHAN:DATA:POIN` 在 RTM2032 上只接受 `DEFault | MAXimum | DMAXimum`；实测发送任意数字点数会产生 `-104,"Data type error"`。
- `DEF` 实测返回屏幕可见点，常见为 10000 点；`DMAX` 可返回显示时间范围内的最大内存点，实测可达 10000000 点。
- `SINGle + *OPC?` 后前面板可能显示停止/暂停；下一次 `capture` 再发送 `SINGle` 可重新启动单次采集。

### 数据窗口相关命令

```text
TIMebase:RANGe <AcquisitionTime>
```

用途：设置 10 格总采集时间。例如：

```text
TIMebase:RANGe 0.01
```

实测 header 约为：

```text
x_start=-5 ms, x_stop=4.999 ms, points=10000, dt=1 us
```

### 输出控制与质量校验

这些不是 SCPI 命令，而是 WaveBench CLI 层行为：

```bash
--no-csv
--no-npy
--points def|max|dmax
--time-range <seconds>
--window-frequency <Hz>
--target-cycles <N>
--expect-frequency <Hz>
--frequency-tolerance <ratio>
```

`--window-frequency` 只用于计算时窗，不判断频率对错；`--expect-frequency` 才用于 metadata 里的频率一致性校验。


### 多通道逐通道采集

CLI 示例：

```bash
python -m wavebench scope capture --config wavebench.toml   --channel 1 --channel 2   --label dual_smoke   --points def   --window-frequency 1000   --target-cycles 10   --no-csv
```

当前实现不是同步多通道采集，而是按通道重复以下序列：

```text
*CLS
TIMebase:RANGe <seconds>
CHAN<n>:STAT ON
FORM REAL
FORM:BORD LSBF
CHAN:DATA:POIN DEF|MAX|DMAX
SINGle
*OPC?
CHAN<n>:DATA:HEAD?
CHAN<n>:DATA?
SYST:ERR?
```

实机验证：CH1/CH2 均可读取；双通道包中 `commands.log` 能看到 `CHAN1:DATA:HEAD?` / `CHAN1:DATA?` 和 `CHAN2:DATA:HEAD?` / `CHAN2:DATA?`。
