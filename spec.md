# 睡眠仪 IoT 与内容分发平台 - 后端系统架构设计草案

### 设计思路概述

本架构旨在为公司初创期的“软硬结合”业务提供一个**高内聚、低耦合、易扩展**的底层支撑。针对当前 MVP 阶段的核心需求（内部 RBAC 管理、动静分离音频分发）以及未来的高并发场景（海量睡眠仪数据上报），系统采用了经典的 **5 层企业级架构体系**进行设计。

---

## 一、 整体后端架构层级说明与数据流向

借鉴 Java Spring 体系中经典的 MVC 与 DAO 思想，并结合 FastAPI 的现代异步特性，我们的后端系统被严格划分为以下 5 个独立层级：

* **Router 层（路由/控制层）：** 负责接收 HTTP 请求，进行基础的鉴权拦截（JWT 解析）和路由分发，不包含任何复杂业务逻辑。
* **Schema 层（数据传输校验层/DTO）：** 基于 Pydantic 实现。负责定义输入（Request）和输出（Response）的数据格式，并在请求进入业务层前完成严格的数据类型与合法性校验。
* **Service 层（业务逻辑层）：** 系统的“大脑”。负责处理所有核心业务规则（如判断用户是否有权限下载、组装各类数据）。它负责调度底层的 CRUD，但绝对不直接写 SQL。
* **CRUD / Repository 层（数据访问层）：** 纯粹的数据库操作层。封装了对 MySQL 的所有增删改查（使用 SQLAlchemy）。
* **Model 层（实体/模型层）：** 对应数据库表结构的 ORM 模型。

**🔄 核心数据流向：**
客户端请求 $\rightarrow$ `Router` $\rightarrow$ 使用 `Schema` 验证数据 $\rightarrow$ 调用 `Service` 处理业务逻辑 $\rightarrow$ `Service` 调用 `CRUD` 获取数据 $\rightarrow$ `CRUD` 操作 `Model` 与 MySQL 交互 $\rightarrow$ 逐层组装并返回。

---

## 二、 FastAPI 项目工程规范与权限设计

### 1. 标准 5 层目录树结构

```text
sleep_app_backend/
├── app/
│   ├── api/             # 1. Router层：存放路由接口
│   ├── schemas/         # 2. Schema层：Pydantic 模型 (DTO)
│   ├── services/        # 3. Service层：核心业务逻辑
│   ├── crud/            # 4. CRUD层：数据库访问层
│   ├── models/          # 5. Model层：SQLAlchemy ORM 模型
│   └── core/            # 核心配置：系统配置、权限拦截、异常处理
├── db/                  # 数据库引擎：MySQL/Redis 连接池初始化
└── main.py              # FastAPI 启动入口

```

### 2. 核心亮点：细粒度 RBAC 权限架构落地

为了满足未来复杂的管理需求，系统采用**动态权限标识**（如 `read:sleep_data.user123`），并在 **Service 层实现行级检查**。

* **Model层：** 定义含资源 ID 的权限名称。
* **CRUD层：** 仅负责查询当前操作用户的权限列表。
* **Service层：** 在业务逻辑中调用 `check_permission()` 进行精细化校验。
* **Router层：** 仅传递用户上下文（Token 解析结果），绝对不处理权限逻辑。

**✨ 架构收益：**

* **新增权限：** 只需在数据库权限表加一行，完全不用改代码。
* **修改逻辑：** 无需改动 Service 层核心代码，真正实现 100% 权限解耦。

---

## 三、 核心数据库表设计 (MVP 阶段)

> *注：以下设计省略了基础的 `created_at`、`updated_at` 等通用审计字段。*

### 1. 内部后台管理系统 (经典 RBAC 五张表)

