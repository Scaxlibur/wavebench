# WaveBench v0.3 收口清单

v0.3 的目标不是扩大仪器覆盖，而是让一次 run 的离线证据更快被读懂：成功了吗、测到了什么、哪里异常。

## v0.3 定位

v0.3 适合：

- 把已有 `run.json` / `summary.csv` / `metadata.json` / `ch*.npy` 组织成更清楚的静态报告。
- 在报告第一屏给出 run status、失败步骤、warning、expect 失败、截图和主要信号指标。
- 把 `[steps.expect]` 的目标值与实测值放在一起。
- 给 capture channel 生成轻量波形预览。
- 对已有 NPY 做可选 FFT 文本摘要。

v0.3 仍不承诺：

- GUI / SPA。
- 新的 YAML 工作流语言。
- 条件分支、循环、矩阵实验。
- 交互式图表。
- 默认开启的频谱报告。
- 自动生成论文式报告。
- `run export --zip`。
- 更多仪器型号。

## 已完成能力

- [x] `run report` 顶部 Summary card。
- [x] `Expected vs measured` 表格。
- [x] 多通道 waveform preview 内联 SVG。
- [x] `report-assets/manifest.json` artifact manifest。
- [x] `capture inspect <capture_dir> --fft` 离线频谱摘要。
- [x] 报告小范围视觉整理：status badge、表格间距、截图 / 波形卡片样式。
- [x] README / doc README 更新。
- [x] `pyproject.toml` 版本号 bump 到 `0.3.0`。

## 离线边界

这些命令只读已有文件，不连接仪器：

```bash
python -m wavebench run report data/runs/<run_dir>
python -m wavebench capture inspect data/raw/<capture_dir>
python -m wavebench capture inspect data/raw/<capture_dir> --fft
```

`run report` 会生成：

```text
report.html
report-assets/manifest.json
```

它不会修改原始 `run.json`、`summary.csv`、`metadata.json` 或 `ch*.npy`。

## 发布门禁

release 前至少跑：

```bash
python -m pytest -q
```

当前收口验证：

```text
124 passed
```

如果需要实机 smoke，建议复用 v0.2 demo plan：

```bash
python -m wavebench run plan --config wavebench.toml --plan plans/demo_dg4202_10k_screenshot_report.toml
python -m wavebench run report data/runs/<run_dir>
python -m wavebench capture inspect data/raw/<capture_dir> --fft
```

## release notes

见仓库根目录：

```text
release-notes-v0.3.0.md
```

## 当前阻塞

代码已在本地提交，但当前 WSL node 上 `git push` 会超时。发布 GitHub release 前需要先把本地 ahead commits 推到远端。

当前本地分支状态：

```text
master...origin/master [ahead 7]
```

如果 push 仍不可用，可以在 Windows / GitHub Desktop / VS Code 中手动推送。

## tag 建议

```text
v0.3.0
```

release 标题：

```text
WaveBench v0.3.0 - visual evidence reports
```
