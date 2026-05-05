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
resource = "TCPIP::192.168.123.5::INSTR"
timeout_ms = 3000
```

DM3000 / RS232 路径（保留 skeleton，实机暂缓）：

```toml
[dmm]
driver = "dm3000"
backend = "serial"
resource = "/dev/ttyUSB0"
baudrate = 9600
bytesize = 8
parity = "N"
stopbits = 1
timeout_ms = 1000
```

这里 `driver` 和 `backend` 是分开的：

- `driver=dm3000|dm3058`：决定用哪些 SCPI 命令、如何解析返回值；
- `backend=serial|lan`：决定如何打开 `/dev/ttyUSB0` 或 `TCPIP::...::INSTR`、如何处理 I/O。

DM3058 LAN 已从 WSL 验证 `*IDN?`：

```text
Rigol Technologies,DM3058,DM3L184650025,01.01.00.02.03.01
```

## 第一阶段 CLI

LAN / DM3058：

```bash
wavebench dmm idn --resource TCPIP::192.168.123.5::INSTR
wavebench dmm read dcv --resource TCPIP::192.168.123.5::INSTR
wavebench dmm read acv --resource TCPIP::192.168.123.5::INSTR
wavebench dmm read res --resource TCPIP::192.168.123.5::INSTR
```

RS232 / DM3000 skeleton：

```bash
wavebench dmm idn --resource /dev/ttyUSB0
wavebench dmm read dcv --resource /dev/ttyUSB0
```

`read` 的返回保持窄而清楚：函数、数值、单位、原始字符串。

## 暂不做

- 不做自动扫描所有串口并盲发命令。串口设备可能不是万用表。
- 不把 DMM 测量直接塞进 scope/source/power 的 service。
- 不在 run plan 中加入 DMM step，等单独 `dmm idn/read` 实机验证后再接入。
