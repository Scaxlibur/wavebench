# WaveBench v0.2 收口清单

v0.2 的目标不是扩大仪器覆盖，而是让 v0.1 留下的采集证据更容易被人读懂、复盘和分享。

## v0.2 定位

```text
从“能采、能跑、能留证据”走到“能读、能看、能复盘”。
```

v0.2 适合：

- 离线查看 `data/raw/...` 采集包。
- 离线查看 `data/runs/...` 实验流程包。
- 从已有 `run.json` / `summary.csv` / `metadata.json` 生成静态 HTML 报告。
- 在采集包里保存示波器截图，并让报告自动引用截图。
- 在报告里直接看到每次采集的频率、Vpp、RMS、均值、duty、rise/fall 和质量 warning。

v0.2 仍不承诺：

- GUI。
- YAML 工作流。
- 条件分支、循环、矩阵实验。
- 自动修正仪器状态。
- 支持更多仪器型号。
- PyPI 发布。

## 已完成能力

### 离线包读取

- [x] `wavebench.data.packages.load_capture_package(path)`。
- [x] `wavebench.data.packages.load_run_package(path)`。
- [x] 单通道 capture metadata 读取。
- [x] 多通道 capture metadata 读取。
- [x] `summary.csv` 读取。
- [x] 缺文件 / 格式错误时给出明确 `ConfigError`。

### 离线命令

- [x] `capture inspect <capture_dir>`。
- [x] `run report <run_dir>`。
- [x] 离线命令只读已有文件，不连接仪器。
- [x] 报告生成失败不改写原始 `run.json` / `metadata.json`。

### 截图 artifact

- [x] `scope capture --screenshot`。
- [x] run plan `scope.capture screenshot = true`。
- [x] RTM2032 `HCOP:DATA?` PNG 截图路径实机验证。
- [x] `metadata.json.files.screenshot` 记录截图路径。
- [x] 截图失败时保留波形采集结果，并记录 `screenshot_error`。

### 报告

- [x] 静态 `report.html`。
- [x] Run 状态、实验名、restore 状态。
- [x] Steps 表。
- [x] Screenshot 缩略图列。
- [x] Screenshots 大图区块。
- [x] Signal analysis 区块：频率、Vpp、RMS、均值、duty、rise/fall、quality warnings。
- [x] 相对路径引用截图，不复制原始图片。
- [x] `report/` 不 import `drivers` / `transport`。

### Demo

- [x] `plans/demo_dg4202_10k_screenshot_report.toml`。
- [x] DG4202 CH2 输出 10 kHz 方波。
- [x] RTM2032 CH1 采集波形 + 截图。
- [x] Source state restore。
- [x] 断言频率和可见信号幅度。
- [x] 生成带 Signal analysis 和 Screenshots 的 HTML 报告。

## 已知边界

- Signal analysis 只汇总 metadata 里已有的波形摘要，不重新读取 NPY 做二次分析。
- Duty / rise / fall 只在波形和算法适用时出现；不可用时留空。
- Demo plan 不假设探头倍率或精确前端缩放，只检查频率和可见幅度。
- 报告是静态 HTML，不引入前端框架。
- 截图是 capture artifact，不是 report 副作用；`run report` 永远不连接仪器。

## release 前门禁

```bash
python -m unittest discover -s tests -p 'test*.py'
python -m wavebench run schema
python -m wavebench run check --config wavebench.example.toml --plan plans/example_scope_expect_quality.toml
python -m wavebench run check --config wavebench.example.toml --plan plans/demo_dg4202_10k_screenshot_report.toml
git diff --check
```

实机 smoke：

```bash
python -m wavebench run plan --config <local-multi-instrument-config.toml> --plan plans/demo_dg4202_10k_screenshot_report.toml
python -m wavebench run report data/runs/<demo_run_dir>
```

报告应包含：

- `Signal analysis` 区块。
- `Screenshots` 区块。
- 10 kHz 附近的频率。
- 非零 Vpp。
- `status = ok`，`restore = ok`，`expect = ok`。

公开资料隐私扫描范围：

```text
README.md
release-notes-v0.2.0.md
doc/*.md
wavebench.example.toml
plans/*.toml
```

排除厂商手册/摘录类 source material。检查项：真实局域网 IP、账号、设备序列号、凭据、私有路径。

## release notes 草案

见仓库根目录：`release-notes-v0.2.0.md`。

## 发布建议

建议 tag：

```text
v0.2.0
```

release 标题：

```text
WaveBench v0.2.0 - readable evidence reports
```

公开 push、tag、GitHub release 前仍需要人确认。
