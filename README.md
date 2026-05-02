# WaveBench

> English version: [doc/README_EN.md](doc/README_EN.md)

WaveBench 是一个面向电子设计竞赛调试场景的轻量 Python 自动测量台。

它提供小而明确的 CLI 命令，用于控制局域网内的实验室仪器。当前重点是可靠采集示波器波形、做信号源到示波器的闭环检查、控制可编程电源，以及用显式 run plan 编排多仪器实验。WaveBench 不做隐藏复位，也不偷偷打开或关闭输出。

## 当前能力

### 示波器：R&S RTM2032

- LAN VISA 连接
- `scope idn`、`scope errors`
- 显式 `scope auto` / `scope autoscale`
- `scope fetch` 与 `scope capture`
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
- `sweep discrete`：信号源到示波器的离散扫频
- 离散扫频可选 `--restore-source-state` 恢复信号源状态

### 电源：RIGOL DP800 系列

- `power idn`、`power status`
- `power set --voltage --current-limit`
- `power output on|off`
- 可配置读回等待：
  - `power.settle_ms_after_set`
  - `power.settle_ms_after_output`

### 多仪器 run plan

- `run check --plan <plan.toml>`：只解析并汇总 plan，不连接仪器
- `run plan --plan <plan.toml>`：执行显式 source、power、scope、sleep 步骤
- `run report <run_dir>`：根据 `run.json` / `summary.csv` 生成静态离线 HTML 报告，包含信号分析指标和截图
- `capture inspect <capture_dir>`：打印离线采集包摘要
- 可选示波器耦合保护：查询配置通道并拒绝不安全的电源探测计划
- 可选 `[restore] source_state = true`：在 `finally` 路径快照并恢复信号源通道状态
- run 输出位于 `data/runs/<timestamp>_<label>/`，包含 `run.json`、`summary.csv`、步骤记录、质量状态和普通采集包引用
- `scope.capture` 可启用 `quality_gate = true`；配合 `auto_recover = true` 时，质量告警会触发最多 `[quality].auto_recover_attempts` 次 autoscale + 重采
- 多次告警采集若测量结果在 `[quality]` 容差内保持稳定，可标记为 `ok_by_consistency`
- `scope.capture` 可包含 `[steps.expect]` 指标约束；expect 失败会把 run 标记为 `failed`，但保留采集产物

## 当前版本

当前包版本：`0.4.0`。

正式 GitHub Release 由项目作者发布。根目录不再保存 release note；后续 release note 草稿放在 `tool-of-rei/`。

## 安全默认值

WaveBench 避免隐藏的高影响动作：

- 默认不发送 `*RST`
- `scope capture` 不会自动 autoscale，除非用户显式请求
- `power set` 不会打开或关闭输出
- `power output` 不会修改电压或电流限制
- `sweep discrete` 不会恢复信号源函数/幅度，除非显式传入 `--restore-source-state`
- 命令不应静默修改示波器输入阻抗
- run-plan 安全保护可以查询仪器状态并拒绝执行，但不能自动修正硬件设置

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
```

检查 run plan：

```powershell
python -m wavebench run check --plan plans/example_scope_expect_quality.toml
```

执行 run plan 并生成报告：

```powershell
python -m wavebench run plan --config wavebench.toml --plan plans/example_scope_expect_quality.toml
python -m wavebench run report data/runs/<run_dir>
```

## 开发与测试

```powershell
python -m pip install -e ".[dev]"
python -m pytest -q
```

GitHub Actions 会在 push 和 pull request 时自动运行 Python 3.11 / 3.12 单元测试。

## 文档

中文文档总览：[`doc/README.md`](doc/README.md)
