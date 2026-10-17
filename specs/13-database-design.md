# 13 · 数据库设计说明书（Database Design）

> 本文档依据 `05-domain-model.md`（领域类）、`07-architecture.md`（分层与仓储）、`02-requirements.md`（FR/BR）、`constitution.md`（P-05/P-08）编制，定义系统关系表结构、主外键、索引与继承映射策略。
> UML 文本源（类图）见 `05-domain-model.md` 与 `06-domain-class-diagram.puml`；表名/字段必须与二者及后续 `07-api-spec.md` 严格一致（P-03）。

| 项 | 内容 |
|---|---|
| 文档编号 | `specs/13-database-design.md` |
| 文档类型 | 数据库设计（逻辑表 + 物理映射） |
| 版本 | v1.0（草案） |
| 生成方式 | Agent 起草（模型：AI 编码助手） |
| 审查状态 | ☐ 待人工审查（P-02） |
| 上游文档 | `05-domain-model.md`、`07-architecture.md`、`02-requirements.md`、`constitution.md` |
| 约束引用 | P-03（命名一致）、P-05（仓储映射）、P-08（规则参数化） |

> 类型采用通用 SQL 类型；物理库为 SQLite（与 `00` §9 基线一致），SQLite 仅区分 `INTEGER`/`TEXT`/`REAL`/`NUMERIC`/`BLOB`，下表的 `VARCHAR`/`DECIMAL`/`DATETIME` 在落地时按亲和性映射（`DATETIME` 存 ISO8601 文本，`DECIMAL` 用 `NUMERIC(10,2)`）。

---

## 1. 表清单与领域类映射

| 表名 | 对应领域类（`05`） | 说明 |
|---|---|---|
| `readers` | `Reader`（含 StudentReader/TeacherReader，STI） | 读者账号与类型 |
| `borrow_cards` | `BorrowCard` | 借阅证（一人一有效证，F-10/BR-012） |
| `librarians` | `Account`（role=librarian） | 图书管理员凭据 |
| `system_admins` | `Account`（role=admin） | 系统管理员凭据 |
| `book_titles` | `Title` | 图书标题/作品层 |
| `library_items` | `LibraryItem`（含 Book/Magazine/Thesis，STI） | 馆藏物理副本 |
| `loans` | `Loan` | 借阅记录 |
| `reservations` | `Reservation` | 预约（标题级 FIFO） |
| `borrow_policies` | `BorrowPolicy`（参数载体） | 借阅数量/期限规则表 |
| `fine_rules` | `FineRule`（参数载体） | 罚款费率规则表 |
| `fine_records` | `FineRecord` | 罚款记录（不接支付，OOS-01） |

> **与 `05` §3.16 `Account` 的 reconciliation**：领域模型将登录账号抽象为 `Account`（role ∈ reader/librarian/admin）。本设计按本实验要求**按角色分表**（`readers` / `librarians` / `system_admins`），三者结构同源；若后续统一，可合并为单 `accounts` 表 + `role` 字段，不影响其余表。

---

## 2. 表结构详述

### 2.1 `readers`（读者 · STI 根表）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `reader_id` | INTEGER | PK, AUTOINCREMENT | 读者标识 |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | 登录名（FR-001） |
| `password_hash` | VARCHAR(255) | NOT NULL | 口令哈希（G-07/NFR-06，禁止明文） |
| `email` | VARCHAR(120) | NULL | 邮箱 |
| `reader_type` | VARCHAR(20) | NOT NULL | 判别列：undergraduate/master/phd/junior/teacher（BR-001/002，D-09） |
| `grade_level` | VARCHAR(20) | NULL | 学生细分（仅 StudentReader 用，STI 可空列） |
| `department` | VARCHAR(50) | NULL | 院系（仅 TeacherReader 用） |
| `created_at` | DATETIME | NOT NULL | 注册时间 |

> 继承策略见 §4：`reader_type` 为**单表继承判别列**。

