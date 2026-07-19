# WaveBench 可安装仪器插件用户指南

可执行仪器插件是普通 Python wheel，通过 `wavebench.instruments` entry point 接入。它是可信代码扩展，不是安全沙箱；只安装来源和版本都可信的包。

## 推荐环境

每套实验环境使用独立 venv，并同时固定 WaveBench 与插件版本：

```bash
python -m venv .venv
.venv/bin/python -m pip install "wavebench==0.7.0"
.venv/bin/python -m pip install "wavebench-rigol-ds1000z==0.1.0"
```

生产实验建议保存 lockfile，并使用 `--require-hashes` 或独立校验 wheel hash。不要把插件安装到系统 Python。

仓库内 DS1000Z 试点可先构建 wheel：

```bash
.venv/bin/python -m pip wheel --no-deps \
  packages/plugins/wavebench-rigol-ds1000z
.venv/bin/python -m pip install wavebench_rigol_ds1000z-0.1.0-py3-none-any.whl
```

## 查看与诊断

```bash
.venv/bin/python -m wavebench plugin list --load
.venv/bin/python -m wavebench plugin info rigol.ds1000z --load
.venv/bin/python -m wavebench plugin doctor --load
```

`--load` 会导入已安装插件。descriptor 导入本身不应连接仪器；真正的 transport 在配置选中该 driver 并执行仪器命令时才创建。

外置 V2 插件首版只接受 entry point 对应的 canonical ID，不解析插件自定义 alias。

## 配置

安装 DS1000Z 试点后，用 canonical ID 显式选择外部实现：

```toml
[connection]
backend = "lan"
resource = "TCPIP::192.0.2.20::INSTR"

[scope]
driver = "rigol.ds1000z"
model_hint = "DS1104Z Plus"
default_channel = 1
check_errors = true

[scope.options]
max_chunk_points = 250000
```

旧 alias `ds1104` 与 `ds1000z` 在试点期继续选择 WaveBench 内置 fallback，不会被外部包覆盖。这样卸载插件后旧配置仍可工作；要验证外部 wheel，必须使用 canonical `rigol.ds1000z`。

## 升级与卸载

```bash
.venv/bin/python -m pip install --upgrade "wavebench-rigol-ds1000z==0.1.0"
.venv/bin/python -m pip uninstall wavebench-rigol-ds1000z
```

卸载后使用 canonical `rigol.ds1000z` 的配置会给出“driver 未安装”提示。可重新安装固定版本，或把配置改回受支持的内置 alias `ds1104` / `ds1000z`。

## 常见问题

- `kind` 不匹配：检查 driver 是否写在正确的 `[scope]` / `[source]` / `[power]` / `[dmm]` 段。
- 版本不兼容：安装 descriptor 声明范围内的 WaveBench 版本，或升级插件。
- alias / ID：外置 V2 插件只能声明 canonical ID，不能声明或覆盖 alias；内置兼容 alias 不受影响。
- import/factory 失败：运行 `plugin doctor --load` 查看具体包；坏插件不会阻止其他内置 driver。
- vendor SDK 依赖互斥：第一阶段不做每插件进程隔离；为不同依赖组合建立独立 venv。
- marketplace：当前只读展示索引，不会下载或自动安装任何包。
