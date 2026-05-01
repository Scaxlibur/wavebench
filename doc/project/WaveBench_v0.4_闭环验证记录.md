# WaveBench v0.4 闭环验证记录

## 2026-05-01：DG4202 基础波形 -> RTM2032 采集 -> FFT 验证

目标：先把“信号源输出已知基础波形，示波器采集，离线 FFT 验证主频和谐波，最后恢复信号源状态”这条闭环跑通。

实验连接：

```text
DG4202 CH1 -> RTM2032 CH1
source resource = TCPIP::192.168.123.3::INSTR
scope resource  = TCPIP::192.168.123.2::INSTR
```

计划：

```text
plans/closure_sine_1k_fft.toml
```

运行：

```bash
python -m wavebench run check --config /tmp/wavebench-lab.toml --plan plans/closure_sine_1k_fft.toml
python -m wavebench run plan  --config /tmp/wavebench-lab.toml --plan plans/closure_sine_1k_fft.toml
python -m wavebench capture inspect data/raw/20260501_021456_closure_sine_1k --fft --harmonics 7 --fft-expect-frequency 1000 --fft-frequency-tolerance 0.02
python -m wavebench run report data/runs/20260501_021455_closure_sine_1k_fft
```

结果：

```text
run=data/runs/20260501_021455_closure_sine_1k_fft
capture=data/raw/20260501_021456_closure_sine_1k
report=data/runs/20260501_021455_closure_sine_1k_fft/report.html
run status=ok
```

FFT 验证：

```text
peak_frequency≈1000 Hz
peak_frequency_error≈0.000%
peak_frequency_ok=True
sample_rate≈1e+06 Hz
resolution≈100 Hz
thd≈7.553%
harmonic_2≈2000 Hz amplitude≈0.000199441 V
harmonic_3≈3000 Hz amplitude≈0.000514435 V
harmonic_4≈4000 Hz amplitude≈0.000590454 V
harmonic_5≈5000 Hz amplitude≈0.000525115 V
harmonic_6≈6000 Hz amplitude≈0.000343898 V
harmonic_7≈7000 Hz amplitude≈0.000228897 V
```

注意：同一采集包的时域频率估计给出 `frequency≈250000 Hz`，并触发：

```text
low_points_per_cycle
frequency_mismatch
```

但 FFT peak 明确落在 1 kHz。结论是：

- 当前时域频率估计不适合作为 sine / 谐波闭环的唯一验收标准。
- v0.4 的基础闭环应采用：`run plan` 负责设置源、采集和恢复；`capture inspect --fft --fft-expect-frequency` 负责频率验收。
- 后续可以考虑把 FFT-based expectation 接入 `run plan` 或 `run report`，但不要混进这次小闭环。