### 2.2 `borrow_cards`（借阅证）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `card_id` | INTEGER | PK | — |
| `card_no` | VARCHAR(20) | NOT NULL, UNIQUE | `CARD+year+6seq`（BR-011/F-09） |
| `reader_id` | INTEGER | NOT NULL, UNIQUE | FK→`readers(reader_id)`；UNIQUE 强制一人一证（BR-012/F-10） |
| `status` | VARCHAR(10) | NOT NULL DEFAULT 'active' | active/inactive（CardStatus） |
| `issued_at` | DATETIME | NOT NULL | 发证时间 |
| `expires_at` | DATETIME | NULL | 失效时间（可选） |

### 2.3 `librarians`（图书管理员）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `librarian_id` | INTEGER | PK | — |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | — |
| `password_hash` | VARCHAR(255) | NOT NULL | — |
| `created_by` | INTEGER | NULL | FK→`system_admins(admin_id)`（谁创建，可选） |
| `created_at` | DATETIME | NOT NULL | — |

### 2.4 `system_admins`（系统管理员）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `admin_id` | INTEGER | PK | — |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | — |
| `password_hash` | VARCHAR(255) | NOT NULL | — |
| `created_at` | DATETIME | NOT NULL | — |

### 2.5 `book_titles`（图书标题/作品）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `title_id` | INTEGER | PK | — |
| `isbn` | VARCHAR(20) | NOT NULL, UNIQUE | ISBN 唯一（FR-006） |
| `name` | VARCHAR(255) | NOT NULL | 书名 |
| `author` | VARCHAR(120) | NULL | 作者 |
| `publisher` | VARCHAR(120) | NULL | 出版社 |
| `category` | VARCHAR(50) | NULL | 分类 |
| `published_year` | INTEGER | NULL | 出版年 |
| `description` | TEXT | NULL | 简介 |
| `is_active` | BOOLEAN | NOT NULL DEFAULT 1 | 软删除标记（FR-007） |

### 2.6 `library_items`（馆藏副本 · STI 根表）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `item_id` | INTEGER | PK | — |
| `title_id` | INTEGER | NOT NULL | FK→`book_titles(title_id)`；组合（1:N） |
| `barcode` | VARCHAR(50) | NOT NULL, UNIQUE | 唯一条码（FR-008） |
| `item_type` | VARCHAR(20) | NOT NULL | 判别列：chinese_book/foreign_book/chinese_magazine/foreign_magazine/thesis（IT-01~05） |
| `language` | VARCHAR(10) | NULL | 中/外（Book/Magazine 细分，可空） |
| `location` | VARCHAR(50) | NULL | 馆藏位置 |
| `status` | VARCHAR(20) | NOT NULL DEFAULT 'in_library' | in_library/borrowed/scrapped（ItemStatus） |
| `created_at` | DATETIME | NOT NULL | — |

### 2.7 `loans`（借阅记录）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `loan_id` | INTEGER | PK | — |
| `reader_id` | INTEGER | NOT NULL | FK→`readers(reader_id)` |
| `item_id` | INTEGER | NOT NULL | FK→`library_items(item_id)` |
| `librarian_id` | INTEGER | NOT NULL | FK→`librarians(librarian_id)`（代理借还，F-02/BR-013） |
| `borrow_date` | DATETIME | NOT NULL | 借出时间 |
| `due_date` | DATETIME | NOT NULL | 应还时间（BorrowPolicy 计算，BR-002/003） |
| `return_date` | DATETIME | NULL | 实还时间 |
| `status` | VARCHAR(20) | NOT NULL DEFAULT 'borrowing' | borrowing/returned/overdue（LoanStatus） |
| `snapshot_rule_version` | VARCHAR(50) | NULL | 规则快照版本（BR-015/16，历史不受变更影响） |
| `created_at` | DATETIME | NOT NULL | — |

### 2.8 `reservations`（预约）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `reservation_id` | INTEGER | PK | — |
| `reader_id` | INTEGER | NOT NULL | FK→`readers(reader_id)` |
| `title_id` | INTEGER | NOT NULL | FK→`book_titles(title_id)`；标题级排队 |
| `created_at` | DATETIME | NOT NULL | 入队时间（BR-008 FIFO，按此排序） |
| `status` | VARCHAR(20) | NOT NULL DEFAULT 'pending' | pending/fulfilled/cancelled/expired（BR-010/D-05） |
| `fulfilled_at` | DATETIME | NULL | 履约时间 |
| UNIQUE | — | (`reader_id`,`title_id`) WHERE status='pending' | 同读者同标题不可重复有效预约（BR-009/F-08） |

