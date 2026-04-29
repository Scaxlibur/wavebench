# 基于 VISA/Python 控制 R&S RTM2032 示波器的开发思路草案

> 目标设备：Rohde & Schwarz RTM2032，属于 RTM2000 系列。
> 目标语言：Python。
> 推荐通信栈：优先 `RsInstrument`，必要时退回 `PyVISA` 直接控制。
> 草拟日期：2026-04-28。

---

## 1. 本次检索到的资料范围

### 1.1 官方资料

1. R&S 官方 GitHub 例程仓库
   `https://github.com/Rohde-Schwarz/Examples/tree/main/Oscilloscopes`

   其中 Python 目录分为：

   - `Oscilloscopes/Python/RsInstrument`
   - `Oscilloscopes/Python/rsmxo_ScpiPackage`
   - `Oscilloscopes/Python/rsrtx_ScpiPackage`

   与示波器波形采集最相关的例程包括：

   - `RsInstrument_RTB2000_Example.py`
   - `RsInstrument_RTA-Waveform_transfer_Screenshot.py`
   - `RsInstrument_RTO-Waveform_transfer_Screenshot.py`
   - `rsrtx_get_waveform_data_ch1.py`
   - `rsrtx_get_waveform_data_ch1+ch2.py`
   - `rsmxo_get_waveform_data_ch1.py`
   - `rsmxo_get_waveform_data_ch1+ch2.py`

2. R&S RTM2000 官方用户手册
   `https://www.rohde-schwarz.com/manual/rtm2000/`

   该页面说明 RTM2000 User Manual 包含：

   - Acquisition and setup
   - Triggers
   - Measurements, mathematics, reference waveforms
   - Remote commands reference and basics of remote control
   - Programming examples

   本地已下载官方 PDF 到：

   ```text
   C:\Users\username\Desktop\RTM2_UserManual_en_10.pdf
   ```

3. R&S 使用 `RsInstrument` 远程控制示波器的官方说明
   `https://www.rohde-schwarz.com/applications/remote-control-of-rohde-schwarz-oscilloscopes-using-the-rsinstrument-python-module-application-card_56279-1443712.html`

   关键点：

   - 官方推荐 `RsInstrument` 控制 R&S 示波器。
   - 需要 Python、R&S VISA，以及 `RsInstrument` 包。
   - `RsInstrument` 相比裸 `PyVISA`，提供同步、错误检查、大块数据传输封装等能力。
   - 最小连接示例形如：

     ```python
     from RsInstrument import *

     instr = RsInstrument('TCPIP::192.168.1.100::INSTR')
     print(instr.query('*IDN?'))
     ```

4. R&S 远程控制入门与 VISA 说明
   官方中文页面强调典型流程：

   - PC 与仪器在同一 LAN 网络。
   - 通过 `ping <仪器 IP>` 验证网络可达。
   - 使用 R&S VISA Tester 或 NI MAX 测试 `*IDN?`。
   - VISA 资源字符串通常为：

     ```text
     TCPIP::<仪器 IP 地址>::INSTR
     ```

5. R&S 关于“仪器驱动程序 vs 直接 SCPI”的说明
   官方建议：对于没有专用 Python 驱动的仪器，使用直接 SCPI；驱动/封装层的价值主要是：

   - 自动处理同步。
   - 自动检查仪器错误。
   - 自动处理参数格式化、响应解析、数组/二进制数据。

### 1.2 Python/VISA 通用资料

1. PyVISA 官方文档：通信配置
   `https://pyvisa.readthedocs.io/en/latest/introduction/communication.html`

   关键点：

   - 通过 `pyvisa.ResourceManager()` 枚举和打开资源。
   - `query()` 本质是 `write()` + `read()`。
   - 通信异常常见原因是终止符、超时、命令不被仪器理解。
   - 常见终止符配置：

     ```python
     inst.read_termination = '\n'
     inst.write_termination = '\n'
     ```

