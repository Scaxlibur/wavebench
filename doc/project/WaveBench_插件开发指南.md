# WaveBench 插件开发指南

这页写给想扩展 WaveBench 插件 metadata、插件市场索引或声明式 SCPI TOML 的人。

先说清楚边界：当前插件系统不是“把任意第三方代码接进真实仪器执行路径”的入口。它主要用于描述仪器能力、做只读诊断、展示插件信息、维护本地 marketplace index，以及对本地声明式 SCPI TOML 做安全受限的 `*IDN?` probe。

如果目标是让一个新仪器真正参与 `run plan`、`doctor`、CLI 控制或 service 执行，请看 [[WaveBench_新增仪器驱动指南]]。

## 插件系统能做什么

- 列出内置仪器 metadata：`plugin list` / `plugin info`。
- 显式加载 Python entry point metadata：`plugin list --include-entry-points`。
- 诊断 metadata API 版本、能力命名、重复 driver id 和加载错误：`plugin doctor`。
- 查询只读本地 marketplace JSON index：`plugin market search/info`。
- 校验本地声明式 SCPI TOML：`plugin scpi check/info/doctor`。
- 对显式指定的 resource 执行受限只读 IDN probe：`plugin scpi probe` 或 `plugin scpi doctor --probe --resource ...`。

## 插件系统不做什么

- 不自动下载、安装或启用插件。
- 默认不加载第三方 Python entry points。
- 不把声明式 SCPI TOML 注册成真实 driver。
- 不自动实例化仪器，不进入 service / run-plan 执行路径。
- 不支持任意 SCPI 下发；当前 probe 只允许安全受限的 IDN 查询。
- 不修改 `wavebench.toml`，不打开或关闭任何仪器输出。

## 代码入口

| 入口 | 作用 |
|---|---|
| `src/wavebench/plugins/api.py` | `InstrumentPlugin` 数据结构、API 版本和诊断记录类型。 |
| `src/wavebench/plugins/builtin.py` | 内置插件 metadata 列表。 |
| `src/wavebench/plugins/registry.py` | 注册表构建、entry point 显式加载、metadata doctor。 |
| `src/wavebench/plugins/market.py` | 本地 marketplace JSON index 读取和 search/info。 |
| `src/wavebench/plugins/scpi.py` | 声明式 SCPI TOML 校验、info、只读 probe。 |
| `src/wavebench/cli_parser.py` | `plugin ...` 子命令参数定义。 |
| `src/wavebench/cli.py` | `plugin ...` 子命令处理逻辑。 |
| `tests/test_plugins.py` | 插件注册表与 doctor 测试。 |
| `tests/test_plugin_market.py` | marketplace index 测试。 |
| `tests/test_plugin_scpi.py` | 声明式 SCPI TOML 与 probe 测试。 |

## `InstrumentPlugin` 字段

`InstrumentPlugin` 只描述 metadata，不代表真实 driver 已接入执行路径。

| 字段 | 说明 |
|---|---|
| `driver_id` | 稳定唯一 ID，例如 `rigol.dg4202`。 |
| `kind` | 仪器类别：`scope`、`source`、`power`、`dmm`。 |
| `display_name` | 面向人的名称。 |
| `manufacturer` | 厂商名称。 |
| `models` | 适配型号列表。 |
| `capabilities` | 能力列表，建议以 `kind.` 为前缀，例如 `source.set_frequency`。 |
| `summary` | 简短说明。 |
| `api_version` | 当前为 `wavebench.instrument.v1`。 |
| `package` | 所属 Python 包，内置插件通常是 `wavebench`。 |
| `origin` | `builtin`、`entry_point` 或 `local`。 |
| `idn_patterns` | 用于 `doctor` 或人工判断的 IDN 匹配线索。 |
| `config_fields` | 关联配置字段提示。 |

## 内置插件

新增或更新内置 metadata 时：

1. 修改 `src/wavebench/plugins/builtin.py`。
2. 确保 `driver_id` 不与已有插件冲突。
3. `capabilities` 至少有一项，并使用清晰的 `kind.` 前缀。
4. 补充或更新 `tests/test_plugins.py`。
5. 运行：

```bash
python -m wavebench plugin list
python -m wavebench plugin info <driver_id>
python -m wavebench plugin doctor
python -m pytest tests/test_plugins.py
```

## Entry Point 插件

Entry point 插件只在用户显式传入 `--include-entry-points` 时加载。

目的：避免普通 `plugin list/info/doctor` 因第三方包导入副作用而执行外部代码。

约束：

- entry point 加载失败不能让 CLI 崩溃；失败应进入 `plugin doctor --include-entry-points` 诊断。
- third-party metadata 只能描述能力，不能绕过 service / driver 层直接执行仪器动作。
- 若 entry point 的 `driver_id` 与内置插件冲突，doctor 应报告 error。

## Marketplace Index

当前 marketplace 是只读本地 JSON index，用于发现可安装/可参考的插件信息。

它不做：

- 自动安装。
- 签名校验。
- 网络下载。
- trust chain。

相关命令：

```bash
python -m wavebench plugin market search rigol
python -m wavebench plugin market info wavebench-rigol-dg4202
```

## 声明式 SCPI TOML

声明式 SCPI 插件适合记录一个仪器的只读识别信息、能力和 IDN 查询方式。它不能把任意 SCPI 变成 WaveBench 执行能力。

常用命令：

```bash
python -m wavebench plugin scpi check doc/project/scpi-plugin.example.toml
python -m wavebench plugin scpi info doc/project/scpi-plugin.example.toml
python -m wavebench plugin scpi doctor doc/project/scpi-dp800.example.toml
python -m wavebench plugin scpi probe doc/project/scpi-dp800.example.toml --resource TCPIP::192.0.2.12::INSTR
python -m wavebench plugin scpi doctor doc/project/scpi-dp800.example.toml --probe --resource TCPIP::192.0.2.12::INSTR
```

Probe 安全规则：

- 必须显式传 `--resource`。
- 只发送 TOML 中的 `scpi.idn_query`。
- `idn_query` 必须是单行查询，不能包含 `;`，必须以 `?` 结尾。
- 不打开/关闭输出，不写仪器状态，不修改配置。

## 什么时候不要写插件

如果你需要这些能力，应该写真实驱动而不是插件 metadata：

- 新 CLI 命令会连接仪器并执行动作。
- 新仪器需要进入 `wavebench.toml` 配置。
- 新仪器要参与 `doctor`、`run verify` 或 `run plan`。
- 新仪器会产生 artifact、读数、采集包或报告区块。
- 需要 safety guard、restore、输出开关等危险状态控制。

这类工作请走 [[WaveBench_新增仪器驱动指南]]。

## 提交前检查

```bash
python -m wavebench plugin doctor
python -m wavebench plugin scpi check doc/project/scpi-plugin.example.toml
python -m pytest tests/test_plugins.py tests/test_plugin_market.py tests/test_plugin_scpi.py
```

公开文档里的 resource 示例使用保留网段，例如 `192.0.2.0/24` 或 `TCPIP::192.0.2.12::INSTR`，不要写真实实验室 IP。
