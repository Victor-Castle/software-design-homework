---
name: user-manage
description: 用户管理技能。由 orchestrator-agent / circulation-agent 按需调用，提供登录与用户信息接口参考。
metadata:
  version: "1.1"
  api-base: "http://localhost:8001"
---

> 说明：本 skill 不在用户输入时自动触发，而是由 `orchestrator-agent`（登录类意图）或 `circulation-agent`（需解析 user_id 时）按需调用。

## 后端真实 API 映射
基址 `http://localhost:8001`，统一返回 `{code, message, data}`。
| 能力 | 方法 | 路径 | 请求体 / 参数 |
|------|------|------|--------------|
| 登录 | POST | `/api/login` | `{username, password}` |
| 查用户信息 | GET | `/api/users/{user_id}` | 路径参数 |

## Input
- action: string（必需）- 操作类型：login / info
- username: string（登录时需要）
- password: string（登录时需要）
- user_id: integer（查询信息时需要）

## Output
- 登录结果或用户信息

## Procedure
### 登录流程
1. 获取用户输入的用户名和密码
2. 调用登录 API：
   ```python
   import httpx
   response = httpx.post(
       "http://localhost:8001/api/login",
       json={"username": username, "password": password}
   )
   ```
3. 登录成功：保存 `user_id` 到对话上下文，返回欢迎信息
4. 登录失败：提示用户名或密码错误

### 查询用户信息流程
1. 调用用户查询 API：
   ```python
   import httpx
   response = httpx.get(f"http://localhost:8001/api/users/{user_id}")
   ```
2. 返回用户信息：用户名、角色、最大借阅数、邮箱

## Acceptance Criteria
- 登录成功后必须保存 `user_id` 用于后续操作
- 未登录状态下，当用户尝试借书时，先引导登录
