# WaveBench DP800 电源输出控制设计

## 背景

`power set` 已经支持显式设置 DP800 通道电压和电流限值，但它不会打开或关闭输出。

输出开关是更高风险动作，必须独立命令、显式调用：

```text
wavebench power output --channel 1 on
wavebench power output --channel 1 off
```

## 原则

### 1. 输出控制独立

`power output` 只负责 output on/off，不设置电压、不设置电流。

`power set` 只负责电压/电流限值，不控制 output。

两者不能互相偷做对方的动作。

### 2. capture / sweep 不默认调用

第一版禁止 `scope capture`、`sweep discrete` 或后续自动流程默认打开电源输出。实验流程以后若需要控制电源，也必须在流程描述中显式出现。

### 3. 写后读回 status

执行 output 写命令后立即读回 `PowerStatus`：

```text
:OUTP CH<n>,ON|OFF
:APPL? CH<n>
:MEAS:ALL? CH<n>
:OUTP? CH<n>
:OUTP:MODE? CH<n>
```

终端输出复用 `power status` 格式。

### 4. 安全注意

调压或输出控制前，若连接示波器，必须确认示波器输入不是 50Ω。

RTM2032 查询示例：

```text
CHAN2:COUP? -> DCL
```

不要自动修改示波器输入阻抗。

## SCPI

输出打开：

```text
:OUTP CH1,ON
```

输出关闭：

```text
:OUTP CH1,OFF
```

查询：

```text
:OUTP? CH1
```

## 测试计划

fake 单元测试：

```text
DP800Power.set_output(1, True)
DP800Power.set_output(1, False)
```

验证：

```text
只写 :OUTP CH1,ON/OFF
随后 get_status(1)
不写 :APPL
CLI 接受 power output --channel 1 on/off
非法 channel 拒绝
```

实机测试另行确认后执行。建议只做：

```text
status -> output off -> status -> output on -> status
```

如果 CH1 接在示波器 CH2 上，实机前先确认 CH2 coupling 非 50Ω。
