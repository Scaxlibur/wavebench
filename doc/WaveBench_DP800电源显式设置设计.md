# WaveBench DP800 电源显式设置设计

## 背景

`power idn/status` 已经完成只读接入。下一步需要支持电压调整测试，但电源控制必须比信号源更谨慎。

第一版只实现显式设置电压和电流限值：

```text
wavebench power set --channel 1 --voltage 5 --current-limit 0.1
```

它只发送 `:APPL CH<n>,<volt>,<curr>`，不发送 `:OUTP CH<n>,ON|OFF`。

## 原则

### 1. set 不改变输出开关

`power set` 只调整通道设定值：

```text
voltage setpoint
current limit
```

它不负责打开或关闭输出。输出控制以后必须是独立命令：

```text
wavebench power output --channel 1 on|off
```

这样做的原因很简单：实验台上电源输出可能正接着被测板，设置电压和打开输出是两个风险等级不同的动作。

### 2. 参数必须显式

第一版要求同时给出：

```text
--voltage <V>
--current-limit <A>
```

不做“只改电压、保持旧电流限值”的隐式行为。以后如果需要 partial update，先 snapshot 旧状态，再明确设计。

### 3. 不做范围表

DP800 不同型号/通道量程不同。第一版只做通用合法性检查：

```text
voltage >= 0
current_limit > 0
channel >= 1
```

具体范围交给仪器拒绝，后续再根据 `:APPL? CH<n>` 的 rating 或型号表补充。

### 4. 返回 status

写入后立即读回状态：

```text
:APPL? CH<n>
:MEAS:ALL? CH<n>
:OUTP? CH<n>
:OUTP:MODE? CH<n>
```

终端输出复用 `power status` 格式，便于人工确认：

```text
CH1: output=ON mode=CV set=5.0V/0.1A measured=5.0115V/0.0A/0.0W rating=30V/3A
```

## SCPI

写命令：

```text
:APPL CH1,5,0.1
```

根据手册，`:APPLy` 对多通道型号会选择指定通道并设置该通道电压和电流值。它不是 output 控制命令。

## 测试计划

fake 单元测试：

```text
DP800Power.set_voltage_current_limit(1, 3.3, 0.2)
```

验证：

```text
write :APPL CH1,3.3,0.2
随后 get_status(1)
非法 voltage/current/channel 会 DataError
CLI 接受 power set --channel 1 --voltage 3.3 --current-limit 0.2
```

实机测试另行执行。建议先从当前 5V 改到 4V 或 3.3V，并同时用 RTM2032 CH2 采集确认。
