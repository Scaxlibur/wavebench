# WaveBench TUI 终端控制面板

WaveBench TUI 是实验性的终端控制面板，用于在实验台前快速查看和操作常用仪器。它不是图形 GUI，也不是 LabVIEW 式流程编排器。

## 当前范围

```text
python -m wavebench tui --config wavebench.toml
python -m wavebench tui --fake
```

当前 TUI 覆盖：

- DP800 / DP832A 电源面板
  - 显示 CH1/CH2/CH3 的输出状态、模式、规格、设定电压、限流、实测电压、电流和功率
  - 支持设置电压与电流限值
  - 支持开关输出
- DM3000 / DM3058 万用表读数面板
  - 显示连接状态、当前 function、value、unit、raw reading
  - 支持读取常用 function
- `--fake` 模式
  - 使用模拟电源和模拟万用表，不连接真实仪器

## 架构边界

TUI 只作为前端，不直接散写 SCPI。

```text
TUI -> service -> driver -> transport -> instrument
```

电源面板复用 `PowerService`；万用表面板复用 `DmmService`。因此 CLI、run plan 和 TUI 共享同一批底层安全检查、错误包装和仪器 driver。

## 刷新策略

默认刷新间隔为 5 秒：

```text
python -m wavebench tui --refresh-interval 5
```

仪器 I/O 在 Textual background worker 中执行，不在 UI 线程里同步访问仪器。若上一次自动刷新仍未完成，下一次自动刷新会跳过，避免堆积请求。

## 安全约束

电源控制保持显式分离：

```text
power set      只修改电压/电流限值，不改变 output
power output   只开关输出，不改变电压/电流限值
```

TUI 沿用同一规则。开关输出前仍会经过 service 层已有的安全上限检查。

## 暂缓内容

暂缓接入信号发生器和示波器 TUI 页面。DG4202 有 sweep/FIX、波形、幅度、偏置和任意波等状态细节；RTM2032 涉及采集、截图、高阻保护和质量门禁。它们应在电源和万用表 TUI 稳定后再做。
