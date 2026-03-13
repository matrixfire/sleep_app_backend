好的，完全没问题。你提供了一份非常有价值的会议草稿，它清晰地指明了项目的下一阶段方向。我的任务是基于对你现有项目（RBAC、分层架构等）的深入理解，将这份草稿提炼成一份结构清晰、表达专业、可直接用于指导开发的技术设计文档。

这份文档将不仅仅是草稿的复制，而是结合了现有架构的优化和补充说明。

---

### **助眠App后端 - 业务功能扩展设计方案**

#### **1. 概述**

本文档旨在将产品UI设计转化为具体的后端技术实现方案。方案将在现有V1.0的RBAC权限管理和基础服务架构之上，进行核心业务功能的精细化扩展，主要涵盖**用户、内容、行为**三大领域，并设计相应的App端与Admin管理端API接口，最终目标是打通一条核心业务链路并完成技术验证。

---

#### **2. 数据库模型精细化设计 (Data Model Design)**

在现有后台RBAC五张表的基础上，新增并优化以下三大业务领域的表结构。

##### **2.1 用户领域 (User Domain)**

**设计说明：**
为明确区分后台操作员与App终端用户，我们需建立独立的 `app_user` 表。现有 `sys_user` 表将继续用于后台管理人员的登录与权限控制。

| 表名: `app_user` | 终端用户表   |            |                                         |
| :--------------- | :----------- | :--------- | :-------------------------------------- |
| **字段名**       | **类型**     | **约束**   | **说明**                                |
| `id`             | BIGINT       | PK, 自增   | 用户唯一ID                              |
| `phone`          | VARCHAR(20)  | 唯一, 可空 | 手机号，作为登录方式之一                |
| `wechat_openid`  | VARCHAR(100) | 唯一, 可空 | 微信开放平台ID，为未来微信登录功能预留  |
| `nickname`       | VARCHAR(50)  | NOT NULL   | 用户昵称 (例如：一眠用户_8829)          |
| `register_time`  | DATETIME     | NOT NULL   | 注册时间，用于计算“已相遇X天”等运营数据 |
| `device_mac`     | VARCHAR(50)  | 可空       | 绑定的外部硬件设备MAC地址               |

##### **2.2 内容领域 (Content Domain)**

**设计说明：**
此领域对应App中由运营人员配置、供用户消费的内容。

**2.2.1 每日一言**

| 表名: `daily_quote` | 每日一言表   |          |                                |
| :------------------ | :----------- | :------- | :----------------------------- |
| `id`                | INT          | PK, 自增 | 主键                           |
| `show_date`         | DATE         | 唯一     | 指定展示日期，便于运营提前配置 |
| `content`           | TEXT         | NOT NULL | 语录内容                       |
| `author`            | VARCHAR(50)  |          | 作者                           |
| `bg_image_url`      | VARCHAR(255) | NOT NULL | 卡片背景图 (OSS链接)           |

**2.2.2 音频资源 (在现有 `audio_resource` 表基础上优化)**

**设计说明：**
对现有的 `audio_resource` 表进行增强，增加分类、场景标签和时长字段，以支持App端的筛选和展示需求。

| 表名: `audio_resource` | 音频/冥想资源表 |                |                                                              |
| :--------------------- | :-------------- | :------------- | :----------------------------------------------------------- |
| `id`                   | INT             | PK, 自增       | 主键                                                         |
| `title`                | VARCHAR(100)    | NOT NULL       | 音频标题                                                     |
| `category`             | VARCHAR(20)     | 索引, NOT NULL | **(新增)** 分类枚举: `sleep`(助眠), `meditation`(冥想), `sound`(声音) |
| `scene_tags`           | VARCHAR(100)    |                | **(新增)** 场景标签,逗号分隔: `nap`(小憩), `focus`(专注), `breathe`(呼吸) |
| `cover_url`            | VARCHAR(255)    |                | 封面图 (OSS链接)                                             |
| `audio_url`            | VARCHAR(255)    | NOT NULL       | 音频文件 (OSS链接)                                           |
| `duration`             | INT             |                | **(新增)** 播放时长（秒）                                    |