2. PyVISA 官方文档：大数组/二进制数据读取
   `https://pyvisa.readthedocs.io/en/latest/introduction/rvalues.html`

   关键点：

   - 示波器波形属于典型大块数据传输。
   - ASCII 易调试但慢；二进制快但要确认数据类型、端序、块头格式。
   - PyVISA 提供：

     ```python
     inst.query_ascii_values(...)
     inst.query_binary_values(...)
     ```

   - 大块二进制读取时可能需要调整 `chunk_size`、超时、是否期待终止符。

### 1.3 社区/第三方检索结论

RTM2032 专门的开源 Python 项目很少。更常见的是：

- R&S 官方 RsInstrument 示例。
- R&S 官方 PyVISA / SCPI 入门文档。
- 针对其他 R&S 示波器系列的波形读取示例。
- 通用 SCPI/PyVISA 自动化教程。

因此开发时应以 RTM2000 官方用户手册中的远程命令为准，把 RTB/RTA/RTO/MXO 示例作为代码结构参考，而不是无脑复制命令。别拿新机型命令直接砸老机型，炸了还得自己收拾。

---

## 2. 技术路线选择

### 2.1 推荐路线：`RsInstrument` + 直接 SCPI

推荐优先使用：

```bash
pip install RsInstrument numpy matplotlib pandas pyarrow
```

最低必要依赖：

```bash
pip install RsInstrument numpy
```

优点：

- 官方支持 R&S SCPI 仪器。
- 自动处理很多 VISA 属性。
- 有 `query_opc()` / `write_str_with_opc()` 等同步能力。
- 有 `query_bin_or_ascii_float_list()` 处理 ASCII/二进制数组。
- 有 `instrument_status_checking` 做仪器错误检查。
- 示例与官方资料一致，减少踩坑。

缺点：

- 仍然需要自己查 RTM2032 支持哪些 SCPI 命令。
- 老型号 RTM2000 的命令可能与 RTB/RTM3000/RTA/RTO/MXO 不完全一致。

### 2.2 备选路线：裸 `PyVISA`

适合情况：

- 不想依赖 `RsInstrument`。
- 需要完全控制底层 VISA 行为。
- `RsInstrument` 某个封装行为不适合 RTM2032。

最低依赖：

```bash
pip install pyvisa numpy
```

还需要安装一个 VISA 后端，例如：

- R&S VISA
- NI VISA
- Keysight VISA
- 或 `pyvisa-py`，但实际仪器兼容性要测试

裸 PyVISA 要自己处理：

- 资源枚举。
- 终止符。
- 超时。
- `*OPC?` 同步。
- `SYST:ERR?` 错误队列。
- 二进制块解析。

所以除非有明确理由，否则先用 `RsInstrument`，别给自己找活。

---

## 3. 预期开发目标

建议先不要一上来就写“大而全控制台”。第一阶段目标应该很窄：

1. 能连接 RTM2032。
2. 能读取 `*IDN?` 并确认型号、固件版本。
3. 能设置基础采集参数。
4. 能设置通道 1 的垂直参数。
5. 能设置边沿触发。
6. 能执行单次采集并等待完成。
7. 能读取 CH1 波形。
8. 能保存为 CSV/NPY/Parquet。
9. 能可选保存截图。
10. 能记录每次采集的配置元数据。

后续再扩展：

- 多通道同步采集。
- 自动测量项读取，如频率、峰峰值、均值、上升沿等。
- 批量采集。
- 配置文件驱动。
- 命令行工具。
- GUI。

---

## 4. 建议项目结构

```text
rtm2032-visa-control/
├─ pyproject.toml
├─ README.md
├─ configs/
│  └─ rtm2032.example.yaml
├─ data/
│  ├─ raw/
│  └─ processed/
├─ scripts/
│  ├─ check_connection.py
│  ├─ acquire_once.py
│  └─ capture_screenshot.py
├─ src/
│  └─ rtm2032/
│     ├─ __init__.py
│     ├─ connection.py
│     ├─ scope.py
│     ├─ waveform.py
│     ├─ scpi.py
│     ├─ export.py
│     └─ errors.py
└─ tests/
   ├─ test_waveform_parse.py
   └─ test_config.py
```

如果只是个人脚本，可以简化成：

