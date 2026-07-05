# WaveBench

> [!WARNING]
> 本项目仍处于早期开发阶段，会读写真实实验设备。错误操作可能导致器件、仪器损坏甚至人身伤害，使用时请务必小心。

WaveBench 是一个面向电子设计竞赛调试场景的轻量 Python 自动测量台。

它提供小而明确的 CLI 命令，用于控制局域网内的实验室仪器，也开始提供实验性的终端 TUI 控制面板。当前重点是可靠采集示波器波形、做信号源到示波器的闭环检查、控制可编程电源、读取万用表，以及用显式 run plan 编排多仪器实验。WaveBench 不做隐藏复位，也不偷偷打开或关闭输出。

## 当前能力

### 示波器：R&S RTM2032

- LAN VISA 连接
- `scope idn`、`scope errors`
- 显式 `scope auto` / `scope autoscale`
- `scope fetch` 与 `scope capture`；默认先只读确认输入为高阻，50 Ω 需显式 `--allow-50ohm`
- 通过重复 `--channel` 顺序采集多通道
- 采集包包含 NPY / CSV / JSON metadata / `commands.log`
- 波形指标：Vpp、RMS、均值、频率估计、占空比、适用时的上升/下降时间
- 波形质量告警：周期数过少、每周期采样点过少、幅度过低、频率不匹配

### 信号源：RIGOL DG4202

- `source idn`、`source status`
- `source set-freq`
- `source set-func`：`sin`、`squ`、`ramp`/`triangle`、`puls`、`nois`、`dc`
- `source set-vpp`
- `source set-duty`
- `source arb-probe`：只查询任意波 SCPI 支持情况
- `source arb-load --dry-run`：离线校验任意波 payload
- `source arb-load --frequency ... --output-on`：已确认可用的 DG4202 `DATA:DAC VOLATILE` 任意波上传
- `source output`
- `sweep discrete`：信号源到示波器的离散扫频，默认同样检查示波器高阻输入
- 离散扫频可选 `--restore-source-state` 恢复信号源状态

### 电源：RIGOL DP800 系列

- `power idn`、`power status`
- `power protection status`
- `power protection set --ovp-threshold --ovp on|off --ocp-threshold --ocp on|off`
- `power set --voltage --current-limit`
- `power output on|off`
- 可配置读回等待：
  - `power.settle_ms_after_set`
  - `power.settle_ms_after_output`


### 万用表：RIGOL DM3000 / DM3058 系列

- `dmm idn`
- `dmm read dcv|acv|dci|aci|res|fres|freq|period|continuity|diode|cap`
- 第一阶段支持 DM3058 LAN/VISA 读取，并保留 DM3000 RS232 skeleton；设备 SCPI 保留在 DMM driver，不进入 CLI / service。
- 可配置 DMM 正式读取前等待：`dmm.settle_ms_before_read`
- 可用 `python scripts/dmm_dcv_staircase_smoke.py --config <toml>` 对 `DP800 -> DMM` 做保守 DCV 阶梯 smoke，并自动恢复电源输出。
- 可用 `python scripts/dmm_acv_source_smoke.py --config <toml>` 对 `DG4202 -> DMM` 做保守 ACV/RMS smoke，并自动恢复信号源状态。


### 终端 TUI：实验性控制面板

- `tui`：启动 Textual 终端界面，默认读取当前目录的 `wavebench.toml`。
- `tui --config <toml>`：从指定 TOML 读取仪器配置，适合不在配置文件目录启动时使用。
- `tui --fake`：使用模拟电源、模拟万用表和模拟信号源，不连接真实仪器，适合检查界面。
- `tui --refresh-interval 5`：设置自动刷新间隔；默认 5 秒。
- `tui --log-file <path>`：指定 TUI 调试日志文件；默认写入 `data/tui/wavebench-tui.log`。
- TUI 持久日志行数限制可在 `[tui]` 中配置，默认超过 10000 行后保留最新 1000 行。
- 电源面板支持三通道状态查看、设置电压/限流、开关输出、查看和设置 OVP/OCP。
- 万用表面板支持常用挡位按钮切换和手动读取。
- 信号源面板支持查看状态、设置波形/频率/幅度和切换输出。

### 多仪器 run plan

