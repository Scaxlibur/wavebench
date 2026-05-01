# WaveBench DP800 电源只读接入设计

## 背景

下一阶段 WaveBench 准备接入 RIGOL DP800 系列可编程直流电源。当前实物为：

```text
RIGOL DP832A @ <dp800-ip>
resource = TCPIP::<dp800-ip>::INSTR
```

2026-04-30 的实验台状态：DP800 CH1 已由人工设置为 5V 并使能输出，连接到 RTM2032 CH2；示波器上能看到该电压。公开文档不记录真实实验台 IP。公开文档不记录真实实验台 IP。

本设计只覆盖第一步：**只读接入**。不写电压，不写电流，不打开/关闭输出。

## 设计原则

### 1. 第一版只读

允许的 SCPI：

```text
*IDN?
:APPL? CH<n>
:OUTP? CH<n>
:OUTP:MODE? CH<n>
:MEAS:ALL? CH<n>
```

暂时不允许的 SCPI：

```text
:APPL CH<n>,...
:VOLT...
:CURR...
:OUTP CH<n>,ON|OFF
*RST
```

电源不是普通测量仪器。写错一个输出命令可能影响被测板，所以先把读状态链路做稳。

### 2. CLI 语义

第一版新增命令建议：

```text
wavebench power idn
wavebench power status --channel 1
```

`power status` 输出应包含两类信息：

```text
设置值：来自 :APPL? CH<n>
输出状态：来自 :OUTP? CH<n> / :OUTP:MODE? CH<n>
实测值：来自 :MEAS:ALL? CH<n>
```

建议终端格式：

```text
CH1: output=ON mode=CV set=5.000V/0.100A measured=5.0114V/0.0000A/0.000W rating=30V/3A
```

### 3. 配置

建议在 `wavebench.toml` 增加：

```toml
[power]
resource = "TCPIP::<dp800-ip>::INSTR"
default_channel = 1
check_errors = true
```

`power` 与已有 `scope` / `source` 分离，不复用 `source` 配置。

### 4. 分层

建议新增：

```text
src/wavebench/drivers/dp800.py
src/wavebench/services/power_service.py
```

Driver 层：

```text
DP800Power.idn() -> str
DP800Power.get_status(channel: int) -> PowerStatus
DP800Power.errors() -> list[str]
```

Service 层：

```text
PowerService.idn() -> str
PowerService.status(channel: int | None = None) -> PowerStatus
```

CLI 层不直接写 SCPI。

### 5. 数据结构

建议第一版：

```python
@dataclass(frozen=True)
class PowerStatus:
    channel: int
    output: str
    mode: str
    rating: str | None
    set_voltage_v: float | None
    set_current_a: float | None
    measured_voltage_v: float | None
    measured_current_a: float | None
    measured_power_w: float | None
```

其中：

- `rating/set_voltage_v/set_current_a` 来自 `:APPL? CH<n>`
- `output` 来自 `:OUTP? CH<n>`
- `mode` 来自 `:OUTP:MODE? CH<n>`
- `measured_*` 来自 `:MEAS:ALL? CH<n>`

### 6. 真实返回格式

2026-04-30 已做只读探测：

```text
*IDN? -> RIGOL TECHNOLOGIES,DP832A,<serial>,<firmware>
:APPL? CH1 -> CH1:30V/3A,5.000,0.100
:OUTP? CH1 -> ON
:OUTP:MODE? CH1 -> CV
:MEAS:ALL? CH1 -> 5.0114,0.0000,0.000
```

HTTP 也可直连：

```text
http://<dp800-ip>/ -> HTTP 200
```

HTTP 第一版只作为人工诊断入口，不进入正式 driver。

### 7. 解析规则

`:APPL? CH1` 示例：

```text
CH1:30V/3A,5.000,0.100
```

解析为：

```text
rating = "30V/3A"
set_voltage_v = 5.000
set_current_a = 0.100
```

`:MEAS:ALL? CH1` 示例：

```text
5.0114,0.0000,0.000
```

解析为：

```text
measured_voltage_v = 5.0114
measured_current_a = 0.0000
measured_power_w = 0.000
```

### 8. 测试计划

第一步 fake 单元测试：

```text
parse_apply_response("CH1:30V/3A,5.000,0.100")
parse_measure_all_response("5.0114,0.0000,0.000")
DP800Power.get_status(1) 查询顺序正确
CLI 接受 power idn/status 参数
```

第二步实机只读 smoke：

```text
python -m wavebench power idn --config wavebench.toml
python -m wavebench power status --config wavebench.toml --channel 1
```

预期：

```text
IDN 返回 DP832A
CH1 output=ON
CH1 mode=CV
CH1 measured voltage 接近 5V
```

### 9. 后续写控制的门槛

只有在只读状态稳定后，才考虑写控制命令。

写控制第一步也必须显式命令，不自动执行：

```text
wavebench power set --channel 1 --voltage 5 --current-limit 0.1
```

输出控制必须单独命令：

```text
wavebench power output --channel 1 on|off
```

并且加入醒目的确认/日志，不允许 sweep 或 capture 默认修改电源。
