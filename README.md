# Home Ops Hub

> 家庭资产管理与运维系统 — 追踪说明书、文档、维修记录和耗材采购，手机端与PC端互通。

[![Flutter Tests](https://github.com/cracklings3d/home-ops-hub/actions/workflows/flutter-tests.yml/badge.svg)](https://github.com/cracklings3d/home-ops-hub/actions)
[![Django Tests](https://github.com/cracklings3d/home-ops-hub/actions/workflows/django-tests.yml/badge.svg)](https://github.com/cracklings3d/home-ops-hub/actions)

## 项目概述

Home Ops Hub 是一个跨设备的家庭资产管理平台，帮助家庭用户集中管理：

- 家用电器的**说明书和文档**（PDF、图片、视频）
- 设备的**维修记录**和故障历史
- **耗材库存**和更换提醒（滤芯、滤网等）
- **维保到期**智能提醒
- **二维码扫码**快速定位设备

### 双端角色差异化

| 角色 | 设备 | 核心场景 |
|------|------|---------|
| **家庭管理员** | PC / Web | 批量导入、规划维护、耗材库存管理 |
| **日常使用者** | 手机 | 扫码定位、扫码添加维修、查看耗材余量 |

## 技术架构

```
Flutter (移动端 + PC端) ←→ Django REST API ←→ PostgreSQL + Redis + S3
```

- **移动端 & PC端**: Flutter 3.x (iOS / Android / Web / Desktop)
- **后端 API**: Django 5.x + Django REST Framework
- **数据库**: PostgreSQL 16
- **缓存**: Redis
- **文件存储**: S3 (本地开发用 MinIO)
- **认证**: JWT (djangorestframework-simplejwt)
- **实时通知**: Django Channels + WebSocket

## 快速开始

### 前置条件

- Flutter SDK 3.7+
- Docker & Docker Compose
- Python 3.12+

### 本地开发环境

```bash
# 1. 克隆仓库
git clone https://github.com/cracklings3d/home-ops-hub.git
cd home-ops-hub

# 2. 启动基础设施 (PostgreSQL + Redis + MinIO)
cd infrastructure
docker compose up -d

# 3. 配置后端
cd ../backend
cp .env.example .env  # 编辑数据库和存储配置
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# 4. 配置前端
cd ../frontend
flutter pub get
flutter run
```

### GitHub Actions CI

每次 push 和 PR 自动运行：

- **Flutter 测试**: `flutter analyze` + `flutter test`
- **Django 测试**: pytest + coverage

## 目录结构

```
home-ops-hub/
├── SPEC.md              # 项目规格说明书
├── README.md
├── .github/workflows/   # CI/CD 流水线
├── backend/             # Django 后端
│   ├── config/          # Django 配置
│   ├── apps/            # 功能模块 (assets/maintenance/consumables/...)
│   ├── tests/
│   └── requirements.txt
├── frontend/            # Flutter 应用
│   ├── lib/
│   │   ├── core/        # 路由/主题/工具
│   │   ├── features/    # 功能模块
│   │   ├── shared/      # 共享组件
│   │   └── models/      # 数据模型
│   └── test/
├── infrastructure/      # Docker 配置
└── docs/                # 文档
```

## 演进路线

- [x] 项目初始化，SPEC.md 编写
- [x] 技术架构设计
- [x] CI/CD 流水线配置
- [x] Flutter 项目基础框架
- [ ] Django 后端基础框架
- [ ] 核心数据模型与 API
- [ ] 移动端完整 UI
- [ ] PC/Web 端完整 UI
- [ ] 文件上传与存储
- [ ] 通知系统
- [ ] 二维码功能
- [ ] 智能提醒引擎

## License

MIT