# WaveBench 配置文件格式

## 结论

WaveBench 第一阶段使用 TOML 作为本机配置文件格式。

分工：

```text
TOML = 本机仪器连接与默认行为配置
YAML = 后续实验流程编排配置
```

第一阶段只实现 TOML，不引入 YAML。

## 文件命名

本地配置文件：

```text
wavebench.toml
```

示例配置文件：

```text
wavebench.example.toml
```

规则：

```text
wavebench.example.toml 进入 git
wavebench.toml 不进入 git
```

原因：

- `wavebench.example.toml` 给用户和开发者作为模板；
- `wavebench.toml` 可能包含真实仪器 IP、输出路径和现场习惯；
- 本地配置不应该提交。

## 查找顺序

第一阶段配置查找顺序：

```text
命令行 --config 指定
  ↓
当前目录 ./wavebench.toml
  ↓
程序默认值
```

示例：

```bash
wavebench scope idn --config lab.toml
```

如果没有传 `--config`，则查找：

```text
./wavebench.toml
```

如果仍然不存在，则使用程序默认值。需要仪器资源字符串的命令，如果没有 `resource`，必须报错。

## 参数优先级

```text
命令行参数 > TOML 配置 > 程序默认值
```

例如配置文件默认 CH1：

```toml
[scope]
default_channel = 1
```

运行：

```bash
wavebench scope capture --channel 2
```

则必须按 CH2 执行。

## 第一版配置结构

```toml
[connection]
backend = "lan"
resource = "TCPIP::192.168.1.100::INSTR"
timeout_ms = 10000
opc_timeout_ms = 30000

[scope]
driver = "rtm2032"
model_hint = "RTM2032"
default_channel = 1
reset_before_run = false
check_errors = true

[autoscale]
wait_opc = true
check_errors = true

[waveform]
format = "real"
byte_order = "lsbf"
points = "dmax"

[output]
directory = "data/raw"
package_naming = "timestamp_label"
save_csv = true
save_npy = true
save_json = true
save_commands_log = true
save_screenshot = false

[source]
driver = "dg4202"
resource = "TCPIP::192.168.123.3::INSTR"
default_channel = 1
check_errors = true
ensure_fix_mode_on_set_frequency = true
```

## `[connection]`

```toml
[connection]
backend = "lan"
resource = "TCPIP::192.168.1.100::INSTR"
timeout_ms = 10000
opc_timeout_ms = 30000
```

当前只支持：

```toml
backend = "lan"
```

`resource` 是 VISA 资源字符串。

当前阶段只考虑 LAN：

```text
TCPIP::<instrument-ip>::INSTR
```

## `[scope]`

```toml
[scope]
driver = "rtm2032"
model_hint = "RTM2032"
default_channel = 1
reset_before_run = false
check_errors = true
```

当前只支持：

```toml
driver = "rtm2032"
```

`reset_before_run` 默认必须为 false。第一阶段不建议通过配置启用 reset。

## `[autoscale]`

```toml
[autoscale]
wait_opc = true
check_errors = true
```

`AUToscale` 是异步命令，所以必须等待完成。

第一阶段即使配置里出现 `wait_opc = false`，程序也可以选择忽略并强制等待，避免误读波形。

## `[waveform]`

```toml
[waveform]
format = "real"
byte_order = "lsbf"
points = "dmax"
```

对应命令方向：

```text
FORM REAL
FORM:BORD LSBF
CHAN1:DATA:POIN DMAX
```

第一阶段只支持：

```text
format = real
byte_order = lsbf
points = dmax
```

暂不支持 UINT、手动点数和复杂采样范围。

## `[output]`

```toml
[output]
directory = "data/raw"
package_naming = "timestamp_label"
save_csv = true
save_npy = true
save_json = true
save_commands_log = true
save_screenshot = false

[source]
driver = "dg4202"
resource = "TCPIP::192.168.123.3::INSTR"
default_channel = 1
check_errors = true
ensure_fix_mode_on_set_frequency = true
```

默认保存：

```text
CSV + NPY + metadata.json + commands.log
```

截图第一阶段先关闭。

## 不进入第一阶段配置的内容

暂不配置：

```text
trigger
channel scale / offset / coupling
timebase
generator
experiment workflow
```

原因：第一阶段不接管前面板主要设置。加入这些配置会诱导提前写基础控制逻辑。

## `.gitignore` 规则

```gitignore
# Rei scratchpad / local helper workspace

# Local WaveBench config and generated data
wavebench.toml
data/
```

## 未来 YAML 的位置

后续如果实现实验流程编排，使用 YAML：

```text
experiments/*.yaml
```

例如：

```text
experiments/lowpass_sweep.yaml
```

TOML 和 YAML 分工：

```text
wavebench.toml        # 本机仪器连接与默认保存配置
experiments/*.yaml    # 实验步骤和流程编排
```

## 第一阶段实现建议

Python 使用标准库读取 TOML：

```python
import tomllib
```

第一阶段只需要读取配置，不需要程序写回配置，因此无需额外 TOML 写入库。


## `[source]`

```toml
[source]
driver = "dg4202"
resource = "TCPIP::192.168.123.3::INSTR"
default_channel = 1
check_errors = true
ensure_fix_mode_on_set_frequency = true
```

当前第二阶段信号源只支持：

```toml
driver = "dg4202"
```

说明：

- `resource` 是信号发生器的 VISA 资源串。
- `default_channel` 是 `wavebench source ...` 未显式传 `--channel` 时使用的通道。
- `ensure_fix_mode_on_set_frequency = true` 表示在执行 `source set-freq` 前，若仪器当前处于 `SWE` 模式，则先切到 `FIX`，避免把 sweep 频率误当成固定频率输出。