##### **2.3 用户行为领域 (User Activity Domain)**

**设计说明：**
采用统一的 `user_activity_record` 表来记录用户所有核心场景的使用行为，避免为每个场景单独建表，极大提高了系统的扩展性和可维护性。

| 表名: `user_activity_record` | 用户场景行为记录表 |                |                                                  |
| :--------------------------- | :----------------- | :------------- | :----------------------------------------------- |
| `id`                         | BIGINT             | PK, 自增       | 主键                                             |
| `user_id`                    | BIGINT             | 索引, NOT NULL | 关联 `app_user.id`                               |
| `activity_type`              | VARCHAR(20)        | 索引, NOT NULL | 行为类型枚举: `sleep`, `nap`, `focus`, `breathe` |
| `start_time`                 | DATETIME           | NOT NULL       | 开始时间                                         |
| `end_time`                   | DATETIME           | 可空           | 结束时间 (若提前终止则记录终止时间)              |
| `duration_min`               | INT                |                | 实际完成时长（分钟）                             |
| `status`                     | TINYINT            | NOT NULL       | 状态 (0:进行中, 1:正常完成, 2:提前终止)          |

---

#### **3. 后端接口 (API) 设计**

所有接口遵循RESTful风格，并按访问端进行明确分离。

##### **3.1 App 端接口 (前缀: `/api/v1/app`)**

*   **鉴权模块 (Auth)**
    *   `POST /auth/login`: 用户登录，支持手机或微信，成功后返回JWT。
    *   `GET /auth/me`: 获取当前登录用户信息。

*   **首页模块 (Home)**
    *   `GET /home/daily-quote`: 获取当日的“每日一言”卡片信息。

*   **内容模块 (Content)**
    *   `GET /audios`: 获取音频列表，支持按 `category` 或 `scene_tags` 筛选。

*   **行为记录模块 (Activity)**
    *   `POST /activities/start`: 开始一项活动（睡眠、小憩等），创建一条“进行中”的记录。
    *   `POST /activities/end`: 结束一项活动，更新记录状态与时长。
    *   `GET /activities/history`: 获取个人历史活动记录列表（分页）。

##### **3.2 Admin 管理端接口 (前缀: `/api/v1/admin`)**

**设计说明：**
所有Admin端接口都将通过依赖注入进行权限校验，要求用户具备如 `rbac:manage`, `content:manage` 等相应权限。

*   **RBAC 系统管理**
    *   `GET /users`, `POST /roles`, `POST /permissions/assign-to-role` 等（复用并扩展现有RBAC管理接口）。

*   **运营内容管理**
    *   `GET /daily-quotes`, `POST /daily-quotes`: 管理“每日一言”。
    *   `GET /audios`, `POST /audios`, `PUT /audios/{id}`, `DELETE /audios/{id}`: 全面的音频资源CRUD管理。

*   **关键指标概览 (Data Stats)**
    *   `GET /stats/users/total`: 查询总注册用户数。
    *   `GET /stats/activities/summary`: 查询今日各类活动的使用人次。

---

#### **4. 下一阶段核心目标：打通关键业务链路**

为确保设计的可行性，下一阶段的核心任务是实现并验证一条完整的业务链路，具体步骤如下：

1.  **后台内容配置**：`admin` 用户登录，调用 `POST /admin/audios` 接口成功上传一条音频。
2.  **App用户登录**：模拟App用户，调用 `POST /app/auth/login` 接口成功登录，获取JWT。
3.  **App内容拉取**：使用上一步的JWT，调用 `GET /app/audios` 接口，成功获取到后台上传的音频。
4.  **App行为上报**：调用 `POST /app/activities/start` 和 `POST /app/activities/end`，成功记录一次完整的“小憩”行为。

此链路将在Postman中进行完整演示，作为本阶段开发工作的最终交付成果。