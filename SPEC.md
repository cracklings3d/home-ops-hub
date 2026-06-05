# Home Ops Hub - 家庭资产管理系统

## 1. 项目概述

**项目名称：** Home Ops Hub（家庭运维中心）

**一句话描述：** 一个跨设备（手机端与PC端）的家庭资产管理平台，用于集中管理家用电器的说明书、文档、维修记录和耗材采购信息。

**核心价值：** 告别纸质文件散落、找不到保修卡、忘记耗材型号的混乱局面——所有家庭资产信息触手可及。

---

## 2. 用户角色与场景

### 2.1 角色定义

| 角色 | 设备倾向 | 主要使用场景 | 核心功能优先级 |
|------|---------|------------|--------------|
| **家庭管理员** | PC / Web | 初始化系统、批量导入资产、规划维护日程、协调采购 | 资产管理、批量操作、维护计划、耗材库存管理 |
| **日常使用者** | 手机 | 快速查找说明书扫码设备、记录维修、查看耗材余量、下单采购 | 扫码识别、快速搜索、维修记录、耗材提醒 |

### 2.2 典型使用场景

**场景A（日常使用者）：**
> 厨房的净水器滤芯该换了，拿出手机扫一下设备二维码，立刻看到滤芯型号、购买链接、上次更换日期，以及推荐的更换周期。

**场景B（家庭管理员）：**
> 空调不制冷了，坐在电脑前查一下空调的所有维修记录和配件型号，联系维修人员，并更新维修档案。

**场景C（家庭管理员）：**
> 年底大扫除，用 PC 端一次性检查所有设备的维护状态，批量导出耗材采购清单，规划下一年的维护计划。

---

## 3. 核心功能模块

### 3.1 资产管理 (Asset Management)

- **设备档案**：名称、品牌、型号、购买日期、保修截止日期、存放位置、购买链接
- **二维码标签**：每个设备生成唯一二维码（可打印贴附），扫码快速定位
- **附件管理**：上传/存储说明书PDF、发票照片、合同扫描件等
- **设备照片**：支持多张设备照片和铭牌照片
- **分类管理**：按房间（客厅/厨房/卧室/卫生间/车库等）或按类别（家电/数码/家具/工具等）组织

### 3.2 维修记录 (Maintenance Log)

- **维修档案**：设备每次维修的时间、原因、维修人员、费用、更换配件清单
- **故障标签**：常用故障类型标签（漏水/不制冷/噪音/无法开机等）
- **关联配件**：记录维修中更换的耗材/配件，关联到耗材库存
- **维修历史时间线**：每个设备展示完整的维修历程

### 3.3 耗材管理 (Consumables)

- **耗材档案**：名称、兼容设备列表、推荐品牌、预计寿命、更换周期
- **库存跟踪**：当前剩余数量、最低价提醒阈值
- **更换记录**：每次更换自动记录时间戳和费用
- **采购链接**：维护常用购买链接，一键跳转电商平台
- **余量提醒**：基于使用频率和更换历史，智能预测下次更换时间

### 3.4 文档管理 (Documents)

- **多格式支持**：PDF、图片、视频（安装教程、维修视频）
- **版本控制**：文档更新后可回溯历史版本
- **标签系统**：可自定义标签（"快速入门"、"故障排除"、"安全须知"等）
- **全文搜索**：文档内容全文索引，快速定位

### 3.5 通知与提醒 (Notifications)

- **维保到期提醒**：保修期结束前自动提醒（如：30天/7天/当天）
- **耗材更换提醒**：基于使用频率预测更换时间，提前通知
- **自定义提醒**：用户可针对任意设备设置一次性或周期性提醒
- **多渠道通知**：APP推送、邮件（PC端可选）

### 3.6 仪表盘 (Dashboard)

- **设备总览**：总数、分类分布、健康状态分布
- **即将到期的维保**：列出保修/维保即将到期的设备
- **待采购耗材**：库存低于阈值的耗材列表
- **近期维护计划**：未来30天内的维护任务

---

## 4. 技术架构

### 4.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                        用户层                                │
│   ┌──────────────┐     ┌──────────────┐     ┌────────────┐ │
│   │   移动端 App  │     │   PC/Web 应用  │     │   API 客户端 │ │
│   │  (Flutter)   │     │   (Flutter)   │     │   (CLI/SDK) │ │
│   └───────┬──────┘     └───────┬──────┘     └────────────┘ │
└───────────┼────────────────────┼──────────────────────────┘
            │                    │