```text
rtm2032_scripts/
├─ config.yaml
├─ rtm2032.py
├─ acquire_once.py
└─ data/
```

但我建议还是保留一点结构，否则过两周你自己都不想看，别问我怎么知道的。

---

## 5. 核心模块设计

### 5.1 `connection.py`

职责：建立、关闭、测试连接。

建议接口：

```python
from RsInstrument import RsInstrument


def open_scope(resource: str, *, id_query: bool = True) -> RsInstrument:
    instr = RsInstrument(resource, id_query, False)
    instr.visa_timeout = 10_000
    instr.opc_timeout = 30_000
    instr.instrument_status_checking = True
    instr.clear_status()
    return instr
```

需要支持的资源字符串：

```text
TCPIP::192.168.2.10::INSTR
USB0::0x0AAD::...::INSTR
```

第一阶段建议只支持 LAN，USB 留到后面。LAN 调试更清楚，VISA 资源字符串也稳定。

### 5.2 `scope.py`

职责：封装 RTM2032 的常用 SCPI 操作。

建议类：

```python
class RTM2032:
    def __init__(self, instr):
        self.instr = instr

    def idn(self) -> str: ...
    def reset(self) -> None: ...
    def setup_channel(self, channel: int, scale: float, offset: float, coupling: str) -> None: ...
    def setup_timebase(self, scale: float | None = None, acquisition_time: float | None = None) -> None: ...
    def setup_edge_trigger(self, source: str, level: float, slope: str = 'POS') -> None: ...
    def single(self) -> None: ...
    def run(self) -> None: ...
    def stop(self) -> None: ...
    def read_waveform(self, channel: int = 1) -> tuple: ...
```

注意：具体 SCPI 命令必须查 RTM2000 手册验证。RTB/RTA/RTO 例程中出现的写法可作为参考，例如：

```text
TIM:ACQT 0.01
CHAN1:RANG 5.0
CHAN1:OFFS 0.0
CHAN1:COUP ACL
CHAN1:STAT ON
TRIG:A:MODE AUTO
TRIG:A:TYPE EDGE
TRIG:A:EDGE:SLOP POS
TRIG:A:SOUR CH1
TRIG:A:LEV1 0.05
SING
FORM REAL,32
CHAN1:DATA?
```

但这些命令对 RTM2032 的兼容性要以上机测试或 RTM2000 手册为准。

### 5.3 `waveform.py`

职责：波形数据读取、时间轴构建、单位转换。

示波器波形读取通常有两类情况：

1. 仪器直接返回已经换算好的浮点电压值。
2. 仪器返回 ADC 原始码，需要结合 preamble/metadata 换算。

从 R&S 官方 `RTB2000_Example.py` 看，示例使用：

```python
trace = rtb.query_bin_or_ascii_float_list('FORM ASC;:CHAN1:DATA?')

rtb.bin_float_numbers_format = BinFloatFormat.Single_4bytes
trace = rtb.query_bin_or_ascii_float_list('FORM REAL,32;:CHAN1:DATA?')
```

这说明某些 R&S 示波器的 `CHAN1:DATA?` 可以直接返回浮点波形。RTM2032 是否完全一致，需要确认。

建议实现两层：

- 第一层：直接读返回浮点列表。
- 第二层：读取波形元信息，构造时间轴。

需要从 RTM2000 手册确认的命令：

- 查询采样点数。
- 查询采样率或时间步进。
- 查询水平起点。
- 查询通道垂直比例、偏置。
- 查询波形数据格式。
- 查询波形数据源。

### 5.4 `export.py`

建议保存三类文件：

1. 原始波形数据：

   ```text
   data/raw/20260428_153000_ch1.npy
   ```

2. CSV 文件，方便 Excel/Origin/Matlab 读取：

   ```text
   time_s,voltage_v
   0.000000000,-0.0012
   0.000000001,-0.0011
   ```

3. 元数据 JSON：

   ```json
   {
     "instrument": "Rohde&Schwarz,RTM2032,...",
     "resource": "TCPIP::192.168.2.10::INSTR",
     "channel": 1,
     "points": 10000,
     "format": "REAL,32",
     "timebase": {},
     "vertical": {},
     "trigger": {},
     "timestamp": "2026-04-28T15:30:00+08:00"
   }
   ```

