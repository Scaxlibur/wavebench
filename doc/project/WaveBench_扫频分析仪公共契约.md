# WaveBench 扫频分析仪公共契约

[English version](WaveBench_sweep_analyzer_contract_EN.md)

## 范围

WaveBench 将独立扫频分析仪建模为 `sweep_analyzer`。`frequency_response` 是这类仪器返回的通用数据域，不是另一个 instrument kind。

当前契约只提供硬件无关的公共模型、driver Protocol 和 capability 到方法的映射。它没有接入 Service、CLI、配置、run plan、artifact 或任何具体仪器，也不代表某个厂商协议、型号、选件或 transport 已通过验证。

## 公共模型

- `SweepPlan`：CW 或 sweep；sweep 使用 start/stop 或 center/span 两种互斥频率窗口之一；还可表达线性/对数轴、自动/手动时间、单次/连续采集、内/外触发、平均、点数以及源输出、电平和阻抗。
- `SweepAnalyzerSnapshot`：分别保存 `requested_plan` 与设备回读形成的 `effective_plan`。恢复和验收必须以后者为准，不能把请求值当成已生效值。
- `FrequencyResponseTrace`：保存可选的频率轴、幅度和相位数组。轴来源必须明确为 `device`、`derived` 或 `unknown`；幅度同时携带单位与 `absolute`、`relative`、`linear` 或 `unknown` 语义。
- `TraceIntegrity`：保存期望点数、实际点数、完整性和 warning。部分数据不能补零、静默截断或标成完整成功。
- `MarkerReading`：保存 marker 频率、幅度、相位和 delta 读数；绝对幅度与 delta 幅度分别声明单位。
- `InstrumentMeasurementResult`：使用 `method` 区分仪器内建结果和 WaveBench core 重算结果。

所有 trace 数组都会复制成只读 `float64` 数组，并拒绝空数组、非有限值、长度不一致和非正频率。采集时间必须带时区。`raw_evidence_ref` 只保存脱敏 artifact 引用，不保存真实资源、序列号或原始私密路径。

## Driver 与 capabilities

`SweepAnalyzerDriver` 延续现有 WaveBench 的原子能力风格：

| Capability | 方法 |
| --- | --- |
| `sweep_analyzer.idn` | `idn()` |
| `sweep_analyzer.status` | `get_snapshot()` |
| `sweep_analyzer.trace` | `fetch_frequency_response()` |
| `sweep_analyzer.configure` | `apply_sweep_plan()` |
| `sweep_analyzer.trigger` | `trigger_single()` |
| `sweep_analyzer.output` | `set_source_output()` |
| `sweep_analyzer.marker` | `read_markers()` |
| `sweep_analyzer.analysis` | `read_measurements()` |

插件只声明它真实实现并验证过的能力。Descriptor 声明的方法缺失时，核心会在 driver 打开后校验失败；kind/capability 不匹配或未知 capability 会在 registry 检查阶段失败。

`apply_sweep_plan()` 不得隐式把源输出从关闭切换为打开；启用 RF 必须经由独立的 `set_source_output(True)` 动作和上层显式授权。计划与 snapshot 中的 `source_output_enabled` 用于表达请求值或有效回读值，不能替代该安全动作。

## 明确延后

以下内容不属于当前核心契约：

- 连续 trace streaming、进度和取消；
- 厂商命令、ACK、状态编码和 parser；
- 外检波、鉴频、反射或驻波等选件 API；
- calibration、fixture 和误差修正模型；
- Service、CLI、配置、run plan 和 artifact 序列化；
- 具体型号的频率、电平、点数或 marker 数量上限。

这些能力应在真实协议证据和恢复语义明确后单独扩展，不能由通用模型反推设备能力。
