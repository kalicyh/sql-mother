from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.admin import admin
from api.auth import auth as auth_router
from api.auth.dependencies import get_current_active_user
from api.db import database, models

description = """
`VScode`启动! 🚀
"""

# ✅ 优雅处理生命周期，取代 @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ 启动时检查数据库表
    print("✅ 检查数据库表...")
    models.Base.metadata.create_all(bind=database.engine)
    print("✅ 数据库表检查完成，如果不存在则已创建！")
    
    # ✅ 可以在这里启动 WebSocket 等服务
    print("🚀 FastAPI 服务已启动")
    
    yield

    # ✅ 停止服务时可添加清理任务
    print("🛑 FastAPI 服务已关闭")


# ✅ 创建 FastAPI 实例
app = FastAPI(
    title="App",
    description=description,
    summary="我们生来，就是为了，在宇宙中，留下印记。",
    version="0.0.1",
    terms_of_service="https://blog.kalicyh.love/",
    contact={
        "name": "kalicyh",
        "url": "https://blog.kalicyh.love/",
        "email": "kalicyh@qq.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/",
    },
    lifespan=lifespan  # ✅ 使用 lifespan 取代 @app.on_event("startup")
)

# ✅ 允许所有域名跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域名
    allow_credentials=True,  # 允许携带 Cookies
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# ✅ 注册认证路由
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

# ✅ 示例：受保护接口，需要 Bearer Token 验证
@app.get("/users/me")
async def read_users_me(current_user=Depends(get_current_active_user)):
    return current_user

# ✅ 挂载 React 前端静态文件
# app.mount("/", StaticFiles(directory="dist", html=True), name="dist")