---

## 6. 第一版脚本执行流程

建议第一版 `acquire_once.py` 流程：

```text
读取配置
  ↓
打开 VISA 连接
  ↓
查询 *IDN?，确认 RTM2032
  ↓
clear_status()
  ↓
可选 reset，默认不 reset，避免破坏前面板设置
  ↓
设置通道/时基/触发
  ↓
query_opc() 等待设置生效
  ↓
执行 single acquisition
  ↓
query_opc() 等待采集完成
  ↓
设置波形传输格式：优先 REAL,32
  ↓
读取 CH1:DATA?
  ↓
读取必要元数据，构建时间轴
  ↓
保存 CSV/NPY/JSON
  ↓
关闭连接
```

注意：默认不建议一连接就 `reset()`。官方例程常用 `reset()` 是为了保证演示环境干净，但实验室实际使用时，一句 `*RST` 可能把你前面板调了半小时的设置清掉。除非你明确需要全自动配置，否则应让 `reset` 成为配置项。

---

## 7. 配置文件建议

`configs/rtm2032.example.yaml`：

```yaml
visa:
  resource: "TCPIP::192.168.2.10::INSTR"
  timeout_ms: 10000
  opc_timeout_ms: 30000

instrument:
  reset_before_run: false
  check_idn_contains: "RTM2032"

acquisition:
  mode: "single"
  acquisition_time_s: 0.01
  points: null

channels:
  - index: 1
    enabled: true
    range_v: 5.0
    offset_v: 0.0
    coupling: "ACL"

trigger:
  mode: "AUTO"
  type: "EDGE"
  source: "CH1"
  slope: "POS"
  level_v: 0.05

waveform:
  source: "CHAN1"
  format: "REAL,32"
  prefer_binary: true

output:
  directory: "data/raw"
  basename: "rtm2032_capture"
  save_csv: true
  save_npy: true
  save_json: true
  save_screenshot: false
```

---

## 8. 最小可行代码骨架

### 8.1 使用 `RsInstrument`

```python
from __future__ import annotations

from pathlib import Path
from time import time
import json
import numpy as np
from RsInstrument import RsInstrument, BinFloatFormat


RESOURCE = "TCPIP::192.168.2.10::INSTR"
OUT_DIR = Path("data/raw")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    scope = RsInstrument(RESOURCE, True, False)
    scope.visa_timeout = 10_000
    scope.opc_timeout = 30_000
    scope.instrument_status_checking = True

    try:
        print("IDN:", scope.idn_string)
        scope.clear_status()

        # 谨慎：不要默认 reset，除非你明确想全自动接管仪器
        # scope.reset()

        # 以下命令来自 R&S 官方相近系列示例，RTM2032 上需查手册或上机验证
        scope.write_str("TIM:ACQT 0.01")
        scope.write_str("CHAN1:RANG 5.0")
        scope.write_str("CHAN1:OFFS 0.0")
        scope.write_str("CHAN1:COUP ACL")
        scope.write_str("CHAN1:STAT ON")

        scope.write_str("TRIG:A:MODE AUTO")
        scope.write_str("TRIG:A:TYPE EDGE;:TRIG:A:EDGE:SLOP POS")
        scope.write_str("TRIG:A:SOUR CH1")
        scope.write_str("TRIG:A:LEV1 0.05")
        scope.query_opc()

        scope.write_str("SING")
        scope.query_opc()

        start = time()
        scope.bin_float_numbers_format = BinFloatFormat.Single_4bytes
        data = scope.query_bin_or_ascii_float_list("FORM REAL,32;:CHAN1:DATA?")
        elapsed = time() - start

        y = np.asarray(data, dtype=np.float32)
        print(f"读取 {y.size} 点，耗时 {elapsed:.3f} s")

        np.save(OUT_DIR / "capture_ch1.npy", y)
        np.savetxt(OUT_DIR / "capture_ch1.csv", y, delimiter=",", header="voltage_v", comments="")

        meta = {
            "resource": RESOURCE,
            "idn": scope.idn_string,
            "points": int(y.size),
            "format": "REAL,32",
            "note": "时间轴构建需要根据 RTM2000 手册补充采样率/时间步进查询命令。",
        }
        (OUT_DIR / "capture_ch1.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    finally:
        scope.close()


if __name__ == "__main__":
    main()
```

