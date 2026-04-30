# WaveBench run plan 使用指南

这页写给“要自己写 plan 的人”。目标不是展示所有内部实现，而是让人能在现场快速写、快速检查、看懂失败原因。

## 先看 schema，再写 plan

先运行：

```powershell
python -m wavebench run schema
```

它会列出当前代码真正支持的 step kind、必填字段和可选字段。文档可能会落后，`run schema` 以当前代码为准。

最小流程：

```powershell
python -m wavebench run schema
python -m wavebench run check --config wavebench.toml --plan plans/example_scope_expect_quality.toml
python -m wavebench run plan  --config wavebench.toml --plan plans/example_scope_expect_quality.toml
```

`run check` 只解析 plan 并打印摘要，不连接仪器。`run plan` 才会真实执行。

## 一个 step 只做一件事

例如设置电源电压不会顺手打开输出：

```toml
[[steps]]
kind = "power.set"
channel = 1
voltage_v = 3.3
current_limit_a = 0.1
```

如果要开关输出，必须另写：

```toml
[[steps]]
kind = "power.output"
channel = 1
state = "on"
```

这看起来啰嗦，但它能避免现场调试时被隐藏动作吓到。

## 常见 `run check` 报错

### step kind 拼错

错误 plan：

```toml
[[steps]]
kind = "scope.captur"
```

输出类似：

```text
wavebench: steps[0].kind 'scope.captur' is not supported. Did you mean 'scope.capture'? Supported kinds: ... Run `python -m wavebench run schema` for field details.
```

修法：改成 `scope.capture`，或先运行 `run schema` 查看支持列表。

### 字段名拼错

错误 plan：

```toml
[[steps]]
kind = "sleep"
duraton_s = 0.5
```

输出类似：

```text
wavebench: steps[0] has unknown key(s): duraton_s. Did you mean 'duraton_s' -> 'duration_s'? Allowed keys: duration_s, kind. Run `python -m wavebench run schema` for field details.
```

修法：改成 `duration_s`。

### 缺少必填字段

错误 plan：

```toml
[[steps]]
kind = "power.set"
voltage_v = 3.3
```

输出类似：

```text
wavebench: steps[0] power.set missing required field 'current_limit_a'. Required fields: voltage_v, current_limit_a. Optional fields: channel. Run `python -m wavebench run schema` for examples.
```

修法：补上 `current_limit_a`。

## `scope.capture` 的质量检查和断言

`scope.capture` 默认只采集。需要截图、质量检查或断言时都要显式写：

```toml
[[steps]]
kind = "scope.capture"
channel = 1
label = "duty_50"
window_frequency_hz = 10000
target_cycles = 10
screenshot = true
quality_gate = true
auto_recover = true

[steps.expect]
frequency_estimate_hz = { min = 9500, max = 10500 }
duty_cycle = { min = 0.45, max = 0.55 }
voltage_vpp_v = { min = 2.8, max = 3.8 }
```

含义：

- `screenshot = true`：本次采集额外保存 `screenshot.png`，并在 `metadata.json.files.screenshot` 记录路径；截图失败不会吞掉波形包。
- `quality_gate = true`：把采集质量状态写入 `run.json` / `summary.csv`。
- `auto_recover = true`：如果质量有 warning，显式执行 `scope.auto` 并重采，最多次数由 `[quality].auto_recover_attempts` 控制。
- `[steps.expect]`：对采集摘要指标做 min/max 断言。断言失败时 run 标记为 `failed`，但采集包仍保留。

## run 输出字段契约

`run plan` 会生成：

```text
data/runs/YYYYMMDD_HHMMSS_<label>/
  plan.toml
  run.json
  summary.csv
  steps/
    00_<kind>.json
    01_<kind>.json
```

### `run.json`

稳定字段：

| 字段 | 含义 |
|---|---|
| `status` | 整个 run 的状态，常见值：`ok`、`failed`。 |
| `plan` | plan 路径、实验名、label 等摘要。 |
| `safety` | safety guard 的检查结果；未启用时为空或简短状态。 |
| `restore` | source restore 的 snapshot / restore 状态；未启用时为空或简短状态。 |
| `steps` | 每个 step 的执行记录。 |

`steps[]` 常见字段：

| 字段 | 含义 |
|---|---|
| `index` | step 序号。 |
| `kind` | step kind，例如 `scope.capture`。 |
| `status` | step 状态，常见值：`ok`、`failed`。 |
| `artifact` | 该 step 产生的结构化结果。 |
| `error` | 失败时的错误类型和消息。 |

`scope.capture` 的 `artifact` 常见字段：

| 字段 | 含义 |
|---|---|
| `package` | 普通采集包路径。 |
| `metadata` | 采集包 `metadata.json` 路径。 |
| `quality` | 质量摘要，含 `status`、warnings 和关键测量指标。 |
| `quality_recovery` | 自动恢复尝试记录；未启用或未触发时可能不存在。 |
| `expect` | `[steps.expect]` 的检查结果；未配置时可能不存在。 |

### `summary.csv`

`summary.csv` 面向脚本和表格查看。常见列：

| 列 | 含义 |
|---|---|
| `step_index` | step 序号。 |
| `kind` | step kind。 |
| `status` | step 状态。 |
| `package` | scope capture 产生的采集包路径。 |
| `metadata` | 对应 `metadata.json` 路径。 |
| `quality_status` | 质量状态，例如 `ok`、`warning`、`ok_by_consistency`。 |
| `quality_warnings` | 质量 warning 摘要。 |
| `expect_status` | 断言状态，例如 `ok`、`failed`。 |
| `expect_failures` | 断言失败原因摘要。 |

后续分析脚本应优先读取 `run.json`。`summary.csv` 适合快速查看和导入表格软件。

## 现场写 plan 的顺序

建议按这个顺序来：

1. 先写 `[experiment]` 和必要的 `[safety]` / `[restore]`。
2. 每次只加 1~2 个 `[[steps]]`。
3. 运行 `run check`。
4. 确认摘要里没有隐藏动作。
5. 接上仪器后再运行 `run plan`。
6. 跑完先看 `run.json.status` 和 `summary.csv`，再看具体采集包。

别急着写很聪明的流程。电赛现场，朴素的记录更可靠。
