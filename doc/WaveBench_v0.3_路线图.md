# WaveBench v0.3 路线图

v0.2 已经把 run / capture 的证据变成了可读 HTML：步骤、截图、信号指标都能离线查看。v0.3 不应该急着做 GUI，也不应该把 run plan 变成复杂工作流语言。

v0.3 的主题是：

```text
让报告一打开就能回答：这次实验成功了吗？测到了什么？哪里异常？
```

## v0.3 目标

```text
从“可读报告”走到“可视化证据包”。
```

具体目标：

- 报告顶部提供清楚的 Summary card。
- 报告中直接展示轻量波形预览，不要求读者手动打开 NPY。
- 把 `[steps.expect]` 的目标值和实测值放在一起，减少翻 JSON 的次数。
- 以可选离线方式补强常见信号处理，例如 FFT / 频谱摘要，但不塞进默认报告第一屏。
- 继续保持离线报告：`run report` 不连接仪器，不改变原始采集包。
- 继续保持静态 HTML：不引入前端框架，不做 GUI。

## 设计原则

### 1. 报告只读已有 artifact

`run report` 仍然只读取：

```text
run.json
summary.csv
metadata.json
ch*.npy
screenshot.png
```

禁止：

```text
report -> drivers
report -> transport
report -> instrument
```

报告可以生成派生预览文件，但不能修改原始 capture metadata / NPY。

### 2. Summary card 先于漂亮图表

v0.3 第一刀应该让报告顶部变得有判断力：

- run status
- total steps
- failed steps
- capture count
- warning count
- expectation pass/fail
- screenshot count
- primary measured frequency / Vpp（如果存在）

这比先做复杂图更重要。打开报告第一屏就应该知道结果。

### 3. 波形预览要轻，不要变成分析平台

波形预览只做“看一眼形状”：

- 从 `ch*.npy` 读取时间 / 电压。
- 下采样到适合报告显示的点数。
- 生成静态 SVG 或小 PNG。
- 嵌入 HTML。

不做：

- 交互式缩放。
- 浏览器端大数组渲染。
- 复杂滤波 / FFT。
- 替代专业示波器或 Origin / Python 分析。

### 4. expected vs measured 要服务现场判断

如果 run step 有 `[steps.expect]`，报告应展示：

```text
metric | expected range | measured | status
```

这比单独列 failures 更容易读。


### 5. 信号处理要可选、可解释

FFT 有必要做，但应该作为“离线分析工具”逐步加入，而不是默认把报告变成重型分析平台。

适合加入：

- FFT / 频谱峰值摘要。
- 基波频率、主要谐波、THD 粗估。
- 噪声地板 / SNR 的轻量估计。
- 用于发现开关电源纹波、振铃、杂散峰的频谱小图。

边界：

- 默认 `run report` 第一屏仍然优先结论和 pass/fail。
- FFT 使用 capture 中已有 `ch*.npy`，不连接仪器。
- 窗函数、采样率、频率分辨率要写清楚，避免给出看起来很精确但其实不可靠的数字。
- 大数组要下采样或限制频点，不把完整频谱塞进 HTML。

推荐形态：

```text
capture inspect <capture_dir> --fft
run report <run_dir> --include-spectrum
```

先做 inspect 里的文本摘要，再考虑 report 里的频谱小图。

## 候选工作包

### A. Report summary card

在 `report.html` 顶部新增 Summary card 区块。

建议内容：

| 字段 | 来源 |
|---|---|
| Run status | `run.json.status` |
| Experiment label | `run.json.experiment.label` |
| Steps | `run.json.steps` |
| Failed steps | `steps[].status` |
| Captures | `steps[].artifact.package` |
| Warnings | `steps[].artifact.quality.warnings` + metadata warnings |
| Expectations | `steps[].artifact.expect.status` |
| Screenshots | capture metadata `files.screenshot` |
| Restore | `run.json.restore.status` |

验收标准：

- 没有 capture 的 run 也能生成 summary。
- failed run 能把失败原因放在第一屏。
- 不读取 NPY，不连接仪器。
- 单元测试覆盖 ok / failed / no capture 三类 run。

