# WaveBench v0.4 路线图

v0.3 已经把采集证据变成了可视化报告。v0.4 不应该立刻去做 GUI 或更复杂的 run plan。下一步更有用的是让 WaveBench 也能生成实验信号。

v0.4 的主题是：

```text
不只测量信号，也生成信号。
```

第一目标：RIGOL DG4202 任意波形输出 MVP。

## 先回答：VISA 支不支持任意波形？

VISA 支持把任意波形所需的数据传给仪器，包括文本命令和 IEEE binary block。真正决定能不能做的是 DG4202 的 SCPI 命令集。

也就是说：

```text
VISA = 通道
SCPI = 仪器听得懂的话
任意波形 = DG4202 固件是否提供上传 / 选择 / 播放命令
```

已知事实：

- DG4202 已通过 PyVISA/NI-VISA 连接，`TCPIP::192.168.123.3::INSTR` 可用。
- 当前 WaveBench 已支持 DG4202 的 IDN、status、function、frequency、Vpp、output、square duty。
- DG4000 系列是函数 / 任意波形发生器，硬件类别支持任意波形。

尚未确认：

- 任意波形上传的确切 SCPI 命令。
- 上传格式：DAC 整数、归一化浮点、ASCII list、binary block，或 RAF 文件。
- volatile / user memory 的命名和容量。
- 播放参数是按 waveform frequency、sample rate，还是 period 控制。
- 上传后如何选择用户波形并输出。

所以 v0.4 第一刀不是写上传代码，而是确认命令表。

## 设计原则

### 1. 先做 DG4202，不急着跨厂商抽象

任意波形上传非常依赖厂商命令。先把 DG4202 跑通，再考虑更高层接口。

### 2. 默认不改变输出状态

任意波形可能接着真实电路。任何上传命令默认只写入/选择波形，不自动打开 output。

如果要开输出，必须显式写：

```bash
--output-on
```

### 3. 数据构建和仪器上传分开

离线 waveform builder 只负责：

- 读取 CSV / NPY。
- 检查 NaN / inf。
- 检查点数。
- 归一化到安全范围。
- 生成待上传 payload。

DG4202 driver 只负责：

- 发送 SCPI。
- 查询错误队列。
- 返回状态。

### 4. 必须有示波器闭环验证

任意波形上传成功不等于输出正确。最小闭环应该是：

```text
source arb upload -> source output -> scope capture -> run report / capture inspect
```

## 候选工作包

### A. DG4202 任意波形命令确认表

新增 `doc/DG4202_任意波形命令确认表.md`。

要确认：

| 项目 | 状态 |
|---|---|
| 编程手册来源 | 未确认 |
| 上传命令 | 未确认 |
| 数据格式 | 未确认 |
| 最大点数 | 未确认 |
| 波形命名 / 存储位置 | 未确认 |
| 选择用户波形命令 | 未确认 |
| 播放频率 / 采样率命令 | 未确认 |
| 输出打开是否独立控制 | 预计是，需验证 |
| 错误队列检查 | 已有 `SYST:ERR?` 机制 |

验收标准：

- 找到可引用的 DG4000/DG4202 programming guide 或通过实机 `SYST:ERR?` probe 确认命令。
- 不向电路输出未知波形。
- 文档里记录成功 / 失败命令和错误码。

### B. Offline waveform builder

新增纯离线 builder：

```text
CSV / NPY -> normalized waveform payload
```

验收标准：

- 支持一列电压或两列 time/voltage。
- 拒绝 NaN / inf。
- 拒绝点数太少。
- 可选择归一化到 `[-1, 1]` 或生成 14-bit DAC 整数。
- 单元测试覆盖正弦、方波、非法数据。

### C. DG4202 driver upload 方法

候选接口：

```python
DG4202Source.upload_arbitrary_waveform(
    channel=2,
    name="REI_ARB",
    points=payload,
    sample_rate_hz=...,  # 或 playback_frequency_hz，取决于手册
)
```

验收标准：

- fake transport 测命令顺序。
- 默认不打开 output。
- 上传后检查错误队列。
- 命令失败时不吞掉错误。

### D. CLI 实验入口

候选命令：

```bash
wavebench source arb-load --channel 2 --file waveform.npy --name REI_ARB --amplitude 1.0 --offset 0.0
```

可选：

```bash
--output-on
```

验收标准：

- 默认不改变 output state。
- 输出 payload 摘要：points、min、max、sample rate / playback setting。
- `--dry-run` 能打印将要发送的摘要，不连接仪器。

### E. Scope 闭环验证计划

新增 demo plan 或手工验证流程：

```text
DG4202 CH2 arbitrary waveform -> RTM2032 CH1 capture -> run report
```

验收标准：

- 上传一个低风险波形：例如 1 kHz、1 Vpp、0 V offset 的正弦或三角。
- 捕获包里能看到 waveform preview。
- `capture inspect --fft` 能读到主频。
- 实验后恢复 DG4202 原状态。

## 推荐顺序

```text
1. DG4202 任意波形命令确认表
2. Offline waveform builder
3. DG4202 driver upload 方法
4. CLI arb-load dry-run
5. 实机 upload + scope capture 闭环
```

## v0.4 暂不做

- GUI waveform editor。
- 内置大量波形库。
- 调制编辑器。
- 跨厂商任意波形抽象。
- 自动校准。
- 默认打开 output。

## 一句话原则

```text
v0.4 不是做任意波形平台，而是安全地把一段数组送进 DG4202，并用示波器证明它真的出来了。
```