> 注：部分 SQLite 版本不支持部分唯一索引（partial index），可在应用层（`ReservationPolicy.isDuplicate`，P-08）补强校验。

### 2.9 `borrow_policies`（借阅规则表 · 参数化）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `policy_id` | INTEGER | PK | — |
| `reader_type` | VARCHAR(20) | NOT NULL | undergraduate/master/phd/junior/teacher |
| `item_type` | VARCHAR(20) | NULL | 借出物类型维度（D-02 TBD，NULL 表示不限） |
| `max_borrow` | INTEGER | NOT NULL | 上限（BR-001/F-04） |
| `loan_period_days` | INTEGER | NOT NULL | 期限天（BR-002/F-05） |
| `version` | VARCHAR(20) | NOT NULL | 规则版本（供 `loans.snapshot_rule_version` 引用） |
| `effective_from` | DATETIME | NOT NULL | 生效时间（未来生效，BR-015） |
| UNIQUE | — | (`reader_type`,`item_type`,`version`) | 版本化唯一 |

### 2.10 `fine_rules`（罚款规则表 · 参数化）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `rule_id` | INTEGER | PK | — |
| `item_type` | VARCHAR(20) | NOT NULL | IT-01~05 或 'ALL' |
| `rate_per_day` | NUMERIC(10,2) | NOT NULL | 日费率（BR-004/F-06：0.1/0.2/0.5） |
| `cap_amount` | NUMERIC(10,2) | NULL | 封顶（D-03 TBD，NULL=不封顶） |
| `grace_days` | INTEGER | NOT NULL DEFAULT 0 | 免罚期（D-03 TBD，默认 0） |
| `version` | VARCHAR(20) | NOT NULL | 规则版本 |
| `effective_from` | DATETIME | NOT NULL | 生效时间 |
| UNIQUE | — | (`item_type`,`version`) | 版本化唯一 |

### 2.11 `fine_records`（罚款记录）
| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `fine_id` | INTEGER | PK | — |
| `loan_id` | INTEGER | NOT NULL, UNIQUE | FK→`loans(loan_id)`；1 对 0..1（BR-004） |
| `reader_id` | INTEGER | NOT NULL | FK→`readers(reader_id)` |
| `item_type` | VARCHAR(20) | NOT NULL | 计算时快照的借出物类型 |
| `overdue_days` | INTEGER | NOT NULL | 超期天数（BR-005 自然日向上取整） |
| `amount` | NUMERIC(10,2) | NOT NULL | 罚款金额（FineRule 计算） |
| `status` | VARCHAR(20) | NOT NULL DEFAULT 'unpaid' | unpaid/paid/waived（FineStatus） |
| `created_at` | DATETIME | NOT NULL | — |
| `paid_at` | DATETIME | NULL | 缴纳时间 |

---

## 3. 外键汇总

| 子表 | 字段 | 父表 | 父字段 | 删除策略 |
|---|---|---|---|---|
| `borrow_cards` | `reader_id` | `readers` | `reader_id` | RESTRICT（有卡/记录不得删读者） |
| `library_items` | `title_id` | `book_titles` | `title_id` | RESTRICT（在借副本阻止，FR-007/009） |
| `loans` | `reader_id` | `readers` | `reader_id` | RESTRICT |
| `loans` | `item_id` | `library_items` | `item_id` | RESTRICT |
| `loans` | `librarian_id` | `librarians` | `librarian_id` | RESTRICT |
| `reservations` | `reader_id` | `readers` | `reader_id` | CASCADE |
| `reservations` | `title_id` | `book_titles` | `title_id` | CASCADE |
| `fine_records` | `loan_id` | `loans` | `loan_id` | CASCADE |
| `fine_records` | `reader_id` | `readers` | `reader_id` | RESTRICT |
| `librarians` | `created_by` | `system_admins` | `admin_id` | SET NULL |

---

## 4. 继承映射策略（P-05 / `05` §3）