### B. Expected vs measured table

把 `[steps.expect]` 的 checks 渲染成独立表格。

示例：

```text
Step 7 - scope.capture
frequency_estimate_hz | 9500..10500 | 10000.0 | ok
voltage_vpp_v         | >= 0.05     | 0.8     | ok
```

验收标准：

- 兼容已有 `artifact.expect.checks` 结构。
- failed checks 高亮。
- unavailable / not_numeric 能读懂。
- 没有 expect 时不显示空表。

### C. Waveform preview artifacts

为每个 capture channel 生成轻量波形预览。

候选实现：

```text
report-assets/
  step7_ch1_waveform.svg
```

或直接内联 SVG。

输入：

```text
ch1.npy / ch2.npy
```

输出：

- time-voltage line preview
- min/max 标注可选
- 图标题包含 step、channel、frequency、Vpp

验收标准：

- 读取 NPY 失败时不影响报告生成，只显示 warning。
- 对大数组做下采样，避免 HTML 过大。
- 多通道 capture 每个通道一张预览。
- 不新增重依赖；优先用标准库 + numpy 生成 SVG。

### D. Report artifact manifest

报告生成后写一个轻量 manifest，便于后续复制 / 打包：

```text
report-assets/manifest.json
```

内容：

- report path
- referenced screenshots
- generated waveform previews
- source capture packages
- missing artifacts / warnings

验收标准：

- manifest 只记录路径和状态，不复制原始数据。
- 方便以后做 `run export`，但 v0.3 暂不做 zip export。

### E. Optional FFT / spectrum summary

为已有 capture 增加可选频谱分析。

第一阶段只做文本摘要：

```text
peak frequency
peak amplitude
noise floor estimate
first few harmonic bins
THD rough estimate（可选）
```

候选入口：

```bash
wavebench capture inspect <capture_dir> --fft
```

后续再考虑：

```bash
wavebench run report <run_dir> --include-spectrum
```

验收标准：

- 明确使用的窗口函数和采样率。
- 对非均匀采样、样本太少、缺少 dt 的数据给出清楚 warning。
- 不连接仪器。
- 不影响默认报告生成速度。

### F. Report visual polish

只做小范围排版，不做前端应用。

可做：

- status badge
- warning / failed 高亮
- summary card 网格
- Signal analysis 表格更紧凑
- 截图和波形预览并排展示

不做：

- SPA。
- JS 图表库。
- 大型 CSS 框架。

## 推荐顺序

```text
1. Report summary card
2. Expected vs measured table
3. Waveform preview SVG
4. Optional FFT / spectrum summary
5. Report artifact manifest
6. 视觉整理
```

理由：

- Summary card 最小、收益最大，完全离线，不引入新数据路径。
- Expected vs measured 复用已有 `expect` 数据结构，能快速提高报告判断力。
- Waveform preview 需要读取 NPY 和处理大数组，放在前两者稳定之后。
- FFT 值得做，但要先作为可选离线分析，不抢默认报告第一屏。
- manifest 是为后续导出铺路，但不应该抢 v0.3 第一刀。

## v0.3 暂不做

- GUI。
- YAML 工作流。
- 复杂 run plan 语法。
- 条件分支、循环、矩阵实验。
- 交互式图表。
- 默认开启的 FFT / 频谱分析。
- 自动生成论文式报告。
- `run export --zip`。
- 更多仪器型号。

这些以后可以做，但不是现在。

## 第一刀建议

先做：

```text
Report summary card
```

最小实现范围：

- 新增 summary 统计函数，输入 `RunPackage`。
- HTML 顶部新增 `<section class="summary-card">`。
- 展示 run status、steps、captures、warnings、expect failed、screenshots、restore。
- 单元测试覆盖 ok / failed / no capture。

如果这刀干净，再做 Expected vs measured table。

## 一句话原则

```text
v0.3 不是让 WaveBench 更像平台，而是让一份报告更快告诉人：实验到底发生了什么。
```