- `run check --plan <plan.toml>`：只解析并汇总 plan，不连接仪器
- `run verify --plan <plan.toml>`：只读查询 plan 涉及仪器的高阻保护状态与 `*IDN?`，用于执行前预检可达性
- `run template --list` / `run template <name> --output <plan.toml>`：列出或生成保守 run plan 模板；可用 `--frequency`、`--vpp`、`--source-channel` 等少量参数定制；不连接仪器，不覆盖已有文件，除非显式 `--force`
- `run plan --plan <plan.toml>`：执行显式 source、power、scope、dmm、sleep 步骤
- `run report <run_dir>`：根据 `run.json` / `summary.csv` 生成静态离线 HTML 报告，包含信号分析指标、DMM 读数卡片、实验证据摘要、产物链接、证据时间线和截图
- `capture inspect <capture_dir>`：打印离线采集包摘要
- 默认示波器高阻保护：`scope.capture` / `scope.fetch` / `sweep discrete` / run-plan `scope.capture` 在采集前查询 `CHAN<n>:COUP?`；`DCL`/`ACL` 视为高阻，`DC`/`AC` 默认拒绝，只有显式 `--allow-50ohm` 或 `[safety] allow_50ohm = true` 才放行
- 可选 `[restore] source_state = true`：在 `finally` 路径快照并恢复信号源通道状态
- run 输出位于 `data/runs/<timestamp>_<label>/`，包含 `run.json`、`summary.csv`、步骤记录、质量状态和普通采集包引用
- `scope.capture` 可启用 `quality_gate = true`；配合 `auto_recover = true` 时，质量告警会触发最多 `[quality].auto_recover_attempts` 次 autoscale + 重采
- 多次告警采集若测量结果在 `[quality]` 容差内保持稳定，可标记为 `ok_by_consistency`
- `scope.capture` 可包含 `[steps.expect]` 指标约束；expect 失败会把 run 标记为 `failed`，但保留采集产物

### 网络发现：只读辅助工具

- `doctor --config <toml>`：只读检查当前配置里的 scope/source/power/dmm 资源，查询 `*IDN?` 并给出可达性、型号匹配和排错建议
- `doctor --discover-subnet <cidr>`：当配置资源不可达或型号不匹配时，顺手扫描网段并按 IDN 匹配可能的替代 resource；只建议，不修改配置
- `net discover --subnet <cidr>`：只读扫描局域网内疑似 SCPI/VISA 仪器，用于 DHCP 漂移后找回当前 IP
- 默认探测 `5025`、`5555` 和 `111` 端口；对 SCPI socket 候选只发送只读 `*IDN?`
- 输出可复制的 VISA resource 候选；不会修改 `wavebench.toml`，也不会打开/关闭任何仪器输出
- 发现命令是救急工具；稳定实验环境仍建议在路由器/DHCP 服务里按 MAC 地址固定仪器 IP

### 插件注册表：只读能力目录

- `plugin list`：列出当前可用的仪器插件 metadata
- `plugin info <driver_id>`：查看单个插件的型号、能力、IDN 匹配和配置字段
- `plugin doctor`：检查插件 metadata 的 API 版本、能力命名、类型和加载错误
- `plugin market search [query]`：搜索本地插件市场 JSON 索引
- `plugin market info <plugin_id>`：查看本地插件市场条目
- `plugin scpi check <path>`：检查本地声明式 SCPI 插件 TOML
- `plugin scpi doctor <path>`：诊断本地声明式 SCPI 插件，可显式加 `--probe --resource <VISA>` 做只读 IDN 匹配
- `plugin scpi info <path>`：查看本地声明式 SCPI 插件 metadata
- `plugin scpi probe <path> --resource <VISA>`：对单个资源执行插件声明的只读 IDN 查询
- 默认只显示 WaveBench 内置插件，不导入第三方包
- 只有显式传入 `--include-entry-points` 时，才加载 Python `wavebench.drivers` entry points
- 插件市场当前只读本地 JSON index，不安装插件，不导入市场条目里的包
- 声明式 SCPI 插件默认只读取并校验本地 TOML；只有显式执行 `plugin scpi probe` 才会对单个资源发送 TOML 中声明的只读 IDN 查询

### HTTP MCP 只读接口

- `mcp serve`：启动本机 HTTP MCP 只读服务
- 默认监听 `127.0.0.1:8765`；显式传入 `0.0.0.0` 会被拒绝
- `/health`：健康检查，不需要 token
- `/mcp`：MCP JSON-RPC 入口，支持 `initialize`、`tools/list`、`tools/call`，需要 Bearer token
- `/tools`：兼容接口，返回当前只读工具列表，需要 Bearer token
- `/call`：兼容接口，调用只读工具，需要 Bearer token
- 当前只读工具：
  - `run.schema`：返回 run plan schema
  - `run.check`：只解析并检查 `plans/*.toml` 下的 run plan，不连接仪器
  - `capture.inspect`：读取 `data/raw/` 下的离线采集包摘要
