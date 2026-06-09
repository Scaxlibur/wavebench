# WaveBench HTTP MCP 只读接口

HTTP MCP 当前是只读 MVP，用于让本机或私网内客户端读取 WaveBench 的离线信息和 run plan 检查结果。

## 启动

```powershell
python -m wavebench mcp serve --config wavebench.toml --token-env WAVEBENCH_MCP_TOKEN
```

`--host` 默认是 `127.0.0.1`，`--port` 默认是 `8765`。如果显式传入 `--host 0.0.0.0`，WaveBench 会拒绝启动。

认证 token 必须通过 `--token` 或 `--token-env` 提供。公开示例只展示环境变量名，不展示 token 值。

## Endpoints

- `GET /health`：健康检查，不需要 token。
- `GET /tools`：返回当前只读工具列表，需要 Bearer token。
- `POST /call`：调用只读工具，需要 Bearer token，请求体为 JSON 对象。

`/call` 请求体格式：

```json
{
  "tool": "run.schema",
  "arguments": {}
}
```

## Tools

- `run.schema`：返回 run plan schema 文本和结构化 schema 行。
- `run.check`：参数 `{"plan": "<plan.toml>"}`，只解析并检查 run plan，不连接仪器。
- `capture.inspect`：参数 `{"path": "<capture_dir>"}`，读取离线采集包摘要。

## 安全边界

- 默认只监听 `127.0.0.1`。
- 拒绝监听 `0.0.0.0`。
- `/mcp`、`/tools` 和 `/call` 强制 Bearer token。
- 当前工具全部只读。
- 不提供 raw SCPI。
- 不提供 power/source output on/off。
- 不提供 run 执行工具。
- HTTP 路径参数会拒绝明显敏感的 key、secret、token、password、pem、SSH、AWS、GitHub 配置路径。