| 继承关系 | 采用策略 | 判别列 | 说明 |
|---|---|---|---|
| `Reader` ← `StudentReader`/`TeacherReader` | **单表继承 STI** | `readers.reader_type` | 子类差异字段（`grade_level`/`department`）以可空列存放；查询简单、标识稳定；代价为可空列。D-09 倾向"类型字段+规则表"，与 STI 一致。 |
| `LibraryItem` ← `Book`/`Magazine`/`Thesis` | **单表继承 STI** | `library_items.item_type` | 中/外细分用可空 `language`；`loans.item_id` 外键稳定，无需 union。 |
| `Account` ← `reader`/`librarian`/`admin` | **按角色分表** | （表本身即区分） | 见 §1 reconciliation；亦可改 JOINED/单表+role。 |

**备选方案与取舍**：
- *JOINED（父类+子类表）*：规范化好但跨表 join 多、借阅聚合查询复杂；本期实体少、子类属性少，STI 更优。
- *Concrete Table（每子类独立全量表）*：外键指向不稳定，放弃。

---

## 5. 索引设计

| 表 | 索引 | 类型 | 目的 |
|---|---|---|---|
| `readers` | `uk_username`(`username`) | UNIQUE | 登录查重（FR-001） |
| `readers` | `idx_reader_type`(`reader_type`) | 普通 | 按类型统计/规则查表 |
| `borrow_cards` | `uk_card_no`(`card_no`) | UNIQUE | 证号唯一（BR-011） |
| `borrow_cards` | `uk_reader_card`(`reader_id`) | UNIQUE | 一人一证（BR-012） |
| `librarians`/`system_admins` | `uk_username`(`username`) | UNIQUE | 角色校验查重（P-07） |
| `book_titles` | `uk_isbn`(`isbn`) | UNIQUE | ISBN 唯一（FR-006） |
| `book_titles` | `idx_title_active_name`(`is_active`,`name`) | 普通 | 检索过滤（FR-010） |
| `library_items` | `uk_barcode`(`barcode`) | UNIQUE | 条码唯一（FR-008） |
| `library_items` | `idx_item_title_status`(`title_id`,`status`) | 普通 | 查某标题可用副本（FR-014 前置） |
| `loans` | `idx_loan_reader_status`(`reader_id`,`status`) | 普通 | 统计在借/超期（BR-001/BR-006） |
| `loans` | `idx_loan_item`(`item_id`) | 普通 | 副本借还状态 |
| `loans` | `idx_loan_due`(`due_date`,`status`) | 普通 | 超期扫描 |
| `reservations` | `uk_reservation_active`(`reader_id`,`title_id`) WHERE status='pending' | 部分唯一 | 去重（BR-009） |
| `reservations` | `idx_resv_title_created`(`title_id`,`created_at`) | 普通 | FIFO 排队（BR-008） |
| `fine_records` | `uk_fine_loan`(`loan_id`) | UNIQUE | 一借一罚 |
| `borrow_policies`/`fine_rules` | `idx_policy_version`(`reader_type`,`item_type`,`version`) | 普通 | 取生效版本 |

---

## 6. 关键设计决策与未决项

- **软删除**：`book_titles.is_active`、`borrow_cards.status`；物理删除受限（FR-003/007/009）。
- **规则快照**：`loans.snapshot_rule_version` 关联 `borrow_policies`/`fine_rules` 的 `version`，保证历史记录不受规则变更影响（BR-015）。
- **规则参数化**：借阅/罚款数值**不在代码硬编码**，全部来自 `*_policies`/`fine_rules` 表（P-08，消解 G-04/G-05）。
- **未决项**：D-01 专科生数值、D-02 `item_type` 期限维度、D-03 罚款封顶/免罚、D-05 预约保留期、D-06 论文可外借——相关字段已预留（可空/默认），实现时按 `TBD(D-xx)` 标注。

---

## 7. 审查与变更

| 版本 | 日期 | 变更摘要 | 审查状态 |
|---|---|---|---|
| v1.0（草案） | 2026-10-17 | 首次生成：11 张表字段/主外键、STI 映射、索引、快照与软删策略 | ☐ 待人工审查 |