- `/mcp` 与 `/call` 的 JSON 请求体有 1 MiB 上限；路径参数按工具限制在项目内固定目录

## 安全默认值

WaveBench 避免隐藏的高影响动作：

- 默认不发送 `*RST`
- `scope capture` 不会自动 autoscale，除非用户显式请求
- `scope fetch` / `scope capture` 默认拒绝可能的 50 Ω 输入；只查询状态，不自动切换 coupling
- `power set` 不会打开或关闭输出
- `power output` 不会修改电压或电流限制
- `power protection` 与普通电压/限流和输出控制分离；写入保护阈值前会检查当前设定值和安全上限
- `sweep discrete` 不会恢复信号源函数/幅度，除非显式传入 `--restore-source-state`
- `sweep discrete` 默认拒绝示波器 50 Ω 输入；确认安全后才可传 `--allow-50ohm`
- 命令不应静默修改示波器输入阻抗
- run-plan 安全保护可以查询仪器状态并拒绝执行，但不能自动修正硬件设置
- HTTP MCP 默认只监听 `127.0.0.1`，拒绝 `0.0.0.0`，并对 `/mcp`、`/tools` 与 `/call` 强制 Bearer token
- HTTP MCP 当前只暴露只读工具，不提供 raw SCPI、输出开关、run 执行或任何会改变仪器状态的工具
- `plugin list/info/doctor` 默认不导入第三方插件；加载 Python entry points 必须显式传入 `--include-entry-points`

用示波器测量电源时，请保持示波器输入在安全的高阻模式。除非已经确认电压和仪器限制，否则不要切换到 50 Ω 端接。

## 快速开始

```powershell
python -m pip install -e .
copy wavebench.example.toml wavebench.toml
python -m wavebench scope idn --config wavebench.toml
```

如果没有 editable install，也可以在项目根目录运行：

```powershell
$env:PYTHONPATH = "src"
python -m wavebench scope idn --config wavebench.toml
```

## 示例命令

采集示波器波形：

```powershell
python -m wavebench scope capture --config wavebench.toml --channel 1 --label smoke --points def --window-frequency 1000 --target-cycles 10 --expect-frequency 1000 --frequency-tolerance 0.05 --target-vpp 1.0 --no-csv
python -m wavebench scope capture --config wavebench.toml --channel 1 --label smoke_with_screen --points def --no-csv --screenshot
```


启动实验性 TUI：

```powershell
python -m wavebench tui
python -m wavebench tui --config wavebench.toml
python -m wavebench tui --log-file data/tui/wavebench-tui.log
python -m wavebench tui --fake
```

启动 HTTP MCP 只读服务：

```powershell
python -m wavebench mcp serve --config wavebench.toml --token-env WAVEBENCH_MCP_TOKEN
```

调用方访问 `http://127.0.0.1:8765/health` 可做健康检查；访问 `/mcp`、`/tools` 和 `/call` 时需要发送 Bearer token。

只读扫描局域网仪器：

```powershell
python -m wavebench doctor --config wavebench.toml
python -m wavebench doctor --config wavebench.toml --discover-subnet 192.168.1.0/24 --discover-timeout-ms 500
python -m wavebench net discover --subnet 192.168.1.0/24
python -m wavebench net discover --subnet 192.168.1.0/24 --idn-only --timeout-ms 500
```

查看插件注册表：

```powershell
python -m wavebench plugin list
python -m wavebench plugin info rigol.dg4202
python -m wavebench plugin doctor
python -m wavebench plugin list --include-entry-points
python -m wavebench plugin market search rigol
python -m wavebench plugin market info wavebench-rigol-dg4202
python -m wavebench plugin scpi check doc/project/scpi-plugin.example.toml
python -m wavebench plugin scpi doctor doc/project/scpi-dp800.example.toml --probe --resource TCPIP::192.168.1.161::INSTR
python -m wavebench plugin scpi info doc/project/scpi-plugin.example.toml
python -m wavebench plugin scpi probe doc/project/scpi-dp800.example.toml --resource TCPIP::192.168.1.161::INSTR
```

设置 DG4202 信号源频率：

```powershell
python -m wavebench source set-freq --config wavebench.toml --channel 1 1000
```

执行离散扫频：

```powershell
python -m wavebench sweep discrete --config wavebench.toml --source-channel 1 --scope-channel 1 --frequencies 1000,2000,5000,10000 --target-cycles 10 --frequency-tolerance 0.05 --label dg4202_discrete_sweep --no-csv
```

执行带信号源状态恢复的扫频：