┌───────────▼────────────────────▼──────────────────────────┐
│                       API 网关层                            │
│            (身份验证 / 限流 / 路由 / 缓存)                   │
└───────────┬────────────────────┬──────────────────────────┘
            │                    │
┌───────────▼────────┐ ┌─────────▼─────────────────────────┐
│     业务逻辑层      │ │           数据层                   │
│  (Django + DRF)    │ │  PostgreSQL + Redis + S3           │
│                    │ │  (文件存储: 说明书PDF/发票/照片)    │
└────────────────────┘ └────────────────────────────────────┘
```

### 4.2 技术选型

| 层级 | 技术 | 选型理由 |
|------|------|---------|
| **移动端** | Flutter 3.x | 跨平台（iOS/Android）、高性能、 expressive UI |
| **PC/Web 端** | Flutter Web / Desktop | 与移动端共享核心代码，统一体验 |
| **后端** | Django 5.x + Django REST Framework | 成熟稳定、快速开发、内置 Admin |
| **数据库** | PostgreSQL 16 | 关系型数据、JSON字段支持全文检索 |
| **缓存** | Redis | 会话缓存、API限流、实时提醒队列 |
| **文件存储** | S3 兼容存储（本地开发用 MinIO） | 大量文件（PDF/图片）的弹性存储 |
| **实时通信** | WebSocket（Channels） | 实时通知、协同编辑 |
| **身份认证** | JWT + Refresh Token | 无状态认证，支持多设备登录 |

### 4.3 目录结构

```
home-ops-hub/
├── SPEC.md                          # 本规格说明书
├── README.md                        # 项目介绍
├── LICENSE
├── .github/
│   └── workflows/                    # CI/CD 流水线
│       ├── flutter-tests.yml
│       ├── django-tests.yml
│       ├── deploy-staging.yml
│       └── deploy-prod.yml
├── backend/                          # Django 后端
│   ├── config/                      # Django 项目配置
│   │   ├── settings/
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── assets/                  # 资产管理
│   │   ├── maintenance/             # 维修记录
│   │   ├── consumables/             # 耗材管理
│   │   ├── documents/               # 文档管理
│   │   ├── notifications/           # 通知系统
│   │   └── accounts/                # 用户账户
│   ├── tests/                       # 后端测试
│   ├── scripts/                     # 管理脚本
│   └── requirements.txt
├── frontend/                        # Flutter 应用
│   ├── lib/
│   │   ├── core/                    # 核心库（路由/主题/工具）
│   │   ├── features/                # 功能模块（与后端 app 对应）
│   │   │   ├── assets/
│   │   │   ├── maintenance/
│   │   │   ├── consumables/
│   │   │   ├── documents/
│   │   │   └── dashboard/
│   │   ├── shared/                  # 共享组件/widgets
│   │   └── models/                  # 数据模型
│   ├── test/                        # Flutter 测试
│   └── pubspec.yaml
├── infrastructure/                  # 基础设施配置
│   ├── docker/
│   │   ├── django/                  # Django Docker 配置
│   │   ├── postgres/
│   │   ├── redis/
│   │   └── nginx/
│   └── docker-compose.yml           # 本地开发环境
├── docs/                            # 项目文档
│   ├── api/                         # API 文档
│   ├── design/                      # 设计文档
│   └── guides/                       # 使用指南
└── scripts/                         # 实用脚本
    ├── setup.sh
    └── seed_data.py
```

---

## 5. 数据模型

### 5.1 核心实体

```
User (用户)
├── Profile (扩展信息: 角色/偏好/通知设置)
└── Household (家庭/组织)

Asset (资产/设备)
├── Category (分类: 房间/类别)
├── Brand (品牌)
├── Document (文档附件)
├── MaintenanceRecord (维修记录)
├── ConsumableUsage (耗材使用)
└── QRCode (二维码)

Consumable (耗材)
├── CompatibleAsset (兼容设备)
├── PurchaseLink (购买链接)
└── UsageRecord (使用记录)

