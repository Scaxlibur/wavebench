# WaveBench 多仪器协同流程设计

## 背景

WaveBench 现在已经有三类仪器的显式命令：

```text
RTM2032 scope: capture/fetch/idn/errors/auto
DG4202 source: idn/status/set-freq/set-func/set-vpp/output
DP800 power : idn/status/set/output
```

下一步自然会想到自动实验流程，例如：

```text
设置电源电压 -> 设置信号源 -> 示波器采集 -> 写 summary -> 下一个条件
```

但这里必须非常克制。多仪器协同不是把几个命令粗暴串起来。电源输出、示波器输入阻抗、信号源输出状态都会影响真实硬件。流程层必须把每个会改变实验台状态的动作显式写出来。

## 目标

第一版流程层只做一件事：**把已经存在的显式 CLI/service 能力组合成可复现实验步骤**。

它应该：

- 明确每一步会读什么、写什么；
- 每个会改变仪器状态的动作都要在流程中出现；
- 每次采集继续生成普通 acquisition package；
- 额外生成一个流程级 summary；
- 出错时记录已完成步骤，不伪装成完整成功。

它不应该：

- 默认打开电源输出；
- 默认切换示波器输入阻抗；
- 默认 `*RST`；
- 自动恢复一堆没有正式设计过的状态；
- 变成通用 LabVIEW 替代品。

## CLI 形态

建议第一版命令：

```text
wavebench run plan --config wavebench.toml --plan plans/dp800_scope_probe_voltage_steps.toml
```

可选命令：

```text
wavebench run check --config wavebench.toml --plan plans/dp800_scope_probe_voltage_steps.toml
```

其中：

- `run check`：只解析计划并检查资源；若计划显式声明离线安全 guard，则只做离线结构校验，不写仪器；
- `run plan`：执行计划。

`run` 是独立 domain，不塞进 `scope` / `source` / `power`。

## 计划文件格式

第一版建议用 TOML，原因是项目已经使用 TOML，用户不用再学一种新格式。

示例：

```toml
[experiment]
name = "dp800_scope_probe_voltage_capture"
label = "dp800_scope_probe_voltage_capture"

[safety]
require_scope_coupling_not = ["DC"]
scope_guard_channel = 2

[[steps]]
kind = "power.status"
channel = 1

[[steps]]
kind = "scope.capture"
channel = 2
label = "before"
points = "def"
time_range_s = 0.01
save_csv = false

[[steps]]
kind = "power.set"
channel = 1
voltage_v = 3.3
current_limit_a = 0.1

[[steps]]
kind = "scope.capture"
channel = 2
label = "v3v3"
points = "def"
time_range_s = 0.01
save_csv = false

[[steps]]
kind = "power.set"
channel = 1
voltage_v = 5.0
current_limit_a = 0.1

[[steps]]
kind = "scope.capture"
channel = 2
label = "restore_5v"
points = "def"
time_range_s = 0.01
save_csv = false
```

注意：计划里没有 `power.output`。如果实验需要开关输出，必须显式写：

```toml
[[steps]]
kind = "power.output"
channel = 1
state = "off"
```

这不是省略项。

## 第一版 step kind 边界

计划解析层可以识别这些显式动作：

```text
scope.capture
source.status
source.set_freq
source.set_func
source.set_vpp
source.output
power.status
power.set
power.output
sleep
```

当前最小执行器已经实装并实机验证的动作是：

```text
power.status
power.set
scope.capture
sleep
```

`source.*` step 已经是计划格式的一部分，但尚未接入执行器。下一步再单独实现，避免把三仪器全开和电源安全验证混在同一次变更里。

暂不支持：

```text
条件分支
循环
表达式
并行执行
自动状态恢复
自动判定 pass/fail
```

循环很诱人，但第一版先不要。可以用多个显式 `[[steps]]` 写清楚，等格式稳定后再考虑 `matrix`。

## 安全 guard

guard 不是所有流程的标准步骤。只有计划显式声明了某个 guard 时，执行器才应该检查它。

第一版可以支持这个特殊 guard：

```toml
[safety]
require_scope_coupling_not = ["DC"]
scope_guard_channel = 2
```

含义：

