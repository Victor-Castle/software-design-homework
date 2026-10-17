# 图书管理系统 - 项目宪法

## 项目概述
这是一个基于Agentic架构的图书管理系统，用户可以通过自然语言与系统交互，完成图书检索、借阅、归还等操作。

## 技术栈约束
- 后端API：Python + FastAPI（已实现，运行在 localhost:8000）
- 数据库：SQLite（内置）
- Agent平台：CodeBuddy
- 规约框架：Spec-Kit

## 架构原则
1. 所有业务逻辑必须通过原子能力API实现，不可直接操作数据库
2. 每个Skill对应一个或多个原子能力API的调用
3. Sub-Agent之间通过上下文隔离，不可直接共享变量
4. Orchestrator Agent负责意图识别和任务分发
5. 所有API调用结果必须经过验证，不可直接相信

## API端点清单
- POST /api/login - 用户登录
- GET /api/users/{user_id} - 查询用户信息
- GET /api/books/search - 图书检索
- GET /api/books/{book_id} - 图书详情
- GET /api/books - 所有图书列表
- GET /api/borrow/check-quota/{user_id} - 检查借阅配额
- POST /api/borrow - 借阅图书
- POST /api/return - 归还图书
- GET /api/borrow/records/{user_id} - 查询借阅记录
- POST /api/books/reserve - 预约图书

## 调用规范
1. 所有API请求必须包含正确的Content-Type: application/json
2. 日期格式统一为 YYYY-MM-DD
3. 错误响应格式：{"code": 状态码, "message": "错误信息", "data": null}
4. 成功响应格式：{"code": 200, "message": "操作成功", "data": {...}}

