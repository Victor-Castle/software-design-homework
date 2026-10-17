---
name: return-book
description: 归还图书技能。由 circulation-agent 在 orchestrator-agent 委派下调用，提供归还接口参考。
metadata:
  version: "1.1"
  api-base: "http://localhost:8001"
---

> 说明：本 skill 不在用户输入时自动触发；还书意图由 `orchestrator-agent` 委派 `circulation-agent` 执行，circulation-agent 需解析参数时参考本 skill。

## 后端真实 API 映射
基址 `http://localhost:8001`，统一返回 `{code, message, data}`。
| 能力 | 方法 | 路径 | 请求体 / 参数 |
|------|------|------|--------------|
| 查借阅记录 | GET | `/api/borrow/records/{user_id}` | 路径参数，可选 `status=borrowing` |
| 归还 | POST | `/api/return` | `{record_id}` |

## Input
- user_id: integer（必需）- 用户ID
- record_id: integer（必需）- 借阅记录ID

## Output
- 归还结果，包含：书名、借阅日期、归还日期、是否超期、罚金

## Procedure
### 第1步：查询用户当前借阅记录
```python
import httpx
# 调用借阅记录查询API
response = httpx.get(f"http://localhost:8001/api/borrow/records/{user_id}?status=borrowing")
records_data = response.json()
# 展示用户正在借阅的图书列表，让用户选择要归还的图书
```

### 第2步：用户选择要归还的记录
展示用户当前借阅的所有图书，格式：
```
[{序号}]《书名》- 借阅日期：{date}，应还日期：{due_date}
```

### 第3步：执行归还操作
```python
# 调用归还API
response = httpx.post(
    "http://localhost:8001/api/return",
    json={"record_id": record_id}
)
result = response.json()
```

### 第4步：返回归还结果
- 成功：显示归还详情，包括是否超期、罚金金额
- 失败：显示错误原因

## Acceptance Criteria
- 必须先查询用户当前借阅列表，让用户选择
- 必须显示借阅日期和应还日期，方便用户确认
- 归还成功后必须告知用户是否超期及罚金