```text
查询 `CHAN<scope_guard_channel>:COUP?`，例如 `scope_guard_channel = 1` 时查询 `CHAN1:COUP?`，`scope_guard_channel = 2` 时查询 `CHAN2:COUP?`
如果返回 DC，则拒绝执行
```

这是为“把 DP800 输出直接接到示波器探头上验证电源控制是否生效”的特殊接线准备的，不是普通电源控制流程的默认要求。RTM2032 的 `DC` 是 50Ω 直连，在这种接线下测电源可能损坏输入。

注意：guard 只能查询，不能自动修改示波器输入阻抗。

## 输出目录

流程级输出建议：

```text
data/runs/YYYYMMDD_HHMMSS_<experiment_label>/
  plan.toml
  run.json
  summary.csv
  steps/
    00_power_status.json
    01_scope_capture.json
```

其中 scope capture 不复制原始波形，只引用现有采集包路径：

```json
{
  "step_index": 1,
  "kind": "scope.capture",
  "package": "data/raw/20260430_...",
  "metadata": "data/raw/20260430_.../metadata.json"
}
```

避免把大文件复制来复制去。

## 错误处理

如果某一步失败：

- 立即停止；
- 写 `run.json`，标记 `status = "failed"`；
- 记录失败 step、错误类型、错误消息；
- 已经生成的 capture package 保留；
- 不执行后续步骤。

第一版不做自动 rollback。

原因：真实仪器 rollback 不是数据库事务。乱恢复比不恢复更危险。

## 当前实现状态

截至 2026-04-30，已完成并验证：

```text
run check: 解析 plan 并打印步骤摘要，不连接仪器
run plan : 执行最小 step set：power.status / power.set / scope.capture / sleep
safety  : 按 scope_guard_channel 查询 CHAN<n>:COUP?；命中 require_scope_coupling_not 时拒绝执行
output  : data/runs/YYYYMMDD_HHMMSS_<label>/run.json + summary.csv + step records
```

DP800 电压阶跃实机 smoke：

```text
plan = plans/dp800_scope_probe_voltage_steps.toml
run  = data/runs/20260430_150454_dp800_scope_probe_voltage_capture
steps = 6, status = ok
sequence = guard -> before capture -> 3.3 V set/capture -> 5 V restore/capture
scope CH2 mean ≈ 4.8826 V -> 3.1976 V -> 4.8842 V
DP800 final = output ON, set 5.0 V / 0.1 A, measured ≈ 5.0114 V
```

## 实现顺序

### Step 1：只写 parser 和 dataclass（已完成）

新增：

```text
src/wavebench/services/run_plan.py
```

数据结构：

```python
RunPlan
RunStep
SafetyGuard
```

只解析 TOML，不执行仪器。

测试：

```text
解析 power.set / scope.capture / safety guard
未知 kind 拒绝
缺必需字段拒绝
```

### Step 2：实现 run check（已完成）

新增 CLI：

```text
wavebench run check --plan <file>
```

只做：

```text
解析 plan
检查 step kind
打印步骤摘要
```

暂时不连仪器。

### Step 3：实现可选只读 guard（已完成）

仅当 plan 声明 safety guard 时连接 scope，查询 coupling。

如果 `CHAN<scope_guard_channel>:COUP? == DC`，拒绝执行。

### Step 4：实现最小执行器（已完成）

只支持：

```text
power.status
power.set
scope.capture
sleep
```

用 DP800 电压阶跃作为第一条实机流程。已在 `data/runs/20260430_150454_dp800_scope_probe_voltage_capture/` 验证通过。

### Step 5：再接 source step（下一步）

接入：

```text
source.set_freq
source.set_func
source.set_vpp
source.output
```

不要一开始就全塞进去。

## 第一条推荐实机流程

推荐从已经验证过的 DP800 电压阶跃开始：

```text
guard CH2 not 50Ω
power status
scope capture before
power set 3.3V / 0.1A
scope capture v3v3
power set 5.0V / 0.1A
scope capture restore_5v
```

它不涉及 signal generator，不涉及 output on/off，比三仪器全开更安全。

## 设计结论

多仪器协同的第一版不应该追求“聪明”。它应该像实验记录本一样直接：每一步写清楚，执行后留下证据。

WaveBench 的流程层要做的不是代替人判断风险，而是减少人重复拼脚本时犯错的机会。
