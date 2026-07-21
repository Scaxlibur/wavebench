# WaveBench 可安装仪器插件用户指南

可执行仪器插件是普通 Python wheel，通过 `wavebench.instruments` entry point 接入。它是可信代码扩展，不是安全沙箱；只安装来源和版本都可信的包。

## 推荐环境

每套实验环境使用独立 venv，并同时固定 WaveBench 与插件版本：

```bash
python -m venv .venv
.venv/bin/python -m pip install "wavebench==0.7.0"
```

WaveBench 的受管插件命令只允许在当前 venv 中运行，拒绝系统 Python。它只接受用户明确指定的本地源码目录或 wheel，不联网、不自动安装依赖，也不修改 `wavebench.toml`。

先做包检查和安装 dry-run：

```bash
.venv/bin/python -m wavebench plugin package check \
  ../wavebench-instrument-plugins/packages/wavebench-rigol-ds1000z
.venv/bin/python -m wavebench plugin install \
  ../wavebench-instrument-plugins/packages/wavebench-rigol-ds1000z --dry-run
.venv/bin/python -m wavebench plugin install \
  ../wavebench-instrument-plugins/packages/wavebench-rigol-ds1000z
```

源码目录会先在临时目录中离线构建 wheel。即使是 `package check` 或 `--dry-run`，源码包的受信任 build backend 也会执行；如果不希望执行构建代码，请只检查已经取得并核验来源的 wheel。

安装器会校验 wheel 的 Python/WaveBench 兼容范围、`METADATA`、`WHEEL`、`RECORD`、SHA-256、成员路径和唯一 `wavebench.instruments` entry point。安装固定使用当前解释器的离线 `pip --no-deps --no-index`，因此插件声明的额外依赖必须预先存在于该 venv，缺失时安装后检查会失败并触发回滚。

## 查看与诊断

```bash
.venv/bin/python -m wavebench plugin installed
.venv/bin/python -m wavebench plugin info rigol.ds1000z --installed
.venv/bin/python -m wavebench plugin list --load
.venv/bin/python -m wavebench plugin info rigol.ds1000z --load
.venv/bin/python -m wavebench plugin doctor --load
```

`plugin installed` 和 `info --installed` 会交叉核对受管账本、已安装 distribution、entry point、`RECORD` 与文件摘要，并报告 `healthy`、`missing`、`drifted`、`broken` 或 `unmanaged`。普通 `plugin info` 仍查看 metadata；只有 `--load` 才导入 V2 descriptor。descriptor 导入本身不应连接仪器；真正的 transport 在配置选中该 driver 并执行仪器命令时才创建。

当前 V2 外置插件只接受 entry point 对应的 canonical ID，不解析插件自定义 alias。

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

升级与降级都要求提供明确的本地源码目录或 wheel，并按目标版本相对当前受管版本的方向进行校验：

```bash
.venv/bin/python -m wavebench plugin upgrade ./wavebench_rigol_ds1000z-0.2.0-py3-none-any.whl --dry-run
.venv/bin/python -m wavebench plugin upgrade ./wavebench_rigol_ds1000z-0.2.0-py3-none-any.whl
.venv/bin/python -m wavebench plugin downgrade ./wavebench_rigol_ds1000z-0.1.0-py3-none-any.whl
.venv/bin/python -m wavebench plugin remove rigol.ds1000z --dry-run
.venv/bin/python -m wavebench plugin remove rigol.ds1000z
```

安装、替换和卸载都使用环境锁、原子账本和写前 transaction journal。升级/降级失败时会使用缓存的旧 wheel 做 best-effort 回滚；没有已校验旧 wheel、插件文件已漂移或 distribution 不受 WaveBench 管理时，操作会拒绝继续。若进程或主机在 pip 修改环境期间中断，先运行：

```bash
.venv/bin/python -m wavebench plugin recover
```

只有能证明环境处于精确旧态或精确目标态时才会自动恢复；状态不唯一时会停止并要求人工检查。不要通过手工删除账本或 journal 来掩盖未知状态。

卸载后使用 canonical `rigol.ds1000z` 的配置会给出“driver 未安装”提示。可重新安装固定版本，或把配置改回受支持的内置 alias `ds1104` / `ds1000z`。

## 常见问题

- `kind` 不匹配：检查 driver 是否写在正确的 `[scope]` / `[source]` / `[power]` / `[dmm]` 段。
- 版本不兼容：安装 descriptor 声明范围内的 WaveBench 版本，或升级插件。
- alias / ID：外置 V2 插件只能声明 canonical ID，不能声明或覆盖 alias；内置兼容 alias 不受影响。
- import/factory 失败：运行 `plugin doctor --load` 查看具体包；坏插件不会阻止其他内置 driver。
- `drifted` / `broken`：不要直接执行升级或卸载；先检查 distribution、entry point 和安装文件，再按提示恢复。
- `recovery required`：运行 `plugin recover`；若仍要求人工检查，保留 venv 中的 `.wavebench` 事务证据。
- vendor SDK 依赖互斥：第一阶段不做每插件进程隔离；为不同依赖组合建立独立 venv。
- marketplace：当前只读展示索引，不会下载或自动安装任何包。
