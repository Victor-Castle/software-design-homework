---
name: book-search
description: 图书检索技能。由 orchestrator-agent / circulation-agent 按需调用，提供图书检索的接口参考。
metadata:
  version: "1.1"
  api-base: "http://localhost:8001"
---

> 说明：本 skill 不在用户输入时自动触发，而是由 `orchestrator-agent`（找书类意图）或 `circulation-agent`（需解析 book_id 时）按需调用。

## 后端真实 API 映射
基址 `http://localhost:8001`，统一返回 `{code, message, data}`。
| 能力 | 方法 | 路径 | 请求体 / 参数 |
|------|------|------|--------------|
| 检索图书 | GET | `/api/books/search` | `keyword`/`category`/`author`/`location`（query） |
| 图书详情 | GET | `/api/books/{book_id}` | 路径参数 |
| 列出全部图书 | GET | `/api/books` | `page`/`page_size`（query） |

## Input
- keyword: string（可选）- 搜索关键词（书名或ISBN）
- category: string（可选）- 图书分类
- author: string（可选）- 作者
- location: string（可选）- 馆藏位置
- page: integer（可选，默认1）- 页码

## Output
- 图书列表，包含：书名、作者、ISBN、馆藏位置、可借复本、状态

## Procedure
### 第1步：解析用户查询意图
从用户输入中提取搜索条件，识别关键词、分类、作者等信息。

### 第2步：调用图书检索API
```python
import httpx

params = {}
if keyword: params["keyword"] = keyword
if category: params["category"] = category
if author: params["author"] = author
if location: params["location"] = location
params["page"] = page

response = httpx.get("http://localhost:8001/api/books/search", params=params)
result = response.json()
```

### 第3步：解析并返回结果
如果检索成功，按以下格式整理结果：
```
总数：{total}本
图书列表（按可借状态排序）：
《书名》- 作者（状态：在馆/已借出，位置：馆藏位置）
```

### 第4步：处理特殊情况
- 如果无结果：建议用户更换关键词或浏览所有图书（`GET /api/books`）
- 如果接口异常：提示"检索服务暂时不可用，请稍后重试"

## Acceptance Criteria
- 必须支持多条件组合查询
- 结果必须按可借状态排序（在馆优先）
- 必须包含馆藏位置信息
- 如果指定了"普通阅览室"等位置，必须在 API 调用中传入 `location` 参数
