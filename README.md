# 评论后端（FastAPI + PostgreSQL）

本目录提供一个最小可用的评论后端，支持：
- 创建评论（POST /api/comments）
- 查询评论列表（GET /api/comments?path=/index&page=1&page_size=20）
- 删除评论（DELETE /api/comments/{id}，需管理员 Bearer Token）
- 健康检查（GET /healthz）

## 目录结构

```
backend/
  app/
    routers/
      __init__.py
      comments.py
    __init__.py
    config.py
    db.py
    main.py
    models.py
    schemas.py
    security.py
  requirements.txt
  Procfile
  render.yaml (可选，便于一键在 Render 部署)
  .env.example
```

## 环境变量

- DATABASE_URL：PostgreSQL 连接串，如：
  - `postgresql+psycopg2://user:password@host:5432/dbname`
- ADMIN_TOKEN：管理员删除口令（任意复杂字符串即可）
- CORS_ORIGINS：允许的跨域源，多个以逗号分隔，如：`https://your-domain.com,https://your-preview.vercel.app`

你可以复制 `.env.example` 为 `.env` 用于本地开发（渲染平台上用环境变量配置即可）。

## 本地运行

1. 准备 Python 3.10+ 环境
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. （选项 A）使用 SQLite 快速启动（无需安装数据库）：
   ```powershell
   $env:DATABASE_URL="sqlite:///./dev.db";
   $env:ADMIN_TOKEN="your_admin_token";
   $env:CORS_ORIGINS="http://127.0.0.1:8083,http://localhost:8083";
   ```
   SQLite 仅用于本地开发验证；线上请使用 Render PostgreSQL。

   （选项 B）使用本地/远程 PostgreSQL（示例）：
   ```powershell
   $env:DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/demo";
   $env:ADMIN_TOKEN="your_admin_token";
   $env:CORS_ORIGINS="http://127.0.0.1:8083,http://localhost:8083";
   ```
4. 启动服务：
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. 打开接口文档：
   - Swagger UI: http://127.0.0.1:8000/docs
   - Redoc: http://127.0.0.1:8000/redoc

### cURL 示例

创建评论：
```bash
curl -X POST "http://127.0.0.1:8000/api/comments" \
  -H "Content-Type: application/json" \
  -d '{"path":"/index","nickname":"Tom","content":"你好"}'
```

查询评论：
```bash
curl "http://127.0.0.1:8000/api/comments?path=/index&page=1&page_size=20"
```

删除评论（需管理员令牌）：
```bash
curl -X DELETE "http://127.0.0.1:8000/api/comments/1" \
  -H "Authorization: Bearer your_admin_token"
```

## API 说明（简要）

- POST /api/comments
  - body: `{ "path": "/index", "nickname": "Tom", "content": "你好" }`
  - 返回：新建的评论对象
- GET /api/comments?path=/index&page=1&page_size=20
  - 返回：分页结果 `{ items, total, page, page_size }`
- DELETE /api/comments/{id}
  - Header: `Authorization: Bearer <ADMIN_TOKEN>`
  - 返回：204 无内容

## Render 部署

- 建议创建一个 Web Service，Python 运行时。
- 关联一个 Render PostgreSQL 实例，将其 `Internal Database URL`/`External Database URL` 复制到 `DATABASE_URL`。
- 设置环境变量：`DATABASE_URL`、`ADMIN_TOKEN`、`CORS_ORIGINS`。
- Start Command 可用：
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- 也可参考本目录的 `render.yaml` 进行基础编排。

## 注意事项

- 服务端已做基础长度校验与 HTML 转义，前端仍建议做输入限制。
- 删除操作需要 Bearer Token。请确保 Token 不在前端硬编码，使用后端管理面板或手工调用。
- 如需“实时推送”，可在后续版本加入 SSE/WebSocket 或直接改用带实时通道的数据库服务。