```powershell
python -m wavebench sweep discrete --config wavebench.toml --source-channel 1 --scope-channel 1 --frequencies 1000,5000 --source-func SQU --source-vpp 3.3 --restore-source-state --no-csv
```

读取 DP800 电源状态：

```powershell
python -m wavebench power status --config wavebench.toml
python -m wavebench power protection status --config wavebench.toml
```

设置 DP800 电压/限流但不改变输出状态：

```powershell
python -m wavebench power set --config wavebench.toml --channel 1 --voltage 5.0 --current-limit 0.1
```

显式打开或关闭 DP800 输出；该命令不会修改电压/电流限值：

```powershell
python -m wavebench power output --config wavebench.toml --channel 1 off
python -m wavebench power output --config wavebench.toml --channel 1 on
```

设置 DG4202 波形和方波占空比但不隐式改变输出状态：

```powershell
python -m wavebench source set-func --config wavebench.toml --channel 1 triangle
python -m wavebench source set-duty --config wavebench.toml --channel 1 25
```

只读探测 DG4202 任意波 SCPI 候选，不上传、不改变输出状态：

```powershell
python -m wavebench source arb-probe --config wavebench.toml --channel 1 --probe-timeout-ms 700
```

离线准备任意波 payload，校验 CSV/NPY 波形并可导出归一化 + 14-bit DAC payload：

```powershell
python -m wavebench source arb-load --channel 1 --file waveform.npy --name REI_ARB --amplitude 1.0 --offset 0.0 --export-payload data/arb/REI_ARB.json --dry-run
```

上传已确认的 DG4202 任意波并显式打开输出：

```powershell
python -m wavebench source arb-load --config wavebench.toml --channel 1 --file waveform.npy --name REI_TRI --amplitude 1.0 --frequency 1000 --offset 0.0 --output-on
```

检查 run plan：

```powershell
python -m wavebench run schema
python -m wavebench run template --list
python -m wavebench run template source-scope-sine --output plans/source_scope_sine_1k.toml
python -m wavebench run template source-scope-sine --frequency 10000 --vpp 3.3 --source-channel 2 --scope-channel 1 --output plans/source_scope_sine_10k.toml
python -m wavebench run check --plan plans/example_scope_expect_quality.toml
python -m wavebench run check --plan plans/closure_sine_1k.toml
python -m wavebench run check --plan plans/closure_triangle_1k.toml
```

执行 run plan 并生成报告：

```powershell
python -m wavebench run plan --config wavebench.toml --plan plans/example_scope_expect_quality.toml
python -m wavebench run report data/runs/<run_dir>
```

DMM ACV smoke 示例：

```powershell
python -m wavebench run verify --config wavebench.toml --plan plans/example_dmm_acv_source_smoke.toml
python -m wavebench run plan --config wavebench.toml --plan plans/example_dmm_acv_source_smoke.toml
```

DMM `dmm.read` 可用 `[steps.expect]` 对读数做门禁，例如 `value = { min = 0.34, max = 0.37 }`。

公开闭环示例：

```powershell
python -m wavebench run check --config wavebench.toml --plan plans/closure_sine_1k.toml
python -m wavebench run check --config wavebench.toml --plan plans/closure_triangle_1k.toml
```


Run plan 可选择在成功或失败路径恢复信号源状态：

```toml
[restore]
source_state = true
source_channel = 1
```

启用后，WaveBench 会在执行步骤前快照 output/function/frequency/amplitude/方波 duty，并在结束时恢复。

Run plan 中的 `scope.auto` 是显式步骤，对应 RTM2032 `AUToscale` 并等待 `*OPC?`；`scope.capture` 不会隐式插入 autoscale：

```toml
[[steps]]
kind = "scope.auto"

[[steps]]
kind = "scope.capture"
channel = 1
label = "after_auto"
```

Run plan 也可以显式组合任意波上传、采集和断言。示例中的输出打开是 `output_on = true` 明确请求，不是默认行为：

```toml
[[steps]]
kind = "source.arb_load"
channel = 1
file = "data/arb/triangle_1024.npy"
frequency_hz = 1000
amplitude_vpp = 1.0
offset_v = 0.0
output_on = true

[[steps]]
kind = "scope.capture"
channel = 1
label = "arb_triangle_1k"
window_frequency_hz = 1000
target_cycles = 10
target_vpp = 1.0
screenshot = true

[steps.expect]
voltage_vpp_v = { min = 0.8, max = 1.2 }
frequency_estimate_hz = { min = 950, max = 1050 }
```

## 开发与测试

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
```

GitHub Actions 会在 push 和 pull request 时自动运行 Python 3.11 / 3.12 单元测试。
