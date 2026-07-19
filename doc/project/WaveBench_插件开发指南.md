# WaveBench 可执行仪器插件开发指南

WaveBench 支持两条互不替代的插件路径：

- `wavebench.drivers` / `wavebench.instrument.v1`：只读 metadata，保留向后兼容。
- `wavebench.instruments` / `wavebench.instrument.v2`：可信 Python 包提供真实仪器 driver factory。

V2 插件只替换设备差异层。transport 创建、resource、timeout、命令日志、安全限制、Service、run plan 和 artifact 仍由 WaveBench 核心掌握。声明式 SCPI TOML 仍只用于校验和显式只读 IDN probe，不能进入真实执行路径。

## 最小目录

仓库中的 DS1000Z 试点包可作为完整模板：

```text
packages/plugins/wavebench-rigol-ds1000z/
├── pyproject.toml
└── src/wavebench_rigol_ds1000z/
    ├── __init__.py
    ├── descriptor.py
    └── driver.py
```

最小 `pyproject.toml`：

```toml
[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"

[project]
name = "wavebench-example-scope"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["wavebench>=0.7,<1"]

[project.entry-points."wavebench.instruments"]
"example.scope" = "wavebench_example_scope:descriptor"
```

entry point 名必须等于 canonical `driver_id`。普通配置解析只读取 entry point 名；只有配置真正选中该 ID、显式查看详情，或运行 `plugin ... --load` 时才导入插件。

## Descriptor 与 factory

插件导出一个 `InstrumentDescriptor` 或返回它的无参函数：

```python
from wavebench.instruments.api import InstrumentDescriptor, OptionSpec


def _open_driver(context):
    from .driver import ExampleScope

    return ExampleScope(
        transport=context.open_transport(),
        check_errors=bool(context.settings["check_errors"]),
        block_points=int(context.options["block_points"]),
    )


def descriptor():
    return InstrumentDescriptor(
        driver_id="example.scope",
        kind="scope",
        display_name="Example Scope",
        manufacturer="Example",
        models=("EX1",),
        aliases=(),
        capabilities=("scope.idn", "scope.capture_waveform"),
        idn_patterns=("EXAMPLE,EX1",),
        backends=("pyvisa",),
        option_specs=(OptionSpec("block_points", int, default=250000, minimum=1),),
        permissions=("instrument.io", "configured-resource-only"),
        factory=_open_driver,
        wavebench_min_version="0.7.0",
        wavebench_max_version="1.0.0",
        scope_coupling_policy="unknown",
    )
```

descriptor 至少声明 canonical ID、kind、API/兼容版本、厂商/型号、capability、IDN pattern、backend、受限选项、权限提示和 factory。外置 V2 插件首版必须使用 `aliases=()`；scope 插件还应准确声明 coupling policy，无法证明输入安全语义时保留 `unknown`，核心会默认拒绝采集。

插件模块导入时不得连接仪器、发送 SCPI、创建文件或修改全局状态。factory 才能调用 `context.open_transport()`，且每次 factory 调用最多只能成功打开一个 transport。

## DriverContext

核心传入的 `DriverContext` 只包含当前插件所需的窄上下文：

- 已解析的 canonical `driver_id` 与 `kind`；
- 配置中选中的单个 `resource`；
- 核心选定的 backend、timeout 与 OPC timeout；
- `CommandLogger`；
- 只读 core settings 与经过 `OptionSpec` 校验的插件 options；
- 受控 transport factory。

插件不应读取完整 WaveBench 配置，也不应持有 Service、TUI、RunService 或 artifact writer。

## Contracts 与 models

按 `kind` 实现对应 Protocol：

- `ScopeDriver`
- `SourceDriver`
- `PowerDriver`
- `DmmDriver`

公共返回类型来自 `wavebench.instruments.models`，包括 `WaveformHeader`、`WaveformData`、`SourceStatus`、`PowerStatus`、`PowerMeasurement`、`PowerProtectionStatus` 和 `DmmReading`。不要复制另一套不兼容的数据模型，也不要实现包含所有仪器方法的巨型接口。

factory 返回对象缺少 contract 方法时，核心会拒绝启用该插件并尝试关闭已创建资源。

## ID、alias 与兼容

- 外置 V2 插件首版只支持 canonical ID，不接受 alias；内置 driver 可继续保留兼容 alias。
- 外部插件不能覆盖内置 canonical ID 或 alias。
- entry point 名与 descriptor `driver_id` 必须一致。
- `kind` 必须与配置槽位一致。
- 当前 WaveBench 版本必须落在插件声明的半开兼容区间内。
- 第一阶段不解决同一 Python 环境中互斥 vendor SDK 依赖；出现真实需求后再评估独立进程或 RPC。

DS1000Z 试点保留内置 fallback，因此旧配置 alias `ds1104` / `ds1000z` 继续选择内置实现；安装试点 wheel 后，使用 canonical `rigol.ds1000z` 才会显式选择外部包。这避免外部包覆盖内置 alias，也便于卸载后安全恢复。

## 测试门槛

至少覆盖：

- descriptor 构建不产生 I/O；
- canonical ID、alias、kind、版本和冲突校验；
- OptionSpec 默认值、类型、范围和未知字段；
- fake transport 下的核心读写能力、错误队列和 close；
- timeout、短 bin-block、坏 preamble、截图失败；
- 坏插件不影响其他内置驱动；
- wheel 在临时 venv 中安装、entry point 发现、重装和卸载；
- 卸载后缺失提示或内置 fallback 行为。

示例：

```bash
python -m pytest -q tests/test_instrument_registry.py tests/test_ds1000z_plugin.py
python -m ruff check packages/plugins/wavebench-rigol-ds1000z
python -m wavebench plugin doctor --load
```

## 信任与发布边界

Python entry point 是可信代码扩展，不是安全沙箱。安装插件等价于允许该包在当前 Python 用户权限下执行代码。WaveBench 不提供在线商店、自动下载、自动 `pip install`、插件评分或每插件进程隔离。

建议每套 WaveBench 使用独立 venv，固定 WaveBench/插件版本，保存 lockfile，并在分发 wheel 时校验 hash。公开示例 resource 使用 RFC 5737 保留地址，例如 `TCPIP::192.0.2.20::INSTR`，不得提交真实实验室地址、序列号、凭据、原始波形或命令日志。
