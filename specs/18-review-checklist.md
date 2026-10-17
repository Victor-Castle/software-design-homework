# 18 · 审查清单（Review Checklist）

> 本文档为实验一全部规格与 UML 制品的人工审查清单，覆盖 `00`~`13`、`constitution.md` 及三份 UML 文本源（`04`/`06`/`08`）。审查人逐项勾选，确认后方可进入实现阶段（P-01/P-02/P-04）。

| 项 | 内容 |
|---|---|
| 文档编号 | `specs/18-review-checklist.md` |
| 文档类型 | 审查清单 |
| 版本 | v1.0（草案） |
| 生成方式 | Agent 起草（模型：AI 编码助手） |
| 审查状态 | ☐ 待人工审查（P-02） |
| 适用范围 | `specs/` 全部文档与 UML 图 |

---

## A. 文档完整性（P-01 路线）

- [ ] `00-project-brief.md` 存在且含范围/参与者/类型/基线差距
- [ ] `01-clarifying-questions.md` 含人类回答区且 F-01~F-10 已录入
- [ ] `02-requirements.md` 含 FR/NFR/BR，编号永久不重编
- [ ] `03-use-cases.md` 含 UC-01~UC-10 与参与者/关系
- [ ] `04-use-case-model.puml` 用例图文本源存在
- [ ] `05-domain-model.md` 含类图 + 实体/值对象/策略分类
- [ ] `06-domain-class-diagram.puml` 领域类图文本源存在
- [ ] `07-architecture.md` 含四层职责 + 模块 + 权限 + 异常 + 事务 + 模式
- [ ] `08-package-diagram.puml` 包图文本源存在
- [ ] `13-database-design.md` 含 11 张表 + 继承映射 + 索引
- [ ] `17-risk-analysis.md` 风险登记完整
- [ ] `18-review-checklist.md` 本清单
- [ ] `constitution.md` 宪章已审查并生效（P-02 自身亦受约束）

---

## B. 各文档重点审查项

### B.0 `constitution.md`（最高约束）
- [ ] 11 条原则（P-01~P-11）逐条阅读并理解
- [ ] 已确认事实 F-01~F-10 与各规格无冲突
- [ ] 未决项 D-01~D-09 在各规格已按"临时处置"标注 `TBD(D-xx)`

### B.1 `00-project-brief.md`
- [ ] 6 项目标、5 类读者、5 类借出物、8 In Scope / 5 OOS 与 `02` 一致
- [ ] 基线差距 G-01~G-09 被后续文档消解或说明

### B.2 `01-clarifying-questions.md`
- [ ] 人类回答区 Q-00~Q-29 已填写
- [ ] F-01~F-10 与 `constitution.md` §1 摘录一致

### B.3 `02-requirements.md`
- [ ] FR-001~FR-019 均可追溯至 UC/BR
- [ ] BR-001~BR-016 数值与 F-04/F-05/F-06/F-07/F-08/F-09/F-10 一致
- [ ] BR-014 权限矩阵与 P-07 一致
- [ ] 未决项 OI-05/D-01~D-09 在本文件正确标注

### B.4 `03-use-cases.md` + `04-use-case-model.puml`
- [ ] 用例图参与者 A-01~A-05、用例 UC-01~UC-10 与文字一致
- [ ] `<<include>>`/`<<extend>>` 关系（如还书 include 罚款）与 FR 一致
- [ ] 图内命名与 `02` 一致（P-03）

### B.5 `05-domain-model.md` + `06-domain-class-diagram.puml`
- [ ] 类图含 Reader 泛化、LibraryItem 泛化、Reader 1:N BorrowCard/Loan/Reservation
- [ ] BorrowPolicy/FineRule 作为独立策略类表达
- [ ] 类图与 `06` 文本源一致；未含 Controller/Repository/DTO 等设计类
- [ ] 实体/值对象/策略分类与 `07` §2 一致

### B.6 `07-architecture.md` + `08-package-diagram.puml`
- [ ] 四层职责表"禁止包含"项被遵守（领域层无框架依赖）
- [ ] 7 模块（reader/card/catalog/circulation/reservation/fine/admin）齐备
- [ ] 权限策略 P-07 矩阵与 `02` BR-014 一致；轻量角色校验方案明确
- [ ] 统一响应 `{code,message,data}` 与 `00` §9 一致（无新错误码）
- [ ] 事务边界定位应用层
- [ ] 包图中 `presentation --> application --> domain`，`infrastructure ..|> domain`
- [ ] **包图无 `pres --> infra`（Controller 不直连 Repository）**
- [ ] 设计模式（Strategy/Factory/Repository/DTO/MVC）定位清晰

### B.7 `13-database-design.md`
- [ ] 11 张表字段/类型/主外键完整
- [ ] 表名/字段与 `05`/`06`/`07-api-spec.md`（待生成）一致（P-03）
- [ ] 继承映射策略（STI）明确且合理
- [ ] 索引覆盖检索/去重/超期扫描关键路径
- [ ] 软删除与规则快照机制明确
- [ ] 规则参数化（无代码硬编码）落地到 `*_policies`/`fine_rules`

### B.8 `17-risk-analysis.md`
- [ ] 覆盖需求/建模/架构/数据库/权限/Agent使用 6 维度
- [ ] P0 风险（RK-01/10/11/13/17）有具体缓解
- [ ] 风险与 `02` D-xx、`constitution` 原则交叉引用正确

---

## C. UML 一致性专项（P-03）

- [ ] 用例图、类图、包图均为 PlantUML/Mermaid 文本源（无二进制唯一来源）
- [ ] 类名/属性名/方法名在 `05`/`06`/`13`/`07-api-spec` 间严格一致
- [ ] 关系基数（1:0..1、1:0..*、1:*）在类图与数据库外键一致
- [ ] 包图依赖方向与 P-05 单向向下一致

---

## D. 过程合规（P-02/P-04/P-10/P-11）

- [ ] 每份文档头含"生成方式 + 审查状态"字段
- [ ] 每份文档附"待人类确认要点清单"
- [ ] 实现期 `specs/` 改动均可在 `10-change-requests.md`（CR-xx）追溯
- [ ] 每次 Agent 产出已在 `19-ai-usage-log.md` 登记（不得漏记/补记）
- [ ] 编码前已执行 `git diff` 确认 `backend/` 未越界改动

---

## E. 签署

| 项 | 内容 |
|---|---|
| 审查人 | ____________ |
| 审查日期 | ____________ |
| 总体结论 | ☐ 通过，可进入实现 ☐ 有条件通过 ☐ 退回修改 |
| 退回/修订说明 | ____________ |

---

## F. 审查与变更

| 版本 | 日期 | 变更摘要 | 审查状态 |
|---|---|---|---|
| v1.0（草案） | 2026-10-17 | 首次生成：A~E 五节审查清单，覆盖全部文档与 UML | ☐ 待人工审查 |
