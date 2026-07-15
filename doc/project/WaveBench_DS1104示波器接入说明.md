# WaveBench DS1104Z / DS1000Z 示波器接入说明

## 支持范围

配置使用 `scope.driver = "ds1104"`，也接受 `"ds1000z"` 别名。当前驱动面向
RIGOL DS1104Z、DS1104Z Plus、DS1104Z-S Plus 及同命令集的 DS1000Z 系列，提供：

- `*IDN?`、`:SYSTem:ERRor?`；
- `:AUToscale` 与 `*OPC?` 同步；
- CH1–CH4 耦合查询；
- 单次触发采集和当前波形读取；
- NORM 屏幕波形与 RAW 存储波形；
- PNG 屏幕截图。

驱动不会自动修改通道耦合、探头倍率、带宽限制、触发源或触发电平。
DS1000Z 连接使用 PyVISA；RTM2032 仍使用 RsInstrument，避免部分 RIGOL VXI-11
固件不支持 RsInstrument 初始化时的 Read STB 操作。

## 波形读取

`waveform.points = "def"` 使用 `:WAVeform:MODE NORMal`。`"max"` 和 `"dmax"`
使用 RAW 模式；RAW 读取前示波器必须处于 STOP 状态。

数据格式固定为 BYTE。驱动读取十字段 `:WAVeform:PREamble?`，按手册公式换算：

```text
voltage = (sample - YORigin - YREFerence) * YINCrement
time[i] = (i - XREFerence) * XINCrement + XORigin
```

DS1000Z 的 BYTE 单次读取上限为 250000 点，长记录通过 `:WAVeform:STARt`、
`:WAVeform:STOP` 和多次 `:WAVeform:DATA?` 连续拼接。
切回 NORM 等非分块模式时，驱动会把 START/STOP 显式恢复为完整 preamble 窗口，
避免上一轮 RAW 分块留下的读取范围影响后续采集。

## 时基和截图

WaveBench 的 `time_range_s` 表示整个采集窗口。DS1000Z 的主时基命令使用 s/div，
且 `:SYSTem:GAM?` 固定为 12 格，因此驱动写入 `time_range_s / 12`。

截图使用 `:DISPlay:DATA? ON,OFF,PNG`，由 VISA 层剥离 TMC block header 后保存 PNG。

## 输入安全语义

DS1000Z 的模拟通道输入固定为 1 MΩ；`:CHANnel<n>:COUPling?` 返回的
`AC`、`DC`、`GND` 是耦合方式，不是 50 Ω/1 MΩ 端接选择。因此 WaveBench 对该
驱动按机型语义接受这三个返回值，但仍只读检查，不主动切换耦合。

## 验证状态

离线单元测试覆盖 preamble 解析、BYTE 电压换算、时间轴、250000 点分块边界、
4 通道限制、时基换算、截图命令、驱动路由和安全语义。

2026-07-15 已在 DS1104Z Plus、固件 `04.04.04.SP4` 上完成 LAN 实机验证：

- `*IDN?`、错误队列及 CH1/CH3 AC 耦合查询正常；
- CH1/CH3 NORM 均返回 1200 点，1 kHz 信号频率估算约为 999.2–1000.3 Hz；
- 单次多通道采集、CSV、NPY、metadata、commands.log 和 800×480 PNG 截图正常；
- 3000000 点 RAW 记录按 12 个 250000 字节块完整读取，结束后错误队列为空；
- `:AUToscale`、`*OPC?` 等待及 autoscale 后再次读取 CH1/CH3 正常。

实机测试发现并修复了两项仅离线模拟不易暴露的问题：RIGOL VXI-11 不支持
RsInstrument 初始化所需的 Read STB，因此 DS1000Z 改用 PyVISA；RAW 最后一块会
保留 START/STOP 范围，因此 NORM 读取前必须恢复为完整 preamble 窗口。

性能方面，该固件通过 VXI-11 读取 250000 字节约需 14 秒，3000000 点 RAW 全程
约 169 秒。功能正确，但高点数 RAW 不适合高频率重复采集。
