# WaveBench 插件注册表

本文档记录 WaveBench 当前插件注册表的设计边界、命令形态和安全规则。

插件注册表目前只管理仪器插件 metadata，不改变现有仪器控制路径。真实连接、SCPI 写入、采集、输出开关和 run plan 执行仍由现有 driver/service 层负责。

## 目标

当前阶段的目标是给内置驱动、显式 Python entry points、本地市场索引和声明式 SCPI metadata 提供统一的只读能力目录：

- 列出 WaveBench 知道哪些仪器驱动；
- 查看单个驱动的型号、能力、IDN 匹配和配置字段；
- 检查插件 metadata 是否符合当前 API 约定；
- 展示只读市场索引；
- 校验本地声明式 SCPI metadata，并在显式授权时执行只读 IDN 匹配。

## 非目标

当前插件注册表不做以下事情：

- 不从插件 metadata 自动实例化真实仪器；
- 不把 service 层改成插件调度；
- 不提供插件安装命令；
- 不默认导入第三方 Python 包；
- 不下载远端 marketplace；
- 不通过 marketplace 安装插件；
- 不让声明式 SCPI 插件执行任意命令。

## 插件 metadata

插件 metadata 使用 `InstrumentPlugin` 表示，当前核心字段包括：

```text
driver_id      稳定驱动 ID，例如 rigol.dg4202
kind           仪器类型：scope / source / power / dmm
display_name   展示名称
manufacturer   厂商
models         支持型号
capabilities   能力列表，例如 source.set_frequency
summary        简短说明
api_version    当前为 wavebench.instrument.v1
package        来源包名
origin         builtin / entry_point / local
idn_patterns   可用于后续自动匹配的 IDN 片段
config_fields  相关配置字段
```

能力名使用点分格式，推荐以仪器类型作为前缀：

```text
scope.capture_waveform
source.set_frequency
power.protection
dmm.read
```

## 内置插件

当前内置插件来自现有驱动能力目录：

```text
rohde-schwarz.rtm2032  scope   R&S RTM2000-series scope capture driver
rigol.dg4202           source  RIGOL DG4000-series signal source driver
rigol.dp800            power   RIGOL DP800-series power supply driver
rigol.dm3000           dmm     RIGOL DM3000/DM3058 multimeter driver
```

这些 metadata 只描述现有驱动，不会改变驱动行为。

## 命令

列出插件：

```bash
python -m wavebench plugin list
python -m wavebench plugin list --kind source
```

查看单个插件：

```bash
python -m wavebench plugin info rigol.dg4202
```

检查插件注册表：

```bash
python -m wavebench plugin doctor
```

`plugin doctor` 会输出 tab 分隔的诊断记录：

```text
ok      rigol.dg4202   metadata valid
error   entry_point:x  ImportError: ...
```

当存在 error 时，`plugin doctor` 返回退出码 `2`。

## Entry Points

外部 Python 包可通过 `wavebench.drivers` entry point 暴露插件 metadata：

```toml
[project.entry-points."wavebench.drivers"]
example-scope = "wavebench_example.scope:plugin"
```

entry point 可以直接返回 `InstrumentPlugin`，也可以返回一个无参 callable，由 WaveBench 调用后得到 `InstrumentPlugin`。

示例：

```python
from wavebench.plugins import InstrumentPlugin

plugin = InstrumentPlugin(
    driver_id="example.scope",
    kind="scope",
    display_name="Example Scope",
    manufacturer="Example",
    models=("EX1",),
    capabilities=("scope.idn",),
    summary="Example scope metadata.",
)
```

## 安全边界

Python entry point 加载会导入第三方代码。因此 WaveBench 默认不加载 entry points。

只有显式传入 `--include-entry-points` 时，以下命令才会加载 `wavebench.drivers`：

```bash
python -m wavebench plugin list --include-entry-points
python -m wavebench plugin info example.scope --include-entry-points
python -m wavebench plugin doctor --include-entry-points
```

加载失败不会让 CLI 直接崩溃。失败会被记录为 `PluginLoadError`，并在 `plugin doctor --include-entry-points` 中显示为 error。

如果外部插件声明了与内置插件相同的 `driver_id`，WaveBench 会保留内置插件，并把外部插件记为重复 ID error。

## Doctor 检查项

当前 `plugin doctor` 检查：

- `api_version` 必须等于 `wavebench.instrument.v1`；
- `kind` 必须是 `scope`、`source`、`power` 或 `dmm`；
- capability 必须是点分小写标识符；
- capability 必须以插件 `kind` 作为前缀；
- entry point 加载失败会输出 error；
- entry point `driver_id` 与已有插件重复会输出 error。

## 当前插件相关命令

```bash
python -m wavebench plugin list
python -m wavebench plugin info rigol.dp800
python -m wavebench plugin doctor
python -m wavebench plugin market search rigol
python -m wavebench plugin market info wavebench-rigol-dg4202
python -m wavebench plugin scpi check doc/project/scpi-plugin.example.toml
python -m wavebench plugin scpi info doc/project/scpi-plugin.example.toml
python -m wavebench plugin scpi probe doc/project/scpi-dp800.example.toml --resource TCPIP::192.168.1.161::INSTR
python -m wavebench plugin scpi doctor doc/project/scpi-dp800.example.toml --probe --resource TCPIP::192.168.1.161::INSTR
```

## 仍然不做的事

- 不自动下载插件；
- 不自动安装插件；
- 不让 service 层按声明式插件执行控制命令；
- 不绕过显式资源参数访问仪器；
- 不执行任意 SCPI；
- 不打开或关闭输出。