| 表名 (Table) | 字段名称 | 数据类型 | 约束/说明 |
| --- | --- | --- | --- |
| **sys_user** (用户表) | `id` | INT | 主键，自增 (PK) |
|  | `username` | VARCHAR(50) | 登录账号，唯一 |
|  | `password_hash` | VARCHAR(255) | 哈希加密后的密码 |
|  | `status` | TINYINT | 账号状态 (1:正常, 0:禁用) |
| **sys_role** (角色表) | `id` | INT | 主键，自增 (PK) |
|  | `role_name` | VARCHAR(50) | 角色名称 (如：内容管理员) |
|  | `role_code` | VARCHAR(50) | 唯一标识 (如：`CONTENT_ADMIN`) |
| **sys_permission** (权限表) | `id` | INT | 主键，自增 (PK) |
|  | `perm_name` | VARCHAR(50) | 权限名称 (如：上传音频) |
|  | `perm_code` | VARCHAR(100) | 路由标识 (如：`audio:upload`) |
| **sys_user_role** (关联表) | `user_id`, `role_id` | INT | 联合主键，分别关联对应表 ID |
| **sys_role_perm** (关联表) | `role_id`, `perm_id` | INT | 联合主键，分别关联对应表 ID |

### 2. 业务核心数据表 (动静分离设计)

| 表名 (Table) | 字段名称 | 数据类型 | 约束/说明 |
| --- | --- | --- | --- |
| **app_user** (APP用户表) | `id` | BIGINT | 主键 (建议未来引入雪花算法) |
|  | `mobile` | VARCHAR(20) | 手机号，唯一索引 |
|  | `nickname` | VARCHAR(50) | 用户昵称 |
|  | `device_mac` | VARCHAR(50) | 绑定的硬件设备 MAC 地址 |
| **audio_resource** (音频表) | `id` | INT | 主键 |
|  | `title` | VARCHAR(100) | 音频标题 (如：夏夜雷雨) |
|  | `cover_url` | VARCHAR(255) | 封面图 OSS CDN 完整链接 |
|  | `audio_url` | VARCHAR(255) | **【核心】音频源文件 OSS 链接** |

---

## 四、 RESTful API 设计规范示例

接口设计严格遵循 RESTful 风格，通过 HTTP 动作（GET/POST/PUT/DELETE）体现对资源的操作语义。以“后台管理-助眠音频资源”为例：

* **获取音频列表 (分页过滤)**
* `GET /api/v1/admin/audios?page=1&size=20&category=白噪音`
* **返回:** `200 OK` (包含 total 总数和 items 列表)


* **新增音频资源**
* `POST /api/v1/admin/audios`
* **请求体:** `{"title": "春日溪流", "audio_url": "https://oss.../audio.mp3"}`
* **返回:** `201 Created`


* **修改音频信息**
* `PUT /api/v1/admin/audios/{audio_id}`
* **请求体:** `{"title": "春日溪流(高清版)"}`
* **返回:** `200 OK`


* **删除音频资源**
* `DELETE /api/v1/admin/audios/{audio_id}`
* **返回:** `204 No Content`



---

## 五、 IoT 高并发数据预留架构方案（Redis 削峰填谷）

针对“未来睡眠仪硬件高频上报体动/心率数据”场景，如果直接将数据 `INSERT` 进 MySQL，会导致数据库连接池耗尽、行锁冲突进而系统崩溃。本系统设计了以下异步消息流转方案：

1. **快速响应（削峰）：** 设备通过 HTTP/长连接发送数据，FastAPI `Router` 层接收到数据后，仅做极其轻量的格式校验，立刻使用 `LPUSH` 将数据压入 **Redis 队列**中。
2. **立即返回：** 数据进入 Redis 后，瞬间给设备返回 `200 OK`。整个过程 API 极速释放，极大提升并发吞吐量。
3. **后台落库（填谷）：** 启动后台异步任务系统（如 Celery 或 BackgroundTasks），Worker 匀速从 Redis 弹出数据（如积攒 500 条），然后通过 **批量插入 (Bulk Insert)** 写入 MySQL。
4. **远期演进：** 待数据量达到千万/TB 级别时，底层存储可平滑替换为专门处理时序数据的 **InfluxDB 或 TDengine**，而外围的 5 层架构和 API 接口几乎无需大改。

---
