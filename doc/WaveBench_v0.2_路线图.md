# WaveBench v0.2 路线图

v0.1 已经证明：WaveBench 可以用一组显式 CLI 命令和 TOML run plan，把示波器、信号源、电源串成可复盘的自动测量流程。

v0.2 不应该急着变成“大平台”。它的重点是把 v0.1 留下的数据用起来，同时守住软件解耦边界。

## v0.2 目标

```text
从“能采、能跑、能留证据”走到“能读、能看、能复盘”。
```

具体目标：

- 让 `data/runs/...` 和 `data/raw/...` 更容易被人查看。
- 把已有 `run.json` / `summary.csv` / `metadata.json` 转成报告或摘要。
- 为截图保存预留干净接口，但不把截图逻辑塞进数据分析或报告层。
- 继续保持显式仪器动作，不引入隐藏自动化。

## 解耦原则

### 1. 仪器控制和离线分析分开

仪器控制层负责和设备说话：

```text
CLI -> Service -> Driver -> Transport -> Instrument
```

离线分析层只读文件：

```text
RunPackage / CapturePackage -> Analysis -> Report
```

离线分析不能依赖真实仪器连接。报告生成失败，也不能影响采集流程。

### 2. 数据模型和渲染分开

v0.2 可以新增结构化读取函数，例如：

```text
wavebench.data.packages.load_capture_package(path)
wavebench.data.runs.load_run_package(path)
```

这些函数只负责读取和规范化数据，不生成 HTML，也不画图。

报告渲染应该在单独模块里，例如：

```text
wavebench.report.html
wavebench.report.markdown
```

这样以后想输出 HTML、Markdown、JSON summary，不需要改采集逻辑。

### 3. 截图是采集 artifact，不是报告功能

如果实现截图，截图应该属于 `scope.capture` 的 artifact：

```text
data/raw/<capture>/
  screenshot.png
  metadata.json
```

报告只引用截图，不负责向示波器请求截图。

这条边界很重要。否则报告命令会意外连接仪器，调试时会很危险。

### 4. run plan 继续保持显式

v0.2 暂不加入：

```text
条件分支
循环
matrix
表达式
自动修正仪器状态
```

run plan 仍然像实验记录本：一步一步写清楚。

## 候选工作包

### A. Run / Capture 包读取 API

新增只读数据访问层。

建议模块：

```text
src/wavebench/data/packages.py
src/wavebench/data/runs.py
```

能力：

- 读取 capture package 的 `metadata.json`。
- 枚举 `ch<n>.npy` / `ch<n>.csv`。
- 读取 run package 的 `run.json`。
- 读取 `summary.csv`。
- 提供小的 dataclass / typed dict，统一字段入口。

验收标准：

- 不连接任何仪器。
- 单元测试覆盖正常包、缺字段、缺文件。
- 不改变 v0.1 采集输出格式。

### B. `wavebench run report`

新增离线报告命令：

```bash
wavebench run report data/runs/<run_dir>
```

默认生成：

```text
data/runs/<run_dir>/report.html
```

报告内容：

- run 状态。
- step 列表。
- capture package 链接。
- quality / expect 状态。
- warning 和 failure 摘要。
- restore 状态。

验收标准：

- 没有仪器也能运行。
- 报告生成失败不修改原始 `run.json` / `summary.csv`。
- HTML 使用静态文件，不引入前端框架。

### C. Capture 摘要命令

新增离线命令：

```bash
wavebench capture inspect data/raw/<capture_dir>
```

输出：

- 通道列表。
- 点数、时间步进、Vpp、RMS、mean。
- 频率估计、duty、rise/fall。
- quality warnings。

验收标准：

- 只读 capture package。
- 不要求 CSV 存在，优先读 `metadata.json` / NPY。
- 输出可被人读，也适合后续转 JSON。

### D. 截图保存

新增显式选项：

```bash
wavebench scope capture --screenshot
```

或 run plan：

```toml
[[steps]]
kind = "scope.capture"
screenshot = true
```

边界：

- 截图只在采集命令里发生。
- 不作为 report 命令的副作用。
- 截图失败不应该吞掉波形采集结果；需要明确状态记录。

验收标准：

- 手册确认 RTM2032 截图 SCPI 路径。
- `metadata.json.files.screenshot` 记录文件名或 `null`。
- failed package 能记录截图失败原因。

## v0.2 推荐顺序

推荐顺序：

```text
1. Run / Capture 包读取 API
2. wavebench run report
3. wavebench capture inspect
4. scope capture --screenshot
```

理由：

- 先做读取 API，后面的 report / inspect / screenshot 引用才不会乱。
- report 不碰仪器，风险最低，最适合 v0.2 第一刀。
- inspect 可以复用读取 API，把已有数据变得更有用。
- screenshot 需要查手册和实机验证，放在数据读取与报告边界稳定之后。

## v0.2 暂不做

- GUI。
- YAML 工作流。
- PyPI 发布。
- 复杂 run plan 语法。
- 自动生成论文式报告。
- 支持更多仪器型号。
- 把私人工具一次性全升格。

私人工具仍然只是孵化区。只有反复用到、边界清楚、能写测试的工具，才升格为正式命令。

## 代码结构建议

当前结构继续保留：

```text
src/wavebench/
  cli.py
  services/
  drivers/
  transport/
  data/
```

v0.2 可新增：

```text
src/wavebench/data/packages.py
src/wavebench/data/runs.py
src/wavebench/report/html.py
src/wavebench/report/templates.py
```

不要让 `report/` import `drivers/` 或 `transport/`。如果需要仪器数据，应该由采集命令先写入 package，再由报告读取 package。

建议依赖方向：

```text
cli -> services -> drivers -> transport
cli -> data -> report
report -> data
```

禁止方向：

```text
report -> drivers
report -> transport
data -> services
data -> drivers
```

这样以后即使做 GUI，也可以只调用 data/report 层，而不是重新碰仪器驱动。

## v0.2 完成标准

v0.2 可以发布时，应满足：

- `run report` 能为至少一个真实 run package 生成 HTML。
- `capture inspect` 能读取单通道和多通道 capture package。
- 所有新增功能都有单元测试。
- 不改变 v0.1 package 的兼容性。
- 公开文档隐私扫描通过。
- release notes 明确说明仍无 GUI / YAML / 隐式自动流程。

## 一句话原则

```text
v0.2 不是让 WaveBench 更聪明，而是让 WaveBench 留下的证据更容易被人读懂。
```
