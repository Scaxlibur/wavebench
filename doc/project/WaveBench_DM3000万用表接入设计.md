# WaveBench DM3000 / DM3058 万用表接入设计

## 原则

万用表继续沿用 WaveBench 的分层：

```text
CLI 层：wavebench dmm idn/read
  ↓
Service 层：DmmService，表达“读一次测量”
  ↓
Device Driver 层：DM3000Dmm，保存 DM3000/DM3058 共用 SCPI 命令
  ↓
Transport 层：SerialTransport / PyVisaTransport，只处理串口字节、LAN/VISA 会话、换行和超时
```

不要把串口或 LAN/VISA 打开逻辑写进 `DM3000Dmm`，也不要把 `:MEASure:VOLTage:DC?` 这类命令写进 CLI 或 service。

## 已确认手册依据

来源：`doc/instruments/普源DM3000万用表_编程手册.md`

- `*IDN?` 查询仪器 ID。
- `:MEASure:VOLTage:DC?` 返回直流电压，单位 V。
- `:MEASure:VOLTage:AC?` 返回交流电压，单位 V。
- `:MEASure:CURRent:DC?` / `:MEASure:CURRent:AC?` 返回电流，单位 A。
- `:MEASure:RESistance?` / `:MEASure:FRESistance?` 返回二线/四线电阻，单位 Ω。
- `:MEASure:FREQuency?` 返回频率，单位 Hz。
- RS232 波特率支持 `1200|2400|4800|9600|19200|38400|57600|115200`。
- RS232 校验位支持 `none8bits|odd7bits|even7bits`，WaveBench 配置中先表达为 `parity=N/O/E` + `bytesize=8/7`。

## 配置形态

DM3058 LAN 路径（当前优先）：

```toml
[dmm]
driver = "dm3058"
backend = "lan"
resource = "TCPIP::192.0.2.13::INSTR"
timeout_ms = 3000
```

DM3000 / DM3058 RS232 路径：

```toml
[dmm]
driver = "dm3058"
backend = "serial"
resource = "/dev/serial/by-id/usb-<adapter-id>"
baudrate = 9600
bytesize = 8
parity = "N"
stopbits = 1
timeout_ms = 3000
write_termination = "crlf"
read_termination = "lf"
xonxoff = false
rtscts = false
dsrdtr = false
```

这里 `driver` 和 `backend` 是分开的：

- `driver=dm3000|dm3058`：决定用哪些 SCPI 命令、如何解析返回值；
- `backend=serial|lan`：决定如何打开 `/dev/serial/by-id/...` 或 `TCPIP::...::INSTR`、如何处理 I/O。

DM3058 LAN 与 RS232 均已验证 `*IDN?`：

```text
Rigol Technologies,DM3058,<serial>,<firmware>
```

2026-07-21 的 RS232 复测使用 CH340、9600 8N1、无软/硬件流控、写
`CRLF`、读 `LF`，连续 20 次 `*IDN?` 全部成功。此前只写 LF 或 CR 的
不稳定现象来自命令行终止不完整，不再归因于驱动或接口锈蚀。

接入 WaveBench 后，正式 `SerialTransport -> DM3000Dmm -> DmmService` 路径
再次完成同一会话 20/20 次 `*IDN?`，延迟 72.7–80.8 ms；`doctor` 能按
serial backend 正确探测，当前功能查询为 DCV，单次只读 DCV 返回
`-1.628406E-04 V`。该结果只验收通信与当前挡位读取，不代表外部标准源精度校准。

## 第一阶段 CLI

LAN / DM3058：

```bash
wavebench dmm idn --resource TCPIP::192.0.2.13::INSTR
wavebench dmm read dcv --resource TCPIP::192.0.2.13::INSTR
wavebench dmm read acv --resource TCPIP::192.0.2.13::INSTR
wavebench dmm read res --resource TCPIP::192.0.2.13::INSTR
```

RS232 / DM3000 或 DM3058：

```bash
wavebench dmm idn --resource /dev/serial/by-id/usb-<adapter-id>
wavebench dmm read dcv --resource /dev/serial/by-id/usb-<adapter-id>
```

`read` 的返回保持窄而清楚：函数、数值、单位、原始字符串。

## 当前边界

- 不做自动扫描所有串口并盲发命令。串口设备可能不是万用表。
- 不把 DMM 测量直接塞进 scope/source/power 的 service；DMM 仍然通过独立 DMM service 和 run-plan step 参与实验。
- run plan 可显式读取 DMM；但不会把 DMM 读数隐式附加到 scope/source/power 步骤里。