Notification (通知)
└── NotificationSchedule (提醒计划)
```

### 5.2 设备 (Asset) 核心字段

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 唯一标识 |
| name | string | 设备名称 |
| brand | string | 品牌 |
| model | string | 型号 |
| serial_number | string | 序列号 |
| purchase_date | date | 购买日期 |
| warranty_end | date | 保修截止 |
| location | string | 存放位置（房间） |
| category | FK | 分类 |
| purchase_link | URL | 购买链接 |
| notes | text | 备注 |
| qr_code | string | 二维码数据 |
| photos | JSON | 照片URL列表 |
| status | enum | 正常/维修中/已报废 |
| created_by | FK | 所有者 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

---

## 6. API 设计

### 6.1 认证

- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/login/` - 登录（返回 JWT）
- `POST /api/auth/refresh/` - 刷新 Token
- `POST /api/auth/logout/` - 登出

### 6.2 资产管理

- `GET/POST /api/assets/` - 列出/创建资产
- `GET/PUT/PATCH/DELETE /api/assets/{id}/` - CRUD 单个资产
- `POST /api/assets/{id}/upload-document/` - 上传文档
- `GET /api/assets/{id}/maintenance-history/` - 维修历史
- `GET /api/assets/{id}/qr-code/` - 获取二维码

### 6.3 维修记录

- `GET/POST /api/maintenance/` - 列出/创建维修记录
- `GET/PUT/PATCH/DELETE /api/maintenance/{id}/` - CRUD 维修记录

### 6.4 耗材管理

- `GET/POST /api/consumables/` - 列出/创建耗材
- `GET/PUT/PATCH/DELETE /api/consumables/{id}/` - CRUD 耗材
- `POST /api/consumables/{id}/record-usage/` - 记录使用/更换
- `GET /api/consumables/low-stock/` - 低库存耗材

### 6.5 文档管理

- `GET/POST /api/documents/` - 列出/上传文档
- `GET/PUT/PATCH/DELETE /api/documents/{id}/` - CRUD 文档
- `GET /api/documents/search/?q=` - 全文搜索

### 6.6 仪表盘

- `GET /api/dashboard/summary/` - 数据总览
- `GET /api/dashboard/upcoming/` - 近期待办
- `GET /api/dashboard/reminders/` - 提醒列表

---

## 7. 演进路线图

### 阶段 0：项目初始化 ✅ (当前阶段)
- [x] 创建 GitHub 仓库
- [ ] 编写 SPEC.md（本文档）
- [ ] 设计目录结构
- [ ] 配置 CI/CD 流水线
- [ ] 搭建本地开发环境（Docker）

### 阶段 1：后端基础框架 ⏳
- [ ] Django 项目初始化
- [ ] 数据库模型设计与迁移
- [ ] 认证系统 (JWT)
- [ ] 基础 API 端点

### 阶段 2：前端移动端原型
- [ ] Flutter 项目初始化
- [ ] 核心 UI 组件库
- [ ] 资产列表与详情页
- [ ] 扫码功能集成

### 阶段 3：PC/Web 端
- [ ] Flutter Desktop/Web 支持
- [ ] 仪表盘界面
- [ ] 批量操作功能

### 阶段 4：高级功能
- [ ] 文件上传与存储（S3/MinIO）
- [ ] 通知系统（推送/邮件）
- [ ] 二维码生成与打印
- [ ] 数据导入/导出

### 阶段 5：智能化
- [ ] 耗材余量预测
- [ ] 维保到期智能提醒
- [ ] 使用数据分析

---

## 8. 开发约束

- **代码质量**：所有 PR 必须通过 CI（测试 + lint）
- **测试覆盖率**：核心业务逻辑 >= 80%
- **文档**：所有新增 API 必须更新 API 文档
- **版本控制**：遵循 Semantic Versioning
- **安全**：敏感数据加密存储，定期密钥轮换

---

## 9. 决策记录

| 日期 | 决策 | 理由 |
|------|------|------|
| 2026-06-05 | Flutter 作为全平台框架 | 移动端与PC端代码高度复用，减少维护成本 |
| 2026-06-05 | Django + DRF 作为后端 | 快速开发、内置 Admin、成熟生态 |
| 2026-06-05 | PostgreSQL 作为主数据库 | 关系型数据 + JSON字段，适合资产关联查询 |
| 2026-06-05 | 本地开发使用 Docker Compose | 环境一致性，快速启动 |

---

*本文档最后更新：2026-06-05*