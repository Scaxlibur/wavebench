# WaveBench v0.4 收口清单

v0.4 的目标是把 DG4202 的真正任意波能力做成可复现的小闭环：从数组文件上传到信号源，再由 RTM2032 捕获并形成 FFT / report 证据链。

## v0.4 定位

v0.4 适合：

- 把 CSV / NPY 波形文件离线校验并映射到 DG4000/DG4202 14-bit DAC 数据。
- 通过 DG4202 `DATA:DAC VOLATILE` 上传任意波。
- 用 `source arb-load` 做最小正式入口，上传时必须显式给出播放频率。
- 用 `source.arb_load` run-plan step 把任意波上传、输出、采集和 `[steps.expect]` 检查放进同一个 plan。
- 用 RTM2032 capture、FFT inspect 和 HTML report 证明波形真的输出。

v0.4 仍不承诺：

- 任意波 GUI / 编辑器。
- 跨厂商 arbitrary waveform 抽象。
- DG4202 非 VOLATILE 存储管理。
- RAF / Ultra Station 文件工作流。
- 自动波形综合或扫参数矩阵。
- report 中完整频谱图或自动论文式分析。

## 已完成能力

- [x] DG4202 任意波 SCPI 路径确认：`DATA:DAC VOLATILE`。
- [x] `InstrumentTransport.write_bytes()` 与 PyVISA `write_raw` 二进制写入。
- [x] CSV / NPY 任意波离线 builder：归一化、NaN / inf 拒绝、点数边界、14-bit DAC 映射。
- [x] `source arb-load --dry-run` 离线校验与 payload artifact 导出。
- [x] `source arb-load --frequency ...` 实机上传入口。
- [x] `DG4202Source.upload_dg4000_dac14_block(...)` driver 方法。
- [x] `SourceService.upload_arbitrary_waveform(...)` service 方法。
- [x] `source.arb_load` run-plan step。
- [x] 三角任意波上机闭环：DG4202 CH1 -> RTM2032 CH1。
- [x] FFT 验证主峰 `1000 Hz`，Vpp 与设置一致。
- [x] README / doc README / v0.4 路线图 / 闭环验证记录更新。
- [x] `pyproject.toml` 版本号 bump 到 `0.4.0`。

## 上机证据

闭环记录见：

```text
doc/project/WaveBench_v0.4_闭环验证记录.md
```

关键结果：

```text
run=data/runs/20260501_232912_closure_arb_triangle_1k
capture=data/raw/20260501_232912_closure_arb_triangle_1k
report=data/runs/20260501_232912_closure_arb_triangle_1k/report.html
peak_frequency≈1000 Hz
peak_frequency_ok=True
vpp=1 V
```

## 发布门禁

release 前至少跑：

```bash
python -m pytest -q
git diff --check
```

当前收口验证：

```text
150 passed
git diff --check OK
```

## release notes

见仓库根目录：

```text
release-notes-v0.4.0.md
```

## tag 建议

```text
v0.4.0
```

release 标题：

```text
WaveBench v0.4.0 - arbitrary waveform closure
```
