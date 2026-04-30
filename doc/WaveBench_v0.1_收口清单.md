# WaveBench v0.1 收口清单

这页用于决定什么时候可以发第一个公开 release。v0.1 的目标不是“功能完整”，而是把已经验证过的能力冻结成一个能被别人读懂、能被自己复现的基线版本。

## v0.1 定位

```text
轻量 Python VISA/SCPI 自动测量台的第一个可用基线。
```

v0.1 适合：

- 电赛调试时远程采集示波器波形。
- 用信号源输出固定波形，并用示波器做闭环检查。
- 显式控制 DP800 系列电源的电压/电流限值和输出状态。
- 用 TOML run plan 串起 source / power / scope / sleep 步骤。
- 生成可复盘的采集包、流程记录和 `commands.log`。

v0.1 不承诺：

- 图形界面。
- 截图保存。
- YAML 实验流程。
- 自动报告生成。
- 隐式“智能”流程编排。
- 完整仪器状态回滚。
- 跨品牌、跨型号的通用仪器抽象。

## 已完成能力

### 示波器采集

- [x] `scope idn`
- [x] `scope errors`
- [x] `scope auto` / `scope autoscale`
- [x] `scope fetch`
- [x] `scope capture`
- [x] 单通道采集。
- [x] 重复 `--channel` 的逐通道多通道采集。
- [x] `--points def|max|dmax`。
- [x] `--time-range`。
- [x] `--window-frequency` + `--target-cycles` 自动采集窗口。
- [x] `--expect-frequency` + `--frequency-tolerance`。
- [x] `--no-csv` / `--no-npy` 输出控制。
- [x] 失败采集包：`metadata.partial.json`、`error.txt`、`commands.log`。

### 数据输出

- [x] 采集包目录。
- [x] CSV：`index,time_s,voltage_v`。
- [x] NPY：二维数组 `[time_s, voltage_v]`。
- [x] `metadata.json`。
- [x] `commands.log`。
- [x] 波形摘要：min/max/mean/RMS/Vpp。
- [x] 频率估计、周期数、每周期点数。
- [x] duty cycle、rise/fall time（适用时）。
- [x] 质量 warning。

### 信号源

- [x] `source idn`
- [x] `source status`
- [x] `source set-freq`
- [x] `source set-func`
- [x] `source set-vpp`
- [x] `source set-duty`
- [x] `source output`
- [x] `sweep discrete`
- [x] `--restore-source-state` 可选 source 状态恢复。

### 电源

- [x] `power idn`
- [x] `power status`
- [x] `power set --voltage --current-limit`
- [x] `power output on|off`
- [x] 设置后 / 输出切换后的 settle delay 配置。

### run plan

- [x] `run check`：只解析和打印摘要，不连接仪器。
- [x] `run schema`：从当前代码打印 step schema。
- [x] `run plan`：执行显式 source / power / scope / sleep 步骤。
- [x] `[safety]`：只读 scope coupling guard。
- [x] `[restore] source_state = true`：source snapshot / restore。
- [x] `scope.auto` 显式 step。
- [x] `scope.capture quality_gate = true`。
- [x] `scope.capture auto_recover = true`。
- [x] `[steps.expect]` 指标断言。
- [x] `data/runs/.../run.json`。
- [x] `data/runs/.../summary.csv`。
- [x] step record JSON。

### 文档

- [x] README 快速入口。
- [x] 文档索引。
- [x] 项目边界。
- [x] CLI 形态。
- [x] 设备抽象层。
- [x] 配置文件格式。
- [x] 数据输出格式。
- [x] 错误处理与日志策略。
- [x] RTM2032 MVP 命令确认。
- [x] DP800 只读 / 设置 / 输出控制设计。
- [x] 多仪器协同流程设计。
- [x] run plan 使用指南。
- [x] 公开 example plan。

## 暂缓事项

这些不要塞进 v0.1：

- [ ] 截图保存。
- [ ] YAML 实验流程。
- [ ] GUI。
- [ ] 自动报告。
- [ ] 表达式、条件分支、循环、矩阵实验。
- [ ] 完整仪器状态 rollback。
- [ ] 支持更多型号仪器。
- [ ] PyPI 发布。

原因很简单：v0.1 应该先稳定，而不是变大。

## 已知边界

- RTM2032 当前只确认了项目用到的 SCPI 路径，不声明覆盖完整手册。
- `scope.auto` 会改变示波器前面板设置，所以只作为显式 step 或显式命令存在。
- `power set` 不会打开输出，`power output` 不会改电压/电流限值。
- DP800 直连示波器探头的流程必须显式声明安全 guard，并由人确认接线安全。
- Source restore 只覆盖 output、function、frequency、amplitude、square duty cycle；不覆盖 offset、phase、load、modulation、sweep mode。
- 多通道采集是逐通道顺序采集，不保证同步采样。
- `summary.csv` 是轻量表格视图；严肃脚本应优先读 `run.json`。
- 公开文档不记录本地实验台 IP、设备序列号、私有路径、账号、密钥或草稿目录。

## release 前门禁

发 GitHub release 前，至少跑完这些检查：

```powershell
python -m unittest discover -s tests -v
python -m wavebench run schema
python -m wavebench run check --config wavebench.example.toml --plan plans/example_scope_expect_quality.toml
git diff --check
```

还要做一次公开资料隐私扫描，范围限于：

```text
README.md
doc/*.md
wavebench.example.toml
plans/*.toml
```

排除厂商手册/摘录类 source material。检查项包括：

- 局域网 IP。
- 私有路径。
- 私有草稿目录名。
- 账号/设备标识。
- 凭据、密钥、认证信息相关敏感词。
- 仪器序列号。

## 第一个 release 建议

建议第一个 tag：

```text
v0.1.0
```

原因：`pyproject.toml` 当前版本已经是 `0.1.0`，功能边界也更像“第一个可用基线”，不是临时预览。

release 标题：

```text
WaveBench v0.1.0 - explicit VISA/SCPI measurement bench baseline
```

release notes 建议结构：

```markdown
## Highlights
- RTM2032 waveform fetch/capture with reproducible acquisition packages.
- DG4202 source control and discrete source-to-scope sweeps.
- DP800 status/set/output commands with explicit safety semantics.
- TOML run plans with `run check`, `run schema`, source restore, quality recovery, and metric expectations.

## Safety model
- No hidden reset.
- No implicit autoscale before capture.
- No implicit power output changes.
- Safety guards query and refuse; they do not auto-correct hardware settings.

## Documentation
- Run plan authoring guide.
- Data output format.
- Error handling and logging policy.
- Public example plans.

## Known limits
- No GUI, screenshot export, YAML workflows, or automatic reports yet.
- Instrument support is intentionally narrow and verified only for the documented paths.
```

## 发布步骤

第一次 release 建议这样做：

```powershell
git status -sb
git push origin master
git tag -a v0.1.0 -m "WaveBench v0.1.0"
git push origin v0.1.0
```

然后在 GitHub 上从 `v0.1.0` 创建 release，粘贴上面的 release notes。

也可以用 GitHub CLI：

```powershell
gh release create v0.1.0 --title "WaveBench v0.1.0 - explicit VISA/SCPI measurement bench baseline" --notes-file release-notes-v0.1.0.md
```

真正执行 push、tag 和 GitHub release 前，应该由人确认。它们是公开动作。

## v0.1 之后

建议 v0.1 之后再考虑：

1. 截图保存。
2. 更好的报告导出。
3. YAML 或更高级实验流程。
4. 更多仪器型号。
5. PyPI 包发布。

现在先把第一根桩钉稳。