### 8.2 使用裸 `PyVISA` 的骨架

```python
import pyvisa

RESOURCE = "TCPIP::192.168.2.10::INSTR"

rm = pyvisa.ResourceManager()
inst = rm.open_resource(RESOURCE)
inst.timeout = 10_000
inst.read_termination = "\n"
inst.write_termination = "\n"

try:
    print(inst.query("*IDN?"))
    inst.write("*CLS")

    # 具体 SCPI 命令需按 RTM2000 手册确认
    inst.write("CHAN1:STAT ON")
    inst.write("TRIG:A:MODE AUTO")
    inst.write("SING")
    inst.query("*OPC?")

    inst.write("FORM REAL,32")
    data = inst.query_binary_values("CHAN1:DATA?", datatype="f", is_big_endian=False)
    print(len(data))
finally:
    inst.close()
```

裸 PyVISA 的二进制读取参数需要按仪器实际返回格式调整：

- `datatype='f'` 表示 32-bit float。
- `is_big_endian` 要根据仪器的 `FORM:BORD` 或手册确认。
- 若读到超时，检查 `expect_termination`、`chunk_size`、`timeout`。

---

## 9. 关键技术风险与规避方案

### 9.1 命令兼容性风险

RTM2032 是 RTM2000 系列，不是 RTB2000、RTM3000、RTA4000、RTO 或 MXO。

规避：

- 以 `RTM2_UserManual_en_10.pdf` 的远程命令章节为准。
- 每引入一个 SCPI 命令，都用小脚本单独验证。
- 保留 `SYST:ERR?` 或 `instrument_status_checking`。

### 9.2 VISA 连接风险

常见问题：

- IP 不通。
- VISA 后端没装好。
- 资源字符串不对。
- 防火墙阻断。
- USBTMC 驱动问题。

规避：

1. 先 `ping`。
2. 用 R&S VISA Tester 或 NI MAX 跑 `*IDN?`。
3. Python 里只做第二步已经验证过的资源字符串。

### 9.3 采集同步风险

错误写法：发 `SING` 后立刻读波形。这样读到旧数据或超时都不奇怪。

规避：

- 使用 `query_opc()` 或 `*OPC?`。
- 单次采集超时时间要大于采集时间。
- 对低频/罕见触发信号，触发模式和超时要单独考虑。

### 9.4 波形格式风险

ASCII 慢，但直观；二进制快，但端序/格式容易错。

建议：

1. 第一轮先用 ASCII 验证数据逻辑。
2. 第二轮切 `REAL,32` 二进制。
3. 用同一次波形比较 ASCII 和二进制前几十个点是否一致。
4. 确认端序后固定在代码里。

### 9.5 数据元信息风险

只有电压数组没有时间轴，后处理很难用。

必须保存：

- 仪器型号和固件版本。
- 通道号。
- 采样点数。
- 采样率或时间步进。
- 水平起点。
- 垂直比例/偏置。
- 触发设置。
- 采集时间。
- 脚本版本。

---

## 10. 建议实施步骤

### 阶段 0：环境确认

- 安装 R&S VISA 或 NI VISA。
- 安装 Python 3.10+。
- 安装依赖：

  ```bash
  pip install RsInstrument numpy matplotlib pandas pyyaml
  ```

- 用 VISA 工具确认：

  ```text
  TCPIP::<RTM2032_IP>::INSTR
  *IDN?
  ```

### 阶段 1：连接测试

写 `check_connection.py`：

- 列出资源。
- 打开指定资源。
- 查询 `*IDN?`。
- 打印 `*OPT?`，如果支持。
- 清状态。

### 阶段 2：单通道单次采集

写 `acquire_once.py`：

- 不 reset。
- 使用当前前面板设置或最少量设置。
- `SING`。
- `*OPC?`。
- 读 CH1 波形。
- 保存 `.npy` 和 `.csv`。

### 阶段 3：补齐元信息

查 RTM2000 手册，补充：

- 采样率/时间步进查询。
- 触发位置查询。
- 水平起点查询。
- 通道比例/偏置查询。

构造：

```python
x = x_origin + np.arange(len(y)) * x_increment
```

### 阶段 4：配置文件驱动

引入 YAML：

- IP。
- 通道。
- 触发。
- 保存路径。
- 是否截图。
- 是否 reset。

### 阶段 5：稳定性增强

- 每条关键命令后检查错误。
- 捕获 VISA 超时并给出明确提示。
- 保存日志。
- 对采集失败保留现场信息。
- 加入 `--dry-run`，只打印命令不执行。

---

## 11. 需要马上查 RTM2000 手册确认的命令清单

优先查这些，不要一页页瞎翻：

1. 通信与基础：

   ```text
   *IDN?
   *RST
   *CLS
   *OPC?
   SYST:ERR?
   ```

2. 采集：

   ```text
   RUN
   STOP
   SING 或 RUNSINGLE
   ACQ:POIN?
   ```

3. 时基：

   ```text
   TIM:SCAL
   TIM:ACQT
   ```

4. 通道：

   ```text
   CHAN1:STAT
   CHAN1:SCAL 或 CHAN1:RANG
   CHAN1:OFFS
   CHAN1:COUP
   ```

5. 触发：

   ```text
   TRIG:A:MODE
   TRIG:A:TYPE
   TRIG:A:SOUR
   TRIG:A:LEV1
   TRIG:A:EDGE:SLOP
   ```

6. 波形传输：

   ```text
   FORM ASC
   FORM REAL,32
   FORM:BORD
   CHAN1:DATA?
   ```

7. 截图/文件传输，可选：

   ```text
   HCOP:LANG PNG
   MMEM:NAME
   HCOP:IMM
   MMEM:DATA?
   ```

如果某个命令在 RTM2000 手册中不存在，就不要幻想“也许能用”。换成手册里的等价命令。

---

## 12. 推荐的第一轮实验顺序

1. 连接：

   ```text
   *IDN?
   ```

2. 清状态：

   ```text
   *CLS
   SYST:ERR?
   ```

3. 不改设置，直接读取当前 CH1 波形：

   ```text
   FORM ASC
   CHAN1:DATA?
   ```

4. 如果 ASCII 正常，再试二进制：

   ```text
   FORM REAL,32
   CHAN1:DATA?
   ```

5. 再加入单次采集同步：

   ```text
   SING
   *OPC?
   CHAN1:DATA?
   ```

6. 最后再加入通道/触发/时基自动配置。

这个顺序能最大限度定位问题。别一上来同时改十个参数，然后问为什么读不出来——那叫给自己制造悬疑剧。

---

## 13. 后续我建议实际写代码前补充的信息

请记录以下信息，后面写脚本会快很多：

1. RTM2032 当前连接方式：LAN 还是 USB。
2. 仪器 IP 地址。
3. `*IDN?` 返回字符串。
4. 固件版本。
5. 你要采集的信号类型：周期波、单次脉冲、随机事件？
6. 采样点数/采样时长需求。
7. 需要几个通道。
8. 输出格式：CSV、NPY、MAT、Parquet、图片？
9. 是否需要截图。
10. 是否需要自动设置前面板，还是只读取当前设置。

---

## 14. 结论

最稳的路线是：

```text
R&S VISA / NI VISA
  ↓
RsInstrument
  ↓
RTM2032 专用 SCPI 封装
  ↓
单次采集脚本
  ↓
数据与元信息导出
  ↓
批量/自动化扩展
```

第一版不要追求“大而全”。先把 `*IDN? → 单次采集 → 读取 CH1 → 保存数据` 跑通，再逐步加自动配置和多通道。对仪器控制来说，稳定比优雅重要；优雅但会超时的脚本，除了让人血压上升没有任何价值。
